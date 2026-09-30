#include "ps2_port.h"

/* First milestone: a deliberately small runtime shell.
 * Game logic will be filled after the ROM data formats are mapped. */

static unsigned long frame_count;

void game_init(void) {
    frame_count = 0;
}

void game_update(float dt) {
    (void)dt;
    ++frame_count;
}

void game_render(void) {
    /* Renderer comes next: GS setup, framebuffer, 2D batcher and sprites. */
}

void game_shutdown(void) {
}
