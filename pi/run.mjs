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

const [stage = "001", previous, mode, unmetCondition, observation] = process.argv.slice(2);
const common = ["guest_write", "guest_read", "notes_write", "notes_read", "vm_boot", "serial_read", "vm_stop"];
const stages = {
  "001": { tools: common },
  "002": { tools: [...common, "serial_send"], requiresCampaign: true },
  "003": { tools: [...common, "serial_send", "vm_boot_network"], requiresCampaign: true },
  "004": { tools: [...common, "serial_send", "vm_boot_tcp"], requiresCampaign: true },
  "005": { tools: [...common, "serial_send", "vm_boot_http"], requiresCampaign: true },
  "006": { tools: [...common, "serial_send", "vm_boot_http"], requiresCampaign: true },
  "007": { tools: [...common, "serial_send", "vm_boot_http"], requiresCampaign: true },
  "008": { tools: [...common, "serial_send", "vm_boot_http", "vm_boot_disk"], requiresCampaign: true },
  "009": { tools: [...common, "serial_send", "vm_boot_http", "vm_boot_disk"], requiresCampaign: true },
  "010": { tools: [...common, "serial_send", "vm_boot_http", "vm_boot_disk"], requiresCampaign: true },
  "011": { tools: [...common, "serial_send", "serial_send_text", "vm_boot_http", "vm_boot_disk"], requiresCampaign: true },
  "012": { tools: [...common, "guest_patch", "serial_send", "serial_send_text", "vm_boot_http", "vm_boot_disk"], requiresCampaign: true },
  "013": { tools: [...common, "guest_patch", "serial_send", "serial_send_text", "vm_boot_http", "vm_boot_disk"], requiresCampaign: true },
  "014": {
    tools: ["notes_write", "notes_read", "vm_boot_disk", "serial_read", "serial_send", "serial_send_text", "vm_stop"],
    requiresCampaign: true,
  },
  "015": {
    tools: ["notes_write", "notes_read", "vm_boot_disk", "serial_read", "serial_send", "serial_send_text", "vm_stop"],
    requiresCampaign: true,
  },
};
const definition = stages[stage];
if (!Object.hasOwn(stages, stage)) throw new Error("Unknown stage");
const names = definition.tools;
if ((definition.requiresCampaign || mode) && !previous) throw new Error("Pass a campaign directory");
if (mode && mode !== "--fresh" && (mode !== "--continue" || !unmetCondition?.trim() || !observation?.trim())) {
  throw new Error("Use --fresh or --continue UNMET_CONDITION OBSERVATION");
}

