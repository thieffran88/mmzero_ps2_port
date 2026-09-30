#ifndef MMZ_PS2_VIDEO_H
#define MMZ_PS2_VIDEO_H

#ifdef __cplusplus
extern "C" {
#endif

int mmz_video_init(void);
void mmz_video_begin(void);
void mmz_video_end(void);
void mmz_video_shutdown(void);

#ifdef __cplusplus
}
#endif

#endif
