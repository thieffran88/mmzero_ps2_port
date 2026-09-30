# Phase 2 — asset reconnaissance and PS2 renderer foundation

## New results

The ROM analysis pipeline now has three independent layers:

1. **LZ77 validation/extraction** — identifies complete GBA 0x10 streams.
2. **4bpp tile preview** — converts candidate decompressed data into 8x8 GBA tile sheets for visual triage.
3. **BGR555 palette scanner** — finds plausible 16-color palette windows without claiming semantic ownership.

The project also gained a PS2 video abstraction backed by **gsKit** when `MMZ_PS2_TARGET` is defined. The target is deliberately kept behind one small interface so the game layer is not coupled to GS registers.

## Important discovery

A public Mega Man Zero recompilation project now exists and identifies the USA revision 0 ROM by SHA-1 `193b14120119162518a73c70876f0b8bffdbd96e`. It reports a static-first recompilation with 10,885 ARM/Thumb functions and a working opening-mission path. We should treat it as a reverse-engineering reference, not as a dependency of this PS2 project.

Reference: https://github.com/mstan/MegaManZeroRecomp

This can dramatically reduce the amount of blind ROM archaeology needed for function boundaries and control-flow understanding, while the PS2 project remains an independent native implementation.

## PS2 graphics direction

The PS2 Graphics Synthesizer is well suited to the game's 2D presentation. gsKit exposes texture upload, CLUT/T8 textures, sprite primitives, VSync and double buffering. The initial renderer uses a 640x448 non-interlaced target and keeps the game's logical coordinate system separate; a later presentation layer can map the original 240x160 viewport to 2x, 3x or widescreen-safe output.

Reference: https://github.com/ps2dev/gsKit

## Next concrete milestone

Build an asset catalog that links:

`ROM pointer -> compressed stream -> decompressed bytes -> palette -> tile set -> tilemap -> scene`

Once one chain is proven, it becomes the template for the remaining stages.
