# ROM analysis — Mega Man Zero

ROM analyzed: `Mega Man Zero (USA, Europe).gba`

- Size: 8,388,608 bytes (8 MiB)
- SHA-256: `cf505422d68295fba36136a49a3c9dedb104ab16aa542edaeecbb89efdd57807`
- Title: `MEGAMAN ZERO`
- Game code: `AZCE`
- Valid Nintendo GBA LZ77 streams found by full-stream validation: **849**

## Important finding

A raw search for byte `0x10` produces many false positives. The scanner in
`tools/gba_asset_scan.py` now validates the entire LZ77 stream before accepting
a candidate. This is the basis for the asset-extraction pipeline.

### Largest validated streams

| ROM offset | Decompressed | Packed | Ratio | Entropy |
|---:|---:|---:|---:|---:|
| `0x30E534` | 65,536 | 14,462 | 4.532 | 1.762 |\n| `0x311EB4` | 65,536 | 15,388 | 4.259 | 2.356 |\n| `0x317110` | 31,872 | 11,210 | 2.843 | 3.239 |\n| `0x315AD0` | 16,384 | 5,440 | 3.012 | 3.362 |\n| `0x319DFC` | 1,728 | 370 | 4.670 | 2.756 |\n| `0x72925A` | 273 | 310 | 0.881 | 0.110 |\n| `0x311DB4` | 224 | 256 | 0.875 | 6.644 |\n| `0x317010` | 224 | 256 | 0.875 | 6.899 |\n| `0x2E8A43` | 121 | 86 | 1.407 | 0.794 |\n| `0x4E5E16` | 119 | 133 | 0.895 | 0.512 |\n
These are **candidates**, not yet classified as sprites, maps, palettes or
audio. Classification requires following the game's code/data references and
testing the decompressed data against known GBA graphics structures.

## Next reverse-engineering targets

1. Identify ROM pointer tables and code references to the large streams.
2. Detect 4bpp/8bpp tile sets and 15-bit GBA palettes.
3. Recover map/tilemap formats.
4. Recover entity/sprite tables.
5. Build a small native PS2 renderer that can display one recovered asset.
6. Only then begin the gameplay-system reimplementation.

## PS2 status

The source skeleton is prepared for PS2SDK, but the current environment does
not contain a PS2SDK compiler. Therefore the project is **source-ready, not
yet PS2-binary-built**.
