# Cross-platform desktop: convention differences and frameworks

Read this when one codebase ships to more than one desktop OS (Electron, Tauri, Flutter, Qt, Compose Multiplatform, Avalonia, Wails, React Native), or when you need the exact per-OS difference for shortcuts, dialog button order, window controls, wording or fonts. The platform files hold each OS's own rules in depth. Every rule cites its source inline; ⚠️ marks claims that couldn't be fully verified (collected at the end). Researched November 2026 — platform details change, so re-check anything version-specific.

Contents: 0. Golden rules · Part A — Platform convention differences · Part B — Frameworks · Part C — "Web app in a window" smells and fixes · Unverified / open questions

## 0. Golden rules (read first)
1. **Detect the platform once, then branch on conventions, not just looks.** Keep one command model (id, label, shortcut, enabled) and render it per OS: mac global menu bar + ⌘ shortcuts; Windows in-window menu/CommandBar + Ctrl and Alt access keys; GNOME header bar + primary "Main Menu"; KDE hamburger or menu bar (A1).
2. **Shortcuts come from a per-OS table, never one literal string.** Redo = ⇧⌘Z / Ctrl+Y / Shift+Ctrl+Z; Settings = ⌘, / (none) / Ctrl+, / Ctrl+Shift+,; Find next = ⌘G / F3 / Ctrl+G / F3 (A2). Use framework helpers (`CmdOrCtrl`, Qt `StandardKey`, Electron/Tauri roles/predefined items).
3. **Dialog button order is platform-specific.** mac & GNOME: Cancel left, default right. Windows & KDE: OK/do-it left, Cancel right. Label with verbs. Destructive → no Return default (GNOME) / Cancel never default (mac) (A3).
4. **Keep native window controls and behaviours** even with a custom title bar: traffic lights top-left on mac; caption buttons via Window Controls Overlay on Win/Linux; read GNOME's `button-layout` (default: close only, right); honour double-click and right-click on the title bar (A1, B1, B2).
5. **Lifecycle:** mac app stays alive with zero windows and reopens on dock click; Windows/Linux quit on last window close (unless a tray app). Never make the tray the only way back on GNOME (no tray by default) (A1, A4).
6. **Arrow cursor on buttons, hand only on links** (Apple, Microsoft, KDE; Flutter 3.41+ default). No text selection on chrome. No whole-window bounce. No white flash. No spinner for local data (Part C).
7. **System font + platform size + OS dark mode/accent/contrast/reduced motion.** SF 13pt / Segoe UI Variable 14px / Adwaita Sans 11pt / Noto Sans 10pt (A4).
8. **Native file dialogs, native notifications, native context menus — always.** On Linux go through XDG portals (A4).
9. **Webview apps (Tauri/Wails) target the oldest WebKit you support**, not Chrome: prefix `-webkit-user-select`, `-webkit-backdrop-filter`; feature-detect View Transitions, anchor positioning, scrollbar styling (B2).
10. **Wording:** "Settings…" (mac) / "Settings" (Win) / "Preferences" (GNOME) / "Configure <App>…" (KDE); Quit vs Exit; Trash vs Recycle Bin; Title Case (mac, KDE) vs sentence case (Windows) vs header caps (GNOME) (A1, A3).

## Part A — Platform convention differences

### A1. Window chrome, menus, settings, lifecycle
Short source keys used below: **HIG-menu** https://developer.apple.com/design/human-interface-guidelines/the-menu-bar · **HIG-kbd** https://developer.apple.com/design/human-interface-guidelines/keyboards · **Win-title** https://learn.microsoft.com/en-us/windows/apps/design/basics/titlebar-design · **Win-acc** https://learn.microsoft.com/en-us/windows/apps/design/input/keyboard-accelerators · **GN-menu** https://developer.gnome.org/hig/patterns/controls/menus.html · **GN-kbd** https://developer.gnome.org/hig/reference/keyboard.html · **KDE-nav** https://develop.kde.org/hig/layout_and_nav/ · **Qt-keys** https://doc.qt.io/qt-6/qkeysequence.html#standard-shortcuts (per-platform table) · **KDE-sc** https://invent.kde.org/frameworks/kconfig/-/blob/master/src/gui/kstandardshortcut.cpp

