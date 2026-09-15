#!/usr/bin/env python3
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "index.html"
MARKER = "const HILLENBRAND_1995 ="


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly 1 anchor, found {count}")
    return text.replace(old, new, 1)


text = PATH.read_text(encoding="utf-8")
if MARKER in text:
    print("Hillenbrand integration already present; no changes.")
    raise SystemExit(0)

text = replace_once(
    text,
    "    lee14: '<a href=\"https://doi.org/10.1121/1.4894799\" target=\"_blank\" rel=\"noreferrer\">Lee, Potamianos & Narayanan (2014)</a>',\n",
    "    lee14: '<a href=\"https://doi.org/10.1121/1.4894799\" target=\"_blank\" rel=\"noreferrer\">Lee, Potamianos & Narayanan (2014)</a>',\n"
    "    hillenbrand: '<a href=\"https://doi.org/10.1121/1.411872\" target=\"_blank\" rel=\"noreferrer\">Hillenbrand, Getty, Clark & Wheeler (1995)</a>',\n",
    "REFS.hillenbrand",
)

h95 = r'''  // Hillenbrand et al. (1995), bigdata.dat. Group means recomputed by Formant Canvas.
  // F1/F2/F3 are sampled at 10–80% of vowel duration in 10% steps.
  // Source bigdata.dat uses "ei" for HAYED; Canvas keeps its existing /eɪ/ key "eI".
  // 0-valued source measurements are missing and were excluded point-wise.
  const HILLENBRAND_1995 = {
    male:{
      eI:{duration:.2672,n:45,points:[
        {p:.10,F1:493.9,F2:2064.4,F3:2671.3},{p:.20,F1:478.8,F2:2089.0,F3:2698.5},
        {p:.30,F1:463.0,F2:2122.0,F3:2710.1},{p:.40,F1:449.7,F2:2154.5,F3:2715.4},
        {p:.50,F1:437.2,F2:2180.6,F3:2727.0},{p:.60,F1:427.7,F2:2204.7,F3:2737.4},
        {p:.70,F1:413.2,F2:2221.8,F3:2740.9},{p:.80,F1:399.6,F2:2229.2,F3:2741.7}
      ]},
      oU:{duration:.2660,n:45,points:[
        {p:.10,F1:525.4,F2:960.5,F3:2448.0},{p:.20,F1:511.1,F2:936.1,F3:2454.9},
        {p:.30,F1:497.6,F2:908.6,F3:2472.1},{p:.40,F1:480.5,F2:884.8,F3:2474.3},
        {p:.50,F1:464.7,F2:865.8,F3:2478.7},{p:.60,F1:454.0,F2:852.1,F3:2477.7},
        {p:.70,F1:444.7,F2:861.6,F3:2466.4},{p:.80,F1:434.6,F2:897.5,F3:2447.9}
      ]}
    },
    female:{
      eI:{duration:.3209,n:48,points:[
        {p:.10,F1:547.8,F2:2483.7,F3:3061.5},{p:.20,F1:534.1,F2:2514.3,F3:3053.3},
        {p:.30,F1:510.2,F2:2539.2,F3:3035.2},{p:.40,F1:493.0,F2:2577.9,F3:3040.8},
        {p:.50,F1:476.4,F2:2611.4,F3:3042.7},{p:.60,F1:463.4,F2:2636.3,F3:3051.9},
        {p:.70,F1:452.4,F2:2672.3,F3:3066.9},{p:.80,F1:446.9,F2:2692.8,F3:3075.8}
      ]},
      oU:{duration:.3267,n:48,points:[
        {p:.10,F1:624.3,F2:1095.6,F3:2803.0},{p:.20,F1:603.0,F2:1078.1,F3:2819.0},
        {p:.30,F1:574.6,F2:1054.4,F3:2833.8},{p:.40,F1:545.9,F2:1020.6,F3:2847.4},
        {p:.50,F1:524.6,F2:1005.6,F3:2852.6},{p:.60,F1:503.3,F2:985.8,F3:2843.5},
        {p:.70,F1:486.2,F2:973.6,F3:2822.9},{p:.80,F1:471.7,F2:996.4,F3:2808.8}
      ]}
    }
  };

'''
text = replace_once(
    text,
    "  // Jacewicz, Fox & Salmons (2011), Appendix B: Wisconsin parent-generation males, F1/F2 at 20/35/50/65/80%.\n",
    h95 + "  // Jacewicz, Fox & Salmons (2011), Appendix B: Wisconsin parent-generation males, F1/F2 at 20/35/50/65/80%.\n",
    "H95 constant insertion",
)

