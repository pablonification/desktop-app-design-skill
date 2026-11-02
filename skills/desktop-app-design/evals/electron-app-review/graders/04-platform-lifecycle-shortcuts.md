---
type: llm
focus: trace
weight: 1
---

The fixed main.js keeps the app running on macOS when all windows are closed (a process.platform !== 'darwin' check, plus re-creating a window on 'activate') and uses CmdOrCtrl (or CommandOrControl) instead of a hard-coded Ctrl accelerator
