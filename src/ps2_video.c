#include "ps2_video.h"

/* PS2 target renderer. Requires PS2SDK + gsKit. */
#ifdef MMZ_PS2_TARGET
#include <gsKit.h>
#include <dmaKit.h>
#include <tamtypes.h>

static GSGLOBAL *s_gs;

int mmz_video_init(void) {
    s_gs = gsKit_init_global();
    if (!s_gs) return -1;
    s_gs->Interlace = GS_NONINTERLACED;
    s_gs->Field = GS_FRAME;
    s_gs->Width = 640;
    s_gs->Height = 448;
    s_gs->PSM = GS_PSM_CT32;
    s_gs->PSMZ = GS_PSMZ_16S;
    s_gs->ZBuffering = GS_SETTING_OFF;
    s_gs->DoubleBuffering = GS_SETTING_ON;
    dmaKit_init(D_CTRL_RELE_OFF, D_CTRL_MFD_OFF, D_CTRL_STS_UNSPEC,
                D_CTRL_STD_OFF, D_CTRL_RCYC_8, 1 << DMA_CHANNEL_GIF);
    dmaKit_chan_init(DMA_CHANNEL_GIF);
    gsKit_init_screen(s_gs);
    gsKit_mode_switch(s_gs, GS_ONESHOT);
    return 0;
}

void mmz_video_begin(void) { if (s_gs) gsKit_clear(s_gs, GS_SETREG_RGBAQ(0,0,0,0,0)); }
void mmz_video_end(void) { if (s_gs) { gsKit_queue_exec(s_gs); gsKit_sync_flip(s_gs); } }
void mmz_video_shutdown(void) { s_gs = 0; }

#else
int mmz_video_init(void) { return 0; }
void mmz_video_begin(void) {}
void mmz_video_end(void) {}
void mmz_video_shutdown(void) {}
#endif
