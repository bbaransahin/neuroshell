const { ipcRenderer } = require('electron');
const React = require('react');
const ReactDOM = require('react-dom');
const { Terminal } = require('xterm');
const { FitAddon } = require('@xterm/addon-fit');

function TerminalApp() {
  const containerRef = React.useRef(null);

  React.useEffect(() => {
    const theme = {
      background: 'transparent',
      foreground: '#222222',
      cursor: '#222222',
      selection: 'rgba(0,0,0,0.25)',
      black: '#0a0a0a',
      red: '#c94f6d',
      green: '#50a14f',
      yellow: '#c18401',
      blue: '#4078f2',
      magenta: '#a626a4',
      cyan: '#0184bc',
      white: '#c0c0c0',
      brightBlack: '#808080',
      brightRed: '#ec6a88',
      brightGreen: '#8dc891',
      brightYellow: '#f6c177',
      brightBlue: '#73baf9',
      brightMagenta: '#d670d6',
      brightCyan: '#5dbbc1',
      brightWhite: '#ffffff'
    };

    const term = new Terminal({ theme });
    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(containerRef.current);
    const root = document.getElementById('root');

    const setAgentTheme = (active) => {
      if (!root) return;
      if (active) {
        root.style.setProperty('--cloud-color1', '#ff9a9e');
        root.style.setProperty('--cloud-color2', '#fecfef');
        root.style.setProperty('--cloud-speed', '20s');
      } else {
        root.style.setProperty('--cloud-color1', '#a1c4fd');
        root.style.setProperty('--cloud-color2', '#c2e9fb');
        root.style.setProperty('--cloud-speed', '60s');
      }
    };
    const fitAndResize = () => {
      fitAddon.fit();
      ipcRenderer.send('resize', { cols: term.cols, rows: term.rows });
    };
    fitAndResize();

    const viewport = containerRef.current.querySelector('.xterm-viewport');
    if (viewport) {
      let scrollTimeout;
      viewport.addEventListener('scroll', () => {
        viewport.classList.add('scrolling');
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => viewport.classList.remove('scrolling'), 800);
      });
    }
    term.focus();
    term.onData(data => ipcRenderer.send('terminal-data', data));
    ipcRenderer.on('shell-data', (_, d) => {
      if (d.includes('[NEURO_START]')) {
        setAgentTheme(true);
        d = d.replace('[NEURO_START]', '');
      }
      if (d.includes('[NEURO_END]')) {
        setAgentTheme(false);
        d = d.replace('[NEURO_END]', '');
      }
      term.write(d);
    });
    ipcRenderer.send('start-shell', { cols: term.cols, rows: term.rows });
    window.addEventListener('resize', fitAndResize);
  }, []);

  return React.createElement('div', { ref: containerRef, style: { height: '100%', width: '100%' } });
}

ReactDOM.render(
  React.createElement(TerminalApp, null, null),
  document.getElementById('root')
);
