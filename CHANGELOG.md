# Changelog — The Recursive Astrology

## July 7, 2026 — The Great Port: tarot's viewers, homepage, and header, adapted for astrology

Ported the whole "family pattern" from `recursive-tarot` (the flagship sibling site) into
this repo, per the builder's repeated directive: copy tarot's working files and adapt
paths/branding/content, don't rebuild in parallel. Full file-by-file record in
`docs/PORT-NOTES.md`.

- **Collection layer**: new `scripts/build_collection.py` scans `grammars/*/grammar.json`
  and writes `grammars/_collection.json` in the same schema `tarot/_collection.json`
  uses — the index every ported viewer reads to discover the whole library. Glob-driven
  (no hardcoded slug list), so it survived two new grammars landing mid-port without
  going stale. Curates 4 branches (primary sources / synthesis / castings / readings) and
  years only where a grammar has a genuine historical anchor (Ptolemy, Alan Leo, Proctor,
  the Vedic/Mesopotamian/Renaissance additions) — everything else is honestly undated
  rather than assigned a fabricated date.
- **Five viewers ported** into `viewers/`: `cards.html`, `explorer.html`, `tree-viewer.html`
  (near-verbatim — already generic, `grammar_type`-driven, not tarot-hardcoded),
  `lenses.html` (real logic rewrite: matches entities across grammars by normalized
  NAME — "Saturn" is "Saturn" in every voice library — instead of tarot's stamped
  `trump_key`, since deck names don't apply here), and `timeline.html` (data source
  rewritten to read the collection directly and the descent-rail genealogy feature
  removed — astro's grammars don't derive from one another the way tarot's decks do).
  Supporting files copied too: `dimension-engine.js`, `grammar-loader.js`,
  `deck-picker.js`, `eco-links.js`, `icons.js`, `view-switcher.js`.
- **Homepage rebuilt** (`index.html`): the old single-grammar `?grammar=` dialog viewer
  is gone, replaced by tarot's gallery-of-real-links pattern — every grammar and every
  view links to its own page, never a popup. Astro's own hero copy (from
  `recursive-eco.json`) is kept verbatim; added a Courses section (History of Astrology,
  The Right Size, Three Doors) and an honesty-checked "How to hold a chart" section
  (looser than tarot's dated arc, since astrology's history doesn't have as clean a
  single turning point as tarot's 1781 occult reframing).
- **Header rebuilt** (`site-header.js`): Home / Views (Cards, Explorer, Lenses, Tree,
  Timeline, Genealogy, Chart Wheel, Chart Viewer, All grammars) / Courses / Grammars /
  GitHub. The Grammars menu is **not hardcoded** — it fetches
  `grammars/_collection.json` live, so it can't go stale as grammars are added. Verified
  with Playwright that the dropdown hover/gap-fix (commit 84934e6's pattern) survives
  the cursor actually crossing the gap toward a menu item, not just a hover snapshot.
- **Blue theme**: `theme.css`'s accent tokens (`--gold`/`--accent`/`--grammar-accent`/
  `--tree-accent`) retoned from tarot's gold (`#9a7322`) to a sky/indigo blue
  (`#2f5d8a`, darker `#1f4468` for hovers). Every purple accent swept out of the ported
  files EXCEPT the recursive.eco wayfinding links/buttons and the shared assistant star
  — purple stays eco-redirect-only. `genealogy.html` and `wheel.html` needed no direct
  color fixes (already 100% theme.css-token-driven); `viewer/astrology-viewer.html`'s own
  local token layer was retoned in both its light and dark-mode blocks, leaving the
  Human Design bodygraph sub-view's colors untouched (already marked out-of-scope by its
  own header comment).
- Old astro `lenses.html` (the 4-tab lens page) renamed to `lenses-legacy.html`, no
  longer linked — the header/homepage now point at the ported `viewers/lenses.html`.
- Verified with Playwright (chromium, local static server): all 12 touched pages return
  HTTP 200 with zero same-origin 404s (caught and fixed 3 viewer scripts that were
  referenced but not copied on the first pass: `grammar-loader.js`, `deck-picker.js`,
  `eco-links.js`). Cover images / Tailwind / d3 / the Supabase CDN / the shared assistant
  script all fail to load in this sandbox's network-restricted environment
  (`ERR_TUNNEL_CONNECTION_FAILED`) — a sandbox limitation, not a new bug; needs a real
  network (Vercel preview or unblocked egress) to confirm the fully-dressed visual pass.

## July 7, 2026 — The ONE shared recursive.eco assistant sidebar on every page

- New `assistant.js`: loads the shared shell from `recursive.eco/js/assistant-launcher.js`,
  which iframes the flow app's `/assistant` embed — the exact same star FAB and tabbed
  sidebar (Chat · Tarot · I Ching · Astro · Story) every recursive.eco page mounts. One
  source, zero drift; auth carries because astro.recursive.eco is a `.recursive.eco`
  subdomain. Included on index, wheel, lenses, genealogy, course, course-viewer, and the
  chart viewer (where it no-ops when iframed by the flow app, which has its own assistant).
- `pages/course-viewer.html` drops the hand-rolled `course/course-assistant.js` chat widget
  (a pattern-copy of recursive-tarot's) in favor of the shared sidebar, matching
  recursive.eco's own course viewer. The old widget file stays in the repo one round for
  easy rollback.

## July 7, 2026 — New reading course "The Right Size" + multi-course viewer

- New thematic course **"The Right Size"** (`course/the-right-size.mdx` → generated
  `grammars/the-right-size/grammar.json`), analogous to recursive-tarot's "How the Cards
  Can Work": not whether the stars decide fate, but what happens when we agree to relate
  to the visible sky as though it were alive — grounded in solid science (the sun as
  life-driver, the sunflower's internal clock, lunar-cued coral spawning, tides, synchrony
  → cooperation), honest about the null result on lunar effects on human behavior and the
  metaphysics we cannot know, and framed as a shared "secondary world" / social contract
  we choose to coordinate by. Voice: PlayfulProcess. Threads Wallis (deity as a form
  consciousness takes), Mīmāṃsā (ritual value without metaphysics), Friedman's "as if,"
  Harari's shared fictions, Chwe's common knowledge, and the "right size" theme (scale
  between hubris and despair).
- **Multi-course viewer**: `pages/course-viewer.html` now reads `?course=<slug>` (default
  stays History of Astrology, all existing links unchanged); each course's manifest names
  its own `sourceGrammar`, so adding a course = one manifest + one grammar, no viewer edit.
- Views menu: "Course" → "History of Astrology" + new "The Right Size (a reading)".
- Research dossiers backing the course live in `research/why-astrology/` (Wallis/devotion,
  empirical hooks, imaginative threads) with ✔/○/◆ confidence markers.

