---
tags: [skill-creator]
max_turns: 35
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

add a command palette to my tauri + react app (⌘K on mac, ctrl+k on windows/linux). the commands are already in src/commands.ts. i want it to feel really polished, like raycast or linear quality, not a generic modal. don't add new npm dependencies. put the component in src/CommandPalette.tsx and wire it into App.tsx.

Input files: package.json, src/App.tsx, src/commands.ts, src/styles.css, src-tauri/tauri.conf.json