old_visibility = '''  function updateRegionalEvidenceVisibility(){
    const applicable = presetLanguageEl.value==='en' && voiceTypeEl.value==='male' && ['aI','aU','OI'].includes(vowelPresetEl.value);
    regionalEvidenceWrap.style.display = applicable ? 'inline-flex' : 'none';
    if(!applicable && bestEvidenceToggle.checked) bestEvidenceToggle.checked=false;
  }
'''
new_visibility = '''  function updateRegionalEvidenceVisibility(){
    const lang=presetLanguageEl.value, voice=voiceTypeEl.value, key=vowelPresetEl.value;
    const hillenbrand = lang==='en' && ['male','female'].includes(voice) && ['eI','oU'].includes(key);
    const jacewicz = lang==='en' && voice==='male' && ['aI','aU','OI'].includes(key);
    const applicable = hillenbrand || jacewicz;
    regionalEvidenceWrap.style.display = applicable ? 'inline-flex' : 'none';
    const label=regionalEvidenceWrap.querySelector('span');
    if(hillenbrand){
      regionalEvidenceWrap.title='Hillenbrand et al. (1995) bigdata.dat から再集計した10–80%（10%刻み）のF1/F2/F3群平均を使用します。0–10%と80–100%は最寄りの実測点を保持します。';
      if(label) label.textContent='8点実測F1–F3を使う（Hillenbrand 1995）';
    } else if(jacewicz){
      regionalEvidenceWrap.title='Jacewicz et al. (2011) のWisconsin親世代男性について公表された20/35/50/65/80%時点のF1/F2平均値を使用します。F3はLee et al. (2014) のendpoint間を補間します。';
      if(label) label.textContent='5点実測F1/F2を使う（Jacewicz 2011・WI成人男性）';
    }
    if(!applicable && bestEvidenceToggle.checked) bestEvidenceToggle.checked=false;
  }
'''
text = replace_once(text, old_visibility, new_visibility, "evidence toggle visibility")

h95_setter = '''  function setHillenbrandTrajectory(key){
    const h=HILLENBRAND_1995[voiceTypeEl.value] && HILLENBRAND_1995[voiceTypeEl.value][key];
    if(!h) return;
    durationEl.value=h.duration.toFixed(4);
    lastDuration=h.duration;
    updateLabels();
    const sampleP=[0,...h.points.map(x=>x.p),1];
    for(const name of ['F1','F2','F3']){
      const values=[h.points[0][name],...h.points.map(x=>x[name]),h.points[h.points.length-1][name]];
      tracks[name]=sampleP.map((p,i)=>({t:duration()*p,hz:values[i]}));
    }
    if(isOrdered()) repairOrdering();
  }

'''
text = replace_once(text, "  function setJacewiczHybrid(key){\n", h95_setter + "  function setJacewiczHybrid(key){\n", "H95 track setter")

text = replace_once(
    text,
    "    const hybrid=Boolean(options.hybrid);\n    const ev=emptyVisualEvidence();\n",
    "    const hybrid=Boolean(options.hybrid);\n    const hillenbrand=Boolean(options.hillenbrand);\n    const ev=emptyVisualEvidence();\n",
    "visual evidence option",
)

