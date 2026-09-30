#!/usr/bin/env python3
import hashlib
import json
import struct
import sys
from pathlib import Path


def u32(b, off):
    return struct.unpack_from('<I', b, off)[0]


def main():
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} ROM.gba')
        raise SystemExit(2)

    p = Path(sys.argv[1])
    data = p.read_bytes()
    if len(data) < 0xC0:
        raise SystemExit('ROM too small for GBA header')

    report = {
        'file': str(p),
        'size': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'gba': {
            'title': data[0xA0:0xAC].decode('ascii', 'replace').rstrip('\0'),
            'game_code': data[0xAC:0xB0].decode('ascii', 'replace'),
            'maker_code': data[0xB0:0xB2].decode('ascii', 'replace'),
            'software_version': data[0xBC],
            'header_checksum': data[0xBD],
            'entry_word': u32(data, 0),
            'entry_bytes': data[:4].hex(),
        },
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
