#!/usr/bin/env python3
from pathlib import Path

path=Path('index.html')
s=path.read_text(encoding='utf-8')

old_duration='<input id="duration" type="range" min="0.15" max="8" step="0.001" value="0.600" />'
new_duration='<input id="duration" type="range" min="0.04" max="8" step="0.001" value="0.600" />'
if old_duration in s:
    s=s.replace(old_duration,new_duration,1)
elif new_duration not in s:
    raise SystemExit('duration slider signature not found')

hara='<li>Hara, I. (2016). <em>An acoustic analysis of vowel sequences in Japanese</em> [Doctoral dissertation, Newcastle University]. <a href="http://hdl.handle.net/10443/3420" target="_blank" rel="noreferrer">Newcastle eTheses</a></li>'
yk='<li>Yazawa, K., &amp; Kondo, M. (2019). Acoustic characteristics of Japanese short and long vowels: Formant displacement effect revisited. <em>Proceedings of ICPhS 2019</em>. Formantasiaの成人短長母音プリセットは、公開された Japanese Vowel Length Acoustic Data v3 の条件別派生平均を使用。 <a href="https://zenodo.org/records/15227304" target="_blank" rel="noreferrer">Zenodo dataset</a></li>'
if yk not in s:
    if hara not in s:
        raise SystemExit('reference insertion anchor not found')
    s=s.replace(hara,yk+'\n      '+hara,1)

loader_signature="  render();\n  loadYazawaKondoData();\n})();"
if loader_signature not in s:
    raise SystemExit('Yazawa-Kondo loader is not inside the app IIFE')

path.write_text(s,encoding='utf-8')
print('Finalized Yazawa-Kondo UI: short-duration support, reference, loader-scope assertion')
