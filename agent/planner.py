"""Planning module for the NeuroShell agent."""
import json
import os
from typing import Any, Dict, List

from dotenv import load_dotenv

load_dotenv()

import openai


def plan_steps(intent: Dict[str, Any]) -> List[str]:
    """Convert a parsed intent dictionary into an ordered list of steps.

    The intent object is sent to an OpenAI model which returns a JSON array of
    strings describing the high-level steps required to fulfil the intent.
    On error or invalid responses, a single-element list describing the error is
    returned instead.
    """

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        return ["Error: OPENAI_API_KEY environment variable not set"]

    messages = [
        {
            "role": "system",
            "content": (
                "You are a planning module for a shell-based AI assistant. "
                "Given a JSON object describing an intent, respond ONLY with "
                "a JSON array containing short, ordered steps to accomplish "
                "that intent."
            ),
        },
        {"role": "user", "content": json.dumps(intent)},
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        content = response.choices[0].message.content.strip()
        steps = json.loads(content)
        if not isinstance(steps, list):
            return ["Error: Planning output was not a list"]
        return [str(step) for step in steps]
    except Exception as exc:  # broad catch to avoid raising inside shell
        return [f"Error: {exc}"]
