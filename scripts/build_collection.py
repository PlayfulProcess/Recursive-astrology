# -*- coding: utf-8 -*-
"""Build grammars/_collection.json for The Recursive Astrology — the collection-index
file the ported viewers (cards.html, explorer.html, lenses.html, tree-viewer.html,
timeline.html) read to discover every grammar in this repo, in the SAME schema
recursive-tarot/tarot/_collection.json uses (only the root path differs: grammars/
here vs tarot/ there). Port of recursive-tarot/scripts/build_tarot_collection.py +
refresh_collection.py, collapsed into one script since this repo has no separate
"migrate from source repo" step — the grammars already live in grammars/*/grammar.json.

The grammar files are the source of truth for name/type/items/cover_image_url/blurb;
this script only ADDS curation this repo doesn't otherwise have anywhere (branch
grouping + a historical year for the primary-source voice libraries that actually
have one). Unlisted / future grammars still get included automatically (glob-driven,
no hardcoded slug list to fall out of date) — they just land in the "synthesis"
branch with no year, which reads honestly as "undated / contemporary" rather than
inventing a false date.

Run from the repo root:  python3 scripts/build_collection.py
"""
import json
import os
import glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GRAMMARS_DIR = os.path.join(ROOT, "grammars")
OUT = os.path.join(GRAMMARS_DIR, "_collection.json")

REPO = "PlayfulProcess/Recursive-astrology"
BRANCH = "main"

BRANCHES = [
    ("primary-sources", "Primary Sources — the voices themselves, in translation"),
    ("synthesis",        "Synthesis — surveys, flagship interpretations, and readings"),
    ("castings",         "Castings — spread-grammars (positions, not interpretations)"),
    ("readings",         "Readings — thematic essays, not interpretation sets"),
]

# slug -> branch id. Curated by hand (mirrors tarot's DECKS dict) but NOT load-bearing:
# any grammar not listed here still appears in the collection, just in "synthesis"
# with no curated year — an honest "undated" default, never a guess.
BRANCH_OF = {
    "tetrabiblos-ashmand":            "primary-sources",
    "alan-leo":                       "primary-sources",
    "proctor-skeptical-astrology":    "primary-sources",
    "jyotisha-brihat-jataka":         "primary-sources",
    "mesopotamian-omens":             "primary-sources",
    "renaissance-lilly":              "primary-sources",
    "historiographies-of-astrology":  "synthesis",
    "western-astrology-canonical":    "synthesis",
    "planetary-myths":                "synthesis",
    "trika-lens":                     "synthesis",
    "casting-big-three":              "castings",
    "casting-single-aspect":          "castings",
    "casting-twelve-houses":          "castings",
    "the-right-size":                 "readings",
    "three-doors":                    "readings",
}

# slug -> (sortable year, display label, provenance). Only the primary-source voice
# libraries have a genuine anchor date; everything else is honestly "living" (a
# contemporary synthesis/reading/casting, not a historically dated artifact).
YEARS = {
    "mesopotamian-omens":    (-1000, "Babylonian / Assyrian omen-craft, 2nd–1st millennium BCE", "record"),
    "tetrabiblos-ashmand":   (150,   "c. 150 CE (Ptolemy) · Ashmand tr. 1822",               "record"),
    "jyotisha-brihat-jataka":(550,   "c. 6th c. CE (Varāhamihira) · 1885 tr.",           "record"),
    "renaissance-lilly":     (1647,  "1647 (William Lilly, Christian Astrology)",                 "record"),
    "proctor-skeptical-astrology": (1896, "1896", "record"),
    "alan-leo":              (1900,  "c. 1900 (Theosophical revival)",                            "record"),
}


def blurb_of(g):
    desc = (g.get("description") or "").strip().split("\n")[0]
    return (desc[:200] + "…") if len(desc) > 200 else desc


def main():
    paths = sorted(glob.glob(os.path.join(GRAMMARS_DIR, "*", "grammar.json")))
    grammars_index = []
    for path in paths:
        slug = os.path.basename(os.path.dirname(path))
        try:
            g = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            print(f"  SKIP {slug}: {e}")
            continue
        branch = BRANCH_OF.get(slug, "synthesis")
        entry = {
            "slug": slug,
            "name": g.get("name"),
            "type": g.get("grammar_type"),
            "branch": branch,
            "is_meta": False,
            "default_preview": g.get("default_preview"),
            "items": len(g.get("items", [])),
            "cover_image_url": g.get("cover_image_url"),
            "blurb": blurb_of(g),
            "path": f"grammars/{slug}/grammar.json",
            "provenance": "living",
        }
        if slug in YEARS:
            year, label, provenance = YEARS[slug]
            entry["year"] = year
            entry["year_label"] = label
            entry["provenance"] = provenance
        grammars_index.append(entry)

    branch_index = [
        {"id": bid, "name": bname,
         "deck_slugs": [e["slug"] for e in grammars_index if e["branch"] == bid]}
        for bid, bname in BRANCHES
    ]

    collection = {
        "repo": REPO,
        "branch": BRANCH,
        "github_url": f"https://github.com/{REPO}",
        "collection": "astrology",
        "name": "The Recursive Astrology",
        "version": "1.0.0",
        "license": "Mixed — see each grammar's own `license` field (public-domain source texts; original synthesis CC-BY-SA-4.0)",
        "original_creator": None,
        "creator_name": "PlayfulProcess",
        "meta_grammar": "historiographies-of-astrology",
        "branches": branch_index,
        "grammars": grammars_index,
    }
    json.dump(collection, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    n_items = sum(e["items"] for e in grammars_index)
    print(f"Wrote {OUT} — {len(grammars_index)} grammars ({n_items} items), {len(branch_index)} branches")


if __name__ == "__main__":
    main()
