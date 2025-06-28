# 🧠 AGENT.md – NeuroShell AI Agent Specification

## Overview

The **NeuroShell Agent** is the modular AI system that enables natural language interaction, voice input, and shell-level task execution inside the NeuroShell terminal. This document defines the agent's purpose, architecture, naming conventions, code structure, and development guidelines.

The repository now also includes a windowless terminal GUI built with
**Electron**, **React**, and **xterm.js**. It opens a borderless window
(800x600 by default) and spawns a real shell via `node-pty` to provide a fully
functional terminal. The implementation lives in `gui/electron/`.

---

## 🧩 Agent Architecture

### 🔄 Core Components

| Module          | Responsibility |
|-----------------|----------------|
| `agent/core.js` | Main controller: input routing, response orchestration |
| `agent/nlu/`    | Natural Language Understanding (GPT prompt logic, parsing) |
| `agent/io/`     | Input/output (speech recognition, TTS, shell I/O) |
| `agent/memory/` | (Optional) Persistent memory, context tracking |
| `agent/tools/`  | Task runners: code gen, file ops, command wrappers |

---

## 🧠 Naming Conventions

### ✅ Files & Folders
- Use `kebab-case` for **folders**
- Use `camelCase` for **functions and variables**
- Use `PascalCase` for **classes**
- Prefix agent tools with `agent` or `ai` if used across systems

Example:
agent/
core.js
nlu/
promptBuilder.js
commandParser.js
io/
voiceInput.js
shellInterface.js

### ✅ Functions
- Functions should be **pure where possible**
- Function names must describe **intent** clearly:  
  - `buildPromptFromInput(input)`  
  - `executeShellCommand(cmd)`  
  - `speakResponse(text)`

---

## 🚦 Agent Behavior Guidelines

- Default mode is **non-executing** — commands must be confirmed before run.
- Agent must gracefully degrade if GPT or TTS is unavailable.
- All interactions must pass through `agent/core.js` for consistency.

---

## 🛠️ Extending the Agent

To add a new skill/tool:
1. Create a module in `agent/tools/` (e.g., `summarizer.js`)
2. Export a function: `async function run(args)`
3. Register it in `agent/core.js` with a handler key or intent pattern

Example:
```js
// core.js
if (intent === 'summarize') {
  return await runSummarizer(args)
}
```

## File Structure
agent/
├── core.js
├── config.js
├── io/
│   ├── voiceInput.js
│   ├── ttsOutput.js
│   └── shellInterface.js
├── nlu/
│   ├── promptBuilder.js
│   ├── commandParser.js
├── tools/
│   ├── codeGenerator.js
│   ├── fileEditor.js
└── memory/
    └── contextCache.js
gui/
└── electron/
    ├── main.js
    ├── index.html
    └── renderer.js

