"""Executor for the NeuroShell agent."""
from typing import List


def execute_steps(steps: List[str]) -> None:
    """Execute a list of plain-text steps.

    Currently this function simply prints each step to the console.
    """
    for step in steps:
        print(step)
