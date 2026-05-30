```
██╗   ██╗ █████╗ ██████╗  ██████╗
╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝
 ╚████╔╝ ███████║██████╔╝██║
  ╚██╔╝  ██╔══██║██╔══██╗██║
   ██║   ██║  ██║██║  ██║╚██████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝

Yet Another Runeword Calculator
```

[![Live](https://img.shields.io/badge/▶%20Play%20online-GitHub%20Pages-c8922a?style=flat-square)](https://MiGaNuTs.github.io/YARC)
[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey?style=flat-square)](LICENSE)

A runeword calculator for **Diablo II: Resurrected** — up to date with patch 3.2 / Reign of the Warlock.

Select the runes you own, filter by item type, sockets and game version,
and instantly see which runewords you can craft.

No install. No account. No ads. One HTML file.

---

## Authors

- **[MiGaNuTs]**
- **Claude** (Anthropic) — co-author and pair-programmer

---

## Features

- All 99 runewords including RoTW Season 13 additions
- Filter by runes owned, item type, sockets, version, ladder/non-ladder
- Craftable runewords highlighted at the top
- Per-rune effects by item type
- Fully offline — database embedded directly in the HTML
- Forkable — wrong data? Fix the SQL and run the build script

---

## Try it

Just open `yarc_standalone.html` in any browser. No server needed.

Or use the [live version on GitHub Pages](https://MiGaNuTs.github.io/YARC).

---

## Repository structure

```
YARC/
├── yarc_seed.sql         ← Source of truth — all game data
├── yarc.html             ← HTML template (no database)
├── build.py              ← Build script
├── yarc.db               ← Compiled database (generated)
├── html/
│   └── index.html        ← Final output, DB embedded (generated)
└── README.md
```

---

## Building

Requirements: **Python 3** — no external dependencies.

```bash
python build.py
```

This will:
1. Compile `yarc_seed.sql` → `yarc.db`
2. Encode the database as base64
3. Inject it into `yarc.html` → `yarc_standalone.html`

---

## Editing the data

All game data lives in `yarc_seed.sql`.

To fix an effect, rename a runeword, or add a missing one:

1. Edit `yarc_seed.sql` directly
2. Run `python build.py`
3. Open `yarc_standalone.html` to check your changes

The SQL is structured around these tables:

| Table | Contents |
|---|---|
| `runes` | The 33 runes (El → Zod) |
| `rune_effects` | Per-rune effects by item type |
| `item_types` | Weapon, armor, shield types |
| `runewords` | All runewords with patch and ladder info |
| `runeword_item_types` | Which item types each runeword accepts |
| `runeword_effects` | Runeword-specific bonus effects |
| `translations` | Reserved for future i18n support |

---

## Editing the interface

The UI template is `yarc.html` — plain HTML, CSS and JavaScript.
No build tools, no framework to install. Edit and run `build.py` to produce the standalone file.

The only external dependencies (loaded from CDN) are:
- [sql.js](https://github.com/sql-js/sql.js) — SQLite compiled to WebAssembly
- [Alpine.js](https://alpinejs.dev) — lightweight reactivity

---

## Contributing

Found a wrong effect? A missing runeword? A season flag that's off?

- Open an issue with the correct value and a source (diablo2.io, maxroll.gg, patch notes...)
- Or submit a pull request directly against `yarc_seed.sql`

> ⚠️ **Known limitations**
> Some runeword effects are not yet fully corrected — particularly
> per-level scaling effects and RoTW additions. Contributions welcome.

---

## Data sources

Game data sourced from [blizzhackers/d2data](https://github.com/blizzhackers/d2data)
and cross-referenced with [diablo2.io](https://diablo2.io) and [d2runewizard.com](https://d2runewizard.com).

*Diablo II is a trademark of Blizzard Entertainment.
This project is not affiliated with or endorsed by Blizzard Entertainment.*

---

## License

Code and structure © [MiGaNuTs] & Claude (Anthropic) —
licensed under [CC BY-NC 4.0](LICENSE).

You are free to use, share and adapt this project for **non-commercial purposes**,
as long as you give appropriate credit and indicate if changes were made.
