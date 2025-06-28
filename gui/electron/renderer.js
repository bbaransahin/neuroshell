const { ipcRenderer } = require('electron');
const React = require('react');
const ReactDOM = require('react-dom');
const { Terminal } = require('xterm');

function TerminalApp() {
  const containerRef = React.useRef(null);

  React.useEffect(() => {
    const term = new Terminal();
    term.open(containerRef.current);
    term.onData(data => ipcRenderer.send('terminal-data', data));
    ipcRenderer.on('shell-data', (_, d) => term.write(d));
    ipcRenderer.send('start-shell');
  }, []);

  return React.createElement('div', { ref: containerRef, style: { height: '100%', width: '100%' } });
}

ReactDOM.render(
  React.createElement(TerminalApp, null, null),
  document.getElementById('root')
);
