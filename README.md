Neuroshell is an AI embedded terminal and focused on making the terminal more ambient, fun and easy.

## Windowless GUI

The GUI is built with **Electron**, **React**, and **xterm.js**. It opens a borderless window (800x600 by default) and runs your shell through `node-pty`. The terminal resizes to fit the window and is ready for future animated backgrounds.

### Running the GUI

```bash
cd gui/electron
npm install
npx electron-rebuild
npm start
```
