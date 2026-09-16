#!/usr/bin/env python3
from pathlib import Path
import re

path=Path('index.html')
s=path.read_text(encoding='utf-8')

if 'Unified same-vowel condition row' in s:
    print('Unified same-vowel condition row already present; no changes.')
    raise SystemExit(0)

def replace_once(old,new,label):
    global s
    count=s.count(old)
    if count!=1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    s=s.replace(old,new,1)

def regex_once(pattern,repl,label,flags=re.S):
    global s
    s2,n=re.subn(pattern,repl,s,count=1,flags=flags)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    s=s2

# Marker + compact five-card row in Learning and Research modes.
replace_once('  /* Beginner vowel comparison experiment */', '  /* Beginner vowel comparison experiment */\n  /* Unified same-vowel condition row */', 'marker')
replace_once('  .compare-launch { display:flex; justify-content:center; }', '  .compare-launch { display:none; }', 'hide compare launcher')
replace_once('  .compare-tabs { display:flex; flex-wrap:wrap; gap:7px; margin-bottom:10px; }', '  .compare-tabs { display:none; }', 'hide compare tabs')
replace_once('  .compare-choices { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; }', '  .compare-choices { display:grid; grid-template-columns:repeat(5,minmax(118px,1fr)); gap:8px; overflow-x:auto; padding-bottom:3px; }', 'five-column compare grid')
replace_once('    cursor:pointer; min-height:112px; display:flex; flex-direction:column; gap:5px;', '    cursor:pointer; min-height:82px; display:flex; flex-direction:column; gap:6px; justify-content:center;', 'compact cards')
replace_once('  .compare-choice .desc { font-size:11px; line-height:1.55; color:#626d82; flex:1; }', '  .compare-choice .desc { display:none; }', 'hide descriptions')
replace_once('  body[data-ui-mode="research"] .beginner-compare { display:none !important; }', '  body[data-ui-mode="research"] .beginner-compare { display:block; }', 'show compare in research')
replace_once('    .compare-choices { grid-template-columns:1fr; }\n    .compare-choice { min-height:0; }', '    .compare-choices { grid-template-columns:repeat(5,minmax(118px,1fr)); }\n    .compare-choice { min-height:76px; }', 'mobile horizontal compare')

# Research mode keeps VV in the dropdown, but no longer repeats 20 Yazawa-Kondo conditions there.
replace_once("    if(lang==='ja' && uiMode!=='research' && oldYk) desired=oldYk.vowel;", "    if(lang==='ja' && oldYk) desired=oldYk.vowel;", 'map YK choice back to base vowel')
pattern=r"\n    if\(researchJapanese && YK2019_DATA && \['male','female'\]\.includes\(voiceTypeEl\.value\)\)\{.*?\n    \}\n    vowelPresetEl\.value=all\.includes\(desired\)\?desired:data\.mono\[0\]\[0\];"
repl="\n    // Yazawa-Kondo same-vowel conditions live in the comparison row, not the dropdown.\n    vowelPresetEl.value=all.includes(desired)?desired:data.mono[0][0];"
regex_once(pattern,repl,'remove YK optgroups')

# Replace the two-theme teaching cards with one concise row of all five conditions.
pattern=r"  function compareChoiceCard\(key,kicker,title,desc,metric\)\{.*?\n  \}\n\n  function renderBeginnerCompare\(\)\{.*?\n  \}\n\n  function updateBeginnerCompareVisibility\(\)\{.*?\n  \}"
repl=r'''  function compareChoiceCard(key,title,metric){
    const active=compareCurrentKey===key ? ' active' : '';
    return `<button class="compare-choice${active}" type="button" data-compare-key="${key}"><strong>${title}</strong><span class="metric">${metric}</span><span class="listen">▶ 聴く</span></button>`;
  }

  function renderBeginnerCompare(){
    if(!beginnerCompareWrap || beginnerCompareWrap.hidden || !YK2019_DATA) return;
    compareBaseVowel=currentCompareVowel();
    const v=compareBaseVowel, kana=BASIC_JA_KANA[v];
    compareTitle.textContent=`「${kana}」の条件を聴き比べ`;
    compareIntro.textContent='同じ母音のまま、発話条件だけを切り替えます。カードを押すとその条件をすぐ再生します。';

    const isolatedShort=compareYkPreset(v,'isolated_word','short');
    const isolatedLong=compareYkPreset(v,'isolated_word','long');
    const sentenceShort=compareYkPreset(v,'carrier_sentence','short');
    const sentenceLong=compareYkPreset(v,'carrier_sentence','long');
    compareChoices.innerHTML=[
      compareChoiceCard(v,'持続','Kasuya 1968 · 静的平均'),
      isolatedShort ? compareChoiceCard(isolatedShort.id,'単独語・短',compareDurationLabel(isolatedShort)) : '',
      isolatedLong ? compareChoiceCard(isolatedLong.id,'単独語・長',compareDurationLabel(isolatedLong)) : '',
      sentenceShort ? compareChoiceCard(sentenceShort.id,'文中・短',compareDurationLabel(sentenceShort)) : '',
      sentenceLong ? compareChoiceCard(sentenceLong.id,'文中・長',compareDurationLabel(sentenceLong)) : ''
    ].join('');

    compareChoices.querySelectorAll('[data-compare-key]').forEach(btn=>btn.addEventListener('click',()=>{
      const key=btn.dataset.compareKey;
      compareCurrentKey=key;
      stop();
      applyPreset('ja',key);
      renderBeginnerCompare();
      transportBtn.click();
    }));
  }

  function updateBeginnerCompareVisibility(){
    if(!beginnerCompareWrap) return;
    const applicable=uiMode!=='casual' && presetLanguageEl.value==='ja' && ['male','female'].includes(voiceTypeEl.value) && Boolean(YK2019_DATA);
    beginnerCompareWrap.hidden=!applicable;
    if(!applicable){
      comparePanel.hidden=true;
      return;
    }
    compareOpen=true;
    compareBaseVowel=currentCompareVowel();
    comparePanel.hidden=false;
    compareToggleBtn.setAttribute('aria-expanded','true');
    renderBeginnerCompare();
  }'''
regex_once(pattern,repl,'replace comparison logic')

# Comparison theme buttons are gone conceptually; leave hidden DOM but remove their behavior.
pattern=r"\n  document\.querySelectorAll\('\[data-compare-theme\]'\)\.forEach\(btn=>btn\.addEventListener\('click',\(\)=>\{.*?\n  \}\)\);"
regex_once(pattern,'','remove theme listener')

# Cleaner explanatory copy in the panel.
replace_once('<p>選択肢を覚えなくてOK。違いが出やすい組み合わせだけ並べます。</p>', '<p>同じ母音を、条件だけ変えてワンタップで比較できます。</p>', 'panel subtitle')
replace_once('<p class="compare-note">※ これは「聞き分けテスト」ではありません。小さい差は耳だけで分かりにくいので、グラフの動きや再生時間も一緒に見てみよう。</p>', '<p class="compare-note">※ 小さい差は耳だけでは分かりにくいことがあります。必要ならグラフと実測durationも一緒に確認できます。</p>', 'panel note')

path.write_text(s,encoding='utf-8')
print('Unified same-vowel condition row added for Learning and Research modes.')
