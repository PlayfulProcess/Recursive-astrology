# App integration — the astro repo now hosts the chart calculator

**Direction change (Jul 19 2026, builder).** The old rule in this repo's docs —
*"this repo builds no app code, it is a thin static library site"* — is **reversed for the
chart calculator**. recursive.eco (flow) will **embed a page served from here**. The
grammar/library side keeps its static, no-backend character; the calculator is the one
deliberate exception.

## What was ported

`viewer/astrology-viewer.html` — the working birth-chart calculator, copied **wholesale**
from recursive-eco `apps/landing/pages/astrology-viewer.html` (read-only clone; that repo
was not edited). The ephemeris math was **not** rewritten — see the critical finding below.

## Critical finding the original port brief did not capture

**The chart math is not in the page — it is a backend API.** The calculator POSTs to
`/api/calculate-chart` (Skyfield / JPL DE421, server-side in the flow app). There is no
client-side ephemeris to "copy." So a page hosted on the astro origin cannot compute a
chart by itself; it must call flow's API cross-origin. The port therefore points
`CHART_API_URL` at flow's absolute origin (dev/prod auto-detected). **This requires flow's
`/api/calculate-chart` (and the app-shell assets) to allow the astro origin via CORS —
that config lives in the recursive-eco repo (off-limits here) and is the one open
dependency before the ported page can calculate live.**

Two embed-contract requirements from the brief were **already implemented in the source**
and are preserved by the copy:
- **Step 2** — on calculation, `postMessage({type:'astrology-chart-calculated', …})` to the
  parent (source line ~3210).
- **Step 3** — the wheel-image responder: on `{type:'astrology-request-chart-image'}` it
  serializes the wheel SVG → canvas → `toDataURL('image/png')` → replies
  `{type:'astrology-chart-image', imageDataUrl}` (source ~2678).

## What the port changed (surgical, low-risk)

- **Asset + API base → flow.** Root-absolute deps (`/config.js`, `/assets/…`, `/style.css`,
  `/icons.svg`, `/spiral/…`, `/js/…`, `/favicon.png`) and `CHART_API_URL` now resolve
  against `https://flow.recursive.eco` (or `dev.flow.…` when the host contains "dev"), so
  the page loads its shell and reaches the math API from the astro origin.
- **`RecursiveAuth.init()` guarded** so a missing/blocked auth shell can't hard-crash the page.
- **Step 4 — theme=light honored.** An appended override reads `?theme=light` and applies a
  light surface / dark text / purple-accent skin (the source was dark-only; dark slabs in
  the light app were the reported bug).
- **Step 5 — fullscreen is a CSS overlay, not the native API.** The native
  `requestFullscreen()` calls (`toggleFullscreen`, `toggleChartWheelFullscreen`,
  `toggleMandalaFullscreen`, `toggleBodygraphFullscreen`) are overridden to toggle a
  `position:fixed; inset:0` overlay with an ✕ / Esc exit — works inside the iframe and on iOS.

## Verification status — HONEST

This page **cannot be verified in the build sandbox**: it needs Tailwind's CDN, flow's
app-shell assets, and the remote `/api/calculate-chart` — all outside the sandbox's network.
It must be verified on a **Vercel preview deploy** against live flow, at mobile width, in
**light and dark**, checking: (a) the form renders and a calculation returns a wheel;
(b) `theme=light` shows light surfaces with no dark slabs; (c) fullscreen expands as an
in-page overlay, not a clipped native box; (d) the parent receives `astrology-chart-calculated`
and answers `astrology-request-chart-image`. Ship order per the brief: 1–3, then 4–5.

## Step 6 — HD Bodygraph (PROPOSAL ONLY, not built, awaiting approval)

Proposed redraw of the Human Design bodygraph so the nine centers read as clean geometric
primitives instead of the current busy rendering:

- **Center shapes (canonical HD geometry):** Head = triangle (apex up); Ajna = triangle
  (apex down); Throat = square; G/Identity = diamond (rotated square); Heart/Ego = small
  triangle; Sacral = square; Solar Plexus = triangle; Spleen = triangle; Root = square.
- **State:** *defined* = filled with the center's canonical colour; *undefined/open* =
  white fill, 2px outline in the same colour. One stroke weight everywhere (2px), one corner
  radius (2px) — consistency over ornament.
- **Channels:** straight lines snapped to fixed gate anchor points on each center's edge;
  a channel both of whose gates are active renders solid, a hanging gate renders as a short
  stub. No curves, no gradients.
- **Layout:** the standard vertical bodygraph proportions (~400×580), centers on the
  traditional grid so it reads as a Human Design chart at a glance.
- **Deliverable first:** a static mockup (SVG) for one sample chart, for approval, before any
  wiring to real gate/channel data.

## Not touched
`ids.json` UUIDs; the grammar/library side; recursive-eco (read-only). Secondary in-page
links to `grammar-viewer.html` still point at flow-relative paths — fine inside the embed,
flagged for a follow-up if the page is used standalone.
