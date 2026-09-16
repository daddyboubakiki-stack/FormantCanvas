#!/usr/bin/env python3
from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, found {count}')
    s = s.replace(old, new, 1)

# If the UI integration is already present, only normalize the loader call so it
# stays inside the app IIFE. This makes the script safe to re-run in CI.
if 'let YK2019_DATA = null;' in s:
    outside = "})();\n  loadYazawaKondoData();\n</script>"
    inside = "  loadYazawaKondoData();\n})();\n</script>"
    if outside in s:
        s = s.replace(outside, inside, 1)
    elif inside not in s:
        raise SystemExit('YK integration exists but loader placement is unknown')
    path.write_text(s, encoding='utf-8')
    print('Normalized existing Yazawa–Kondo UI integration')
    raise SystemExit(0)

# 1) Runtime data store + helpers, inserted before cloneTarget.
marker = "  function cloneTarget(v){ return {F1:v.F1,F2:v.F2,F3:v.F3}; }"
insert = r'''  let YK2019_DATA = null;
  let YK2019_PRESETS = new Map();

  function ykContextLabel(p){ return p.context_label==='isolated_word'?'単独語':'文中'; }
  function ykLengthLabel(p){ return p.length==='long'?'長':'短'; }
  function ykOptionLabel(p){
    const shortKana={i:'い',e:'え',a:'あ',o:'お',u:'う'};
    const longKana={i:'いい',e:'ええ',a:'ああ',o:'おお',u:'うう'};
    return p.length==='long' ? `/${p.vowel}ː/ ${longKana[p.vowel]}` : `/${p.vowel}/ ${shortKana[p.vowel]}`;
  }
  function ykMatchingPreset(source, sex){
    if(!source || !YK2019_DATA) return null;
    return YK2019_DATA.presets.find(p=>p.sex===sex && p.context_label===source.context_label && p.length===source.length && p.vowel===source.vowel) || null;
  }

  async function loadYazawaKondoData(){
    try{
      const response=await fetch('data/yazawa_kondo_2019_adult_presets.json',{cache:'force-cache'});
      if(!response.ok) throw new Error(`HTTP ${response.status}`);
      const data=await response.json();
      if(!data || !Array.isArray(data.presets) || data.presets.length!==40) throw new Error('expected 40 presets');
      YK2019_DATA=data;
      YK2019_PRESETS=new Map(data.presets.map(p=>[p.id,p]));
      if(presetLanguageEl.value==='ja') buildPresetOptions(vowelPresetEl.value);
    }catch(err){
      console.warn('Yazawa–Kondo presets could not be loaded:',err);
    }
  }

''' + marker
replace_once(marker, insert, 'insert YK runtime helpers')

# 2) Duration comes from the measured condition mean.
old = """  function presetDuration(lang,key,voice=voiceTypeEl.value){\n    if(lang==='en' && EN_DIPH[voice] && EN_DIPH[voice][key]) return EN_DIPH[voice][key].duration;\n    return SYNTH_DEFAULTS.duration;\n  }"""
new = """  function presetDuration(lang,key,voice=voiceTypeEl.value){\n    const yk=YK2019_PRESETS.get(key);\n    if(lang==='ja' && yk) return yk.duration_ms.mean/1000;\n    if(lang==='en' && EN_DIPH[voice] && EN_DIPH[voice][key]) return EN_DIPH[voice][key].duration;\n    return SYNTH_DEFAULTS.duration;\n  }"""
replace_once(old, new, 'patch presetDuration')

