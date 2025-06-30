"""Simple planning module for the NeuroShell agent."""
from typing import Any, Dict, List


def _get_file_name(intent: Dict[str, Any]) -> str | None:
    """Return a file name from the intent if present."""
    for key in ("file", "filename", "path", "filepath"):
        value = intent.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def plan_steps(intent: Dict[str, Any]) -> List[str]:
    """Convert a parsed intent into executable steps.

    The planner performs a very small set of rule-based translations from a
    structured intent dictionary into human readable steps.  It is intentionally
    simple so the caller can later convert these steps into tool invocations.
    """

    steps: List[str] = []

    # Use any natural language description as the first step if available.
    description = (
        intent.get("description")
        or intent.get("goal")
        or intent.get("user_input")
    )
    if isinstance(description, str) and description:
        steps.append(description)

    action = intent.get("action", "").lower()
    file_name = _get_file_name(intent)

    if action in {"create_file", "write_code", "create_python_script", "add_file"}:
        # Create a new file and populate it with code/content
        if file_name:
            steps.append(f"Create the file {file_name}")
        else:
            steps.append("Create the target file")

        if file_name:
            steps.append(f"Write code into {file_name}")
        else:
            steps.append("Write the provided code")

    elif action in {"run_command", "execute", "command"}:
        command = intent.get("command")
        if isinstance(command, list):
            cmd_str = " ".join(str(part) for part in command)
        else:
            cmd_str = str(command) if command is not None else ""

        if cmd_str:
            steps.append(f"Run the command {cmd_str}")
        else:
            steps.append("Run the specified command")

    elif action in {"install_package", "pip_install"}:
        pkg = intent.get("package") or intent.get("packages")
        if isinstance(pkg, list):
            pkg_str = " ".join(pkg)
        elif isinstance(pkg, str):
            pkg_str = pkg
        else:
            pkg_str = ""
        if pkg_str:
            steps.append(f"Install package(s) {pkg_str}")
        else:
            steps.append("Install the required package")

    # Fallback: if specific rules didn't add any additional steps, describe the
    # action in a generic way.
    if len(steps) <= (1 if description else 0):
        if action:
            steps.append(f"Action: {action}")
        else:
            steps.append("Determine appropriate action from intent")

    return steps
