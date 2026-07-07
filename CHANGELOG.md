# Changelog — The Recursive Astrology

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