# 3) Extend the existing vowel menu without adding more selector columns.
old = """  function buildPresetOptions(preferred=null){\n    const lang=presetLanguageEl.value;\n    const data=PRESETS[lang];\n    const keep=preferred || vowelPresetEl.value;\n    vowelPresetEl.innerHTML='';\n    const mono=document.createElement('optgroup'); mono.label='単母音';\n    data.mono.forEach(([value,label])=>{ const o=document.createElement('option'); o.value=value; o.textContent=label; mono.appendChild(o); });\n    const diph=document.createElement('optgroup'); diph.label=lang==='ja'?'母音連続 (VV)':'二重母音';\n    data.diph.forEach(([value,label])=>{ const o=document.createElement('option'); o.value=value; o.textContent=label; diph.appendChild(o); });\n    vowelPresetEl.append(mono,diph);\n    const all=[...data.mono,...data.diph].map(x=>x[0]);\n    vowelPresetEl.value=all.includes(keep)?keep:data.mono[0][0];\n  }"""
new = r'''  function buildPresetOptions(preferred=null){
    const lang=presetLanguageEl.value;
    const data=PRESETS[lang];
    let desired=preferred || vowelPresetEl.value;
    const oldYk=YK2019_PRESETS.get(desired);
    if(oldYk && oldYk.sex!==voiceTypeEl.value){
      const translated=ykMatchingPreset(oldYk,voiceTypeEl.value);
      if(translated) desired=translated.id;
    }
    vowelPresetEl.innerHTML='';
    const mono=document.createElement('optgroup');
    mono.label=lang==='ja'?'持続母音（Kasuya 1968）':'単母音';
    data.mono.forEach(([value,label])=>{ const o=document.createElement('option'); o.value=value; o.textContent=label; mono.appendChild(o); });
    const diph=document.createElement('optgroup'); diph.label=lang==='ja'?'母音連続 (VV)':'二重母音';
    data.diph.forEach(([value,label])=>{ const o=document.createElement('option'); o.value=value; o.textContent=label; diph.appendChild(o); });
    vowelPresetEl.append(mono,diph);
    const all=[...data.mono,...data.diph].map(x=>x[0]);

    if(lang==='ja' && YK2019_DATA && ['male','female'].includes(voiceTypeEl.value)){
      const groupSpecs=[
        ['isolated_word','short','単独語・短（Yazawa–Kondo）'],
        ['isolated_word','long','単独語・長（Yazawa–Kondo）'],
        ['carrier_sentence','short','文中・短（Yazawa–Kondo）'],
        ['carrier_sentence','long','文中・長（Yazawa–Kondo）']
      ];
      const vowelOrder={i:0,e:1,a:2,o:3,u:4};
      for(const [context,length,label] of groupSpecs){
        const group=document.createElement('optgroup'); group.label=label;
        const presets=YK2019_DATA.presets
          .filter(p=>p.sex===voiceTypeEl.value && p.context_label===context && p.length===length)
          .sort((a,b)=>vowelOrder[a.vowel]-vowelOrder[b.vowel]);
        presets.forEach(p=>{
          const o=document.createElement('option'); o.value=p.id; o.textContent=ykOptionLabel(p); group.appendChild(o); all.push(p.id);
        });
        vowelPresetEl.appendChild(group);
      }
    }
    vowelPresetEl.value=all.includes(desired)?desired:data.mono[0][0];
  }'''
replace_once(old, new, 'patch buildPresetOptions')

# 4) Resolve dataset-backed menu values before legacy Japanese logic.
old = """  function getPresetSpec(lang,key){\n    if(lang==='ja'){\n      if(JA_MONO[voiceTypeEl.value][key]) return {type:'mono',target:getJapaneseTarget(key)};\n      return {type:'jvv',pair:japanesePairForKey(key)};\n    }\n    if(EN_MONO[voiceTypeEl.value][key]) return {type:'mono',target:getEnglishTarget(key)};\n    return {type:'ediph',key};\n  }"""
new = """  function getPresetSpec(lang,key){\n    if(lang==='ja'){\n      const yk=YK2019_PRESETS.get(key);\n      if(yk) return {type:'yk',preset:yk};\n      if(JA_MONO[voiceTypeEl.value][key]) return {type:'mono',target:getJapaneseTarget(key)};\n      return {type:'jvv',pair:japanesePairForKey(key)};\n    }\n    if(EN_MONO[voiceTypeEl.value][key]) return {type:'mono',target:getEnglishTarget(key)};\n    return {type:'ediph',key};\n  }"""
replace_once(old, new, 'patch getPresetSpec')

