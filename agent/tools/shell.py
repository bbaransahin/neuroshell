"""Shell tool used by the NeuroShell agent."""
import subprocess
from typing import List


def run_command(cmd: List[str]) -> str:
    """Run a shell command and return its output."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
