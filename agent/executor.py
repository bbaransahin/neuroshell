"""Executor for the NeuroShell agent."""

from __future__ import annotations

import json
import os
import shlex
from typing import Any, Dict, List

from dotenv import load_dotenv
import openai

from tools.shell import run_command

load_dotenv()


def _generate_command(step: str, context: List[Dict[str, Any]], parsed: Dict[str, Any]) -> str:
    """Use OpenAI to generate a shell command for a step."""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a Linux shell assistant. Given a description of a task, "
                "you respond with a single JSON object containing only one field: 'command'."
                "Do not include explanations or text outside the JSON."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Step: {step}\n"
                f"Previous steps (for context): {[s['description'] for s in context]}"
                f"Parsed user intent (for context): {parsed}"
            ),
        },
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    content = response.choices[0].message.content.strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse command JSON: {exc}\nRaw content:\n{content}") from exc

    cmd = data.get("command")
    if not isinstance(cmd, str):
        raise RuntimeError("Command field missing in response")
    return cmd

def execute_steps(steps: List[str], parsed: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Execute a list of plain-text steps.

    Each step is converted to an executable shell command using an OpenAI
    model. Commands are executed sequentially and their outputs stored. The
    returned list contains dictionaries with ``description``, ``executableCommand``,
    ``output``, and ``isDone`` keys for each step.
    """

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        return [{"error": "OPENAI_API_KEY environment variable not set"}]

    step_states: List[Dict[str, Any]] = [
        {
            "description": desc,
            "executableCommand": None,
            "output": None,
            "isDone": False,
        }
        for desc in steps
    ]

    for idx, state in enumerate(step_states):
        try:
            command = _generate_command(state["description"], step_states[:idx], parsed)
            state["executableCommand"] = command
        except Exception as exc:  # pragma: no cover - network call
            state["output"] = f"Error generating command: {exc}"
            continue

        try:
            cmd_list = shlex.split(command)
            result = run_command(cmd_list)
            state["output"] = result
            state["isDone"] = True
        except Exception as exc:  # pragma: no cover - execution error
            state["output"] = f"Error executing command: {exc}"

    return step_states