# 5) Dataset-backed track/evidence/meta renderer.
apply_marker = "  function applyPreset(lang=presetLanguageEl.value,key=vowelPresetEl.value){"
yk_renderer = r'''  function applyYazawaKondoPreset(preset){
    const d=duration();
    const ev=emptyVisualEvidence();
    for(const name of ['F1','F2','F3']){
      const field=`${name}_hz`;
      const measured=preset.trajectory.map(pt=>({p:pt.position_normalized,hz:pt[field]}));
      const first=measured[0], last=measured[measured.length-1];
      tracks[name]=[
        {t:0,hz:first.hz},
        ...measured.map(pt=>({t:d*pt.p,hz:pt.hz})),
        {t:d,hz:last.hz}
      ];
      addEvidencePath(ev,name,[{p:0,hz:first.hz},{p:first.p,hz:first.hz}],'modeled');
      addEvidencePath(ev,name,measured,'empirical');
      addEvidencePath(ev,name,[{p:last.p,hz:last.hz},{p:1,hz:last.hz}],'modeled');
      [0,Math.floor((measured.length-1)/2),measured.length-1].forEach(i=>addEvidenceMarker(ev,name,measured[i].p,measured[i].hz,'empirical','Yazawa–Kondo 2019'));
    }
    currentEvidence=ev;
    const midpoint=preset.midpoint_hz;
    const midpointSd=preset.midpoint_sd_across_speaker_means_hz;
    const context=ykContextLabel(preset), length=ykLengthLabel(preset);
    const vowelLabel=preset.length==='long'?`/${preset.vowel}ː/`:`/${preset.vowel}/`;
    setMeta({
      title:`Japanese ${vowelLabel} — ${context}・${length} — ${voiceTypeEl.options[voiceTypeEl.selectedIndex].text}`,
      confidence:'A · 公開実測データの話者均衡平均',level:'a',
      summary:`Yazawa & Kondo (2019) の公開CSVから、8話者×各10発話を話者均衡で再集計。再生時間と中央20–80%のF1–F3軌跡は、この発話条件の実測値に基づきます。`,
      evidence:[
        {item:'Duration',status:'empirical',detail:`${preset.duration_ms.mean.toFixed(1)} ms（話者平均間SD ${preset.duration_ms.sd_across_speaker_means.toFixed(1)} ms; 8話者, 80 tokens）`},
        {item:'F1 midpoint',status:'empirical',detail:`${fmtHz(midpoint.F1)} Hz（話者平均間SD ${fmtHz(midpointSd.F1)} Hz）`},
        {item:'F2 midpoint',status:'empirical',detail:`${fmtHz(midpoint.F2)} Hz（話者平均間SD ${fmtHz(midpointSd.F2)} Hz）`},
        {item:'F3 midpoint',status:'empirical',detail:`${fmtHz(midpoint.F3)} Hz（話者平均間SD ${fmtHz(midpointSd.F3)} Hz）`},
        {item:'F1–F3 時系列',status:'empirical',detail:'母音区間の中央20–80%を30点で測定した公開値を、各話者内10発話→8話者等重みで平均。'},
        {item:'0–20% / 80–100%',status:'synthetic',detail:'公開データの30点測定範囲外。再生のため最初/最後の実測点を一定値で延長しており、実測軌跡とは主張しません。'}
      ],
      source:'Yazawa & Kondo (2019), Japanese Vowel Length Acoustic Data v3. Formantasiaが公開 JPLongShortVowels.csv から sex × context × vowel length × vowel ごとに話者均衡平均を再計算。',
      trajectory:'中央20–80%の30点は公開測定値の派生平均。0–20%と80–100%のみ、音声合成を成立させるため端の実測平均値を水平に保持しています。',
      reuse:'Formantasiaには元の3,200行を埋め込まず、条件別に再集計した派生平均と話者平均間SDを収録しています。利用時は元研究とZenodoデータセットを引用してください。',
      refs:'<a href="https://zenodo.org/records/15227304" target="_blank" rel="noreferrer">Yazawa & Kondo dataset — Zenodo 15227304</a>'
    });
  }

''' + apply_marker
replace_once(apply_marker, yk_renderer, 'insert YK renderer')

# 6) Route YK specs through renderer; legacy branches remain untouched.
old = """    const spec=getPresetSpec(lang,key), voice=voiceTypeEl.value;\n    if(spec.type==='mono'){"""
new = """    const spec=getPresetSpec(lang,key), voice=voiceTypeEl.value;\n    if(spec.type==='yk'){\n      applyYazawaKondoPreset(spec.preset);\n    } else if(spec.type==='mono'){"""
replace_once(old, new, 'route YK applyPreset')

# 7) Rebuild menu when speaker changes so equivalent male/female YK condition is selected safely.
old = """  voiceTypeEl.addEventListener('change',()=>{\n    const cfg=VOICE_DEFAULTS[presetLanguageEl.value][voiceTypeEl.value];"""
new = """  voiceTypeEl.addEventListener('change',()=>{\n    const previousPreset=vowelPresetEl.value;\n    buildPresetOptions(previousPreset);\n    const cfg=VOICE_DEFAULTS[presetLanguageEl.value][voiceTypeEl.value];"""
replace_once(old, new, 'patch voice change menu rebuild')

# 8) Start async data load after the existing startup render, but still inside
# the app IIFE so it can see the integration helpers and DOM bindings.
startup = "  applyPreset('ja','i');\n  render();\n})();"
startup_with_load = "  applyPreset('ja','i');\n  render();\n  loadYazawaKondoData();\n})();"
replace_once(startup, startup_with_load, 'start YK data loader')

path.write_text(s, encoding='utf-8')
print('Patched index.html for Yazawa–Kondo UI integration')
