#!/usr/bin/python3
# coding: utf-8 

from __future__ import unicode_literals

"""
    Smartly - Digital et Data : Snips Parse Service (REST API)
    -----------------------------------------------------------
    
    This module link Smartly language resource repository to Snips resource data.
    
    :author: MTE
    :copyright: © 2021 by Smartly and OBS D&D
    :license: Smartly and D&D, all rights reserved
"""

__version__ =  '0.0'


from pathlib import Path
import shutil
import importlib

# get current languages resources
current_path = Path(__file__).parent
resources = [x for x in current_path.glob('*') if not str(x).startswith('b')]

# Find Snips package name and path
name = 'snips-nlu'.replace("-", "_")
pkg  = importlib.import_module(name)
pkg_name = Path(pkg.__file__).parent
resource_langs = pkg_name / "data"

# Symlink language to resource data
for lang in resources:
    if lang.is_dir() and not str(lang).startswith('.'):
        dest_pkg_lang = resource_langs / lang.name
        try: 
            lang.symlink_to(dest_pkg_lang)
            print(f"Successfully symlink resource: {lang} --> {dest_pkg_lang} ")
        except Exception as e: print(str(e))
        