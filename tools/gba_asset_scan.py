#!/usr/bin/env python3
"""Scan a GBA ROM for valid Nintendo LZ77 (0x10) streams.

Usage:
  python3 gba_asset_scan.py ROM.gba [output_dir]

The scanner validates the complete stream before reporting it, avoiding the
large number of false positives produced by blindly searching for byte 0x10.
"""
from __future__ import annotations
import hashlib, json, math, sys
from collections import Counter
from pathlib import Path

def lz77(data: bytes, off: int):
    if off + 4 > len(data) or data[off] != 0x10:
        return None
    size = data[off+1] | (data[off+2] << 8) | (data[off+3] << 16)
    if size == 0 or size > 0x400000:
        return None
    pos, out = off + 4, bytearray()
    while len(out) < size:
        if pos >= len(data):
            return None
        flags = data[pos]; pos += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                if pos + 1 >= len(data):
                    return None
                x = (data[pos] << 8) | data[pos+1]; pos += 2
                length = (x >> 12) + 3
                distance = (x & 0xFFF) + 1
                if distance > len(out):
                    return None
                for _ in range(length):
                    out.append(out[-distance])
                    if len(out) >= size:
                        break
            else:
                if pos >= len(data):
                    return None
                out.append(data[pos]); pos += 1
    return bytes(out), pos - off

def entropy(data: bytes) -> float:
    if not data: return 0.0
    n = len(data)
    return -sum((c/n) * math.log2(c/n) for c in Counter(data).values())

def likely_4bpp_tile_data(raw: bytes) -> bool:
    # A weak heuristic only: 32-byte alignment and a nontrivial number of
    # repeated 8x8 tiles. It is not used to classify assets as fact.
    if len(raw) < 32 or len(raw) % 32:
        return False
    tiles = [raw[i:i+32] for i in range(0, len(raw), 32)]
    unique = len({t for t in tiles})
    return unique < len(tiles) * 0.9

def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: gba_asset_scan.py ROM.gba [output_dir]")
    rom = Path(sys.argv[1]); data = rom.read_bytes()
    outdir = Path(sys.argv[2]) if len(sys.argv) == 3 else rom.with_suffix("")
    outdir.mkdir(parents=True, exist_ok=True)

    hits = []
    for off in range(0x200, len(data) - 4):
        if data[off] != 0x10:
            continue
        r = lz77(data, off)
        if not r:
            continue
        raw, used = r
        hits.append({
            "offset": off,
            "offset_hex": f"0x{off:06X}",
            "decompressed_size": len(raw),
            "compressed_size": used,
            "ratio": round(len(raw)/used, 3),
            "entropy": round(entropy(raw), 3),
            "aligned_32": len(raw) % 32 == 0,
            "possible_4bpp_tiles": likely_4bpp_tile_data(raw),
        })

    # Keep exact offsets unique and sort by ROM location.
    hits.sort(key=lambda x: x["offset"])
    manifest = {
        "rom": str(rom),
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "title": data[0xA0:0xAC].decode("ascii", "replace").rstrip("\0"),
        "game_code": data[0xAC:0xB0].decode("ascii", "replace"),
        "valid_lz77_streams": len(hits),
        "streams": hits,
    }
    (outdir / "lz77_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    # Extract only substantial streams, making later visual inspection easier.
    extracted = []
    for idx, h in enumerate(hits):
        if h["decompressed_size"] < 1024:
            continue
        raw, used = lz77(data, h["offset"])
        name = f"lz_{idx:03d}_{h['offset']:06X}_{len(raw):05d}.bin"
        (outdir / name).write_bytes(raw)
        extracted.append(name)
    (outdir / "extracted_large.json").write_text(
        json.dumps(extracted, indent=2), encoding="utf-8"
    )

    print(f"ROM: {rom}")
    print(f"Valid LZ77 streams: {len(hits)}")
    print("Largest streams:")
    for h in sorted(hits, key=lambda x: x["decompressed_size"], reverse=True)[:12]:
        print("  {offset_hex} -> {decompressed_size} bytes "
              "(packed {compressed_size}, ratio {ratio}, entropy {entropy})"
              .format(**h))
    print(f"Manifest: {outdir / 'lz77_manifest.json'}")
    print(f"Large extractions: {len(extracted)}")

if __name__ == "__main__":
    main()
