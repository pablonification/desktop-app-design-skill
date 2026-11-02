---
type: llm
focus: trace
weight: 1
---

The fixed main.js avoids the white flash on launch by creating the window with show:false and showing it on 'ready-to-show', and/or by setting backgroundColor to the app's surface color
