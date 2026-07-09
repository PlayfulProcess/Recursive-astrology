# Changelog — The Recursive Astrology

## July 9, 2026 — Astro enrichment lane: aspects + dignities commented grammars

The parked "astro enrichment lane" from the builder's I Ching plan (recursive-starter
`docs/PLAN-iching-channel.md` §5): aspects and dignities/rulerships now have their own
commented grammars, same PD-source discipline as `renaissance-lilly`.

**New grammar `grammars/aspects-commented/grammar.json`** — the five classical (Ptolemaic)
aspects, each an item with three clearly-labeled commentary sections: `Ptolemy (Tetrabiblos)`
(Ashmand 1822 PD quotes reused verbatim from this repo's already-verified
`tetrabiblos-ashmand` aspect items), `Lilly (1647)` (the "imperfect enmity" / "perfect
hatred" / "arguments of Love, Unity and Friendship" doctrine — corroborated this session only
via a secondary reproduction, so marked ○; unverifiable wording is paraphrased and marked
low-confidence, never fabricated), and a contemporary `Canonical` synthesis in the
western-astrology-canonical register. The Ptolemy/Lilly sections use the lens `[attribution]`
prefix so the Provenance Ribbon dates them (1822/1647). Matcher keys documented in the
grammar description: `category:'aspect'`, `metadata.aspect` (capitalized, matching
western-astrology-canonical), `metadata.angle`, `metadata.nature` ('soft'/'hard'/'neutral'),
`metadata.orb` (contemporary convention, explicitly NOT a traditional claim — Ptolemy is
sign-based, Lilly puts orbs on planets/moieties). Description carries the reality note: orbs
and minor aspects vary by tradition; five classical ones to start; contributors welcome.

