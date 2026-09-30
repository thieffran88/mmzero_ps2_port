#include "asset_bank.h"

void mmz_asset_bank_init(void) {
    /* Phase 2: runtime asset registry. */
}

int mmz_asset_decode_gba_lz77(const uint8_t *src, uint32_t src_size,
                               uint8_t *dst, uint32_t dst_capacity,
                               uint32_t *dst_size) {
    /* Runtime decoder is intentionally separate from the offline scanner.
       The PS2 port should normally use pre-converted assets for speed. */
    if (!src || !dst || !dst_size || src_size < 4 || src[0] != 0x10)
        return -1;

    uint32_t want = src[1] | ((uint32_t)src[2] << 8) |
                    ((uint32_t)src[3] << 16);
    if (!want || want > dst_capacity)
        return -2;

    uint32_t si = 4, di = 0;
    while (di < want) {
        if (si >= src_size) return -3;
        uint8_t flags = src[si++];
        for (int bit = 7; bit >= 0 && di < want; --bit) {
            if (flags & (1u << bit)) {
                if (si + 1 >= src_size) return -4;
                uint16_t pair = ((uint16_t)src[si] << 8) | src[si + 1];
                si += 2;
                uint32_t len = (pair >> 12) + 3;
                uint32_t disp = (pair & 0x0FFF) + 1;
                if (disp > di || di + len > want) return -5;
                while (len--) {
                    dst[di] = dst[di - disp];
                    ++di;
                }
            } else {
                if (si >= src_size) return -6;
                dst[di++] = src[si++];
            }
        }
    }
    *dst_size = di;
    return 0;
}
