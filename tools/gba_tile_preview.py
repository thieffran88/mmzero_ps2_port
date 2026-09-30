#!/usr/bin/env python3
"""Render GBA 4bpp tile data into a diagnostic PNG.

This tool intentionally does not assume a game-specific map format. It is for
visual triage of extracted ROM assets.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image


def render_4bpp(data: bytes, tiles: int, cols: int) -> Image.Image:
    tiles = min(tiles, len(data) // 32)
    rows = (tiles + cols - 1) // cols
    out = Image.new("RGBA", (cols * 8, rows * 8), (0, 0, 0, 255))
    px = out.load()
    for ti in range(tiles):
        base = ti * 32
        x0 = (ti % cols) * 8
        y0 = (ti // cols) * 8
        for y in range(8):
            for x in range(8):
                q = data[base + y * 4 + x // 2]
                idx = (q >> (4 * (x & 1))) & 0xF
                v = idx * 17
                px[x0 + x, y0 + y] = (v, v, v, 255 if idx else 0)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--tiles", type=int, default=512)
    ap.add_argument("--cols", type=int, default=16)
    args = ap.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    render_4bpp(args.input.read_bytes(), args.tiles, args.cols).save(args.output)


if __name__ == "__main__":
    main()
