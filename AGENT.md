# 🧠 AGENT.md – NeuroShell AI Agent Specification

## Overview

The **NeuroShell Agent** is the modular AI system that enables natural language interaction, voice input, and shell-level task execution inside the NeuroShell terminal. This document defines the agent's purpose, architecture, naming conventions, code structure, and development guidelines.

The repository now also includes a windowless terminal GUI built with
**Electron**, **React**, and **xterm.js**. It opens a borderless window
(800x600 by default) and spawns a real shell via `node-pty` to provide a fully
functional terminal. The implementation lives in `gui/electron/`.

---

## 🧩 Agent Architecture
internal architecture of the **agentic AI system** embedded in the `neuroshell` project. The agent lives in its own development branch and is designed to interpret natural language instructions, plan their execution, interact with the terminal environment, and display output in the `neuroshell` GUI.

The agent works in the following pipeline:

1. **Intent Parsing**  
   Input from the user is parsed using a GPT-based model to understand what the user wants.

2. **Planning**  
   The intent is broken down into smaller executable steps in plain language.

3. **Tool Selection + Execution**  
   These steps are converted into shell commands or code edits, and executed via tools (primarily the shell environment itself).

4. **Output Display**  
   All output is displayed directly to the terminal, with no filtering.

---

## File Structure
agent/                      # Agent-specific logic and configuration
    ├── __init__.py
    ├── parser.py              # Parses user input into intent
    ├── planner.py             # Breaks intent into steps
    ├── executor.py            # Executes selected tools/commands
    ├── tools/                 # Toolset layer (terminal interaction, file I/O, etc.)
    │   ├── shell.py
    │   └── editor.py
    └── memory.py              # Logs, history, context

gui/
└── electron/
    ├── main.js
    ├── index.html
    └── renderer.js

