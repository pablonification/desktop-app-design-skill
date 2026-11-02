const { app, BrowserWindow, Menu, globalShortcut, ipcMain } = require('electron');
const path = require('path');

let win;

function createWindow() {
  win = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 1100,
    minHeight: 700,
    frame: false,
    webPreferences: { preload: path.join(__dirname, 'preload.js') },
  });
  win.loadURL(process.env.VITE_DEV_SERVER_URL || `file://${__dirname}/dist/index.html`);
}

app.whenReady().then(() => {
  Menu.setApplicationMenu(null);
  createWindow();
  globalShortcut.register('Ctrl+Shift+M', () => win.show());
});

ipcMain.on('win:minimize', () => win.minimize());
ipcMain.on('win:maximize', () => (win.isMaximized() ? win.unmaximize() : win.maximize()));
ipcMain.on('win:close', () => win.close());

app.on('window-all-closed', () => app.quit());
