#!/usr/bin/env python3
"""Build a deterministic four-file plugin zip."""
from pathlib import Path
import json
import zipfile
ROOT=Path(__file__).resolve().parents[1]
FILES=('manifest.json','plugin.js','index.html','icon.svg')

def build(tag: str | None = None):
    src=ROOT/'plugin'
    manifest=json.loads((src/'manifest.json').read_text())
    assert manifest['id']=='sp-today-tasks-habits'
    assert manifest['iFrame'] is True
    assert manifest['manifestVersion']==1
    if tag and tag != 'v'+manifest['version']:
        raise ValueError(f'Release tag {tag!r} does not match manifest v{manifest["version"]}')
    assert set(p.name for p in src.iterdir() if p.is_file())==set(FILES)
    dst=ROOT/'dist'/'today-plus-super-productivity.zip'
    dst.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dst,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in FILES:
            entry=zipfile.ZipInfo(f,(2026,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(entry,(src/f).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(dst) as z:
        assert z.namelist()==list(FILES) and z.testzip() is None
    print(dst)
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag', help='Optional tag to match against the plugin manifest version')
    args=parser.parse_args()
    build(args.tag)
