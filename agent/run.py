"""Entry point for the NeuroShell agent using LangChain ReAct."""

from __future__ import annotations

import os
import sys
import warnings

from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, Tool, initialize_agent
from langchain._api.deprecation import LangChainDeprecationWarning

from tools.shell import run_command

GRAY = "\033[90m"
RESET = "\033[0m"

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)


def main() -> None:
    """Run the NeuroShell agent."""
    if len(sys.argv) < 2:
        print("Usage: python run.py 'your request here'")
        return

    if os.getenv("OPENAI_API_KEY") is None:
        print("Error: OPENAI_API_KEY environment variable not set")
        return

    user_input = " ".join(sys.argv[1:])

    print("[NEURO_START]", flush=True)
    print(f"{GRAY}\nUser Input:\n{user_input}\n{RESET}")

    def shell_tool(command: str) -> str:
        """Execute a shell command and return at most 2000 chars of its output."""
        return run_command(command.split(), max_chars=2000)

    tools = [
        Tool(
            name="shell",
            func=shell_tool,
            description="Execute shell commands",
        )
    ]

    llm = ChatOpenAI(model="gpt-3.5-turbo")
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )

    final = None
    try:
        for chunk in agent.stream(user_input):
            if "actions" in chunk:
                for action in chunk["actions"]:
                    print(f"{GRAY}{action.log}{RESET}", flush=True)
            if "steps" in chunk:
                for step in chunk["steps"]:
                    print(f"{GRAY}Observation: {step.observation}{RESET}", flush=True)
            if "output" in chunk:
                final = chunk["output"]
    except Exception as exc:  # pragma: no cover - network call
        print(f"{GRAY}Error: {exc}{RESET}")
        print("[NEURO_END]", flush=True)
        return

    print(f"{GRAY}Agent Output:\n{final}{RESET}")
    print("[NEURO_END]", flush=True)


if __name__ == "__main__":
    main()
