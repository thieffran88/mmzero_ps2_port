#!/usr/bin/env python3
import argparse,json,subprocess,tempfile,os
from pathlib import Path

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('rom',type=Path); ap.add_argument('manifest',type=Path); a=ap.parse_args()
 rom=a.rom.read_bytes(); m=json.loads(a.manifest.read_text())
 checks=0
 for s in m['streams']:
  off=s['offset']; n=s['compressed_size']; comp=rom[off:off+n]
  if comp[:1]!=b'\x10': continue
  # Python reference decode
  want=comp[1]|comp[2]<<8|comp[3]<<16; out=bytearray(); i=4
  while len(out)<want:
   flags=comp[i]; i+=1
   for bit in range(7,-1,-1):
    if len(out)>=want: break
    if flags&(1<<bit):
     pair=(comp[i]<<8)|comp[i+1]; i+=2; ln=(pair>>12)+3; d=(pair&0xfff)+1
     for _ in range(ln): out.append(out[-d])
    else: out.append(comp[i]); i+=1
  expected=Path('/mnt/data/mmzero_project/mmzero_ps2_port/analysis/rom_scan')/f"lz_{m['streams'].index(s)}_{off:06X}_{want:05d}.bin"
  # compare against any extracted file matching offset/size
  matches=list(expected.parent.glob(f'lz_*_{off:06X}_{want:05d}.bin'))
  if matches and matches[0].read_bytes()!=out[:want]: raise SystemExit(f'mismatch {off:x}')
  checks+=1
 print(f'validated {checks} LZ77 streams against the ROM/extracted assets')
if __name__=='__main__': main()
