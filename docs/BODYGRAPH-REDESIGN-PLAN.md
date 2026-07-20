# Bodygraph redesign — plan (approve before building)

The builder's verdict on the first mockup: **ugly, and the channels don't follow the right
framework.** Both true. This plan says why, and what to actually do.

## What went wrong (honest root cause)

I hand-rolled a *new* bodygraph in `viewer/bodygraph-mockup.html` and invented the wiring:
gate numbers spaced evenly around each center, and **channels drawn centroid-to-centroid**
(arbitrary straight lines between center middles). That is not Human Design. Real channels
are **36 specific gate-to-gate connections**, each running from one gate's fixed anchor point
to another's.

The important discovery: **the ported calculator already renders the bodygraph correctly.**
Inside `viewer/astrology-viewer.html` are:

- `HD_CENTERS` — the 9 centers with their gates, positions, motor/awareness flags, colours.
- `HD_CHANNELS` — the **exact 36 channels** (`'34-20': Charisma [throat,sacral]`, …), each
  naming its two gates and two centers. This is the canonical framework.
- `GATE_POSITIONS` — a fixed `{x,y}` for **every one of the 64 gates**, placed at its real
  channel-attachment point (each entry is even commented with the channel it serves).
- The renderer (the function around `GATE_POSITIONS`) already: *"Draw all channels first as
  lines between gate positions"* → iterates `HD_CHANNELS`, reads both gates' `GATE_POSITIONS`,
  draws a `<line x1 y1 x2 y2>`, and colours it by `hdChart.definedChannels`. Centers fill by
  `hdChart.definedCenters`; gates sit at `GATE_POSITIONS`.

So the **framework is already right and already wired to real chart data.** What's wrong is
only the *look* — the reported bug was dark slabs in the light app, and the styling is dated.
My separate mockup should never have reinvented the geometry.

## The plan

**1. Retire the wrong mockup.** Delete/replace `viewer/bodygraph-mockup.html`'s invented
geometry. Any approval mockup must use the app's own `GATE_POSITIONS` + `HD_CHANNELS`, not a
parallel model — same one-source rule the rest of the family follows.

**2. Restyle the existing renderer, never its framework.** Touch only the drawing/CSS of the
bodygraph function; leave `HD_CENTERS`, `HD_CHANNELS`, `GATE_POSITIONS`, and the
defined/undefined logic exactly as they are. The redesign:

- **Centers** as clean geometric primitives (Head/Ajna triangles, Throat/Sacral/Root squares,
  G diamond, Heart/Spleen/Solar triangles), one stroke weight, one corner radius. *Defined* =
  filled with the centre's canonical colour; *open* = surface fill + outline. (This is the part
  the builder said was "just ok" — keep it, clean it.)
- **Gates** as small numbered nodes **at their `GATE_POSITIONS` anchors** (not evenly spread) —
  so every channel line meets its gate exactly where it should. Active gate = filled dot; dormant
  = hollow.
- **Channels** exactly as the renderer already does — gate-to-gate over the 36 — but restyled:
  a defined channel (both gates active) solid in the ink colour; a **hanging channel** (one gate
  active) shown as a half-line/stub from the active gate; an undefined channel faint or omitted.
  Decision needed on the classic **split colour** (Personality = black, Design = red) — see below.
- **Theme**: honour `?theme=light` (light surfaces, dark ink, purple accents) and dark, matching
  the calculator. No dark slabs in the light app.
- **Proportions**: match the standard vertical bodygraph (the BodyGraph.com reference the builder
  shared) — balanced, generous whitespace, gate numbers legible at mobile width.

**3. Approval mockup, correctly sourced.** Before folding styling into the live renderer, produce
one static preview that imports the app's real `GATE_POSITIONS`/`HD_CHANNELS` and a **sample real
chart** (a known defined-centers/defined-channels set), rendered in the new style, light + dark.
This proves the framework is correct (real 36 channels, real anchors) with the new look. Only
after sign-off does the styling merge into `astrology-viewer.html`'s bodygraph function.

**4. Verify** on a Vercel preview (the page needs Tailwind + flow assets + the API, not testable
in-sandbox) at mobile width, light and dark: channels land on their gates, defined/hanging/open
read correctly against a known chart, no dark slabs.

## Decisions needed from the builder

1. **Split colour?** Full HD shows each gate/channel half red (Design) + half black (Personality),
   with four channel states (both-personality, both-design, mixed, hanging). Do we render that
   canonical split, or simplify to defined/hanging/open for v1? (BodyGraph.com renders the split.)
2. **Match BodyGraph.com exactly**, or our own cleaner minimalist take on the same framework?
3. **Gate numbers** always visible, or only on active gates / on hover (less clutter)?
4. Keep the tidied geometric-primitive centre shapes, or move to the more rounded standard
   bodygraph centre rendering?

## Not in scope / untouched
The 36-channel framework, `GATE_POSITIONS`, `HD_CENTERS`, and the chart-calculation data flow —
all correct already. recursive-eco (read-only). `ids.json`.
