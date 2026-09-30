#!/usr/bin/env python3
"""Find plausible 16-color GBA BGR555 palettes.

Heuristic only: candidates must contain legal 15-bit colors and enough color
variation. The result is a search aid, not a semantic classification.
"""
from __future__ import annotations
import argparse, json, struct
from pathlib import Path


def rgb555(v: int):
    return (v & 31, (v >> 5) & 31, (v >> 10) & 31)


def score(vals):
    colors = [rgb555(v) for v in vals]
    unique = len(set(colors))
    chroma = sum(max(c) - min(c) for c in colors) / 16
    nonblack = sum(c != (0, 0, 0) for c in colors)
    return unique + chroma * 0.35 + nonblack * 0.15


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", type=Path)
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--output", type=Path, default=Path("palette_candidates.json"))
    args = ap.parse_args()
    data = args.rom.read_bytes()
    hits = []
    for off in range(0, len(data) - 32, 2):
        vals = struct.unpack_from("<16H", data, off)
        # GBA palette entries use BGR555; bit 15 is unused.
        if any(v & 0x8000 for v in vals):
            continue
        s = score(vals)
        if s < 10:
            continue
        hits.append({
            "offset": off,
            "offset_hex": f"0x{off:06X}",
            "score": round(s, 3),
            "colors": [rgb555(v) for v in vals],
        })
    hits.sort(key=lambda x: x["score"], reverse=True)
    result = {"rom": str(args.rom), "candidates": hits[:args.limit]}
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"palette candidates: {len(hits)}; wrote {min(len(hits), args.limit)}")


if __name__ == "__main__":
    main()
