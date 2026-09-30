#pragma once
#include <stdint.h>

typedef struct {
    const uint8_t *data;
    uint32_t size;
    uint16_t width;
    uint16_t height;
    uint8_t bpp;
} MMZ_Asset;

void mmz_asset_bank_init(void);
int  mmz_asset_decode_gba_lz77(const uint8_t *src, uint32_t src_size,
                               uint8_t *dst, uint32_t dst_capacity,
                               uint32_t *dst_size);
