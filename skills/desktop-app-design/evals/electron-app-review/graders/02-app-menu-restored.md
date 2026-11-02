---
type: llm
focus: trace
weight: 1
---

The fixed main.js no longer calls Menu.setApplicationMenu(null); it builds an application menu from roles (e.g. appMenu/editMenu/viewMenu/windowMenu or undo/copy/paste/zoom) or keeps the default menu, and the response says why (Mac menu bar, Undo/Copy/Paste/Zoom)
