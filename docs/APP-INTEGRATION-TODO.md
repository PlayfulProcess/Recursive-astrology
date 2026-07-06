# APP-INTEGRATION-TODO — the recursive.eco side (hand-off notes)

*This repo builds no app code (house rule). These are the four wiring steps for the recursive.eco
side, in order, matching `DESIGN-oracle-app-spreads-as-grammars.md` Phase 0/1. Written 2026-07-06.*

1. **Bind this repo as a repo-canonical channel.** Import
   `PlayfulProcess/Recursive-astrology` via its `recursive-eco.json` (channel slug `astrology`,
   `source_of_truth: 'repo'`), exactly like nara / kali-paradevi / recursive-tarot. Grammars come
   from `grammars/*/grammar.json`; the slug→UUID bindings land in this repo's `ids.json`
   (currently empty — first import fills it; update `_public_now` as grammars go public).

2. **Point the astrology oracle at this channel's grammars** (retire the hardcoded selector —
   design doc Phase 0/1). The flagship interpretation set is `western-astrology-canonical`; the
   public-domain voice libraries (`tetrabiblos-ashmand`, `alan-leo`,
   `proctor-skeptical-astrology`) are alternate reading lenses the picker can offer. Oracle kind
   is `astro` (`oracle:astro:<UUID>`), shared with nara.

3. **The in-app caster reads the `casting-*` spread-grammars.** Three exist:
   `casting-big-three`, `casting-twelve-houses` (`layout: "wheel"`), `casting-single-aspect`.
   The binding rule this channel adds to `castThroughSpread`: **`draw` is `derived`/`choose`,
   never `random`** — a position resolves to an aspect of the querent's own chart via
   `maps_to` (`planet-in-sign` | `house` | `angle` | `any-chart-feature`), against the grammar
   named in `casting.from`. Birth-data → placements needs the ephemeris engine (the Skyfield
   `calculate-chart.py` already in the family); until wired, honor
   `casting.fallback: "user_entered_placements"` so the oracle ships data-only. This repo's
   `wheel.html` is the reference rendering of the twelve-house casting (thin SVG, no calc).

4. **Make the cast-reading enrichment data-driven.** The AI enrichment must read *this* repo's
   item sections (`Story` / `Light` / `Shadow` / `Archetype` on the flagship;
   `Interpretation` / `Light` / `Shadow` on the voice libraries; `Position` / `Prompt` on
   castings) — not tarot-shaped `Scene`/`Symbol`. Don't special-case the app: sections are
   whatever the grammar carries; render what's there. The autonomy floor is part of the contract:
   enriched readings are mirror-prompts about the querent's own chart, never predictions.

*Later (design doc Phase 4 / REPLAN G2, the builder's subscription vision): discovery `+` in the
oracle pill row → this channel's castings listed; free-on-repo vs. paid-in-app tiers; owner-set
`subscription: { price, period }` on the channel-doc. Nothing in this repo blocks it — castings
are already data.*
