Neuroshell is an AI embedded terminal and focused on making the terminal more ambient, fun and easy.

## Windowless GUI

The GUI is built with **Electron**, **React**, and **xterm.js**. It opens a borderless window (800x600 by default) and runs your shell through `node-pty`. The terminal resizes to fit the window and is ready for future animated backgrounds.

Type `exit` inside the terminal to close the shell and quit the GUI.

### Agent Command

Inside the GUI shell you can run the NeuroShell agent by typing:

```bash
neuro <your request here>
```

While the agent runs, the background clouds turn reddish and move faster.
When finished, the theme returns to normal.

### Running the GUI

```bash
cd gui/electron
npm install
npx electron-rebuild
npm start
```
