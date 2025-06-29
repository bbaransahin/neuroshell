const { app, BrowserWindow, ipcMain } = require('electron');
const os = require('os');
const pty = require('node-pty');

let ptyProcess;
let win;

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 100,
    minHeight: 100,
    frame: false,
    fullscreen: false,
    autoHideMenuBar: true,
    transparent: true,
    backgroundColor: '#00000000',
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

ipcMain.on('start-shell', (event, size = {}) => {
  const shell = os.platform() === 'win32' ? 'powershell.exe' : process.env.SHELL || 'bash';
  const { cols = 80, rows = 24 } = size;
  ptyProcess = pty.spawn(shell, [], {
    name: 'xterm-color',
    cols,
    rows,
    cwd: process.env.HOME,
    env: process.env
  });
  ptyProcess.on('data', (data) => event.sender.send('shell-data', data));
  ptyProcess.on('exit', () => {
    if (win) {
      win.close();
    }
    app.quit();
  });
});

ipcMain.on('terminal-data', (_, data) => {
  ptyProcess && ptyProcess.write(data);
});

ipcMain.on('resize', (_, size) => {
  if (ptyProcess && size) {
    ptyProcess.resize(size.cols, size.rows);
  }
});