h95_visual = '''    if(hillenbrand && HILLENBRAND_1995[voice] && HILLENBRAND_1995[voice][key]){
      const h=HILLENBRAND_1995[voice][key], pts=h.points;
      for(const name of ['F1','F2','F3']){
        const seq=[{p:0,hz:pts[0][name]},...pts.map(x=>({p:x.p,hz:x[name]})),{p:1,hz:pts[pts.length-1][name]}];
        addEvidencePath(ev,name,seq);
        pts.forEach(x=>addEvidenceMarker(ev,name,x.p,x[name],'empirical','Hillenbrand 1995'));
      }
      return ev;
    }
'''
text = replace_once(
    text,
    "    if(hybrid && voice==='male' && JACEWICZ_WI_PARENT_MALE[key]){\n",
    h95_visual + "    if(hybrid && voice==='male' && JACEWICZ_WI_PARENT_MALE[key]){\n",
    "H95 visual evidence",
)

old_apply = '''      const d=EN_DIPH[voice][key];
      const hybrid=bestEvidenceToggle.checked && voice==='male' && JACEWICZ_WI_PARENT_MALE[key];
      currentEvidence=buildVisualEvidence(lang,key,voice,{hybrid});
      if(hybrid){
'''
new_apply = '''      const d=EN_DIPH[voice][key];
      const hillenbrand=bestEvidenceToggle.checked && HILLENBRAND_1995[voice] && HILLENBRAND_1995[voice][key];
      const hybrid=bestEvidenceToggle.checked && !hillenbrand && voice==='male' && JACEWICZ_WI_PARENT_MALE[key];
      currentEvidence=buildVisualEvidence(lang,key,voice,{hybrid,hillenbrand});
      if(hillenbrand){
        const h=HILLENBRAND_1995[voice][key], pts=h.points;
        setHillenbrandTrajectory(key);
        setMeta({
          title:`American English /${EN_DIPH_IPA[key]}/ — ${voiceTypeEl.options[voiceTypeEl.selectedIndex].text} · Hillenbrand 1995 trajectory`,
          confidence:'A · 同一資料8実測時点',level:'a',
          summary:`Hillenbrand et al. (1995) bigdata.dat の同一話者群から、durationと10–80%（10%刻み）のF1–F3をFormant Canvasで再集計した群平均です（n=${h.n}）。`,
          evidence:[
            {item:'duration',status:'empirical',detail:`${Math.round(h.duration*1000)} ms（Hillenbrand 1995; 群平均）`},
            {item:'F1 8時点',status:'empirical',detail:`10–80% = ${pts.map(p=>fmtHz(p.F1)).join(' / ')} Hz`},
            {item:'F2 8時点',status:'empirical',detail:`10–80% = ${pts.map(p=>fmtHz(p.F2)).join(' / ')} Hz`},
            {item:'F3 8時点',status:'empirical',detail:`10–80% = ${pts.map(p=>fmtHz(p.F3)).join(' / ')} Hz`},
            {item:'0–10% / 80–100%',status:'canvas',detail:'bigdata.datの測定点外なので、最寄りの10% / 80%実測平均を保持。'},
            {item:'実測点間',status:'canvas',detail:'表示・合成時は隣接する実測平均点どうしを線形補間。'}
          ],
          source:'Hillenbrand et al. (1995) bigdata.dat。F1/F2/F3は母音継続時間の10–80%を10%刻みで測定。Formant Canvasが話者群×意図母音ごとに算術平均を再集計。',
          trajectory:'10–80%の8点は同一資料の実測群平均。0–10%と80–100%は端点保持、実測点間はCanvasの線形補間です。',
          reuse:'公開ミラーの数値データから派生群平均のみを収録。raw recordingsおよび1668行のsource table自体はアプリに同梱していません。sourceのHAYEDコード ei はCanvas内部キー eI に対応付けています。',
          refs:REFS.hillenbrand
        });
      } else if(hybrid){
'''
text = replace_once(text, old_apply, new_apply, "applyPreset H95 branch")

PATH.write_text(text, encoding="utf-8")
print("Patched index.html with Hillenbrand 1995 adult /eɪ, oʊ/ trajectories.")
