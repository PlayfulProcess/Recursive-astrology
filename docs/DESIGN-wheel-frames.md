# Design — Wheel Frames (the astro repo's own instrument)

Builder's design (Jul 2026), superseding the flow-app "AstroCaster/Frame" experiment —
which is being REMOVED from recursive-eco per the same ruling.

## The architecture ruling (applies family-wide)

> **The flow app is the minimum common denominator. The open-source repo is where
> individuality comes to life — like private and public life.** Once a pattern matures it may
> migrate back into flow (as tarot spreads did), but the frames belong HERE, with a UI that is
> fairly flexible, in the astro repo. Flow keeps chart data + aspects + AI journaling, and
> **redirects** people to this site for the wheel — never an embedded preview of it.

## Frames are hardcoded UI, not grammars

The earlier casting-* spread-grammars approach is retired for astro. The frames (All Houses,
the Big Three, One Aspect, …) are **hardcoded modes of the wheel UI**:

- The wheel renders with **highlightings** showing what the current frame selects
  (e.g. All Houses frame → the twelve house sectors glow; Big Three → Sun, Moon, Ascendant).
- **Hover/tap a highlighted element** (Taurus, House 1, Mars…) → its meaning appears.
- **Below the wheel, all highlighted meanings render STACKED** — and, exactly like the tarot
  cards viewer, the reader can stack MULTIPLE voice grammars at once: several Mars entries
  together, several Taurus together (Ptolemy + Lilly + Jyotiṣa + Leo + myths), the same
  multi-voice stacking the lenses view already does, applied to a framed chart.

## Save as grammar — two steps, two scopes

Like save-a-spread / save-a-cast in tarot, but with an explicit two-step choice:

1. **Scope**: save ONE item (this highlighted placement + its stacked meanings) or the WHOLE
   framed reading (e.g. all twelve houses with every attached meaning).
2. **Destination**: a NEW grammar, or into an EXISTING one (search picker — the app's
   Add-Reading-to-Grammar pattern).

A saved frame is a real grammar. Even private, it can then be LOADED BACK into this wheel
as a frame source — your own house-meanings driving the highlights.

## The data structure (the part to get right)

When a saved frame draws on multiple source grammars, the export must stay legible to both
the AI and the UI:

- **Base items**: a saved placement copies the entity item(s) with their matcher keys
  (`category` planet/sign/house + `metadata.planet/sign/house`) and records provenance in
  `metadata.source_grammars: [{uuid, name, item_id}]` — sources as METADATA.
- **Emergences**: "What does House 1 in Taurus mean?" is a genuine EMERGENCE — a new item
  `composite_of: [house-1-ref, sign-taurus-ref]` (the kali↔paradevi machinery), carrying the
  reader's own synthesis text plus the provenance of both parents. The UI (and the AI) must
  read BOTH base items and emergences: an emergence renders stacked beneath its parents when
  its parents are on the wheel.
- **Publishing + resolution**: a frame grammar published to this channel lets others build on
  it — but an emergence only fully POPULATES for a reader who also has the base grammars it
  references (resolution by item keys + source UUIDs). Unresolved parents render honestly:
  the emergence's own text always shows; the missing parent shows as a named gap with a link
  to the source grammar, never silently dropped. This is the recursive-public shape: my
  synthesis is usable alone, and richer inside the commons that produced it.

## What flow keeps (minimum common denominator)

Birth-data entry, the aspects/placements list, Select-for-AI-context, the placement detail +
Interpret-with-AI, save-reading — the journaling loop. The wheel itself: a redirect card to
this site ("Open your chart in The Recursive Astrology ↗", purple eco-redirect), params
carried so the chart opens ready. If frames mature here, we revisit what migrates back.

## Order of work (here, not flow)

1. Frame modes on wheel.html (All Houses first — it's the one the homepage already promises),
   highlight + hover-meaning + stacked meanings below, multi-voice stacking via the existing
   lenses matcher (entity keys).
2. Save-as-grammar (two-step scope/destination) writing grammar JSON downloads first;
   publish-loop integration after.
3. Emergence authoring in the stack ("add your reading of House 1 in Taurus" → composite_of).
4. Load-a-frame-grammar-back (private frames as wheel sources).
