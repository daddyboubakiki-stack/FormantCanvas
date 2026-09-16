#!/usr/bin/env python3
from pathlib import Path

path=Path('index.html')
s=path.read_text(encoding='utf-8')
marker='Compact glossary source dedupe v1'
if marker in s:
    print('Compact glossary source dedupe already present.')
    raise SystemExit(0)

old="""  function renderLearningSourceShort(container,item){
    if(!container) return;
    container.textContent='';
    const sources=(item && item.sources) || [];
    if(!sources.length){ container.hidden=true; return; }
    container.hidden=false;
    const prefix=document.createElement('span'); prefix.textContent='出典：'; container.appendChild(prefix);
    sources.forEach((source,index)=>{
      if(index){ const sep=document.createElement('span'); sep.className='learning-source-sep'; sep.textContent='·'; container.appendChild(sep); }
      const info=learningSourceInfo(source);
      appendLearningSourceLink(container,info,info.short);
    });
  }
"""
new="""  // Compact glossary source dedupe v1
  function renderLearningSourceShort(container,item){
    if(!container) return;
    container.textContent='';
    const sources=(item && item.sources) || [];
    if(!sources.length){ container.hidden=true; return; }
    container.hidden=false;
    const prefix=document.createElement('span'); prefix.textContent='出典：'; container.appendChild(prefix);
    const seen=new Set();
    let rendered=0;
    sources.forEach(source=>{
      const info=learningSourceInfo(source);
      if(seen.has(info.short)) return;
      seen.add(info.short);
      if(rendered){ const sep=document.createElement('span'); sep.className='learning-source-sep'; sep.textContent='·'; container.appendChild(sep); }
      appendLearningSourceLink(container,info,info.short);
      rendered++;
    });
  }
"""
if s.count(old)!=1:
    raise SystemExit(f'expected one compact source renderer, found {s.count(old)}')
s=s.replace(old,new,1)
path.write_text(s,encoding='utf-8')
print('Deduplicated compact popover source labels while preserving full lower references.')
