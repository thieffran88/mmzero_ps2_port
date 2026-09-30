#!/usr/bin/env python3
import argparse, json, struct
from pathlib import Path

def u32(b,o): return struct.unpack_from('<I',b,o)[0]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rom')
    ap.add_argument('manifest')
    ap.add_argument('-o','--out',required=True)
    a=ap.parse_args()
    rom=Path(a.rom).read_bytes()
    streams=json.loads(Path(a.manifest).read_text())['streams']
    byoff={s['offset']:s for s in streams}
    hits={s['offset']:[] for s in streams}
    generic=[]
    for o in range(0,len(rom)-3,4):
        p=u32(rom,o)
        if 0x08000000 <= p < 0x0A000000:
            target=p-0x08000000
            if target in byoff:
                hits[target].append(o)
            elif target < len(rom):
                generic.append((o,target))
    result=[]
    for off,s in byoff.items():
        result.append({**s,'pointer_refs':len(hits[off]),'ref_offsets_hex':[hex(x) for x in hits[off][:64]]})
    result.sort(key=lambda x:(-x['pointer_refs'],-x['decompressed_size']))
    Path(a.out).write_text(json.dumps({'rom_size':len(rom),'streams':result,'direct_pointer_refs':sum(x['pointer_refs'] for x in result)},indent=2))
    print('streams',len(result),'direct refs',sum(x['pointer_refs'] for x in result),'referenced streams',sum(bool(x['pointer_refs']) for x in result))
    for x in result[:30]:
        if x['pointer_refs']:
            print(x['offset_hex'],x['decompressed_size'],x['pointer_refs'],x['ref_offsets_hex'][:8])
if __name__=='__main__': main()
