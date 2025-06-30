"""Intent parser for NeuroShell agent."""
import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
load_dotenv()

import openai


def parse_intent(text: str) -> Dict[str, Any]:
    """Parse natural language instructions into a structured intent dictionary.

    Parameters
    ----------
    text: str
        Natural language user input describing the desired action.

    Returns
    -------
    dict
        Parsed intent as a dictionary. On failure, returns a dictionary with an
        ``error`` key describing the issue.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        return {"error": "OPENAI_API_KEY environment variable not set"}

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intent parser for a shell-based AI assistant. "
                "Given a user instruction, respond ONLY with a JSON object "
                "describing the intent. The JSON should be short and use \"action\" "
                "and other relevant fields."
            ),
        },
        {"role": "user", "content": text},
    ]

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        content = response.choices[0].message.content.strip()
        parsed = json.loads(content)
        parsed["user_input"] = text
        return parsed
    except Exception as exc:  # broad catch to avoid raising inside shell
        return {"error": str(exc)}
