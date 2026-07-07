# How to Write a Course (Recursive method)

This is the pipeline used to write **"The Right Size"** (astro) and **"How the Cards Can Work"** (tarot). It exists so the next course — by the builder, by Claude, or by a contributor — is made the same careful way. The same doc lives in `recursive-tarot/docs/` and `recursive-astrology/docs/`.

The goal is courses that are **honest, grounded, in the builder's voice, and non-repetitive** — a reading you'd trust, not a sales pitch for a belief.

## The four phases

### 1. Research first — with adversarial honesty
Never write from memory. Spin up focused research agents (one per theme), and hold them to one rule: **verify every factual or attributed claim by actually fetching/finding the source before it goes in.** Each dossier marks confidence explicitly:

- ✔︎ verified (title + author + venue + year, with DOI/URL)
- ○ real source but paraphrased / partial
- ◆ contested or could-not-verify

Dossiers live in `research/why-<topic>/`. Rules learned the hard way:
- **Exclude contested claims.** The tarot research caught a *retracted* paper (Brooks 2016) and dropped it; the astro course dropped the "wood-wide-web" because the mycorrhizal "mother tree" claims are contested (Karst et al. 2023). If the record is mixed, either leave it out or **show both sides** — never launder a contested claim into a confident sentence.
- **Report against yourself.** Where the evidence undercuts the course's own thesis, say so in the course. (The astro course states plainly that the lunar-behavior effect — the claim closest to astrology's own — mostly isn't there.)
- **Don't overclaim a person's view.** Wallis has no stated position on astrology, so the course uses him only to ground deity/devotion, never implying he endorses astrology.

### 2. Thesis + outline — proposed, then confirmed
Synthesize the dossiers into **one-sentence thesis** + a **section outline**, and get the builder's sign-off before writing. Two hard constraints:
- **Distinct but rhyming.** Each course must stand on its own spine, not repeat a sibling. Tarot grounds in *Tolkien* (made-up pictures carry real seeing); the astro reading grounds in *devotion / relationship / right-size* (the sky as a shared secondary world). Same honesty spine ("real X, yes; prediction, no"), different body. If your opening reads like another course's opening, rewrite it.
- **The honesty spine is non-negotiable.** The course never claims the practice predicts. It claims something truer and more interesting.

### 3. Write the prose — in the builder's voice
Author the course as a single `course/<slug>.mdx` (source of truth). Voice: **first-person, warm, humble, literary, willing to argue against itself, no AI-ish bullet sprawl.** Read the builder's own writing (her books repo, prior courses) to match register and borrow her load-bearing ideas *in her words* ("you just relate; the moon is relationship"; "right size" between hubris and despair). Close the loop: the final section should call back to the opening image so the whole reads as one gesture.

### 4. Deliver + verify + review
- **Tarot:** the course-viewer renders MDX directly (`?course=<slug>`). Regenerate the compiled anthology + grammar mirrors (`scripts/course_to_grammar.py`, `scripts/build_reading_course.py`).
- **Astro:** the course-viewer is grammar-driven. Convert the MDX into `grammars/<slug>/grammar.json` (each `##` section → one chapter item, prose in a `Reading` section), add `course/<slug>.manifest.json` naming its `sourceGrammar`, and register it in the `COURSES` map in `pages/course-viewer.html` + the Views menu in `site-header.js`. Default course (no `?course=`) must keep working.
- **Verify** with Playwright at 390×844 against a local `python3 -m http.server`: the course renders, TOC works, no page errors, and the default course still loads.
- **Review for flow:** read the whole thing start to finish and check it doesn't contradict itself or repeat a sibling course. This step is not optional.

## The principle under all of it

> The metaphysics we cannot know; the relating we can.

A Recursive course never asks you to believe the practice works by magic. It grounds what is real, is honest about what isn't, and offers the rest as a secondary world we may *choose* to relate through — held lightly, with room for the cracks. That honesty is the reason the courses are worth trusting.
