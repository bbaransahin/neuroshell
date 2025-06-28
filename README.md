Neuroshell is an AI embedded terminal and focused on making the terminal more ambient, fun and easy.

## Windowless GUI

The project now includes a minimal terminal-based GUI implemented with the
`curses` library. It runs full-screen with no window decorations and presents a
single input line at the bottom. Type a command and press **Enter** to send it.
Press `Esc` to exit. The script lives in `gui/windowless.py` and is designed to
be easily extended with ambient animations in the future.
