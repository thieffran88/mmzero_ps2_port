#include <stdio.h>
#include "ps2_port.h"
#include "ps2_video.h"

#ifdef _EE
#include <kernel.h>
#endif

int main(void) {
    if (mmz_video_init() != 0) return 1;
    printf("Mega Man Zero PS2 Port - bootstrap\n");
    game_init();

    /* Placeholder loop. The next milestone replaces this with the GS/VSync loop. */
    for (int i = 0; i < 60; ++i) {
        game_update(1.0f / 60.0f);
        game_render();
    }

    game_shutdown();
    printf("bootstrap complete\n");
    return 0;
}
