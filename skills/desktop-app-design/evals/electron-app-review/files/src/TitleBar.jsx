export default function TitleBar() {
  const send = (msg) => window.electron.send(msg);
  return (
    <div className="titlebar" style={{ WebkitAppRegion: 'drag' }}>
      <span className="titlebar-name">✨ PulseDesk</span>
      <div className="titlebar-buttons">
        <button onClick={() => send('win:minimize')}>—</button>
        <button onClick={() => send('win:maximize')}>▢</button>
        <button className="close" onClick={() => send('win:close')}>✕</button>
      </div>
    </div>
  );
}