| | macOS | Windows 11 | GNOME (libadwaita) | KDE Plasma (Breeze) |
|---|---|---|---|---|
| Window controls | Traffic lights, **top-left**: close, minimize, zoom (green = full screen; ⌥ = zoom) | Caption buttons **top-right**: min, max/restore, close; 32px-tall title bar; full-bleed hover backplates; Segoe Fluent glyphs E921/E922/E923/E8BB (Win-title) | Default gsetting `button-layout = 'appmenu:close'` → **Close only, right** (https://gitlab.gnome.org/GNOME/gsettings-desktop-schemas/-/blob/master/schemas/org.gnome.desktop.wm.preferences.gschema.xml.in). Users/distros change it (Ubuntu adds min/max ⚠️). Read it; never assume | Default right: help, minimize, maximize, close; left: window menu, on-all-desktops (https://invent.kde.org/plasma/kwin/-/blob/master/src/decorations/settings.cpp) |
| Title bar double-click | User setting: Fill / Zoom / Minimize / No Action (System Settings › Desktop & Dock) (https://support.apple.com/guide/mac-help/change-desktop-dock-settings-mchlp1119/mac) | Toggle maximize/restore; single-click icon = system menu; double-click icon = close (Win-title) | `action-double-click-titlebar = 'toggle-maximize'`, right-click = window menu (gsettings schema above) | Maximize (KWin setting) ⚠️ |
| Title bar content | Unified toolbar under/merged with title; title centered or hidden | Icon 16px + title left; title bar blends with Mica; elements go semi-transparent when inactive (Win-title) | Header bar: main actions at start, title/view switcher center, menus at end; always leave blank space to drag (https://developer.gnome.org/hig/patterns/containers/header-bars.html) | Separate title bar + toolbar (+ optional menu bar between them) |
| App menu | **Global menu bar** at top of screen; first menu = app name (About, Settings…, Services, Hide, Quit) (HIG-menu) | In-window menu bar (File Edit View Tools Help) for document apps; modern WinUI apps use NavigationView/CommandBar instead (https://learn.microsoft.com/en-us/windows/win32/uxguide/cmd-menus) | **No menu bar.** Primary menu = `open-menu-symbolic` button at end of header bar, named "Main Menu", contains Preferences, Keyboard Shortcuts, Help, About <App>; **no Quit/Close in it** (GN-menu) | ≤~15 global actions → hamburger (`application-menu` icon); more → real menu bar between title bar and toolbar; no Quit/Minimize in hamburger (KDE-nav). `KHamburgerMenu` gives both |
| Settings | **App menu › Settings…**, ⌘, (older apps say "Preferences…"; Apple's shortcut list: "Open settings (preferences)" https://support.apple.com/en-us/102650); settings window: dim min/zoom buttons (https://developer.apple.com/design/human-interface-guidelines/settings) | "Settings" page, last item pinned at bottom of NavigationView (`IsSettingsVisible=true`) or last in "More" overflow; full-window page, max ~1000–1100px wide, SettingsCard/SettingsExpander; **no standard shortcut** (Qt-keys row empty) (https://learn.microsoft.com/en-us/windows/apps/design/app-settings/guidelines-for-app-settings). Legacy Win32: Tools › Options | **Preferences**, Ctrl+, (GN-kbd), `AdwPreferencesDialog` | **Settings › Configure <AppName>…**, Ctrl+Shift+, ; also Configure Keyboard Shortcuts… (Ctrl+Alt+,), Configure Toolbars… (KDE-sc; https://invent.kde.org/frameworks/kxmlgui) |
| Quit wording / key | "Quit <App>" ⌘Q (HIG-kbd) | "Exit"; Alt+F4 closes the window; no app-level quit shortcut (Qt-keys `Quit` empty for Windows) | "Quit" Ctrl+Q (GN-kbd), not in primary menu | "Quit" Ctrl+Q (KDE-sc) |
| Last window closed | App **keeps running** (dock icon + menu bar stay); clicking the dock icon reopens a window. AppKit default: `applicationShouldTerminateAfterLastWindowClosed` → `false` (https://developer.apple.com/documentation/appkit/nsapplicationdelegate/applicationshouldterminateafterlastwindowclosed(_:); https://www.electronjs.org/docs/latest/tutorial/tutorial-first-app). Single-window utilities may opt to quit | App exits | App exits (unless it's a background app) | App exits (unless it has a tray icon) |
| Capitalization | Title Case for menus, buttons (https://developer.apple.com/design/human-interface-guidelines/menus) | **Sentence case for all UI text** incl. titles (https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/typography) | Header Capitalization for buttons/menus/headings; sentence case for checkbox/radio/field labels (https://developer.gnome.org/hig/guidelines/writing-style.html) | Title Case except sentences, tooltips, subtitles, checkbox/radio/field labels (https://develop.kde.org/hig/text_and_labels/) |
| Ellipsis "…" | Item needs more input (Open…, Settings…) | Same (Win32 UX guide) | Same | Same; use real U+2026 (KDE text_and_labels) |

Rules:
- Build *one* command model (id, label, shortcut, enabled) and render it as: mac global menu bar; Windows menu bar or CommandBar; GNOME primary menu + header-bar buttons; KDE hamburger/menu bar. Don't ship a mac-style global menu on Windows/Linux or a hamburger on mac.
- On mac, never put Settings/Quit/About anywhere but the app menu (you may *also* add a settings button in-window). On GNOME, never add Quit to the primary menu.
- Custom title bars must still: drag from empty space, double-click per OS, right-click → system window menu (Win/Linux), keep native caption buttons (Electron `titleBarOverlay`, Tauri decorations) and respect left/right placement.

### A2. Keyboard
Mapping rule: mac **⌘ = Ctrl** elsewhere for app shortcuts; mac **⌥ = Alt**; mac **⌃ (Control)** is mostly for text/emacs keys and system — don't map Ctrl→⌃. In Qt, `Qt::CTRL` already means ⌘ on mac and `Qt::META` means ⌃ (Qt-keys). In Electron/Tauri write `CmdOrCtrl`.

| Action | macOS | Windows | GNOME | KDE |
|---|---|---|---|---|
| Redo | ⇧⌘Z | **Ctrl+Y** (also Ctrl+Shift+Z) (Win-acc) | Shift+Ctrl+Z (GN-kbd) | Ctrl+Shift+Z (KDE-sc) |
| Full screen | ⌃⌘F (HIG-kbd; also Fn/Globe-F ⚠️) | F11 (Qt-keys) | F11 ⚠️ (Qt-keys says Ctrl+F11; not in GNOME HIG table) | **Ctrl+Shift+F** (also F11 via Qt) (KDE-sc) |
| Close window/tab | ⌘W; ⌥⌘W close all | Ctrl+W (Win-acc), Ctrl+F4 (doc/tab), Alt+F4 (window) | Ctrl+W (tab or window) | Ctrl+W |
| Quit app | ⌘Q | (none; Alt+F4 on last window) | Ctrl+Q | Ctrl+Q |
| Settings | ⌘, | (none standard) | Ctrl+, | Ctrl+Shift+, |
| Find / next / prev | ⌘F / ⌘G / ⇧⌘G | Ctrl+F / **F3** / Shift+F3 | Ctrl+F / Ctrl+G / Shift+Ctrl+G | Ctrl+F / F3 / Shift+F3 |
| Replace | none standard (⌥⌘F = jump to search field, HIG-kbd) | Ctrl+H | Ctrl+H | Ctrl+R (Qt-keys) |
| Rename | Return (Finder) ⚠️ | F2 | F2 | F2 |
| Refresh | ⌘R | F5 / Ctrl+R | Ctrl+R | F5 |
| Help | ⌘? (opens Help menu search) | F1 | F1 | F1 |
| Shortcuts list | — | — | Ctrl+? | Ctrl+Alt+, (configure) |
| Panes / menus | View › Show/Hide Sidebar (⌃⌘S ⚠️ common, not in HIG table) | F6 / Shift+F6 = next/prev pane (Win-acc) | F9 = side pane; F10 = open primary menu | Ctrl+M = show menu bar |
| Delete item | ⌘⌫ (Move to Trash) | Del (with undo); Shift+Del permanent (Win-acc) | Delete → trash | Delete → Move to Trash; Shift+Del delete (KDE-sc) |
| Back / forward | ⌘[ / ⌘] | Alt+← / Alt+→ | Alt+← / Alt+→ | Alt+← / Alt+→ |
| Cancel dialog | Esc **and ⌘.** (https://developer.apple.com/design/human-interface-guidelines/alerts) | Esc | Esc | Esc |

Text editing differences (https://support.apple.com/en-us/102650, Qt-keys):
- The mac key labeled **Delete = Backspace**. Forward delete = Fn-Delete or ⌃D. Never bind an action only to the "Delete" (forward) key on mac — laptops don't have it; use ⌘⌫ for "delete item".
- **Home/End on mac scroll the document; they don't move the caret.** Line start/end = ⌘←/⌘→; doc start/end = ⌘↑/⌘↓; word = ⌥←/⌥→; delete word = ⌥⌫. Windows/Linux: Home/End = line, Ctrl+Home/End = doc, Ctrl+←/→ = word, Ctrl+Backspace = delete word. Native text widgets do this for you; custom editors (canvas, contenteditable with key handlers) must branch on platform.
- mac text fields also support emacs keys (⌃A/⌃E/⌃K/⌃D) — don't steal ⌃-letter combos on mac.

Access keys / mnemonics:
- Windows: Alt+letter; WinUI shows **KeyTips** badges when Alt is pressed (`AccessKey` property); single-char access keys double as Alt+key shortcuts (https://learn.microsoft.com/en-us/windows/apps/design/input/access-keys). Win32 menus underline letters (`&File`).
- GNOME: every labelled control and menu item should get an access key (underline shown while Alt held); **don't use Alt for shortcuts** (conflicts) and never use Super (https://developer.gnome.org/hig/guidelines/keyboard.html, GN-menu). In GTK: `use-underline` / `_File`.
- KDE: `&` mnemonics, auto-assigned by KDE frameworks (KAcceleratorManager ⚠️).
- **macOS: no mnemonics.** Hide underline/`&` markers on mac. Electron: `&File` in top-level menu labels → Alt+F on Win/Linux (https://www.electronjs.org/docs/latest/api/menu); `dialog.showMessageBox({ normalizeAccessKeys: true })` strips `&` on mac, converts to `_` on Linux (https://www.electronjs.org/docs/latest/api/dialog).
- Windows tooltips show the keyboard accelerator by default — include it if you write custom tooltips (https://learn.microsoft.com/en-us/windows/apps/design/controls/tooltips). Do the same on all platforms: "Bold (Ctrl+B)" / "Bold (⌘B)".
- mac Full Keyboard Access: by default Tab only moves between text fields and lists; buttons are reachable only when the user turns on keyboard navigation (HIG focus-and-selection: you only need focus for content elements like list items). Don't force Tab-stops on every button on mac; do on Windows/Linux.

### A3. Dialogs, buttons, terminology
**Button order (horizontal, LTR)** — Qt encodes all four conventions in one table (https://github.com/qt/qtbase/blob/dev/src/gui/kernel/qplatformdialoghelper.cpp, `buttonRoleLayouts`). Qt picks MacLayout on mac, **KdeLayout for all Linux** (GNOME apps should use libadwaita order instead), WinLayout on Windows.

| | Order (left → right) | Default (Return) | Esc | Sources |
|---|---|---|---|---|
| macOS | [Help] [extra] ⋯ [Don't Save] ⋯ [Cancel] **[OK/Save]** | Trailing (rightmost) button | Cancel; also ⌘. | "Always place the default button on the trailing side… Cancel… on the leading side"; never make Cancel default; title it "Cancel" (https://developer.apple.com/design/human-interface-guidelines/alerts) |
| Windows ContentDialog | **[Primary "do it"] [Secondary] [Close/Cancel]** | None by default; set `DefaultButton` | `CloseButton` (also Back, gamepad B) | "do it" buttons leftmost, safe button rightmost (https://learn.microsoft.com/en-us/windows/apps/design/controls/dialogs-and-flyouts/dialogs) |
| Windows Win32 | OK/[Do it]/Yes, [Don't do it]/No, Cancel, Apply, Help — right-aligned | OK/Do it | Cancel | https://learn.microsoft.com/en-us/windows/win32/uxguide/win-dialog-box |
| GNOME | **[Cancel] [Affirmative]** — cancel first ("on the left" in LTR) | Affirmative, *unless* destructive/irreversible → no default | Cancel | https://developer.gnome.org/hig/patterns/feedback/dialogs.html; `AdwAlertDialog` |
| KDE | [Help] [Reset] ⋯ [Yes] [No] [Action] **[OK] [Apply]** [Destructive] [Cancel] (Windows-like: OK before Cancel) | OK | Cancel | Qt KdeLayout |

- Label buttons with verbs ("Save", "Delete", "Move to Trash"), not OK/Yes/No — all four guidelines agree (Apple alerts, MS dialogs, GNOME dialogs, KDE text_and_labels).
- Destructive: mac `hasDestructiveAction`/red text only when the destructive result wasn't what the user deliberately chose (e.g. "Empty Trash" confirm button is *not* styled destructive) (Apple alerts). GNOME `destructive-action` style + no Return default. Windows: no red button; use clear verb + safe Close button. Prefer **undo (toast/snackbar) over confirmation** for reversible deletes (GNOME dialogs; Apple alerts "avoid alerts for common, undoable actions").
- Don't stack dialogs; never open unprompted; always parent/modal to a window (GNOME dialogs, KDE getting_input). mac: document-scoped dialogs are **sheets** attached to the window.
- In code: Qt `QDialogButtonBox` with roles (never hand-order buttons). Electron `dialog.showMessageBox({ buttons, defaultId, cancelId, noLink })` shows buttons in the array order you pass ⚠️ (docs don't promise reordering) → build the array per platform; on Windows Electron turns non-common buttons into command links unless `noLink: true`. Flutter/web/Compose: write a `platformButtonOrder()` helper.

Helper sketch (web stacks; `os` from Tauri `@tauri-apps/plugin-os` `platform()` or Electron `process.platform` mapped `darwin→macos`, `win32→windows`; `desktop` from env `XDG_CURRENT_DESKTOP`):
```ts
type Btn = { label: string; role: 'confirm' | 'cancel' | 'alt' }
function orderButtons(btns: Btn[], os: 'macos'|'windows'|'linux', desktop = ''): Btn[] {
  const by = (r: Btn['role']) => btns.filter(b => b.role === r)
  const gnomeLike = os === 'linux' && !/KDE/i.test(desktop)
  return os === 'macos' || gnomeLike
    ? [...by('alt'), ...by('cancel'), ...by('confirm')]   // confirm rightmost (mac, GNOME)
    : [...by('confirm'), ...by('alt'), ...by('cancel')]   // confirm leftmost (Windows, KDE)
}
const SHORTCUTS = { // per-OS table beats a single "CmdOrCtrl+X" for anything beyond copy/paste
  redo:     { macos: 'Cmd+Shift+Z', windows: 'Ctrl+Y',  gnome: 'Ctrl+Shift+Z', kde: 'Ctrl+Shift+Z' },
  settings: { macos: 'Cmd+,',       windows: null,      gnome: 'Ctrl+,',       kde: 'Ctrl+Shift+,' },
  findNext: { macos: 'Cmd+G',       windows: 'F3',      gnome: 'Ctrl+G',       kde: 'F3' },
  fullscreen:{ macos: 'Ctrl+Cmd+F', windows: 'F11',     gnome: 'F11',          kde: 'Ctrl+Shift+F' },
  quit:     { macos: 'Cmd+Q',       windows: null,      gnome: 'Ctrl+Q',       kde: 'Ctrl+Q' },
} as const
```

**Terminology**
| Concept | macOS | Windows | GNOME | KDE |
|---|---|---|---|---|
| Deleted-items bin | Trash ("Move to Trash") | Recycle Bin ("Delete") | Trash ("Move to Trash") | Trash ("Move to Trash") |
| Reveal file | "Show in Finder" | "Show in File Explorer" / "Open file location" ⚠️ | "Show in Files" ⚠️ (app is "Files", not Nautilus) | "Open Containing Folder" ⚠️ — API for all: Electron `shell.showItemInFolder(path)`, Tauri `plugin-opener` `revealItemInDir` ⚠️ |
| Settings | Settings… | Settings (Win32 legacy: Options) | Preferences | Configure <App>… / Settings menu |
| Quit | Quit <App> | Exit | Quit | Quit |
| Folder | Folder | Folder | Folder | Folder |
| Right-click menu | Context menu (https://developer.apple.com/design/human-interface-guidelines/context-menus) | Context menu | Context menu | Context menu |
| Modifier names | Command ⌘, Option ⌥, Control ⌃, Shift ⇧ — use the **symbols** in menus | Ctrl, Alt, Shift — **text**, joined with "+" | Ctrl, Alt, Shift, "Shift+Ctrl+Z" order in HIG | Ctrl+Shift+Z |

### A4. Fonts, scrollbars, menus, tooltips, cursors, focus, DnD, notifications, tray, file dialogs, clicks

| | macOS | Windows 11 | GNOME | KDE |
|---|---|---|---|---|
| UI font / body size | SF Pro, 13pt body, 10pt min; don't embed system fonts (https://developer.apple.com/design/human-interface-guidelines/typography) | Segoe UI Variable, 14px body (type ramp 14/20 epx); min 12px Regular / 14px Semibold; HTML must name it explicitly (https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/typography) | **Adwaita Sans 11** (Inter-derived, GNOME 48+; was Cantarell) + Adwaita Mono (`org.gnome.desktop.interface font-name` default; https://developer.gnome.org/hig/guidelines/typography.html) | **Noto Sans 10pt** (https://invent.kde.org/plasma/plasma-integration — `kfontsettingsdata.cpp`) |
| Scrollbars | Overlay, appear while scrolling (user can set "always") | Thin panning indicator that morphs into a full scrollbar on pointer hover (https://learn.microsoft.com/en-us/windows/apps/design/controls/scroll-controls) | Overlay indicators (GTK4) | Classic always-visible Breeze scrollbars |
| Context menu | Right-click or **Control-click** | Right-click, Shift+F10, Menu key | Right-click, Shift+F10/Menu, long-press | Right-click, Menu key |
| Tooltips | "Help tags"; optional | Show on hover *and keyboard focus*; include accelerator | **Every header-bar control must have one**; Header Capitalization; don't repeat the label (https://developer.gnome.org/hig/patterns/feedback/tooltips.html) | Sentence case (KDE text_and_labels) |
| Pointer on buttons | **Arrow.** Pointing hand = "URL link" only (`NSCursor.pointingHand`) (https://developer.apple.com/design/human-interface-guidelines/pointing-devices) | **Arrow.** "it is imperative not to use the hand pointer for other purposes… command buttons… don't need a hand pointer" (https://learn.microsoft.com/en-us/windows/win32/uxguide/inter-mouse) | Arrow | "Only use the pointing finger cursor… for underlined web-style links" (https://develop.kde.org/hig/getting_input/) |
| Click to open | Finder lists/icons: double-click opens, single selects | Selectable objects: single-click selects, double-click opens; non-selectable: single click (inter-mouse) | Same as Windows in lists; `activate-on-single-click` for nav lists | User setting: single-click opens files (Plasma default single-click until Plasma 5.25 → now double-click ⚠️) |

**CSS font stack** (Electron/Tauri/Wails):
```css
:root {
  font-family: -apple-system, BlinkMacSystemFont,            /* SF on mac (Chromium + WebKit) */
    "Segoe UI Variable Text", "Segoe UI Variable", "Segoe UI", /* Win 11, Win 10 */
    system-ui,                                                 /* Linux: user's GTK/Plasma font */
    "Adwaita Sans", Cantarell, "Noto Sans", Ubuntu, sans-serif;
  font-size: 13px;                     /* mac; set 14px on Windows, ~14.6px(11pt) GNOME via a platform class */
}
code, pre { font-family: ui-monospace, "SF Mono", "Cascadia Mono", Consolas, "Adwaita Mono", "Noto Sans Mono", monospace; }
```
- `system-ui` = "default UI font on a given platform", meant for UI not long text; can render CJK/Latin poorly on Windows (https://developer.mozilla.org/en-US/docs/Web/CSS/font-family). On Windows Chromium `system-ui` resolves to classic "Segoe UI", not the Variable font ⚠️ → name Segoe UI Variable first. Microsoft: "When using HTML… you will need to specify the Segoe UI Variable font in CSS" (Windows typography page).
- Never ship Inter/Roboto as your *UI* font on desktop unless it's a deliberate brand choice; never hard-code px sizes that ignore OS text scaling (GNOME: "Don't hard-code font styles or sizes").

**Focus rings** — mac: accent-colored halo ring around text fields; lists use selection highlight, not a ring (https://developer.apple.com/design/human-interface-guidelines/focus-and-selection). Windows: two-tone (black + white) focus visual shown only after keyboard input ⚠️ (Fluent "Reveal Focus" page not fetched). GNOME/KDE: ring only after keyboard use. In web stacks: `:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px }` and never `outline: none` without replacement.

**Accent color** — follow the OS accent for selection, focus, primary buttons. CSS `AccentColor`/`AccentColorText` system colors exist but some browsers return a fixed value (anti-fingerprinting) (https://developer.mozilla.org/en-US/docs/Web/CSS/system-color) → inject from native side: Electron `systemPreferences.getAccentColor()`, GNOME `org.gnome.desktop.interface accent-color` (via portal `org.freedesktop.appearance accent-color` ⚠️), Windows `UISettings.GetColorValue(UIColorType.Accent)`.

**Drag & drop** — accept file drops anywhere it makes sense (window, list, editor) and show a drop target highlight; support dragging *out* (Electron `webContents.startDrag({ file, icon })` https://www.electronjs.org/docs/latest/tutorial/native-file-drag-drop). Copy/move modifiers differ: mac ⌥ = copy, ⌘ = move to another volume, ⌥⌘ = alias (https://support.apple.com/en-us/102650; cursors `dragCopy`/`dragLink` in HIG pointing-devices); Windows Ctrl = copy, Shift = move, Alt = shortcut ⚠️. Support spring-loading on mac (HIG drag-and-drop).

**Notifications** — mac: `UNUserNotificationCenter`, needs permission + code signing (Electron 42+). Windows: toast via AppUserModelID (unpackaged apps must set `app.setAppUserModelId()` ⚠️). GNOME: `GNotification` / portal; don't notify about things only relevant while the app is focused (use a toast), remove stale notifications, let users reduce them (https://developer.gnome.org/hig/patterns/feedback/notifications.html).

**Tray / menu bar extras**
- mac: menu-bar extra = monochrome **template** image (system tints it); click shows a **menu, not a popover** (unless complex); **let the user opt in** to showing it; don't rely on it being visible — offer a Dock menu too (https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Menu-bar-extras).
- Windows: notification-area icon only for status/notifications or features without desktop presence; one icon per component; minimize-to-tray must be optional opt-in; status changes subtle (https://learn.microsoft.com/en-us/windows/win32/uxguide/winenv-notification).
- Linux: StatusNotifierItem (Electron uses it, https://www.electronjs.org/docs/latest/api/tray). **Stock GNOME Shell shows no tray icons** without the AppIndicator extension (Ubuntu ships it) (https://github.com/ubuntu/gnome-shell-extension-appindicator) → never make the tray the only way to reach a window or quit; on GNOME prefer the Background portal ⚠️. KDE shows tray icons natively.

**File dialogs: always native.** Electron `dialog.showOpenDialog`, Tauri `plugin-dialog`, Qt `QFileDialog`/`FileDialog` (native by default), Flutter `file_selector`, Compose `FileDialog`/AWT ⚠️. On Linux these go through the **XDG Desktop Portal** FileChooser (required in Flatpak; GTK4 `GtkFileDialog` uses it). Electron: `defaultPath` ignored with portal backends < v4 unless `--xdg-portal-required-version` (https://www.electronjs.org/docs/latest/api/dialog). KDE HIG: "Don't implement a custom file-choosing UI" (https://develop.kde.org/hig/getting_input/). Remember last folder (Electron 43+ no longer does it for you).

## Part B — Frameworks

### B1. Electron (stable 45.x, Chromium 156, Oct 2026; 3 majors supported, 8-week cadence)
Sources: releases https://releases.electronjs.org/releases.json · options https://www.electronjs.org/docs/latest/api/structures/base-window-options · breaking changes https://github.com/electron/electron/blob/main/docs/breaking-changes.md

**Title bar (pick one per platform, don't ship one look everywhere)** — https://www.electronjs.org/docs/latest/tutorial/custom-title-bar
- `titleBarStyle: 'hidden'` → mac keeps traffic lights top-left over full-size content; on Win/Linux you get *no* controls unless you also set `titleBarOverlay`.
- `'hiddenInset'` (mac) → traffic lights inset further (toolbar-style window). `'customButtonsOnHover'` (mac, *experimental*) → lights hidden until hover.
- `trafficLightPosition: {x, y}` (mac) → align lights with your toolbar's vertical center. `win.setWindowButtonVisibility(bool)`.
- `titleBarOverlay: true | {color, symbolColor, height}` → real OS caption buttons (min/max/close) on Win/Linux = Window Controls Overlay. Needs `titleBarStyle` ≠ `'default'`. Keep `height` equal to your toolbar height.
- Keep content out of the caption area with CSS env vars: `padding-left: env(titlebar-area-x, 0); width: env(titlebar-area-width, 100%); height: env(titlebar-area-height, 32px)`.
- **Electron 43+:** WCO on Linux follows the user's native button layout — on GNOME only a Close button by default; buttons can be left, right or both; RTL flips them. Never hard-code "controls are top-right" — https://github.com/electron/electron/blob/main/docs/breaking-changes.md#behavior-changed-wco-respects-the-native-title-bar-layout-on-linux
```js
const isMac = process.platform === 'darwin'
const win = new BrowserWindow({
  show: false, backgroundColor: nativeTheme.shouldUseDarkColors ? '#1e1e1e' : '#ffffff',
  titleBarStyle: 'hidden',
  ...(isMac ? { trafficLightPosition: { x: 14, y: 14 }, vibrancy: 'sidebar' }
            : { titleBarOverlay: { color: '#00000000', symbolColor: '#888', height: 40 },
                backgroundMaterial: 'mica' }),
  name: 'main', windowStatePersistence: true,   // Electron 44+, experimental
})
win.once('ready-to-show', () => win.show())
```
**Drag regions** — https://www.electronjs.org/docs/latest/tutorial/custom-window-interactions
- Current docs use unprefixed `app-region: drag` / `no-drag` (`-webkit-app-region` still referenced in API docs). Drag areas swallow all pointer events → mark every button/input inside as `no-drag`. Add `user-select: none` to the title bar. Never put a custom context menu on a drag region (Windows shows the system menu there). Debug with env `ELECTRON_DEBUG_DRAGGABLE_REGIONS=1` (unpackaged only, experimental).
- Frameless (`frame:false`) on Wayland gets GTK shadows/resize borders; Electron 43+ frameless windows get rounded corners on Linux too (`roundedCorners`, default `true`).

**Materials** — `vibrancy` (mac): `'sidebar' | 'titlebar' | 'menu' | 'popover' | 'header' | 'sheet' | 'window' | 'hud' | 'under-window' | 'content' | …`, plus `visualEffectState: 'followWindow'` (default; goes inactive when window is). `backgroundMaterial` (Windows 11 22H2+): `'auto' | 'none' | 'mica' | 'acrylic' | 'tabbed'` — Mica for main long-lived windows, Acrylic for transient ones (https://www.electronjs.org/docs/latest/api/browser-window#winsetbackgroundmaterialmaterial-windows). For the material to show, your page background must be transparent where you want it.

**Theme & accent** — `nativeTheme.themeSource = 'system' | 'light' | 'dark'` (drives CSS `prefers-color-scheme` too); read `nativeTheme.shouldUseDarkColors`, `shouldUseHighContrastColors`, listen `nativeTheme.on('updated')` (https://www.electronjs.org/docs/latest/api/native-theme). Accent: `systemPreferences.getAccentColor()` → `"rrggbbaa"` (Win/mac), event `'accent-color-changed'` (Win/Linux); `systemPreferences.getSystemColor('blue')` (mac) (https://www.electronjs.org/docs/latest/api/system-preferences). New window option `accentColor` (Windows) tints the frame; follows OS by default. CSS alternative inside the page: `accent-color: AccentColor` / system colors `Canvas`, `CanvasText`, `Highlight`.

**Menus** — https://www.electronjs.org/docs/latest/api/menu-item
- Build from roles so labels, shortcuts and localization come from the OS: `appMenu`, `fileMenu`, `editMenu`, `viewMenu`, `windowMenu`, `help`, plus `undo redo cut copy paste pasteAndMatchStyle selectAll`, `about hide hideOthers unhide quit services`, `togglefullscreen minimize zoom close front`.
- Accelerators: `'CmdOrCtrl+Shift+Z'`, `'CmdOrCtrl+,'`. On mac the first menu is the app menu (`{ role: 'appMenu' }`) containing About, Settings…, Services, Hide, Quit. On Win/Linux put Settings in File/Edit/Tools menu and use `role: 'quit'` (label "Exit" on Windows ⚠️ label varies by OS).
- If you ship no menu, call `Menu.setApplicationMenu(null)` before `ready` — saves startup work (https://www.electronjs.org/docs/latest/tutorial/performance). On mac keep at least the app menu + an Edit menu built from roles — mac routes ⌘C/⌘V/⌘Q through menu items, so without them those shortcuts can stop working ⚠️ (common Electron pitfall, not stated in docs).
- Context menus: `Menu.buildFromTemplate([...]).popup()` from the main process on the renderer's `context-menu` event (`webContents.on('context-menu', (e, params) => …)` gives `params.isEditable`, `params.selectionText`, `params.misspelledWord`, `params.dictionarySuggestions`) — never an HTML div menu (https://www.electronjs.org/docs/latest/api/web-contents). Pass `menu.popup({ frame: params.frame })` so macOS Writing Tools and other system items work (https://www.electronjs.org/docs/latest/api/menu#menupopupoptions).

**Lifecycle** — https://www.electronjs.org/docs/latest/tutorial/tutorial-first-app
```js
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })
app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow() }) // dock click
```
**No white flash** — `show:false` + `win.once('ready-to-show', () => win.show())`, and *always* set `backgroundColor` to your app's real background (default is `#FFF`) (https://www.electronjs.org/docs/latest/api/browser-window#showing-the-window-gracefully). Pick it from `nativeTheme.shouldUseDarkColors`.

**Dialogs** — use `dialog.showOpenDialog/showSaveDialog/showMessageBox` (native). **Electron 43+:** `defaultPath` now defaults to Downloads and the OS no longer remembers the last folder → store and pass the last-used directory yourself. `showHiddenFiles` removed on Linux (GTK made it a user choice) (breaking-changes 43.0).

**Window state** — **Electron 44+:** `new BrowserWindow({ name: 'main', windowStatePersistence: true | { bounds, displayMode } })`, event `'persisted-state-restored'`, `BaseWindow.clearPersistedState(name)`; *experimental*. Older: `electron-window-state` package or save `getNormalBounds()` + `isMaximized()` yourself, and clamp to `screen.getAllDisplays()` work areas on restore.

**Startup** — profile first; lazy-`require` modules; don't block main process (no sync IPC / sync fs); bundle code; avoid polyfills; `Menu.setApplicationMenu(null)` if no menu (https://www.electronjs.org/docs/latest/tutorial/performance). Use V8 snapshot / code cache only after measuring.

**Accessibility** — Chromium's a11y tree is enabled automatically when a screen reader is detected; `app.setAccessibilitySupportEnabled(true)` forces it (https://www.electronjs.org/docs/latest/tutorial/accessibility). Accessibility = your HTML semantics: real `<button>`, ARIA roles for custom widgets (`role="tree"`, `role="grid"`, `aria-activedescendant`).

**Linux / Wayland** — **Electron 38+** runs as a native Wayland client automatically when `XDG_SESSION_TYPE=wayland`; `ELECTRON_OZONE_PLATFORM_HINT` was removed; force XWayland with `--ozone-platform=x11` in the `.desktop` file (not `app.commandLine.appendSwitch` — too late) (https://www.electronjs.org/docs/latest/api/command-line-switches#--ozone-platformplatform-linux). On Wayland you can't position, move or focus windows (or resize after creation) without user input, and `getPosition()` returns 0,0 → window-state restore can only restore size/maximized there (https://www.electronjs.org/docs/latest/api/browser-window).

**Other 2025–26 changes to know:** mac notifications now use `UNNotification` and require code signing (42); macOS 13+ required (44); `clipboard` removed from renderer — use the W3C Clipboard API (44); Windows ia32 dropped (44).

### B2. Tauri 2 (stable 2.12.x, Oct 2026; 3.0 in alpha)
Sources: releases https://github.com/tauri-apps/tauri/releases · 2.12 notes https://v2.tauri.app/blog/tauri-2.12/ · config schema https://v2.tauri.app/reference/config/ (generated from https://github.com/tauri-apps/tauri/blob/dev/crates/tauri-schema-generator/schemas/config.schema.json) · window guide https://v2.tauri.app/learn/window-customization/
- 2.12 (Sep 2026) dropped Windows 7, MSRV Rust 1.90, added `on_permission_request`. `tauri-v3.0.0-alpha.5` tagged Oct 2026 ⚠️ (no public v3 migration guide found).

**Window config (`tauri.conf.json > app.windows[]` or `WebviewWindowBuilder`)**
- `decorations: false` → fully custom chrome (you draw min/max/close — avoid unless you must). macOS loses native window tiling/move gestures with custom title bars (window guide note).
- macOS: `titleBarStyle: "Visible" | "Transparent" | "Overlay"`, `hiddenTitle: true`, `trafficLightPosition` (needs `Overlay` + `decorations: true`). `Overlay` caveats from schema: title bar height varies per macOS version; you must add your own drag region; you **can't drag the window when it's unfocused** (tauri#4316). `Transparent` = keeps native title bar behaviour, just shows your window background color → safest native-feeling choice.
- `tabbingIdentifier` (mac native window tabs), `acceptFirstMouse` (mac click-through on inactive window), `theme: "Light"|"Dark"` (omit = follow OS), `backgroundColor` (avoid white flash), `visible: false` then `show()` once rendered, `preventOverflow`, `shadow`.
- `windowEffects: { effects: [...], state, radius, color }` — requires `transparent: true`; **Linux unsupported**. Values: mac `sidebar | titlebar | menu | popover | headerView | sheet | windowBackground | hudWindow | underWindowBackground | …` and **`liquidGlassRegular` / `liquidGlassClear` (macOS 26+)** with `interactive` (macOS 27+); Windows 11 `mica | micaDark | micaLight | tabbed | tabbedDark | tabbedLight`; `acrylic`/`blur` (Win10/11, laggy while dragging/resizing per schema).
- `scrollBarStyle: "fluentOverlay"` (Windows, WebView2 ≥125) → Windows 11 thin overlay scrollbars for free. No-op elsewhere.
- `dragDropEnabled` (default true) — Tauri intercepts OS file drops and emits `DragDropEvent` with real paths; set `false` if you need HTML5 drag-and-drop *inside* the page on Windows.
- `zoomHotkeysEnabled` (default off) — leave off for app UI; give real View > Zoom commands if content is zoomable.

**Drag regions** — `data-tauri-drag-region` on the element (only the element itself, not children); `="deep"` makes descendants drag too; `="false"` opts out. Buttons/inputs/links/`[tabindex]`/`role=button|tab|…` are automatically excluded. Double-click on a drag region toggles maximize (mac: on mouseup without movement) — source: https://github.com/tauri-apps/tauri/blob/tauri-v2.12.5/crates/tauri/src/window/scripts/drag.js. ⚠️ It ignores the macOS user setting "Double-click a window's title bar to: Zoom/Minimize/Fill". Needs capability `core:window:allow-start-dragging`. On Windows the guide suggests `[data-tauri-drag-region] { app-region: drag; }` for touch/pen.

**Menus & tray** — https://v2.tauri.app/learn/window-menu/ · https://v2.tauri.app/learn/system-tray/
```js
import { Menu, Submenu, PredefinedMenuItem } from '@tauri-apps/api/menu'
const appMenu = await Submenu.new({ text: 'App', items: [
  await PredefinedMenuItem.new({ item: { About: null } }),
  await PredefinedMenuItem.new({ item: 'Separator' }),
  await PredefinedMenuItem.new({ item: 'Quit' }) ]})
const edit = await Submenu.new({ text: 'Edit', items: await Promise.all(
  ['Undo','Redo','Separator','Cut','Copy','Paste','SelectAll'].map(item => PredefinedMenuItem.new({ item })))})
await (await Menu.new({ items: [appMenu, edit] })).setAsAppMenu()
```
- macOS: every top-level item must be a `Submenu`; top-level items are ignored; the **first submenu becomes the app menu** regardless of its label. Use `PredefinedMenuItem` (Copy/Paste/Undo/…/Quit) so the OS supplies labels and shortcuts. Accelerators: `'CmdOrCtrl+N'`.
- Predefined items also include `Hide`, `HideOthers`, `Services`, `Fullscreen` (mac only), `CloseWindow`, `Minimize` (https://github.com/tauri-apps/tauri/blob/tauri-v2.12.5/packages/api/src/menu/predefinedMenuItem.ts).
- Tray: `TrayIcon.new({ icon, menu, tooltip, showMenuOnLeftClick, iconAsTemplate })` (`menuOnLeftClick` is deprecated). On mac set `iconAsTemplate: true` and ship a monochrome icon so it adapts to light/dark menu bars (https://github.com/tauri-apps/tauri/blob/tauri-v2.12.5/packages/api/src/tray.ts).
- Window state: official plugin `tauri-plugin-window-state` (`cargo tauri add window-state`) saves/restores size, position, maximized — https://v2.tauri.app/plugin/window-state/.
- Native dialogs: `@tauri-apps/plugin-dialog` (`open`, `save`, `ask`, `confirm`, `message`) — https://v2.tauri.app/plugin/dialog/.

**Webview differences = your real cross-platform risk** — https://v2.tauri.app/reference/webview-versions/
| | macOS | Windows | Linux |
|---|---|---|---|
| Engine | WKWebView (system WebKit = the user's Safari version; only updated with OS/Safari updates) | WebView2 (evergreen Chromium/Edge, auto-updates; preinstalled on Win 11) | WebKitGTK (`webkit2gtk-4.1`), version = whatever the distro ships; current upstream 2.54 (Sep 2026, Skia compositor) https://webkitgtk.org/ |
| Test with | Safari of the oldest macOS you support | Edge | GNOME Web (Epiphany) |

Feature floor checks (caniuse, https://caniuse.com — Safari version that first fully supports it):
- `backdrop-filter` unprefixed: Safari **18.0** (before: `-webkit-backdrop-filter`) → always write both.
- `user-select: none`: Safari *still* needs `-webkit-user-select: none` (caniuse user-select-none) → always write both or chrome text stays selectable on mac.
- Same-document View Transitions: Safari 18.0; cross-document: 18.2. `:has()`: 15.4. CSS nesting (full): 17.2. Container queries: 16.0. `overscroll-behavior`: 16.0.
- `scrollbar-color`/`scrollbar-width`: Safari **26.2** only; `::-webkit-scrollbar` styling doesn't work in WKWebView per caniuse note → on mac leave native overlay scrollbars alone.
- Anchor positioning: full only in Safari 27 (partial 26.0). WebGPU: Safari 26 partial. Chrome-only: CSS `if()`, many `@container style()` queries → feature-detect with `@supports` or don't use.
- `-webkit-font-smoothing` works only on macOS; Linux text rendering follows fontconfig (hinting/subpixel from the user's settings) → expect different glyph widths; never size UI to exact text widths. WebKitGTK 2.52 changed text blending to linear color space "like other browsers".
- Linux WebKitGTK GPU issues (blank/white windows on some NVIDIA/Wayland setups): common workaround env `WEBKIT_DISABLE_DMABUF_RENDERER=1` ⚠️ (community workaround, not an official doc).

### B3. Flutter desktop (stable 3.47.x, Oct 2026)
Sources: releases https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json · source tag https://github.com/flutter/flutter/tree/3.47.9 · package versions from https://pub.dev/api/packages/<name> (2026-11-02)
Flutter draws every pixel itself (Skia/Impeller). Out of the box you get **Material on every OS** = the #1 "not native" tell. Budget for platform adaptation.
- **Menu bar:** `PlatformMenuBar(menus: [PlatformMenu(label:'App', menus:[PlatformProvidedMenuItem(type: PlatformProvidedMenuItemType.about), …, PlatformProvidedMenuItem(type: …quit)]), …], child: …)`. **Native only on macOS**; on Windows/Linux it does nothing unless a plugin sets `WidgetsBinding.platformMenuDelegate` → use Material `MenuBar` + `MenuItemButton(shortcut: …)` / `MenuAnchor` in-window there (https://github.com/flutter/flutter/blob/3.47.9/packages/flutter/lib/src/widgets/platform_menu_bar.dart). Provided mac items: about, quit, servicesSubmenu, hide, hideOtherApplications, showAllApplications, toggleFullScreen, minimizeWindow, zoomWindow, arrangeWindowsInFront.
- **Shortcuts:** `Shortcuts` → `Intent` → `Actions` (https://docs.flutter.dev/ui/interactivity/actions-and-shortcuts). No `CmdOrCtrl`: branch yourself — `SingleActivator(LogicalKeyboardKey.keyS, meta: isMac, control: !isMac)`; use `PlatformMenuItem.shortcut` so mac menus display the shortcut. Wrap regions in `FocusTraversalGroup` (+ `OrderedTraversalPolicy`) so Tab order is logical; `FocusableActionDetector` for custom controls (focus + hover + shortcuts in one).
- **Pointer:** since **Flutter 3.41** Material buttons use `WidgetStateMouseCursor.adaptiveClickable` = hand on web, **arrow (`basic`) on desktop**, documented as reflecting native conventions (https://github.com/flutter/flutter/blob/3.47.9/packages/flutter/lib/src/widgets/widget_state.dart). Don't override it back to `SystemMouseCursors.click`; use `MouseRegion(cursor: SystemMouseCursors.click)` only for links. Hover states are mandatory on desktop.
- **Density:** `VisualDensity.adaptivePlatformDensity` → `compact` on macOS/Windows/Linux (https://github.com/flutter/flutter/blob/3.47.9/packages/flutter/lib/src/material/theme_data.dart). Don't ship 48px mobile touch targets on desktop.
- **Scrollbars:** `ScrollBehavior` auto-adds `Scrollbar` on desktop (https://docs.flutter.dev/release/breaking-changes/default-desktop-scrollbars); disable bouncing/stretch overscroll (`ClampingScrollPhysics`) on Windows/Linux; mac users expect elastic scroll.
- **Text:** desktop text-selection toolbars exist (`desktop_text_selection.dart`); make sure context menus on text are the desktop variant (`contextMenuBuilder`), and right-click works everywhere.
- **Native-look packages** (latest on pub.dev): `macos_ui` 2.2.2 (Oct 2025 — check it covers macOS 26 look before relying on it); `fluent_ui` 4.17.0 (Oct 2026, active); `yaru` 11.0.0 (Ubuntu/Canonical, Oct 2026); `libadwaita` 2.0.2 / `adwaita` 1.1.0 (**last published 2023 → stale**, likely behind libadwaita 1.6+ ⚠️). Pick one per platform via `defaultTargetPlatform`, or use a neutral custom design that honours each platform's conventions (menus, dialogs order, shortcuts).
- **Window chrome/state:** `window_manager` 0.6.0 (Nov 2026: `setTitleBarStyle(TitleBarStyle.hidden)`, min size, position, `waitUntilReadyToShow`) + `macos_window_utils` 1.9.1 (NSWindow: full-size content view, toolbar style, materials); `system_theme` 3.3.0 for accent color; `tray_manager` 0.8.2; `super_drag_and_drop` 0.9.1 for native DnD; `file_selector` 1.1.0 (official) for native file dialogs. Persist window bounds yourself (no built-in).
- **Multi-window:** official API (`RegularWindowController`, `_window.dart`) is **still experimental/internal in 3.47** — main channel + feature flag only, "Do not use… in production" (https://github.com/flutter/flutter/issues/30701). Use `desktop_multi_window` 0.3.1 if you must (separate engines).
- **Accessibility:** desktop embedders bridge semantics to UIA (Windows `accessibility_bridge_windows`), NSAccessibility (mac) and ATK (Linux `fl_accessible_node`) (https://github.com/flutter/flutter/tree/3.47.9/engine/src/flutter/shell/platform). Test with Narrator/NVDA, VoiceOver, Orca (https://docs.flutter.dev/ui/accessibility/assistive-technologies). Wrap custom widgets in `Semantics(label:, button: true, …)`.
- Linux embedder is GTK3-based (`gtk+-3.0` in engine `shell/platform/linux/config/BUILD.gn`) → no libadwaita styling for free; `file_selector` uses GTK/portal dialogs.

### B4. Qt 6 (6.12 LTS, released 2026-09-30)
Sources: https://doc.qt.io/qt-6/whatsnew612.html · styles https://doc.qt.io/qt-6/qtquickcontrols-styles.html · https://download.qt.io/official_releases/qt/
- **Qt Widgets** = most native-feeling cross-platform toolkit: real platform styles (`macos`, `windows11` default on Win 11 since 6.7 with dark mode (https://doc.qt.io/qt-6/whatsnew67.html), `fusion` on Linux unless Plasma/GTK platform theme supplies Breeze). Native menu bar on mac (`QMenuBar` becomes global automatically), native file/color/font dialogs, `QDialogButtonBox` auto-orders buttons per platform, `QKeySequence::StandardKey` gives per-OS shortcuts (Quit, Preferences, Redo, FullScreen…) — **always use StandardKey instead of literal strings**. Menu roles: `QAction::PreferencesRole`, `AboutRole`, `QuitRole` move items into the mac app menu; default `TextHeuristicRole` guesses from the label text (e.g. an action named "Settings…" may jump to the app menu) — set roles explicitly (https://doc.qt.io/qt-6/qaction.html#MenuRole-enum). 6.12: macOS unified title+toolbar now uses effect views; `QDialogButtonBox::standardButtonText()/standardButtonShortcut()`.
- **Qt Quick Controls**: default style per OS — macOS → **macOS** style (mac-only), Windows → **Windows** style (Windows-only), Linux → **Fusion**; **FluentWinUI3** (6.8+, Win 11 look, runs on all platforms; better contrast-theme support in 6.10). **6.12 adds `import QtQuick.Controls.Native`** = picks the platform's best style at compile time. Material/Universal/Imagine/Basic are *not* native — don't ship Material on desktop. 6.12: `MenuItem` shows the shortcut from its `Action`.
- KDE apps: Kirigami + `org.kde.desktop` style (Breeze) on Plasma; Qt Quick Dialogs `FileDialog` for files (KDE HIG).
- Theme: `QStyleHints::colorScheme()` + `setColorScheme()` override (6.8+); `QAccessibilityHints::motionPreference` for reduced motion (6.12); `QStyleHints::toolTipWakeUpDelay` (6.12).
- Accessibility: UIA/NSAccessibility/AT-SPI bridges built in; 6.11 added AT-SPI Collection, Switch role; 6.12 expanded/expandable notifications (whatsnew611/612).
- New in Labs: **StyleKit** (6.11+) — one QML style for both Widgets and Quick; useful for a branded design system, but it's your look, not the platform's.
- Watch: Qt Quick custom styles easily drift from native (focus rings, hover, density); Wayland: prefers server-side decorations (6.11).

### B5. Compose Multiplatform desktop (1.12.2 stable Oct 2026; 1.13 beta)
Sources: https://github.com/JetBrains/compose-multiplatform/blob/master/CHANGELOG.md · https://kotlinlang.org/docs/multiplatform/compose-desktop-top-level-windows-management.html ⚠️ (URL not re-fetched)
- Skia-rendered Material on JVM/AWT → same "Material everywhere" risk as Flutter. Native bits: `Window(onCloseRequest, state = rememberWindowState(...))`, `MenuBar { Menu("File") { Item("Open…", shortcut = KeyShortcut(Key.O, meta = isMac, ctrl = !isMac)) } }` (native on mac via AWT ⚠️), `Tray(icon, menu = { Item(…) })`, `Notification`, `FileDialog` via AWT/`java.awt.FileDialog` (native) — avoid Swing `JFileChooser`.
- 1.12: new experimental **`WindowState` API**; `LocalAwtWindow.current`; `isSystemInDarkTheme()` now updates live on Windows/macOS (polls once a second) (CHANGELOG). Persist `WindowState` (position, size, placement) yourself.
- **JetBrains Jewel** (`org.jetbrains.jewel:jewel-int-ui-standalone`, latest 0.41.0-262.11879.100 on Maven Central, Oct 2026; source now in `intellij-community/platform/jewel`) = IntelliJ "Int UI" components for standalone Compose desktop apps + `jewel-decorated-window` (custom title bar; needs JetBrains Runtime) (https://github.com/JetBrains/intellij-community/tree/master/platform/jewel). Looks like a JetBrains IDE — great for dev tools, not "native" for consumer apps.

### B6. Avalonia / .NET MAUI / Uno
- **Avalonia 12** (12.0 Apr 2026, now 12.1.4): own renderer (Skia), Fluent theme by default ⚠️ → consistent but not native; 12.0 added **themeable client-side window decorations**, `NativeDock.Menu` (mac dock menu), and an **AT-SPI2 Linux accessibility backend** ("first .NET UI framework" to ship one) (https://avaloniaui.net/blog/avalonia-12). Use `NativeMenu` for the mac global menu ⚠️, and platform-specific button order yourself. Best .NET choice for Linux.
- **.NET MAUI 10** (10.0.120; 11 in RC): Windows = WinUI 3 (native Fluent), **macOS = Mac Catalyst** (iPad-style app on mac — menus, window behaviour and controls feel iPadOS-ish); **no Linux** in supported platforms (https://learn.microsoft.com/en-us/dotnet/maui/supported-platforms). Fine for Windows-first apps; weak as a mac or Linux desktop story.
- **Uno Platform 6.6**: WinUI/XAML API everywhere; renders with Skia on mac/Linux (or native WinUI on Windows) ⚠️ → Fluent look on every OS. Good if you already have WinUI code; adapt mac menus/shortcuts manually.

### B7. React Native for Windows / macOS
- **RNW 0.85** (Oct 2026): **New Architecture (Fabric) only**, Windows App SDK 1.8, .NET 10, VS 2026; adds `Modal` `hideTitleBar`/`hideBorder`, `outline` styles (https://github.com/microsoft/react-native-windows/releases/tag/react-native-windows_v0.85.0). Renders real platform controls (Fluent-ish) — closest to native among JS options on Windows.
- **react-native-macos 0.83** (Sep 2026): AppKit views (https://github.com/microsoft/react-native-macos/releases). Two separate forks → mac and Windows apps are effectively separate codebases for anything beyond basic views; menus, keyboard handling (`keyDownEvents`/`onKeyDown` ⚠️), window management need native modules. No Linux.

### B8. Wails (v3.0.0 stable 2026-10-26, v3.1.0 2026-11-01; v2.17 maintained)
Sources: https://github.com/wailsapp/wails/releases/tag/v3.0.0 · https://github.com/wailsapp/wails/blob/v3.1.0/docs/mpress/content/features/windows/frameless.md
- Go backend + **system webview** (same WKWebView / WebView2 / WebKitGTK caveats as Tauri — reuse B2's feature-floor table). v3 (Go 1.26+): multiple windows, services, typed events, generated TS bindings; **system tray** (light/dark + mac template icons, window attached to tray), app/context/tray menus (context menus from HTML via WML attributes), native message/file dialogs, frameless windows with native corners/shadows, translucency incl. **native Liquid Glass on macOS 26**.
- Drag regions: CSS custom property `--wails-draggable: drag | no-drag` (not `app-region`). mac transparent webview needs `Mac.Backdrop: application.MacBackdropTransparent` + build tag `private_mac_apis`.
- Watch: same webview inconsistency as Tauri; smaller ecosystem; v3 is brand new — pin versions.

## Part C — "Web app in a window" smells and fixes
Applies to Electron, Tauri, Wails (and partly Flutter/Compose). Base reset first, then the list.
```css
html, body { height: 100%; overflow: hidden; overscroll-behavior: none; }      /* no whole-window bounce */
body { -webkit-user-select: none; user-select: none; cursor: default;           /* chrome isn't text */
       font: 13px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI Variable Text", "Segoe UI", system-ui, sans-serif;
       color-scheme: light dark; background: Canvas; color: CanvasText;
       -webkit-tap-highlight-color: transparent; }
input, textarea, [contenteditable], .selectable, .content { -webkit-user-select: text; user-select: text; cursor: auto; }
.scroll { overflow: auto; overscroll-behavior: contain; }                        /* inner panes scroll */
:focus { outline: none } :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
img, svg { -webkit-user-drag: none; }                                             /* ⚠️ WebKit/Blink only */
```
| Smell | Fix | Source |
|---|---|---|
| Labels, buttons, toolbars are text-selectable; ⌘A selects the whole UI | `user-select: none` on chrome **plus `-webkit-user-select`** (Safari/WKWebView still needs the prefix); re-enable on content and inputs; make ⌘A/Ctrl+A act on the focused list/editor | https://caniuse.com/user-select-none |
| Browser context menu (Back, Reload, Inspect) | Electron: handle `webContents.on('context-menu')` and `Menu.popup()`; Tauri/Wails: native `Menu` popup; never show "Inspect" in production; keep the text-field menu (Cut/Copy/Paste/Spelling) | https://www.electronjs.org/docs/latest/api/web-contents |
| Whole window rubber-bands / overscroll glow; pinch-zoom scales the UI | `overscroll-behavior: none` on root, scroll only inner panes (mac inner lists may stay elastic — that's native; Electron `scrollBounce` mac option); Electron keeps visual (pinch) zoom off by default — don't re-enable; Tauri `zoomHotkeysEnabled: false` | https://www.electronjs.org/docs/latest/api/structures/web-preferences · Tauri config schema |
| White flash on launch / new window | Hidden window until first paint (`show:false` + `ready-to-show`; Tauri `visible:false` then `show()`), `backgroundColor` = real theme bg, inline critical CSS, no splash for <1s loads | https://www.electronjs.org/docs/latest/api/browser-window#showing-the-window-gracefully |
| Spinners/skeletons for **local** data | Local data must appear instantly: load from disk/SQLite synchronously-fast via IPC, render last state from cache, show progress only for >~1s work; "best content-loading experience finishes before people become aware of it" | https://developer.apple.com/design/human-interface-guidelines/loading |
| Blue underlined links for in-app navigation; URL routes, "pages", browser-style back stack | Use sidebars, tabs, split views, toolbar buttons; links only for real URLs (open in default browser via `shell.openExternal` / opener plugin). KDE: "Don't use links for internal navigation within your app" | https://develop.kde.org/hig/getting_input/ |
| No keyboard shortcuts / no menu | Real menu with standard roles + per-OS shortcut table (A2); every toolbar action has a menu item + shortcut; tooltips show the shortcut | A1/A2 sources |
| Window opens at default size/center every time | Persist bounds + maximized/fullscreen per window; clamp to visible displays on restore (Electron 44 `windowStatePersistence`, Tauri `window-state` plugin) | B1/B2 |
| Can't drop files on the window / can't drag out | Handle OS file drops (Tauri `DragDropEvent`, Electron `drop` event + `webUtils.getPathForFile(file)` in preload, https://www.electronjs.org/docs/latest/api/web-utils), visible drop target, support drag-out | B1/B2 |
| No focus styles, or `outline:none` everywhere | `:focus-visible` ring in accent color; logical Tab order; arrow keys inside lists/grids/toolbars (roving tabindex) | WAI-ARIA APG https://www.w3.org/WAI/ARIA/apg/ |
| `cursor: pointer` on every button/card | Arrow on buttons, tabs, list rows; pointing hand only on real hyperlinks (Apple, Microsoft, KDE all say so; Flutter 3.41+ switched desktop buttons to arrow). The web convention of pointer-on-buttons is a web-only debate — desktop guidelines are unanimous | A4 sources |
| Thick grey always-on scrollbars (Windows-98 look on mac), or custom thin bars that ignore OS settings | Don't style scrollbars on mac (overlay); on Windows WebView2 use Tauri `scrollBarStyle: "fluentOverlay"` or `scrollbar-width: thin; scrollbar-color: …` (Chromium 121+, Safari 26.2+); respect "always show scrollbars" settings by not hiding them | caniuse css-scrollbar; Tauri schema |
| Tooltips via `title` attribute (slow, unstyled, not keyboard-accessible) | Native-feeling tooltip component: ~500ms delay ⚠️, appears on keyboard focus too, includes shortcut, header-cased on GNOME; or native tooltips where the framework offers them | https://learn.microsoft.com/en-us/windows/apps/design/controls/tooltips |
| Hard-coded Inter/Roboto 16px web type scale | System font stack + platform base size (13pt mac, 14px Win, 11pt GNOME, 10pt KDE); relative units so OS text scaling works | A4 |
| Ignores dark mode / accent / reduced motion / high contrast | `color-scheme: light dark` + `prefers-color-scheme`; accent from native API into `--accent`; `prefers-reduced-motion`, `prefers-contrast`, `forced-colors: active` (Windows contrast themes); Electron `nativeTheme.on('updated')` | https://www.electronjs.org/docs/latest/api/native-theme |
| Web-style modals for everything (centered card + dim overlay) | Native message boxes for confirmations (`dialog.showMessageBox`, Tauri `ask/confirm`), mac sheets for document-scoped dialogs, platform button order (A3); prefer undo toasts over confirms | A3 |
| Custom title bar that breaks OS behaviour | Keep native caption buttons/traffic lights (WCO/`titleBarStyle`), leave drag space, honour double-click and right-click system menu, respect GNOME button-layout | A1, B1 |
| Single window can't be re-opened on mac after closing; or app quits on mac when window closes | `activate` handler re-creates window; don't quit on `window-all-closed` on mac | B1 |
| Electron default menu shipped (View › Toggle Developer Tools, Reload) | Build your own menu from roles; remove reload/devtools in production | https://www.electronjs.org/docs/latest/api/menu |
| Notifications/badges via web APIs only | Use native notifications (signed app on mac), dock/taskbar badge (`app.setBadgeCount` mac/Linux, `win.setOverlayIcon` Windows), taskbar/dock progress (`win.setProgressBar`) | https://www.electronjs.org/docs/latest/api/browser-window |

## Unverified / open questions
- ⚠️ Ubuntu's default GNOME `button-layout` (believed to add minimize/maximize); KDE's default title-bar double-click action (believed Maximize).
- ⚠️ mac full screen via Fn/Globe-F (in addition to ⌃⌘F); "View › Show Sidebar ⌃⌘S" is common practice, not in the HIG table; mac Rename = Return is Finder behaviour, not a general rule.
- ⚠️ GNOME HIG's keyboard reference has no Fullscreen row; F11 is common GTK practice; Qt's GNOME table says Ctrl+F11.
- ⚠️ "Reveal in folder" labels per OS (Show in File Explorer / Show in Files / Open Containing Folder) are common practice, not from official guidelines. Tauri `revealItemInDir` exists in `@tauri-apps/plugin-opener` (source checked), label is yours.
- ⚠️ Electron on mac without an Edit menu: ⌘C/⌘V may stop working in text fields (well-known pitfall, not in current docs).
- ⚠️ Electron `role: 'quit'` default label on Windows ("Exit" vs "Quit") — not checked in source; set `label` explicitly per OS.
- ⚠️ Electron `showMessageBox` button order: docs don't say it reorders by platform; assume array order.
- ⚠️ Chromium on Windows resolving `system-ui` to "Segoe UI" (not "Segoe UI Variable"); exact CSS family names for Segoe UI Variable optical-size families.
- ⚠️ Windows focus visual details (two-tone ring, keyboard-only) and Windows drag modifiers (Ctrl copy / Shift move / Alt link) — from memory, Microsoft pages not fetched.
- ⚠️ GNOME accent via portal key `org.freedesktop.appearance accent-color`; GNOME Background portal as tray alternative.
- ⚠️ Windows toast notifications from unpackaged Electron apps needing `app.setAppUserModelId()`.
- ⚠️ KDE: Plasma default single- vs double-click; KAcceleratorManager auto-assigning mnemonics.
- ⚠️ Tauri drag-region double-click ignores the macOS "double-click title bar" user setting (inferred from `drag.js`, not documented); Tauri 3.0 alpha scope unknown.
- ⚠️ `WEBKIT_DISABLE_DMABUF_RENDERER=1` for blank WebKitGTK windows — community workaround. Tauri's own webview-versions table is stale (latest distro row: WebKitGTK 2.36); upstream is 2.54 (Sep 2026). Whether Ubuntu/Debian LTS ship new WebKitGTK majors as security updates — not checked.
- ⚠️ Flutter `libadwaita`/`adwaita` packages: last published 2023 — check for forks before using. `macos_ui` 2.2.2 (Oct 2025) coverage of macOS 26 design not checked.
- ⚠️ Compose `MenuBar` being a native global menu on mac; Compose docs URL not re-fetched. Avalonia default theme (Fluent) and `NativeMenu` API; Uno rendering backends per OS; RN-macOS keyboard event props.
- ⚠️ Tooltip delay (~500 ms) is a typical value; each OS differs (Qt 6.12 exposes `QStyleHints::toolTipWakeUpDelay`).
- ⚠️ `-webkit-user-drag: none` support across WebView2/WKWebView/WebKitGTK.
- Open question: Electron `windowStatePersistence` is experimental (44+) — behaviour on Wayland (no positions) and multi-monitor clamping not tested.
- Open question: Liquid Glass (macOS 26) — Tauri (`liquidGlassRegular/Clear`) and Wails v3 expose it; Electron's `vibrancy` list has no Liquid Glass value in 45 docs. Whether to adopt it in cross-platform apps is a design call (see macOS reference file).
