#!/usr/bin/env python3
from pathlib import Path

old_label='UC San Diego — Quality Factor and Bandwidth'
old_url='https://musicweb.ucsd.edu/~trsmyth/vibration/Quality_Factor_Bandwidth.html'
new_label='OpenStax University Physics — Resonance and Q'
new_url='https://openstax.org/books/university-physics-volume-2/pages/15-5-resonance-in-an-ac-circuit'

changed=[]
for filename in ['index.html','tools/expand_learning_glossary.py']:
    path=Path(filename)
    s=path.read_text(encoding='utf-8')
    original=s
    s=s.replace(old_label,new_label).replace(old_url,new_url)
    if s!=original:
        path.write_text(s,encoding='utf-8')
        changed.append(filename)
print('Updated Q source in: '+(', '.join(changed) if changed else 'nothing (already current)'))
