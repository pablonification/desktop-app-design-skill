import './styles.css';

export default function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <nav>
          <a className="nav-item is-active">Dashboard</a>
          <a className="nav-item">Invoices</a>
          <a className="nav-item">Expenses</a>
          <a className="nav-item">Reports</a>
        </nav>
      </aside>
      <main className="content">
        <h1 className="page-title">Dashboard</h1>
        <p className="secondary">October 2026 · 14 open invoices · €18,420.00 outstanding</p>
      </main>
    </div>
  );
}
