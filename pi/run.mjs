import { spawn } from "node:child_process";
import { appendFileSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { createInterface } from "node:readline";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import {
  createAgentSession, createExtensionRuntime, ModelRuntime, SessionManager, SettingsManager,
} from "@earendil-works/pi-coding-agent";
import { getModel } from "@earendil-works/pi-ai/compat";

const stage = process.argv[2] ?? "001";
const stages = {
  "001": ["guest_write", "guest_read", "vm_boot", "serial_read", "vm_stop"],
  "002": ["guest_write", "guest_read", "vm_boot", "serial_read", "serial_send", "vm_stop"],
};
const names = stages[stage];
if (!Array.isArray(names)) throw new Error("Choose stage 001 or 002");

const root = fileURLToPath(new URL("../", import.meta.url));
const trials = join(root, ".local", "experiments");
mkdirSync(trials, { recursive: true });
const previous = process.argv[3];
if (stage === "002" && !previous) throw new Error("Pass the stage 001 campaign directory");
const trial = previous ? resolve(previous) : mkdtempSync(join(trials, "pi-"));
const work = join(trial, "work");
mkdirSync(work, { recursive: true });
console.log(trial);
const sessionPointer = join(trial, "session-path.txt");
const prompt = readFileSync(join(root, "experiments", `${stage}-campaign-prompt.txt`), "utf8");

const model = getModel("openai-codex", "gpt-6.1-sol");
const authPath = join(process.env.CODEX_HOME ?? join(homedir(), ".codex"), "auth.json");
const accessToken = JSON.parse(readFileSync(authPath, "utf8")).tokens?.access_token;
if (!accessToken) throw new Error("A signed-in Codex CLI is required");
const expires = JSON.parse(Buffer.from(accessToken.split(".")[1], "base64url")).exp * 1000;
if (expires < Date.now() + 600000) throw new Error("Refresh your Codex login before running Pi");
const credential = { type: "oauth", access: accessToken, expires };
const modelRuntime = await ModelRuntime.create({
  modelsPath: null,
  credentials: {
    read: async provider => provider === "openai-codex" ? credential : undefined,
    list: async () => [{ providerId: "openai-codex", type: "oauth" }],
    modify: async () => { throw new Error("Refresh credentials with Codex CLI"); },
  },
});

const broker = spawn("python3", [join(root, "guest_tool.py"), work], {
  stdio: ["pipe", "pipe", "inherit"],
});
const replies = createInterface({ input: broker.stdout })[Symbol.asyncIterator]();
let pending = Promise.resolve();
function callBroker(name, args) {
  const call = pending.then(async () => {
    broker.stdin.write(JSON.stringify({ name, args }) + "\n");
    const reply = await replies.next();
    if (reply.done) throw new Error("Guest broker exited");
    const response = JSON.parse(reply.value);
    if (response.error) throw new Error(response.error);
    return response.result;
  });
  pending = call.catch(() => {});
  return call;
}

const descriptions = {
  guest_write: "Replace the campaign guest image with whitespace-separated raw hex.",
  guest_read: "Read the current campaign guest image as hex.",
  vm_boot: "Boot the saved guest image. The VM runs until you stop it.",
  vm_stop: "Stop the running VM.",
  serial_read: "Read new guest serial output without waiting. Read again if empty.",
  serial_send: "Send up to 256 bytes encoded as hex to the running guest.",
};
const image = join(work, "guest.hex");
const tools = names.map(name => {
  const takesHex = name === "guest_write" || name === "serial_send";
  return {
    name, label: name, description: descriptions[name],
    parameters: {
      type: "object",
      properties: takesHex ? { hex: { type: "string", maxLength: 65536 } } : {},
      required: takesHex ? ["hex"] : [],
      additionalProperties: false,
    },
    async execute(_id, args) {
      let output;
      if (name === "guest_write") {
        const hex = args.hex.replace(/\s/g, "");
        if (!/^(?:[0-9a-fA-F]{2}){4,}$/.test(hex)) throw new Error("Invalid raw hex image");
        writeFileSync(image, hex + "\n");
        output = { bytes: hex.length / 2 };
      } else if (name === "guest_read") {
        output = { hex: readFileSync(image, "utf8").trim() };
      } else {
        output = await callBroker(name, args);
      }
      return { content: [{ type: "text", text: JSON.stringify(output) }] };
    },
  };
});
const resourceLoader = {
  getExtensions: () => ({ extensions: [], errors: [], runtime: createExtensionRuntime() }),
  getSkills: () => ({ skills: [], diagnostics: [] }),
  getPrompts: () => ({ prompts: [], diagnostics: [] }),
  getThemes: () => ({ themes: [], diagnostics: [] }),
  getAgentsFiles: () => ({ agentsFiles: [] }),
  getSystemPrompt: () => "You are the experimental agent. Use only the provided tools.",
  getSystemPromptSource: () => undefined,
  getAppendSystemPrompt: () => [],
  getAppendSystemPromptSources: () => [],
  extendResources: () => {},
  reload: async () => {},
};
const { session } = await createAgentSession({
  cwd: work,
  agentDir: trial,
  model, modelRuntime, resourceLoader,
  tools: tools.map(tool => tool.name),
  customTools: tools,
  sessionManager: previous
    ? SessionManager.open(readFileSync(sessionPointer, "utf8").trim(), trial, work)
    : SessionManager.create(work, trial),
  settingsManager: SettingsManager.inMemory({
    compaction: { enabled: false },
    retry: { enabled: false },
  }),
});
try {
  const active = session.getActiveToolNames();
  if (JSON.stringify(active) !== JSON.stringify(names)) {
    throw new Error("Unexpected active tools: " + active.join(", "));
  }
  writeFileSync(join(trial, `${stage}-config.json`), JSON.stringify({
    provider: model.provider, model: model.id, activeTools: active,
    systemPrompt: session.systemPrompt,
  }, null, 2) + "\n");
  writeFileSync(join(trial, `${stage}-prompt.txt`), prompt);
  session.subscribe(event => {
    if (["message_end", "tool_execution_start", "tool_execution_end"].includes(event.type)) {
      appendFileSync(join(trial, `${stage}-events.jsonl`), JSON.stringify(event) + "\n");
    }
  });
  await session.prompt(prompt);
  writeFileSync(sessionPointer, session.sessionFile + "\n");
  const last = session.messages.at(-1);
  if (last?.role !== "assistant" || ["error", "aborted"].includes(last.stopReason)) {
    throw new Error(last?.errorMessage ?? "No successful final assistant message");
  }
} finally {
  session.dispose();
  broker.stdin.end();
}