const root = fileURLToPath(new URL("../", import.meta.url));
const trials = join(root, ".local", "experiments");
mkdirSync(trials, { recursive: true });
const trial = previous ? resolve(previous) : mkdtempSync(join(trials, "pi-"));
const work = join(trial, "work");
mkdirSync(work, { recursive: true });
console.log(trial);
const sessionPointer = join(trial, "session-path.txt");
const prompt = mode === "--continue"
  ? `The stage is still incomplete. Continue working. Unmet acceptance condition: ${unmetCondition}\nObserved result: ${observation}`
  : readFileSync(join(root, "experiments", `${stage}-campaign-prompt.txt`), "utf8");

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
  guest_read: "Read the current campaign guest image as hex, optionally selecting a byte range.",
  guest_patch: "Overwrite a byte range of your saved image or append at its end. Offsets are in bytes.",
  vm_boot: "Boot the saved guest image. The VM runs until you stop it.",
  vm_boot_network: "Boot the saved guest with a private Ethernet link to the ARP peer.",
  vm_boot_tcp: "Boot the saved guest with the private ARP and TCP challenge peer.",
  vm_boot_http: "Boot with the private ARP peer and host HTTP origin.",
  vm_boot_disk: "Boot the saved image with the campaign’s persistent virtual disk.",
  vm_stop: "Stop the running VM.",
  serial_read: "Read new guest serial output. Optionally wait up to wait_ms (0 to 5000) for data.",
  notes_write: "Replace your campaign handoff notes with up to 8192 characters.",
  notes_read: "Read your campaign handoff notes.",
  serial_send_text: "Send up to 4096 UTF-8 bytes as literal serial input. Include LF to submit each shell line.",
  serial_send: "Send up to 256 bytes encoded as hex to the running guest.",
};
const notes = join(work, "notes.txt");
const image = join(work, "guest.hex");
const tools = names.map(name => {
  const properties = {
    guest_write: { hex: { type: "string", maxLength: 65536 } },
    guest_read: {
      offset: { type: "integer", minimum: 0 },
      length: { type: "integer", minimum: 1 },
    },
    guest_patch: {
      offset: { type: "integer", minimum: 0 },
      hex: { type: "string", maxLength: 65536 },
    },
    serial_send: { hex: { type: "string", maxLength: 512 } },
    serial_send_text: { text: { type: "string", maxLength: 4096 } },
    notes_write: { text: { type: "string", maxLength: 8192 } },
    serial_read: { wait_ms: { type: "integer", minimum: 0, maximum: 5000 } },
  }[name] ?? {};
  return {
    name, label: name, description: descriptions[name],
    parameters: {
      type: "object",
      properties,
      required: ["serial_read", "guest_read"].includes(name) ? [] : Object.keys(properties),
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
        const hex = readFileSync(image, "utf8").trim();
        const offset = args.offset ?? 0;
        const length = args.length ?? hex.length / 2;
        output = { hex: hex.slice(offset * 2, (offset + length) * 2) };
      } else if (name === "guest_patch") {
        const current = readFileSync(image, "utf8").trim();
        const replacement = args.hex.replace(/\s/g, "");
        const start = args.offset * 2;
        if (start > current.length || !/^(?:[0-9a-fA-F]{2})+$/.test(replacement)
            || start + replacement.length > 65536) {
          throw new Error("Invalid guest image patch");
        }
        const hex = current.slice(0, start) + replacement + current.slice(start + replacement.length);
        writeFileSync(image, hex + "\n");
        output = { bytes: hex.length / 2 };
      } else if (name === "serial_send_text") {
        const bytes = Buffer.from(args.text, "utf8");
        if (!bytes.length || bytes.length > 4096) throw new Error("Send 1 to 4096 UTF-8 bytes");
        let sent = 0;
        while (sent < bytes.length) {
          const chunk = bytes.subarray(sent, sent + 256);
          const result = await callBroker("serial_send", { hex: chunk.toString("hex") });
          sent += result.sent;
          if (result.sent !== chunk.length) break;
        }
        output = { sent };
      } else if (name === "notes_write") {
        writeFileSync(notes, args.text);
        output = { saved: true };
      } else if (name === "notes_read") {
        output = { text: readFileSync(notes, "utf8") };
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
  sessionManager: previous && mode !== "--fresh"
    ? SessionManager.open(readFileSync(sessionPointer, "utf8").trim(), trial, work)
    : SessionManager.create(work, trial),
  settingsManager: SettingsManager.inMemory({
    compaction: { enabled: true },
    retry: { enabled: false },
  }),
});
try {
  writeFileSync(sessionPointer, session.sessionFile + "\n");
  const active = session.getActiveToolNames();
  if (JSON.stringify(active) !== JSON.stringify(names)) {
    throw new Error("Unexpected active tools: " + active.join(", "));
  }
  writeFileSync(join(trial, `${stage}-config.json`), JSON.stringify({
    provider: model.provider, model: model.id, activeTools: active,
    systemPrompt: session.systemPrompt,
  }, null, 2) + "\n");
  appendFileSync(join(trial, `${stage}-prompts.jsonl`), JSON.stringify({
    timestamp: new Date().toISOString(), mode, unmetCondition, observation, prompt,
  }) + "\n");
  session.subscribe(event => {
    if (["message_end", "tool_execution_start", "tool_execution_end", "compaction_start", "compaction_end"].includes(event.type)) {
      appendFileSync(join(trial, `${stage}-events.jsonl`), JSON.stringify({ ...event, timestamp: new Date().toISOString() }) + "\n");
    }
  });
  await session.prompt(prompt);
  const last = session.messages.at(-1);
  if (last?.role !== "assistant" || ["error", "aborted"].includes(last.stopReason)) {
    throw new Error(last?.errorMessage ?? "No successful final assistant message");
  }
} finally {
  session.dispose();
  broker.stdin.end();
}
