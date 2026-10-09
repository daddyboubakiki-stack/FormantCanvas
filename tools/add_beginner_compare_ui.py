#!/usr/bin/env python3
from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

if 'id="beginnerCompareWrap"' in s:
    print('Beginner compare UI already present; no changes.')
    raise SystemExit(0)

def replace_once(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, found {count}')
    s = s.replace(old, new, 1)

# 1) Styles: lightweight experiment card that stays out of Research mode.
css_marker = '  @media (max-width: 820px) {'
css = r'''  /* Beginner vowel comparison experiment */
  .beginner-compare { margin:10px 0 14px; }
  .compare-launch { display:flex; justify-content:center; }
  .compare-toggle {
    border:1px solid #d8dff0; background:#fff; color:var(--text); border-radius:999px;
    padding:9px 15px; font-weight:800; cursor:pointer; box-shadow:0 4px 14px rgba(34,53,94,.08);
  }
  .compare-toggle:hover { transform:translateY(-1px); }
  .compare-panel {
    margin-top:9px; border:1px solid #dfe5f2; background:linear-gradient(180deg,#fff,#f8faff);
    border-radius:18px; padding:14px; box-shadow:0 8px 24px rgba(34,53,94,.08);
  }
  .compare-head { display:flex; justify-content:space-between; gap:12px; align-items:flex-start; margin-bottom:10px; }
  .compare-head strong { font-size:15px; }
  .compare-head p { margin:3px 0 0; color:var(--muted); font-size:12px; line-height:1.55; }
  .compare-tabs { display:flex; flex-wrap:wrap; gap:7px; margin-bottom:10px; }
  .compare-tab { border:1px solid #d8dff0; background:#fff; border-radius:999px; padding:7px 11px; font-weight:800; cursor:pointer; }
  .compare-tab.active { background:#202b45; border-color:#202b45; color:#fff; }
  .compare-intro { margin:0 0 10px; font-size:12px; line-height:1.65; color:#505b72; }
  .compare-choices { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; }
  .compare-choice {
    text-align:left; border:1px solid #dce3f1; background:#fff; border-radius:14px; padding:11px;
    cursor:pointer; min-height:112px; display:flex; flex-direction:column; gap:5px;
  }
  .compare-choice:hover { border-color:#aebbd8; transform:translateY(-1px); }
  .compare-choice.active { outline:2px solid #6a7fae; border-color:#6a7fae; background:#f6f8ff; }
  .compare-choice .kicker { font-size:10px; font-weight:900; color:#778198; letter-spacing:.03em; }
  .compare-choice strong { font-size:14px; }
  .compare-choice .desc { font-size:11px; line-height:1.55; color:#626d82; flex:1; }
  .compare-choice .metric { font-size:11px; font-weight:800; color:#34415f; }
  .compare-choice .listen { font-size:11px; font-weight:900; color:#536b9e; }
  .compare-note { margin:9px 0 0; font-size:10.5px; line-height:1.55; color:#7a8497; }
  body[data-ui-mode="research"] .beginner-compare { display:none !important; }

  @media (max-width: 720px) {
    .compare-choices { grid-template-columns:1fr; }
    .compare-choice { min-height:0; }
  }

''' + css_marker
replace_once(css_marker, css, 'insert compare CSS')

# 2) Compare launcher/panel just below the existing four-column selector.
html_marker = '''  </div>\n\n  <div class="canvas-card">'''
html = r'''  </div>

  <section class="beginner-compare" id="beginnerCompareWrap" hidden aria-label="同じ母音のくらべ聴き">
    <div class="compare-launch">
      <button class="compare-toggle" id="compareToggleBtn" type="button" aria-expanded="false">🔬 同じ母音をくらべてみる</button>
    </div>
    <div class="compare-panel" id="comparePanel" hidden>
      <div class="compare-head">
        <div>
          <strong id="compareTitle">同じ母音をくらべてみよう</strong>
          <p>選択肢を覚えなくてOK。違いが出やすい組み合わせだけ並べます。</p>
        </div>
      </div>
      <div class="compare-tabs" role="group" aria-label="比較テーマ">
        <button class="compare-tab active" type="button" data-compare-theme="context">どこで言う？</button>
        <button class="compare-tab" type="button" data-compare-theme="length">短い？長い？</button>
      </div>
      <p class="compare-intro" id="compareIntro"></p>
      <div class="compare-choices" id="compareChoices"></div>
      <p class="compare-note">※ これは「聞き分けテスト」ではありません。小さい差は耳だけで分かりにくいので、グラフの動きや再生時間も一緒に見てみよう。</p>
    </div>
  </section>

  <div class="canvas-card">'''
replace_once(html_marker, html, 'insert compare panel')

# 3) DOM refs and state.
refs_marker = "  const researchModeBtn = document.getElementById('researchModeBtn');\n"
refs = refs_marker + r'''  const beginnerCompareWrap = document.getElementById('beginnerCompareWrap');
  const compareToggleBtn = document.getElementById('compareToggleBtn');
  const comparePanel = document.getElementById('comparePanel');
  const compareTitle = document.getElementById('compareTitle');
  const compareIntro = document.getElementById('compareIntro');
  const compareChoices = document.getElementById('compareChoices');
'''
replace_once(refs_marker, refs, 'insert compare refs')

state_marker = "  let uiMode = 'casual';\n"
state = state_marker + "  let compareTheme = 'context';\n  let compareOpen = false;\n  let compareBaseVowel = 'a';\n  let compareCurrentKey = null;\n"
replace_once(state_marker, state, 'insert compare state')

# 4) After dataset load, refresh both menu and beginner compare surface.
old = "      if(presetLanguageEl.value==='ja') buildPresetOptions(vowelPresetEl.value);"
new = "      if(presetLanguageEl.value==='ja') buildPresetOptions(vowelPresetEl.value);\n      updateBeginnerCompareVisibility();"
replace_once(old, new, 'refresh compare after YK load')

# 5) Beginner modes show only the basic five Japanese vowels; Research keeps everything.
old = """    const oldYk=YK2019_PRESETS.get(desired);\n    if(oldYk && oldYk.sex!==voiceTypeEl.value){\n      const translated=ykMatchingPreset(oldYk,voiceTypeEl.value);\n      if(translated) desired=translated.id;\n    }\n    vowelPresetEl.innerHTML='';"""
new = """    const oldYk=YK2019_PRESETS.get(desired);\n    if(oldYk && oldYk.sex!==voiceTypeEl.value){\n      const translated=ykMatchingPreset(oldYk,voiceTypeEl.value);\n      if(translated) desired=translated.id;\n    }\n    if(lang==='ja' && uiMode!=='research' && oldYk) desired=oldYk.vowel;\n    vowelPresetEl.innerHTML='';"""
replace_once(old, new, 'preserve base vowel outside research')

old = """    vowelPresetEl.append(mono,diph);\n    const all=[...data.mono,...data.diph].map(x=>x[0]);\n\n    if(lang==='ja' && YK2019_DATA && ['male','female'].includes(voiceTypeEl.value)){"""
new = """    const researchJapanese=lang==='ja' && uiMode==='research';\n    if(lang==='ja' && !researchJapanese) vowelPresetEl.append(mono);\n    else vowelPresetEl.append(mono,diph);\n    const all=(lang==='ja' && !researchJapanese ? data.mono : [...data.mono,...data.diph]).map(x=>x[0]);\n\n    if(researchJapanese && YK2019_DATA && ['male','female'].includes(voiceTypeEl.value)){"""
replace_once(old, new, 'simplify beginner Japanese menu')

# 6) Beginner compare logic. Buttons apply + immediately play from the same user gesture.
logic_marker = "  const EVIDENCE_LABELS = {"
logic = r'''  const BASIC_JA_VOWELS=['i','e','a','o','u'];
  const BASIC_JA_KANA={i:'い',e:'え',a:'あ',o:'お',u:'う'};

  function compareYkPreset(vowel,context,length){
    if(!YK2019_DATA) return null;
    return YK2019_DATA.presets.find(p=>p.sex===voiceTypeEl.value && p.vowel===vowel && p.context_label===context && p.length===length) || null;
  }

  function currentCompareVowel(){
    const selected=vowelPresetEl.value;
    if(BASIC_JA_VOWELS.includes(selected)) return selected;
    const yk=YK2019_PRESETS.get(selected);
    if(yk) return yk.vowel;
    return BASIC_JA_VOWELS.includes(compareBaseVowel)?compareBaseVowel:'a';
  }

  function compareDurationLabel(preset){
    return preset ? `${Math.round(preset.duration_ms.mean)} ms` : '—';
  }

  function compareChoiceCard(key,kicker,title,desc,metric){
    const active=compareCurrentKey===key ? ' active' : '';
    return `<button class="compare-choice${active}" type="button" data-compare-key="${key}"><span class="kicker">${kicker}</span><strong>${title}</strong><span class="desc">${desc}</span><span class="metric">${metric}</span><span class="listen">▶ 聴く</span></button>`;
  }

  function renderBeginnerCompare(){
    if(!beginnerCompareWrap || beginnerCompareWrap.hidden || !YK2019_DATA) return;
    compareBaseVowel=currentCompareVowel();
    const v=compareBaseVowel, kana=BASIC_JA_KANA[v];
    compareTitle.textContent=`「${kana}」をくらべてみよう`;
    document.querySelectorAll('[data-compare-theme]').forEach(btn=>btn.classList.toggle('active',btn.dataset.compareTheme===compareTheme));

    if(compareTheme==='length'){
      const shortP=compareYkPreset(v,'isolated_word','short');
      const longP=compareYkPreset(v,'isolated_word','long');
      const ratio=shortP && longP ? longP.duration_ms.mean/shortP.duration_ms.mean : null;
      compareIntro.textContent=ratio
        ? `まず一番わかりやすいのは長さ。単独語では長母音が短母音の約${ratio.toFixed(1)}倍です。フォルマントの位置も少し変わります。`
        : '短母音と長母音を、同じ話者・同じ母音で比べます。';
      compareChoices.innerHTML=[
        shortP ? compareChoiceCard(shortP.id,'SHORT',`短く「${kana}」`,'単語の中で短く発音した母音。動く時間が短いぶん、目標の形に届ききらないことがあります。',`実測平均 ${compareDurationLabel(shortP)}`) : '',
        longP ? compareChoiceCard(longP.id,'LONG',`長く「${kana}ー」`,'同じ単語条件の長母音。まず再生時間の差を聴き、そのあと線の位置も見てみよう。',`実測平均 ${compareDurationLabel(longP)}`) : ''
      ].join('');
    } else {
      const isolated=compareYkPreset(v,'isolated_word','short');
      const carrier=compareYkPreset(v,'carrier_sentence','short');
      compareIntro.textContent='同じ母音でも、単独でじっくり言うとき・単語の中・文の流れの中では少し形が変わります。耳だけでなく線も一緒に見るのがおすすめ。';
      compareChoices.innerHTML=[
        compareChoiceCard(v,'SUSTAINED',`じっくり「${kana}ー」`,'持続して発音した母音の静的な基準値。時間方向の長さは教材用の表示時間です。','Kasuya 1968 · 静的平均'),
        isolated ? compareChoiceCard(isolated.id,'WORD',`単語の中で「${kana}」`,'単独で読んだ単語の中の短母音。実際の時間変化を30点のデータから再現します。',`実測平均 ${compareDurationLabel(isolated)}`) : '',
        carrier ? compareChoiceCard(carrier.id,'SENTENCE',`文の中で「${kana}」`,'キャリア文の流れの中に入った短母音。発話速度や周囲の影響を受けます。',`実測平均 ${compareDurationLabel(carrier)}`) : ''
      ].join('');
    }

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
    const applicable=uiMode!=='research' && presetLanguageEl.value==='ja' && ['male','female'].includes(voiceTypeEl.value) && Boolean(YK2019_DATA);
    beginnerCompareWrap.hidden=!applicable;
    if(!applicable){
      compareOpen=false;
      comparePanel.hidden=true;
      compareToggleBtn.setAttribute('aria-expanded','false');
      return;
    }
    compareBaseVowel=currentCompareVowel();
    comparePanel.hidden=!compareOpen;
    compareToggleBtn.setAttribute('aria-expanded',String(compareOpen));
    compareToggleBtn.textContent=compareOpen?'🔬 くらべる画面を閉じる':'🔬 同じ母音をくらべてみる';
    renderBeginnerCompare();
  }

''' + logic_marker
replace_once(logic_marker, logic, 'insert beginner compare logic')

# 7) UI mode changes rebuild the preset menu so research is the only full-catalog surface.
old = """    if(persist){ try{ localStorage.setItem('formantCanvasUiMode',uiMode); }catch(e){} }\n    updateLearningPanel();"""
new = """    if(persist){ try{ localStorage.setItem('formantCanvasUiMode',uiMode); }catch(e){} }\n    const previousPreset=vowelPresetEl.value;\n    buildPresetOptions(previousPreset);\n    updateBeginnerCompareVisibility();\n    updateLearningPanel();"""
replace_once(old, new, 'rebuild menu on mode change')

# 8) Compare controls + lightweight refresh listeners.
listener_marker = "  researchModeBtn.addEventListener('click',()=>setUIMode('research'));\n"
listeners = listener_marker + r'''
  compareToggleBtn.addEventListener('click',()=>{
    compareOpen=!compareOpen;
    updateBeginnerCompareVisibility();
  });
  document.querySelectorAll('[data-compare-theme]').forEach(btn=>btn.addEventListener('click',()=>{
    compareTheme=btn.dataset.compareTheme;
    compareCurrentKey=null;
    renderBeginnerCompare();
  }));
  vowelPresetEl.addEventListener('change',()=>{
    if(BASIC_JA_VOWELS.includes(vowelPresetEl.value)) compareBaseVowel=vowelPresetEl.value;
    compareCurrentKey=null;
    updateBeginnerCompareVisibility();
  });
  presetLanguageEl.addEventListener('change',()=>setTimeout(updateBeginnerCompareVisibility,0));
  voiceTypeEl.addEventListener('change',()=>setTimeout(()=>{ compareCurrentKey=null; updateBeginnerCompareVisibility(); },0));
'''
replace_once(listener_marker, listeners, 'insert compare listeners')

path.write_text(s, encoding='utf-8')
print('Added beginner five-vowel menu + comparison experiment UI')
