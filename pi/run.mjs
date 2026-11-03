import { spawnSync } from "node:child_process";
import { appendFileSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  createAgentSession, createExtensionRuntime, ModelRuntime, SessionManager, SettingsManager,
} from "@earendil-works/pi-coding-agent";
import { getModel } from "@earendil-works/pi-ai/compat";

const root = fileURLToPath(new URL("../", import.meta.url));
const trials = join(root, ".local", "experiments");
mkdirSync(trials, { recursive: true });
const trial = mkdtempSync(join(trials, "pi-"));
const work = join(trial, "work");
mkdirSync(work);
console.log(trial);

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

const broker = fileURLToPath(new URL("../guest_tool.py", import.meta.url));
function callBroker(method, params) {
  const request = { jsonrpc: "2.0", id: 1, method, params };
  const result = spawnSync("python3", [broker], {
    input: JSON.stringify(request) + "\n", encoding: "utf8", timeout: 12000,
  });
  if (result.status !== 0) throw new Error("Guest broker failed");
  const response = JSON.parse(result.stdout);
  if (response.error) throw new Error(response.error.message);
  return response.result;
}

const { tools: [spec] } = callBroker("tools/list");
const runGuest = {
  name: spec.name,
  label: "Run guest",
  description: spec.description,
  parameters: spec.inputSchema,
  async execute(_id, args) {
    const result = callBroker("tools/call", { name: spec.name, arguments: args });
    if (result.isError) throw new Error(result.content[0].text);
    return result;
  },
};

// Each stage selects its own explicit tools. New stages do not inherit built-ins.
const tools = [runGuest];
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
  sessionManager: SessionManager.inMemory(work),
  settingsManager: SettingsManager.inMemory({
    compaction: { enabled: false },
    retry: { enabled: false },
  }),
});
try {
  const active = session.getActiveToolNames();
  if (JSON.stringify(active) !== JSON.stringify([spec.name])) {
    throw new Error("Unexpected active tools: " + active.join(", "));
  }
  writeFileSync(join(trial, "config.json"), JSON.stringify({
    provider: model.provider, model: model.id, activeTools: active,
    systemPrompt: session.systemPrompt,
  }, null, 2) + "\n");
  const prompt = readFileSync(new URL("../experiments/001-pi-prompt.txt", import.meta.url), "utf8");
  writeFileSync(join(trial, "prompt.txt"), prompt);
  session.subscribe(event => {
    if (["message_end", "tool_execution_start", "tool_execution_end"].includes(event.type)) {
      appendFileSync(join(trial, "events.jsonl"), JSON.stringify(event) + "\n");
    }
  });
  await session.prompt(prompt);
  const last = session.messages.at(-1);
  if (last?.role !== "assistant" || ["error", "aborted"].includes(last.stopReason)) {
    throw new Error(last?.errorMessage ?? "No successful final assistant message");
  }
} finally {
  session.dispose();
}
