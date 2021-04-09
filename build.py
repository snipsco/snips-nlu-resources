

import os
from pathlib import Path
import shutil

current_path = Path(__file__).parent
bundles = current_path / "bundles"
resources = [x for x in current_path.glob('*') if not str(x).startswith('b')]
bundles = bundles.glob('*')

for r in bundles:
    form = str(r).split('snips_nlu_')[1].split('-')
    lang = form[0]
    vers = form[1]
    for x in resources:
        if str(x) in str(lang):
            print(x, r)
            filer = Path(f"{str(r)}/snips_nlu_{lang}/snips_nlu_{lang}-{vers}")
            for v in x.glob('*'):
                dest = filer / v.name
                if v.is_dir():
                    try: shutil.copytree(v, dest, symlinks=True)
                    except Exception as e: print(str(e))
                else: 
                    try: shutil.copy2(v, dest, follow_symlinks=True)
                    except Exception as e: print(str(e))
