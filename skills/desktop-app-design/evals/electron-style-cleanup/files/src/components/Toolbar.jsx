export default function Toolbar({ title, onNew, onShare, saving }) {
  return (
    <header className="toolbar">
      <span className="toolbar-title">{title}</span>
      <span style={{ color: '#a8a8a8', fontSize: 12, marginLeft: 6 }}>{saving ? 'Saving…' : 'Saved'}</span>
      <div style={{ marginLeft: 'auto', display: 'flex', gap: 6 }}>
        <button onClick={onShare}>Share</button>
        <button className="primary" onClick={onNew}>New Note</button>
      </div>
    </header>
  );
}
