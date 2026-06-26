# Wiring the `today` board to a Google Sheet

The [`today.html`](./today.html) board reads from a hard-coded `TODAY` object by default. To update it from a phone each morning instead of editing code, point it at a published Google Sheet. No API key, no backend — it fetches the sheet as CSV client-side, and falls back to the built-in board if the sheet is unreachable.

## 1. Build the sheet

One row per flavor. Header row (exact names, lowercase):

| group | name | glyph | price | count | total |
|---|---|---|---|---|---|
| all-star | vanilla | vanilla | $4.00 | 6 | 6 |
| all-star | chocolate | chocolate | $4.00 | 4 | 6 |
| all-star | milk tea | milktea | $4.50 | 3 | 6 |
| all-star | pour over | pour | $4.50 | 5 | 6 |
| rotating | earl grey | earlgrey | $4.50 | 5 | 8 |
| rotating | thai tea | thaitea | $5.00 | 0 | 8 |
| meta | date | | Thu 26 Jun | | |
| meta | updated | | 8:30 | | |

- **group**: `all-star`, `rotating`, or `meta`.
- **glyph**: one of `vanilla chocolate milktea pour earlgrey thaitea matcha eggnog mochi` (matches the recipe-site illustrations). Unknown glyph → falls back to the vanilla shape.
- **count / total**: dots remaining vs. dots total. `count = 0` renders the pink **SOLD OUT** strike.
- **meta rows**: optional. `name=date` sets the header date; `name=updated` sets the timestamp. Put the value in the **price** column.

## 2. Publish it as CSV

In the sheet: **File → Share → Publish to web → (pick the sheet tab) → Comma-separated values (.csv) → Publish.** Copy the URL it gives you. It looks like:

```
https://docs.google.com/spreadsheets/d/e/XXXXXXXX/pub?gid=0&single=true&output=csv
```

> Publishing exposes that one tab read-only to anyone with the link (fine — it's just today's flavors). It is *not* your whole Google account or other sheets.

## 3. Paste the URL into the page

In `today.html`, set:

```js
const SHEET_CSV_URL = "https://docs.google.com/.../pub?...output=csv";
```

That's it. Each morning: edit the sheet on your phone, and the board (and the in-store screen, if you display it) updates on next load. Knock `count` down as flavors sell; set it to `0` for sold out.

## Notes

- **Caching:** Google's published CSV can lag a few minutes behind edits. The page fetches with `cache:"no-store"`, but the CDN may still serve a slightly stale copy. For instant sold-out updates in-store, edit the static object or hard-refresh.
- **Offline / failure:** if the fetch fails (no URL, no network, bad sheet), the board silently shows the built-in `TODAY` data. It never breaks.
- **Auto-refresh (optional):** to make an always-on in-store screen poll, add `setInterval(()=>location.reload(), 120000)` — reloads every 2 min.
