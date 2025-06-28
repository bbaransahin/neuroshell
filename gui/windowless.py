"""Minimal windowless GUI built with curses.

This script creates a full-screen, borderless interface that captures user input
from the bottom of the terminal. Future versions can draw animations or other
effects on the main screen area.
"""

import curses


class WindowlessGUI:
    """Simple text input interface using curses."""

    def __init__(self) -> None:
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.height, self.width = self.screen.getmaxyx()
        self.inputWin = curses.newwin(1, self.width, self.height - 1, 0)

    def _refreshBackground(self) -> None:
        """Placeholder for future animated background."""
        self.screen.clear()
        self.screen.refresh()

    def _readInput(self) -> str:
        buffer = []
        while True:
            self.inputWin.clear()
            self.inputWin.addstr(0, 0, "".join(buffer))
            self.inputWin.refresh()
            ch = self.inputWin.getch()
            if ch in (curses.KEY_ENTER, 10, 13):
                return "".join(buffer)
            if ch in (27,):  # ESC
                return ""
            if ch in (curses.KEY_BACKSPACE, 127, 8):
                if buffer:
                    buffer.pop()
            elif 32 <= ch < 127:
                buffer.append(chr(ch))

    def run(self) -> None:
        try:
            while True:
                self._refreshBackground()
                user_input = self._readInput()
                if not user_input:
                    break
                print(user_input)
        finally:
            curses.nocbreak()
            self.screen.keypad(False)
            curses.echo()
            curses.endwin()


if __name__ == "__main__":
    gui = WindowlessGUI()
    gui.run()
