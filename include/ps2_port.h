#pragma once

/* Runtime-independent public interface for the PS2 port. */
void game_init(void);
void game_update(float dt);
void game_render(void);
void game_shutdown(void);
