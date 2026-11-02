export type Command = {
  id: string;
  title: string;
  section: 'Create' | 'Go to' | 'View' | 'Account';
  keywords?: string[];
  // Platform-neutral shortcut: "Mod" means ⌘ on macOS and Ctrl elsewhere.
  shortcut?: string;
  run: () => void;
};

const log = (msg: string) => () => console.log(msg);

export const commands: Command[] = [
  { id: 'new-invoice', title: 'New Invoice', section: 'Create', keywords: ['bill', 'create'], shortcut: 'Mod+N', run: log('new invoice') },
  { id: 'new-expense', title: 'New Expense', section: 'Create', keywords: ['receipt', 'spend'], shortcut: 'Mod+Shift+E', run: log('new expense') },
  { id: 'new-client', title: 'New Client', section: 'Create', keywords: ['customer', 'contact'], run: log('new client') },
  { id: 'go-dashboard', title: 'Go to Dashboard', section: 'Go to', keywords: ['home', 'overview'], shortcut: 'Mod+1', run: log('dashboard') },
  { id: 'go-invoices', title: 'Go to Invoices', section: 'Go to', keywords: ['bills'], shortcut: 'Mod+2', run: log('invoices') },
  { id: 'go-expenses', title: 'Go to Expenses', section: 'Go to', shortcut: 'Mod+3', run: log('expenses') },
  { id: 'go-reports', title: 'Go to Reports', section: 'Go to', keywords: ['profit', 'loss', 'tax'], shortcut: 'Mod+4', run: log('reports') },
  { id: 'toggle-sidebar', title: 'Toggle Sidebar', section: 'View', shortcut: 'Mod+Alt+S', run: log('sidebar') },
  { id: 'toggle-density', title: 'Switch to Compact Rows', section: 'View', keywords: ['density', 'dense'], run: log('density') },
  { id: 'export-csv', title: 'Export Transactions as CSV…', section: 'View', keywords: ['download', 'spreadsheet'], shortcut: 'Mod+Shift+X', run: log('export') },
  { id: 'settings', title: 'Settings…', section: 'Account', keywords: ['preferences', 'options'], shortcut: 'Mod+,', run: log('settings') },
  { id: 'sign-out', title: 'Sign Out', section: 'Account', keywords: ['logout', 'log out'], run: log('sign out') },
];
