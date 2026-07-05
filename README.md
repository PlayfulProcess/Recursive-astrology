# The Recursive Astrology — a seed

This is a **seed**: a self-contained starter for the astrology counterpart of
[The Recursive Tarot](https://tarot.recursive.eco). It is the **same creed and method, a different
domain** — a static, backend-free site that turns a folder of JSON into a browsable library of the
*historiographical views of astrology*, held honestly to the record and autonomy-preserving
throughout.

Where the tarot library asks you to *relate to the card, never obey it*, this one asks you to **read
the sky to know yourself, not to be told your fate** — a chart is a mirror and a calendar, never a
command. And the subject here is not how to cast a chart but the **history of the practice**: the
five-thousand-year record of humans reading meaning *into* the sky, each tradition presented
faithfully in its own terms.

> **This repo is itself a Rung 6/7 move.** In the contribution ladder of the parent project, Rung 6
> teaches you to make your own *grammars* and Rung 7 to make your own *site* to show them. This seed
> is a whole commons **founded from** the tarot one — the method taken home and pointed at a new
> subject. If it grows, it becomes its own repo (`recursive-astrology`-ish), sibling to the tarot.

## What's in the box

```
recursive-astrology/
├── index.html                                       reads one grammar and renders it as cards
├── theme.css                                        the single source of colour (light only)
├── voices.json                                      the creed, translated — shared_intention + 3 voices
├── grammars/
│   └── historiographies-of-astrology/
│       └── grammar.json                             the library: 10 views + 3 pattern groupings
├── check.py                                         the pre-commit gate, zero dependencies
├── CLAUDE.md                                         the rules of this commons (the creed is the spine)
├── GRAMMAR_FORMAT.md                                the canonical shape of a grammar
└── README.md                                        this file
```

Everything is plain HTML, one CSS file, and JSON. No build step, no framework, no server in
production. GitHub Pages serves it as-is.

**No images, on purpose.** Every item is imageless. Honest sourcing of public-domain star charts and
plates is a later, separate job — an honest gap beats a wrong picture. See `CLAUDE.md` for the full
sourcing guardrails (never invent a citation, hedge contested claims, flag paraphrase as paraphrase).

## The first hour

**1. See it work (2 min).** Browsers block `file://` fetches, so open it over a tiny local server:

```bash
cd recursive-astrology
python -m http.server 8091
# now visit http://localhost:8091/
```

You'll see the library — the major historiographical views (Mesopotamian omen-craft, the Hellenistic
synthesis, Jyotiṣa, the Islamic golden age, and on through the modern test tradition and the
contemporary resurgence) plus a few *patterns* that group them — rendered as cards you can open.

**2. Read the grammar (15 min).** Open `grammars/historiographies-of-astrology/grammar.json`. Each
item is one **view**: an `id`, a `name`, and `sections` — `What this view holds` (faithful, in the
tradition's own terms), sometimes `In its own words` (a verifiable line or a flagged paraphrase),
`The record` (the honest, hedged history), and `Reading` (2–3 standard scholarly works as pointers,
no page numbers). The last three items are **patterns** — they hold no view of their own; they have
`composite_of: [ids]` and make a historiographical shape visible across several views.

**3. Add a view (20 min).** Copy an existing item, give it a new `id`, and fill the sections for a
tradition or era you know. Keep the creed: read the record, don't predict; hedge what's contested
(`metadata.confidence: "low"`); name only sources you're sure of. Reload the page.

**4. Check it (1 min).**

```bash
python check.py
# → OK: all checks passed (1 grammar)
```

`check.py` catches the handful of mistakes that stop a grammar from loading. Keep it green.

**5. Put it on the web (15 min).** Create a GitHub repo, push this folder, then **Settings → Pages →
Deploy from a branch → (your default branch) / root**. In a minute your library is live at
`https://<you>.github.io/<repo>/`. Share the link.

## The three voices

`voices.json` mirrors the tarot's `shared_intention` structure exactly (same keys, so tooling ports),
then seeds three orientations you can read a sky through — each a genuine stance, presented faithfully:

- **Ptolemy** — natural-philosophy astrology: celestial influence as the physics of its age, and
  explicitly hedged (as Ptolemy himself hedged the *Tetrabiblos*) as a fallible, conjectural art.
- **Jung** — the archetypal mirror: the chart as a map of the psyche, meaningful by synchronicity
  (correspondence, not cause). An *inspired-by* framing, not the man's endorsement.
- **The Skeptical School** — from Pico della Mirandola to the modern controlled test: the view that
  astrology's effects are supplied by the reader, not the sky — presented as *its own* tradition of
  critique, not as our verdict on the rest.

Any disagreement a voice has with the record lives in the long form (its `course` pointer / the
grammar's `The record`), never in the short `intention`. Every voice obeys the one creed.

## The two rules worth keeping

1. **All colour lives in `theme.css`.** One `:root` of tokens, linked everywhere, light only. Never
   redeclare a colour in a page, never add a dark-mode block. To recolour the whole site, edit that
   one file.
2. **The data outlives the platform.** The viewer is deliberately thin. If this starter vanished
   tomorrow, `grammars/*.json` would still be a clean, portable, public record of the subject. That's
   the point.

## Where this connects

- **The parent project:** [The Recursive Tarot](https://tarot.recursive.eco) — this seed's sibling,
  same creed, and the source of the grammar format and the theme.
- **The ladder you're on:** [Ways to Contribute](https://tarot.recursive.eco/pages/course-viewer.html?course=how-to-contribute)
  — Rungs 1–5 tend an existing commons; Rung 6 makes your own grammars; Rung 7 makes your own site.
  This whole seed is a Rung 6/7 move: a new commons founded from the tarot one.
- **Go further — the live app:** grammars here can also open in [recursive.eco](https://recursive.eco)
  for a live oracle, AI readings, and community editing. The parent's
  `docs/RECURSIVE-ECO-INTEGRATION.md` shows how a repo wires to a channel.

Take the method home. Found your own.
