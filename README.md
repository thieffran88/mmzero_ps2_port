# Mega Man Zero — PS2 Native Port

Independent research/port project targeting the PlayStation 2.

## Current phase

**Phase 2: asset reconnaissance + PS2 renderer foundation.**

The project has a validated GBA LZ77 extractor, diagnostic 4bpp tile renderer,
BGR555 palette candidate scanner, an asset-bank abstraction, and a gsKit-backed
PS2 video layer.

The supplied ROM is used locally for analysis. The project archive does not
need to redistribute the ROM itself.

## Build status

Host-side C syntax checks pass. A native PS2 build is not claimed yet because
PS2SDK/gsKit are not installed in the current build environment. PS2SDK and
gsKit are the intended target toolchain.

## References

See `docs/EXTERNAL_REFERENCES.md` and `docs/PHASE2.md`.
