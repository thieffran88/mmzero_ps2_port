# Phase 3 — ROM reference graph + asset pipeline

## Goal

Turn the broad LZ77 scan into a reproducible asset pipeline and remove an important decoder edge case before PS2 integration.

## Results

- The supplied ROM SHA-1 is `193b14120119162518a73c70876f0b8bffdbd96e`, matching the public Mega Man Zero USA revision-0 reference project.
- 849 LZ77 streams were validated against the ROM.
- Only 9 streams are exactly tile-aligned to 32-byte GBA 4bpp tiles; the five largest are 64 KiB, 64 KiB, 31,872 bytes, 16 KiB and 1,728 bytes.
- A direct 32-bit ROM-pointer graph currently reaches 26 of the 849 streams. The largest graphics candidates are not referenced by simple literal pointers, so the next pass must recover table/base-address construction rather than assuming every asset has a direct pointer.
- Added `pointer_graph.py` to record direct references.
- Added `asset_probe.py` to test 4bpp tile layouts and produce reviewable previews.
- Added `verify_lz77.py` and a host C test for the runtime decoder.

## Decoder correction

The original GBA LZ77 decoder rejected a valid stream when the final back-reference produced more bytes than the declared output size. GBA decoders must clamp the final copy to the requested output length. The PS2 runtime decoder now performs that clamp.

The corrected implementation was tested against all 849 discovered streams; all extracted payloads match the ROM-derived reference data through the declared output length.

## PS2 direction

The renderer remains based on PS2SDK + gsKit. gsKit exposes low-level access to the PS2 Graphics Synthesizer and supports texture handling, primitives, VSync and double buffering, which fits the planned 2D renderer. The current environment does not contain PS2SDK, so no ELF/ISO build is claimed yet.

## Next engineering target

1. Recover the data tables that construct addresses for the large graphics streams.
2. Identify one complete graphics asset: compressed payload + palette + dimensions + tilemap.
3. Convert it offline into a PS2-friendly texture/CLUT asset.
4. Upload that asset through gsKit and render a first authentic game-derived scene.
5. Only then begin replacing GBA PPU concepts with the PS2 scene renderer.
