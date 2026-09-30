#!/usr/bin/env python3
"""Offline probe for GBA LZ77 payloads that may contain 4bpp tile graphics.

No game-specific assumptions beyond the standard GBA 4bpp tile layout.
Outputs candidate dimensions and a grayscale contact sheet for human review.
"""
import argparse, json, math
from pathlib import Path
from PIL import Image, ImageDraw

def lz77(src):
    if len(src)<4 or src[0]!=0x10: raise ValueError('not GBA LZ77')
    want=src[1]|src[2]<<8|src[3]<<16
    out=bytearray(); i=4
    while len(out)<want:
        flags=src[i]; i+=1
        for bit in range(7,-1,-1):
            if len(out)>=want: break
            if flags&(1<<bit):
                pair=(src[i]<<8)|src[i+1]; i+=2
                n=(pair>>12)+3; d=(pair&0xfff)+1
                if d>len(out): raise ValueError('bad distance')
                for _ in range(n): out.append(out[-d])
            else:
                out.append(src[i]); i+=1
    return bytes(out)

def nibble_image(raw,wtiles):
    tiles=len(raw)//32
    htiles=max(1,math.ceil(tiles/wtiles))
    im=Image.new('L',(wtiles*8,htiles*8),0)
    px=im.load()
    for t in range(tiles):
        tx=(t%wtiles)*8; ty=(t//wtiles)*8
        base=t*32
        for y in range(8):
            for x in range(8):
                b=raw[base+y*4+x//2]
                v=(b>>4) if x&1 else (b&15)
                px[tx+x,ty+y]=v*17
    return im

def score(im):
    hist=im.histogram(); nonzero=sum(hist[1:]); total=sum(hist)
    if not total:return 0
    # Favor moderate occupancy and varied colors; reject mostly-empty noise.
    used=sum(1 for i in range(1,256) if hist[i])
    occupancy=nonzero/total
    return round(occupancy*0.55 + min(used/16,1)*0.45,4)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('bin',type=Path); ap.add_argument('-o','--out',type=Path,required=True)
    a=ap.parse_args(); raw=a.bin.read_bytes();
    # Input may already be decompressed.
    if raw[:1]==bytes([0x10]): raw=lz77(raw)
    if len(raw)%32: raise SystemExit('size is not a whole number of 4bpp tiles')
    candidates=[]
    for wt in [8,10,12,16,20,24,32,40,48,64]:
        im=nibble_image(raw,wt)
        candidates.append({'width_tiles':wt,'height_tiles':math.ceil((len(raw)//32)/wt),'score':score(im)})
    candidates.sort(key=lambda x:-x['score'])
    best=candidates[0]
    preview=nibble_image(raw,best['width_tiles']).resize((best['width_tiles']*16,best['height_tiles']*16),Image.Resampling.NEAREST)
    preview.save(a.out.with_suffix('.png'))
    a.out.write_text(json.dumps({'bytes':len(raw),'tiles':len(raw)//32,'candidates':candidates,'best':best},indent=2))
    print(json.dumps({'bytes':len(raw),'tiles':len(raw)//32,'best':best},indent=2))
if __name__=='__main__': main()
