# -*- coding: utf-8 -*-
"""Derive _collection.json from grammars/*/grammar.json — the index channels.html reads.
The grammars are the source of truth; this only extracts card-level facts (name,
description first sentence, item count, category mix). Idempotent; run after any
grammar change:  python scripts/build_collection.py
(Astrology port of recursive-tarot's refresh_collection.py, slimmed to what the
channels page needs.)"""
import json
import io
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "_collection.json")


def main():
    entries = []
    gdir = os.path.join(ROOT, "grammars")
    for slug in sorted(os.listdir(gdir)):
        p = os.path.join(gdir, slug, "grammar.json")
        if not os.path.isfile(p):
            continue
        g = json.load(io.open(p, encoding="utf-8"))
        items = g.get("items", [])
        cats = {}
        for i in items:
            c = i.get("category", "item")
            cats[c] = cats.get(c, 0) + 1
        entries.append({
            "slug": slug,
            "name": g.get("name", slug),
            "description": (g.get("description") or "").split(". ")[0][:220],
            "grammar_type": g.get("grammar_type", "custom"),
            "items": len(items),
            "categories": cats,
        })
    col = {
        "repo": "PlayfulProcess/Recursive-astrology",
        "channel": "astrology",
        "_note": "Derived index for channels.html — regenerate with scripts/build_collection.py; never hand-edit.",
        "grammars": entries,
    }
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(col, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote _collection.json — {len(entries)} grammars")


if __name__ == "__main__":
    main()
