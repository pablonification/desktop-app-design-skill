import { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Trash2, Pencil } from 'lucide-react';
import toast from 'react-hot-toast';
import TitleBar from './TitleBar';
import './styles.css';

const MONITORS = [
  { id: 1, name: 'Lorem ipsum API', url: 'https://api.example.com', status: 'up', uptime: '99.9%', latency: 120 },
  { id: 2, name: 'Marketing site', url: 'https://example.com', status: 'down', uptime: '97.1%', latency: 0 },
  { id: 3, name: 'Billing webhooks', url: 'https://hooks.example.com/billing', status: 'up', uptime: '100%', latency: 87 },
];

export default function Dashboard() {
  const [monitors, setMonitors] = useState(MONITORS);

  async function remove(id) {
    if (!window.confirm('Are you sure?')) return;
    try {
      await window.api.deleteMonitor(id);
      setMonitors((m) => m.filter((x) => x.id !== id));
      toast.success('Deleted!');
    } catch (e) {
      toast.error('Something went wrong');
    }
  }

  return (
    <div className="app">
      <TitleBar />
      <aside className="sidebar">
        <a className="nav active">📊 Dashboard</a>
        <a className="nav">🔔 Alerts</a>
        <a className="nav">📁 Reports</a>
        <a className="nav">⚙️ Settings</a>
      </aside>
      <main className="content">
        <section className="hero">
          <h1 className="hero-title">Welcome back, John Doe 👋</h1>
          <p className="muted">Here's what's happening with your monitors today.</p>
          <button className="ai-button"><Sparkles size={16} /> Ask AI</button>
        </section>

        <div className="stats">
          {['Uptime', 'Incidents', 'Avg latency', 'Monitors'].map((label, i) => (
            <motion.div key={label} className="card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: i * 0.15 }}>
              <span className="muted">{label}</span>
              <strong className="stat">{['99.2%', '3', '104ms', '$1,234'][i]}</strong>
            </motion.div>
          ))}
        </div>

        <table className="table">
          <tbody>
            {monitors.map((m) => (
              <tr key={m.id} className="row">
                <td>{m.name}</td>
                <td className="muted">{m.url}</td>
                <td><span className={m.status === 'up' ? 'dot green' : 'dot red'} /></td>
                <td>{m.uptime}</td>
                <td>{m.latency}ms</td>
                <td className="row-actions">
                  <button onClick={() => {}}><Pencil size={14} /></button>
                  <button onClick={() => remove(m.id)}><Trash2 size={14} /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}
