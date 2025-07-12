"""Shell tool used by the NeuroShell agent."""
import subprocess
from typing import List

def run_command(cmd: List[str]) -> str:
    """Run a shell command using shell=True to support redirection, pipes, etc."""
    result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
    return result.stdout or result.stderr

