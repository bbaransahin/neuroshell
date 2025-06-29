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
    const fitAndResize = () => {
      fitAddon.fit();
      ipcRenderer.send('resize', { cols: term.cols, rows: term.rows });
    };
    fitAndResize();

    const viewport = containerRef.current.querySelector('.xterm-viewport');
    if (viewport) {
      let snapTimeout;
      const animateTo = (target) => {
        const start = viewport.scrollTop;
        const diff = target - start;
        const startTime = performance.now();
        const duration = 150;
        const step = (t) => {
          const progress = Math.min((t - startTime) / duration, 1);
          viewport.scrollTop = start + diff * progress;
          if (progress < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      };

      const alignViewport = () => {
        const cellHeight = term._core?._renderService.dimensions.css.cell.height;
        if (!cellHeight) return;
        const target = Math.round(viewport.scrollTop / cellHeight) * cellHeight;
        if (target !== viewport.scrollTop) {
          animateTo(target);
        }
      };

      const scheduleSnap = () => {
        clearTimeout(snapTimeout);
        snapTimeout = setTimeout(alignViewport, 100);
      };

      viewport.addEventListener(
        'wheel',
        (e) => {
          e.preventDefault();
          e.stopPropagation();
          viewport.scrollTop += e.deltaY;
          scheduleSnap();
        },
        { passive: false }
      );
    }
    term.focus();
    term.onData(data => ipcRenderer.send('terminal-data', data));
    ipcRenderer.on('shell-data', (_, d) => term.write(d));
    ipcRenderer.send('start-shell', { cols: term.cols, rows: term.rows });
    window.addEventListener('resize', fitAndResize);
  }, []);

  return React.createElement('div', { ref: containerRef, style: { height: '100%', width: '100%' } });
}

ReactDOM.render(
  React.createElement(TerminalApp, null, null),
  document.getElementById('root')
);
