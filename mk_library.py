#!/usr/bin/env python3
import zipfile
import os, subprocess, json
from pathlib import Path

library_zip_fn = 'dist/library.zip'
zf = zipfile.ZipFile(library_zip_fn, 'w')

os.chdir('combined_lib')
subprocess.call(['leanpkg', 'build'])
lean_p = json.loads(subprocess.check_output(['lean', '-p']))
lean_path = [Path(p).resolve() for p in lean_p["path"]]

already_seen = set()
for p in lean_path:
    for fn in p.glob('**/*.olean'):
        rel = fn.relative_to(p)
        if '_target' in rel.parts:
            continue
        elif rel in already_seen:
            print('duplicate: {0}'.format(fn))
        else:
            content = open(fn, 'rb').read()
            zf.writestr(zipfile.ZipInfo(filename=str(rel)), content)
            already_seen.add(rel)

print('Created {0} with {1} olean files'.format(library_zip_fn, len(already_seen)))

zf.close()