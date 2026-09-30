#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "../include/asset_bank.h"
int main(int argc,char **argv){
 if(argc!=3){fprintf(stderr,"usage: %s compressed.bin output.bin\n",argv[0]);return 2;}
 FILE *f=fopen(argv[1],"rb"); if(!f)return 3; fseek(f,0,SEEK_END); long n=ftell(f); rewind(f);
 uint8_t *src=malloc((size_t)n); if(!src)return 4; fread(src,1,(size_t)n,f); fclose(f);
 uint32_t cap=src[1]|((uint32_t)src[2]<<8)|((uint32_t)src[3]<<16); uint8_t *dst=malloc(cap); uint32_t out=0;
 int rc=mmz_asset_decode_gba_lz77(src,(uint32_t)n,dst,cap,&out); printf("rc=%d out=%u cap=%u\n",rc,out,cap);
 free(src); free(dst); return rc?1:0;
}
