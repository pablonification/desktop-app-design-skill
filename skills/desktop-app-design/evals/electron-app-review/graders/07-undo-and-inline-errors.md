---
type: llm
focus: trace
weight: 1
---

The fixed Dashboard.jsx no longer uses window.confirm for deleting a monitor; it offers undo (or a proper non-browser confirmation justified as irreversible), and errors are no longer only a generic 'Something went wrong' toast — the message says what failed and what to do
