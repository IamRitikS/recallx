# RecallX — Codebase Documentation

## What It Is
A **pure HTML/CSS/JavaScript** science study web app. No framework, no build tool, no package manager, no dependencies. Designed to be mobile-responsive and runs directly in a browser (just open `index.html`).

---

## File Tree
```
RecallX/
├── index.html              ← Root landing page (subject selector)
├── README.md               ← Empty (just "# recallx")
├── CODEBASE_NOTES.md       ← This file
├── physics/
│   └── index.html          ← Physics page ("Coming Soon…")
├── biology/
│   └── index.html          ← Biology page ("Coming Soon…")
└── chemistry/
    ├── index.html          ← Chemistry topic menu
    └── periodic.html       ← Periodic Table Trainer (currently empty/blank)
```

---

## Page-by-Page Breakdown

### `index.html` — Home / Subject Selector
- Centered full-viewport layout, `#fafafa` background
- Shows three subject buttons: **Physics**, **Chemistry**, **Biology**
- Each `.subject` div calls `goTo(page)` → `window.location.href`
- Color: light blue (`#e3f2fd` active: `#bbdefb`)
- Responsive breakpoint at `min-width: 600px`

### `chemistry/index.html` — Chemistry Topic Menu
- Lists available chemistry tools via `.item` divs
- Currently has **one item**: `Periodic Table Trainer` → links to `./periodic.html`
- Color: light green (`#e6f4ea` active: `#c8e6c9`)
- Has a **Back** button → `../index.html`
- Same `goTo()` navigation pattern as root

### `chemistry/periodic.html` — Periodic Table Trainer
- **Currently completely empty** — the main feature to build next

### `physics/index.html` and `biology/index.html`
- Identical structure — both show `<h1>` + `<p>Coming Soon...</p>` + Back button
- **Known bug:** `physics/index.html` has `<title>Biology</title>` instead of `Physics`
- Neither has any content or sub-tools yet

---

## Architecture Patterns

| Pattern | Detail |
|---|---|
| **Navigation** | `window.location.href` via `goTo(page)` helper, inline `onclick` attributes |
| **Styling** | Inline `<style>` block per file — no shared CSS file |
| **Responsiveness** | `<meta viewport>` + `@media (min-width: 600px)` breakpoint in every file |
| **State / Data** | None — completely stateless, no JS storage or backend |
| **Back navigation** | Every sub-page has a `<button>` linking back to `../index.html` |

---

## Current State of Features

| Feature | Status |
|---|---|
| Subject home screen | ✅ Done |
| Chemistry topic menu | ✅ Done |
| Periodic Table Trainer | ⬜ Empty file — **to be built** |
| Physics content | ⬜ Coming Soon placeholder |
| Biology content | ⬜ Coming Soon placeholder |

---

## Key Observations / Known Issues
- No shared stylesheet — each page duplicates the same `body`, `button`, and media query CSS
- `periodic.html` is the **next active development target**
- No server needed — the whole project works opened directly from the filesystem
