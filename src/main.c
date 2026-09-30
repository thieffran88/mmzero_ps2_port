#include <stdio.h>
#include "ps2_port.h"

#ifdef _EE
#include <kernel.h>
#endif

int main(void) {
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
