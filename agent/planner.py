"""Simple planning module for the NeuroShell agent."""
from typing import Any, Dict, List


def plan_steps(intent: Dict[str, Any]) -> List[str]:
    """Convert a parsed intent into executable steps.

    This is a placeholder implementation that simply describes the intent.
    """
    action = intent.get("action", "do_something")
    description = intent.get("description", "")
    return [f"Action: {action}", f"Description: {description}"]
