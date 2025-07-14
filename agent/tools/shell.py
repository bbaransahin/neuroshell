"""Shell tool used by the NeuroShell agent."""

from __future__ import annotations

import subprocess
from typing import List


def run_command(cmd: List[str], *, max_chars: int = 2000) -> str:
    """Run a shell command and return at most ``max_chars`` of its output."""

    result = subprocess.run(
        " ".join(cmd),
        shell=True,
        capture_output=True,
        text=True,
    )

    output = result.stdout or result.stderr
    if len(output) > max_chars:
        output = output[:max_chars] + "\n...[truncated]..."
    return output

