const { ipcRenderer } = require('electron');
const React = require('react');
const ReactDOM = require('react-dom');
const { Terminal } = require('xterm');
const { FitAddon } = require('@xterm/addon-fit');

function TerminalApp() {
  const containerRef = React.useRef(null);

  React.useEffect(() => {
    const term = new Terminal({
      theme: { background: 'transparent' }
    });
    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(containerRef.current);
    fitAddon.fit();

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
    ipcRenderer.on('shell-data', (_, d) => term.write(d));
    ipcRenderer.send('start-shell');
    window.addEventListener('resize', () => fitAddon.fit());
  }, []);

  return React.createElement('div', { ref: containerRef, style: { height: '100%', width: '100%' } });
}

ReactDOM.render(
  React.createElement(TerminalApp, null, null),
  document.getElementById('root')
);
