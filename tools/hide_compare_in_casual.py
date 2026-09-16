#!/usr/bin/env python3
from pathlib import Path

path=Path('index.html')
s=path.read_text(encoding='utf-8')
old="const applicable=presetLanguageEl.value==='ja' && ['male','female'].includes(voiceTypeEl.value) && Boolean(YK2019_DATA);"
new="const applicable=uiMode!=='casual' && presetLanguageEl.value==='ja' && ['male','female'].includes(voiceTypeEl.value) && Boolean(YK2019_DATA);"
if new in s:
    print('Casual compare already hidden; no changes.')
    raise SystemExit(0)
if s.count(old)!=1:
    raise SystemExit(f'expected 1 visibility expression, found {s.count(old)}')
s=s.replace(old,new,1)
path.write_text(s,encoding='utf-8')
print('Hidden same-vowel comparison in casual mode.')