**New grammar `grammars/dignities-rulerships/grammar.json`** — essential dignities as a lens:
7 planet items (domicile(s), exaltation + traditional degree, detriment, fall; sections
`Dignities table` / `What dignity means` (Lilly's +5/+4/+3/+2/+1, −5/−4 scoring + the "lord
of his own house" doctrine via Zadkiel's 1852 PD abridgment) / `Canonical`) and 12 sign items
stating the same table from the sign's side (`metadata.sign`), with modern outer-planet
co-rulerships (Uranus/Neptune/Pluto) ONLY in Canonical sections, clearly marked as modern
additions. `metadata.planet` on every planet item → federates automatically into lenses,
wheel, and archetypal stacks. Machine-readable dignity keys ride in metadata
(domicile[]/exaltation/exaltation_degree/detriment[]/fall; ruler/modern_co_ruler on signs).
**Exaltation-degree verification**: direct fetches of primary scans were network-blocked this
session (proxy 403 on archive.org/gutenberg/wikipedia), so the degrees (Sun 19° Aries, Moon
3° Taurus, Mercury 15° Virgo, Venus 27° Pisces [some tables 28°], Mars 28° Capricorn, Jupiter
15° Cancer, Saturn 21° Libra) were cross-checked via multiple independently-phrased web
searches whose results (Wikipedia's Exaltation article, renaissanceastrology.com, al-Biruni's
Book of Instruction and Dorotheus's Carmen as reported by secondary scholarship) all agree;
the only variance found anywhere is Venus 27° vs 28°, noted honestly in the grammar. Sign
statements double-anchored to already-verified in-repo quotes (Ptolemy: "Capricorn is the
house of Saturn and exaltation of Mars", "Pisces is the house of Jupiter and exaltation of
Venus"; Lilly: Virgo "the house and exaltation of Mercury").

**Wiring**: both registered in `scripts/build_collection.py` (synthesis branch — multi-voice
compilations, not single primary sources), `_collection.json` regenerated (19 grammars, 328
items); both added to `ids.json` `_public_now` + `ids` (new UUIDs
`dee46a22-3848-433e-a793-8c7a2206e8cb` aspects, `1ab72d9f-f283-475e-951a-1841215e1274`
dignities) + `preview_links` — the orchestrator inserts the Supabase rows. `check.py` passes
on all 19. **Playwright-verified** (chromium, local server): lenses.html picker lists both
new voices; Synopsis on Saturn stacks the dignities card ("Domicile: Capricorn, Aquarius ·
Exaltation: Libra (21°)") with the picker highlighting it as having Saturn; Synopsis on
Square stacks the aspects-commented column incl. Lilly's "imperfect enmity"; archetypal.html
single-tap on Saturn auto-discovers the dignities voice in the every-voice stack — 10/10
checks pass.

## July 9, 2026 — Assistant/header z-index fix + grammar picker on `wheel.html` and `lenses.html`

**Bug fix: the site's own sticky header was painting over the assistant panel's top content.**
Builder reported (screenshot on a course page, mid-chat-response) the header covering the
first lines of the assistant's reply while scrolling. Root cause, confirmed by reading the
actual shared source (`recursive-eco/apps/landing/js/assistant-launcher.js`, fetched via the
GitHub API since `recursive.eco` is network-blocked from this sandbox): `.rec-assistant-shell`
is `z-index:45` — LOWER than this site's own sticky `<site-header>` (`site-header.js`,
`z-index:50`). Both are `position:fixed`/`sticky` elements competing directly at the document
root, so the bigger number simply wins — no stacking-context trap, no missing
`scroll-margin-top`. `site-header.js` also **auto-hides on scroll-down and reveals on
scroll-up** (a normal reading gesture), which re-plants the header at `top:0` while the
assistant panel (fixed, unaffected by page scroll) is open — that's the exact moment the
header's opaque background paints over the panel's top ~129px.
- **Reproduced deterministically** with Playwright: a repro page with the real
  `site-header.js` + the real `.rec-assistant-shell`/`.rec-open` CSS (values copied from the
  fetched source), scrolled down then up (triggering the reveal), then
  `document.elementFromPoint()` at the overlap band's midpoint returned `SITE-HEADER` before
  the fix and the assistant's own message `DIV` after — the same coordinate-overlap technique
  `TourRunner.tsx`'s `?tour-debug=1` uses in the sibling flow app.
- **Fix** (`assistant.js`): after loading the shared launcher, inject one override rule —
  `.rec-assistant-shell{z-index:2147483000!important}` — forcing the panel to always sit above
  any page chrome regardless of the shared launcher's current or future z-index. The proper
  long-term fix is bumping the z-index in the shared launcher itself (it's meant to be the
  topmost layer on every recursive.eco family site) — that file lives in the private
  `recursive-eco` repo and needs its own session/approval; this is the safe, self-contained
  stopgap on this repo's side. (`recursive-tarot`'s own header is also `z-index:50` — worth a
  matching stopgap there if/when it adopts this same shared launcher.)

**Feature: a user-curated, multi-select grammar picker for the "every voice" stack.**
Builder: *"in the astro viewers I want the flexibility to pull different grammars. we could
recon grammars with houses and render there and highlight the ones for which they populate.
maybe we can multiselect and stack several grammars."* Before this, `wheel.html` (and
`archetypal.html`) auto-loaded and stacked EVERY public grammar with no reader control.
- **New shared module `grammar-picker.js`** (repo root, alongside `site-header.js`/`icons.js`
  — no bundler, so a plain shared `<script>` is this family's existing pattern for
  cross-page code): loads `grammars/_collection.json` + every `grammar.json` once, detects
  what each grammar "has" (`house`/`planet`/`sign` — by `category` OR `metadata.<shape>`,
  the same data-shape inference `findHouseItem`/`findPlanetItem` already use — never a
  `document_type`/slug check), and renders a chip checklist: chips that populate the
  current view stay full-ink and highlighted when selected; chips that don't are shown
  de-emphasized (dimmed, italic) but **never hidden** — the family's honesty convention is
  to show gaps, not hide them. Every toggle fires `onChange` immediately — no page reload,
  no "Load" button. Selection persists per-viewer via `localStorage`.
- **`wheel.html`**: replaced its hardcoded `loadTraditions()` (fetch-all, filter by
  `category==='house'`, stack unconditionally) with `GrammarPicker.create({shape:'house', ...})`.
  Default selection = every house-bearing grammar (byte-identical stack to before: 5 voices —
  Ptolemy, Proctor, Alan Leo, Astro-of-all-astros, Western Astrology Canonical), so nothing
  regresses for a reader who never touches the picker; narrowing the selection now narrows
  the stack live, including while a house dialog is later reopened.
- **`viewers/lenses.html`**: it already had its own working live multi-select ("Grammars"
  panel) — the gap was purely "highlight which ones populate the current view." Added
  `currentEntityKey` tracking (the entity resolved by whichever entity-scoped lens —
  Synopsis/Ribbon/Small-multiples — is active; null for Matrix/Reader, which aren't
  entity-scoped) and a `dp-has`/`dp-gap` highlight in the existing deck panel, plus a count
  line ("8 of 17 grammars have 'Saturn'"). Fixed in passing: the deck-button click handler
  only toggled the panel's `open` class without rebuilding it, so opening the panel after
  picking a new entity showed stale (unhighlighted) content — now rebuilds on open.
  `archetypal.html` intentionally left untouched per the builder's explicit "always on"
  every-voice design for that page.
- **Playwright-verified** at 390×844 (headless Chromium, local `python3 -m http.server`):
  `wheel.html` picker lists all 17 grammars, exactly 5 highlighted as house-bearing
  (cross-checked against the page's own data, matched); default selection stacks 5 voice
  cards (no regression); selecting 2 stacks 2; deselecting one and reopening a house shows 1
  — live, no navigation. `lenses.html`'s picker highlight for "Saturn" matched the page's own
  `ITEMS` data exactly (8 of 17); unchecking one has-Saturn grammar dropped the Synopsis
  column count from 8 to 7 live, no reload. No console/page errors from either page's own
  code (only the sandbox's expected network blocks on the assistant launcher script).

## July 8, 2026 (2) — Archetypal Astrology: planetary pairs, after Tarnas (`archetypal.html`)

New grammar + its own dedicated UI, per the builder's direction: "Archetypal astrology of
Richard Tarnas gets its own UI (just planets relationships) ... it is itself a meta grammar
of just the planets over time coming from different grammars — since his impetus was to
find what is common across all traditions by looking at what the traditions themselves kept
agreeing to look at (planetary relationships)."

- **`grammars/archetypal-pairs/grammar.json`** (25 items) — new grammar, `branch: synthesis`.
  - **3 authored base items** for the outer planets the classical/historical voice grammars
    in this repo lack (`planet-uranus`, `planet-neptune`, `planet-pluto`), each with an
    "Archetype" section written from Tarnas's characterizations (Uranus: the Promethean;
    Neptune: dissolution/the oceanic; Pluto: the underworld drive), framed explicitly as
    interpretation, not Tarnas's own words.
  - **7 thin local stubs** for the classical planets (Sun…Saturn) — carry only
    `metadata.source_grammars` provenance + a one-line pointer to
    `western-astrology-canonical`, so `composite_of` below resolves *locally* per
    `GRAMMAR_FORMAT.md`'s hard rule and `check.py`'s enforcement of it. No content is
    duplicated; the real multi-voice reading stacks live in the UI (see below). This is the
    "Base items ... copies the entity item(s) ... records provenance in
    `metadata.source_grammars`" pattern from `docs/DESIGN-wheel-frames.md`, its first use.
  - **15 authored pair items** (`category: "archetypal-pair"`, `composite_of: [planet-a,
    planet-b]`): the 10 outer/social-planet complexes Tarnas actually treats in *Cosmos and
    Psyche* (Saturn–Pluto, Uranus–Pluto, Jupiter–Uranus, Uranus–Neptune, Saturn–Neptune,
    Saturn–Uranus, Jupiter–Saturn, Jupiter–Neptune, Jupiter–Pluto, Neptune–Pluto) plus 5
    personal-planet pairs (Sun–Saturn, Sun–Pluto, Venus–Mars, Moon–Saturn, Mercury–Uranus).
    Each has "The complex" (~100-150 words), "In history" (2-3 real correlations, "Tarnas
    correlates..."; the 5 personal pairs honestly note that fast personal-planet cycles fall
    outside the book's own historical dataset instead of inventing a citation), and "A
    question."
  - **Honesty frame** — non-negotiable, present in the grammar `description`, a
    `_synthesis_note`, a dedicated `_honesty_frame` field, AND visible on the UI: "Inspired
    by Richard Tarnas's archetypal astrology (*Cosmos and Psyche*, 2006; *The Passion of the
    Western Mind*). These readings are PlayfulProcess's interpretation, written with an AI
    from its knowledge of his work — NOT Tarnas's words, not his endorsement. Go to the
    source: https://cosmosandpsyche.com/" (verified findable via search this session).
- **`archetypal.html`** — new page. Ten planets (Sun…Pluto) on a ring; tap two → a chord
  line highlights between them and the reading stacks below: (a) the pair's authored
  complex from `archetypal-pairs` if one exists, or an honest "no authored complex yet — the
  parents speak below" note if not; (b) each parent planet's own entry from *every other*
  voice grammar in the repo (Planetary Myths, Ptolemy, Lilly, Jyotiṣa, Alan Leo, Canonical),
  matched live via `grammars/_collection.json` — the same cross-grammar matcher
  `viewers/lenses.html` uses. **This live parent-stacking IS the meta layer** — no second
  generator script, per the design note in `docs/DESIGN-archetypal.md`.
  Mobile-first (verified at 390px with Playwright): ring renders, labels don't clip at the
  viewBox edge (dynamic text-anchor by angle), tapping Saturn+Pluto renders the authored
  synthesis + 20 voice cards (10 traditions × 2 planets), tapping an unauthored pair
  (Mars–Neptune) renders the honest gap note.
- **Wired in**: `ids.json` (`_public_now` + a placeholder UUID, `preview_links` entry),
  `scripts/build_collection.py` (`BRANCH_OF["archetypal-pairs"] = "synthesis"`, re-run —
  `grammars/_collection.json` now 17 grammars / 304 items), `site-header.js` Views menu
  ("Archetypal — planet pairs", `?v=45`), `index.html` gallery card. `astro-of-all-astros`
  intentionally NOT extended to include this grammar — it's not a per-entity voice, it's its
  own synthesis; the design note explains why.
- Validated every grammar in the repo with `python3 check.py` (17/17 pass, including the new
  one) both before and after wiring.

## July 8, 2026 — Lilly's twelve zodiac signs, sourced (`grammars/renaissance-lilly/`)

Fills the gap the Jul 7 session flagged: `renaissance-lilly` covered only the seven
planets; the app's own AI (no web research) had tried to fill signs and produced one
generic, unsourced "Taurus" draft. This pass adds all twelve signs as William Lilly
actually describes them in *Christian Astrology* (1647), Book I.

- **12 new items** in `grammars/renaissance-lilly/grammar.json` (`sign-aries` …
  `sign-pisces`, `category: "sign"`, `metadata.sign` canonical-cased), each with an
  "In the text" section (the sourced quote/summary, book+chapter ref, confidence marker)
  and a "What this lens reads" one-liner comparing Lilly's formula to
  `western-astrology-canonical`'s light/shadow archetypes (and occasionally Ptolemy/
  Jyotiṣa). These `id`/`name`/`metadata.sign` values match the app's canonical shape, so
  they supersede the two AI-drafted placeholder items cleanly on next reindex rather than
  duplicating.
- **WebFetch was 403'd on every source again this session** (archive.org, skyscript.co.uk,
  sacred-texts.com, astroamerica.com) — same session-wide proxy block as Jul 7. All twelve
  quotes rest on WebSearch synthesis, each cross-corroborated via at least two independently
  worded queries. **9 of 12 signs: medium confidence** (Aries, Taurus, Gemini, Cancer, Leo,
  Virgo, Libra, Sagittarius, Pisces — identical wording surfaced across independent secondary
  mirrors). **3 of 12: low/○** (Scorpio — only a short paraphrase locatable, presented as
  "summarized from," not quoted; Capricorn and Aquarius — full formula from a single
  secondary source, with the constituent facts but not the whole sentence independently
  corroborated). Full per-sign table in `research/why-astrology/06-genealogy-grammars.md`
  §3b.
- **`grammars/astro-of-all-astros/grammar.json` regenerated** — Lilly now covers signs
  (12/12, up from the Jul 7 build's 4/6 sources on signs), so every sign item in the
  meta-voice grammar gains a `"Lilly (1647)"` section alongside Canonical/Ptolemy/Jyotiṣa/
  Alan Leo. `grammars/_collection.json` regenerated too (16 grammars, 279 items, up from
  267 — the +12 Lilly sign items).
- Validated with `python3 -c "import json;json.load(...)"` before and after both generator
  runs.

## July 7, 2026 (2) — "Astro of All Astros": a generated meta-voice grammar

Proves out the Oracle Trinity design (`docs/DESIGN-oracle-trinity.md`, "Astro of all Astros" /
"the same mechanism as Tarot of All Tarots + the lenses matcher") as an actual artifact, not
just a plan.

- **New generator** `scripts/build_meta_astro.py`, mirroring
  `recursive-tarot/scripts/build_meta_grammar.py`'s pattern (generated projection over the
  repo's own grammar files, idempotent, `_do_not_hand_edit`). Reads all six voice grammars
  (`western-astrology-canonical`, `tetrabiblos-ashmand`, `renaissance-lilly`,
  `jyotisha-brihat-jataka`, `alan-leo`, `planetary-myths`), canonicalizes each source item's
  planet/sign/house identity (name matching + `metadata.planet`/`metadata.sign`/
  `metadata.western_equivalent` + the same id-pattern house-number heuristic
  `astrology.types.ts`'s `extractHouseNumber` uses, kept in sync on purpose), and produces
  one item per shared entity — 7 classical planets + 12 signs + 12 houses (aspects excluded;
  out of scope for this pass) — with a `sections` entry per source that actually covers that
  entity: `"Canonical"`, `"Ptolemy (Tetrabiblos)"`, `"Lilly (1647)"`, `"Jyotiṣa (Bṛhat Jātaka)"`,
  `"Alan Leo"`, `"Planetary Myths"`. No fabricated coverage — e.g. Lilly (planets only) never
  gets a sign/house section; Jyotiṣa (planets + signs) never gets a house section.
- **New output** `grammars/astro-of-all-astros/grammar.json` — 31 items total (7 planets ×
  6/6 sources, 12 signs × 4/6 sources — Lilly + Planetary Myths don't cover signs, 12 houses ×
  2–3/6 sources — only Canonical, Ptolemy, and Alan Leo cover houses in this repo today).
  `grammar_type: "astrology"`, `category: "planet"/"sign"/"house"` + matching
  `metadata.planet`/`metadata.sign`/`metadata.house` on every item, so it reads as a
  first-class astro voice everywhere the app/viewers already look for one (unlike the tarot
  companion task this same day, which needed a caveat — this grammar's items get the
  *category* the matcher expects, not metadata alone). `_generated: true` +
  `_rebuild_note` pointing back at the generator; `_sources` records which six grammars fed it
  and their display names, for traceability.
- **Registered in the collection**: added `astro-of-all-astros` → `synthesis` branch in
  `scripts/build_collection.py`'s `BRANCH_OF` (cosmetic — it would have landed in
  `synthesis` by default anyway via the glob, since the script has no hardcoded slug list to
  fall out of date) and reran the script — `grammars/_collection.json` now lists 16 grammars
  (267 items total, up from 15/236). No site-header edit needed: `site-header.js`'s Grammars
  dropdown fetches `_collection.json` live and groups by branch, so the new voice already
  appears there and in every ported viewer (`cards.html`, `explorer.html`, `lenses.html`,
  `tree-viewer.html`, `timeline.html`) without any hardcoded menu to touch.

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

