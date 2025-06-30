"""Simple in-memory log for the NeuroShell agent."""
from typing import List


class Memory:
    """Stores past interactions in memory."""

    def __init__(self) -> None:
        self.logs: List[str] = []

    def add(self, entry: str) -> None:
        """Add a log entry."""
        self.logs.append(entry)

    def get(self) -> List[str]:
        """Return all log entries."""
        return self.logs
