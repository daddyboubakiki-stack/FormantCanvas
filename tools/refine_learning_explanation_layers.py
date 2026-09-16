#!/usr/bin/env python3
from pathlib import Path
import re

path=Path('index.html')
s=path.read_text(encoding='utf-8')

if 'Layered learning explanation v1' in s:
    print('Layered learning explanation already present.')
    raise SystemExit(0)

def replace_once(old,new,label):
    global s
    count=s.count(old)
    if count!=1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    s=s.replace(old,new,1)

# CSS: make the lower card read like a guided explanation instead of one dense definition.
replace_once(
"  .learning-example { margin-top:7px!important; padding-top:7px; border-top:1px dashed #ccd4e0; color:#667085!important; }",
"""  .learning-example { margin-top:7px!important; padding-top:7px; border-top:1px dashed #ccd4e0; color:#667085!important; }
  /* Layered learning explanation v1 */
  .learning-explain-block { margin-top:9px; }
  .learning-explain-block:first-of-type { margin-top:7px; }
  .learning-explain-label {
    display:inline-flex; align-items:center; margin-bottom:4px; padding:3px 7px;
    border-radius:999px; background:#e9eef8; color:#43516a; font-size:9.5px; font-weight:900;
  }
  .learning-explain-block.try .learning-explain-label { background:#edf8f3; color:#35624e; }
  .learning-explain-block.precise .learning-explain-label { background:#f3f0fa; color:#5b4d75; }
  .learning-explain-block.try { padding:9px 10px; border-radius:11px; background:#fbfdfc; border:1px solid #e1eee7; }
  .learning-explain-block.precise { padding-top:9px; border-top:1px dashed #ccd4e0; }
  .learning-explain-block.precise p { color:#5a6475; }
  .learning-popover-kicker {
    display:inline-block; margin:7px 0 3px; padding:2px 6px; border-radius:999px;
    background:#eef2f8; color:#657087; font-size:9px; font-weight:900;
  }
  .learning-popover-title + .learning-popover-kicker { margin-top:2px; }
  .learning-popover-example { margin-top:0!important; padding-top:0!important; border-top:0!important; }
""",
'layered learning css')

replace_once(
'        <p>用語を選ぶと短い説明が出ます。大きなQ&amp;Aは仕様が固まってから追加予定。</p>',
'        <p>まずひとことでつかんで、触って確かめて、必要なら少し正確に。</p>',
'learning card intro')

old_markup='''    <div class="learning-explain" aria-live="polite">\n      <h3 id="learningExplainTitle">F1（第1フォルマント）</h3>\n      <p id="learningExplainText">声道の1番目の大きな共鳴です。</p>\n      <p class="learning-example" id="learningExplainExample">線を上下に動かして、音の変化を聴いてみよう。</p>\n      <div class="learning-source" id="learningExplainSources" aria-label="この用語の出典"></div>\n      <p class="learning-citation-note">本文は出典を踏まえたFormantasiaによる要約です。原文の直接引用ではありません。</p>\n    </div>'''
new_markup='''    <div class="learning-explain" aria-live="polite">\n      <h3 id="learningExplainTitle">F1（第1フォルマント）</h3>\n      <div class="learning-explain-block one">\n        <span class="learning-explain-label">ひとことで</span>\n        <p id="learningExplainText">母音の「口の開き」に強く関わる、いちばん低いフォルマントです。</p>\n      </div>\n      <div class="learning-explain-block try">\n        <span class="learning-explain-label">触ってみよう</span>\n        <p id="learningExplainExample">F1の線だけ上下に動かして、聞こえ方を比べてみよう。</p>\n      </div>\n      <div class="learning-explain-block precise">\n        <span class="learning-explain-label">もう少し正確に</span>\n        <p id="learningExplainPrecise">F1は第1フォルマントの中心周波数です。母音の高さと強く関係しますが、舌の位置だけで一対一に決まる値ではありません。</p>\n      </div>\n      <div class="learning-source" id="learningExplainSources" aria-label="この用語の出典"></div>\n      <p class="learning-citation-note">本文は出典を踏まえたFormantasiaによる要約です。原文の直接引用ではありません。</p>\n    </div>'''
replace_once(old_markup,new_markup,'learning explanation markup')

replace_once(
"  const learningExplainExample = document.getElementById('learningExplainExample');",
"  const learningExplainExample = document.getElementById('learningExplainExample');\n  const learningExplainPrecise = document.getElementById('learningExplainPrecise');",
'learning precise reference')

# Replace the glossary prose but keep the source arrays/source detail map below.
pattern=r"  const LEARNING_TOPICS = \{.*?\n  \};\n\n  const GLOSSARY_SOURCE_DETAILS = \{"
new_topics=r'''  const LEARNING_TOPICS = {
    f0: {
      title:'F0（基本周波数）',
      one:'声の高さの土台になる、声帯の振動の速さです。',
      more:'数字が大きいほど、基本的には高い声に聞こえます。F1〜F3とは別のものです。',
      tryIt:()=>`いまのF0は ${Math.round(Number(f0El.value))} Hz。スライダーを動かして、母音らしさをなるべく保ったまま高さだけがどう変わるか聴いてみよう。`,
      precise:'周期的な声帯振動の基本的な繰り返し周波数をF0と呼びます。Hzで表し、知覚されるピッチと強く関係しますが、声道の共鳴を表すF1〜F3とは異なる量です。',
      sources:[
        {label:'Praat Manual — frequency',url:'https://www.fon.hum.uva.nl/praat/manual/frequency.html'},
        {label:'Oxford — Source–Filter Theory',url:'https://doi.org/10.1093/acrefore/9780199384655.013.894'}
      ]
    },
    f1: {
      title:'F1（第1フォルマント）',
      one:'母音の「口の開き」に強く関わる、いちばん低いフォルマントです。',
      more:'一般にF1が高いほど、口を大きく開いた母音になりやすいです。',
      tryIt:()=>{ const v=interpolate('F1',duration()/2); return `中央付近のF1は ${v==null?'—':Math.round(v)+' Hz'}。F1の線だけ上下に動かして、母音の変化を聴いてみよう。`; },
      precise:'F1は第1フォルマントの中心周波数です。母音の高さと逆方向に強く関係しますが、声道全体の共鳴の結果なので、舌の高さだけと一対一に対応する値ではありません。',
      sources:[
        {label:'MIT OCW 24.901 — Lecture 8',url:'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/resources/mit24_901f10_lec08/'},
        {label:'Macquarie — Vocal Tract Resonance',url:'https://www.mq.edu.au/faculty-of-medicine-health-and-human-sciences/departments-and-schools/department-of-linguistics/our-research/phonetics-and-phonology/speech/acoustics/acoustic-theory-of-speech-production/vocal-tract-resonance'}
      ]
    },
    f2: {
      title:'F2（第2フォルマント）',
      one:'母音の「前っぽさ／後ろっぽさ」に強く関わる、2番目のフォルマントです。',
      more:'一般にF2が高いほど前寄り、低いほど後ろ寄りの母音になりやすいです。唇の丸めもF2に影響します。',
      tryIt:()=>{ const v=interpolate('F2',duration()/2); return `中央付近のF2は ${v==null?'—':Math.round(v)+' Hz'}。F2だけを動かして、「前っぽい／後ろっぽい」聞こえ方がどう変わるか試そう。`; },
      precise:'F2は第2フォルマントの中心周波数です。舌の前後位置や唇の丸めと強く関係しますが、F1と同じく声道全体の形から生じる共鳴なので、単一の調音器官だけで決まるわけではありません。',
      sources:[
        {label:'MIT OCW 24.901 — Lecture 8',url:'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/resources/mit24_901f10_lec08/'},
        {label:'Macquarie — Vocal Tract Resonance',url:'https://www.mq.edu.au/faculty-of-medicine-health-and-human-sciences/departments-and-schools/department-of-linguistics/our-research/phonetics-and-phonology/speech/acoustics/acoustic-theory-of-speech-production/vocal-tract-resonance'}
      ]
    },
    f3: {
      title:'F3（第3フォルマント）',
      one:'F1・F2より上にある、3番目のフォルマントです。',
      more:'F1・F2ほど単純に母音の位置へ結びつけにくいですが、音の特徴や音色を考えるときに使われます。',
      tryIt:()=>{ const v=interpolate('F3',duration()/2); return `中央付近のF3は ${v==null?'—':Math.round(v)+' Hz'}。F1/F2をそのままにしてF3だけ動かし、どのくらい聞こえ方が変わるか探してみよう。`; },
      precise:'F3は第3フォルマントの中心周波数です。F1・F2とともに低い周波数側のスペクトル構造を記述しますが、その役割は音・話者・文脈によって異なるため、万能な「舌の○○を表す値」とは扱いません。',
      sources:[
        {label:'MIT OCW 24.901 — Lecture 8',url:'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/resources/mit24_901f10_lec08/'},
        {label:'Praat Manual — Formant',url:'https://www.fon.hum.uva.nl/praat/manual/Formant.html'}
      ]
    },
    formant: {
      title:'フォルマント（formant）',
      one:'声道が特に響きやすい周波数にできる「音の山」です。',
      more:'低いほうからF1、F2、F3…と呼びます。母音らしさを作る重要な手がかりです。',
      tryIt:'F1〜F3の線を1本ずつ動かしてみよう。同じF0でも、フォルマントを変えると母音の聞こえ方が変わります。',
      precise:'声道の共鳴は音声のスペクトル包絡に特徴的なピークを作ります。フォルマントはその共鳴に対応する周波数として扱われ、Praatでは各フォルマントを中心周波数と帯域幅の組として時間ごとに表します。',
      sources:[
        {label:'Oxford Phonetics — Source-Filter Model',url:'https://www.phon.ox.ac.uk/jcoleman/source_filter'},
        {label:'Praat Manual — Formant',url:'https://www.fon.hum.uva.nl/praat/manual/Formant.html'}
      ]
    },
    resonance: {
      title:'共鳴（resonance）',
      one:'ある高さの音だけが、特に響きやすくなる性質です。',
      more:'声道にもいくつか「響きやすい高さ」があり、その位置が変わると声の聞こえ方も変わります。',
      tryIt:'F1〜F3を少し動かして、同じ声の高さでも響き方が変わるのを聴いてみよう。',
      precise:'共鳴系は特定の周波数付近に強く応答します。声道は形に応じて複数の共鳴を持ち、音源スペクトルの一部を相対的に強めたり弱めたりします。これがフォルマントを理解する土台になります。',
      sources:[
        {label:'Oxford Phonetics — Source-Filter Model',url:'https://www.phon.ox.ac.uk/jcoleman/source_filter'},
        {label:'Macquarie — Vocal Tract Resonance',url:'https://www.mq.edu.au/faculty-of-medicine-health-and-human-sciences/departments-and-schools/department-of-linguistics/our-research/phonetics-and-phonology/speech/acoustics/acoustic-theory-of-speech-production/vocal-tract-resonance'}
      ]
    },
    hz: {
      title:'Hz（ヘルツ）',
      one:'「1秒に何回くり返すか」を表す、周波数の単位です。',
      more:'たとえば140 Hzなら、1秒に140回くり返すという意味です。',
      tryIt:()=>`いまのF0は ${Math.round(Number(f0El.value))} Hz。F0スライダーを動かして、数字と声の高さの変化を結びつけてみよう。`,
      precise:'Hz（ヘルツ）は周波数のSI単位で、1 Hzは1秒あたり1周期に相当します。F0もフォルマント周波数もHzで表せますが、同じ単位でも表している物理的・音響的な役割は異なります。',
      sources:[
        {label:'NIST — SI Units: Time / Frequency',url:'https://www.nist.gov/pml/owm/si-units-time'},
        {label:'Praat Manual — frequency',url:'https://www.fon.hum.uva.nl/praat/manual/frequency.html'}
      ]
    },
    spectrogram: {
      title:'スペクトログラム（spectrogram）',
      one:'音を「時間 × 周波数」の地図にしたものです。',
      more:'横に時間、縦に周波数をとり、濃い部分ほどそのあたりの音のエネルギーが強いことを表します。',
      tryIt:'Praatで母音を録音してスペクトログラムを表示すると、フォルマントが帯のように見えます。Formantasiaでは、そのF1〜F3だけを線として直接扱っています。',
      precise:'スペクトログラムは信号の周波数成分が時間とともにどう変化するかを表す時間–周波数表示です。表示の濃さや色は、各時間・周波数付近のエネルギーや強度を表します。',
      sources:[
        {label:'Praat Manual — Spectrogram',url:'https://www.fon.hum.uva.nl/praat/manual/Spectrogram.html'},
        {label:'Praat Tutorial — Viewing a spectrogram',url:'https://www.fon.hum.uva.nl/praat/manual/Intro_3_1__Viewing_a_spectrogram.html'}
      ]
    },
    sourcefilter: {
      title:'音源–フィルタ理論（source–filter theory）',
      one:'声を「音のもと」と「声道による加工」に分けて考えるモデルです。',
      more:'ざっくり言えば、声帯が音の材料を作り、声道がその響きを整えます。',
      tryIt:'F0だけを変えたあと、今度はF1〜F3だけを変えてみよう。「音源側」と「フィルタ側」の違いを耳で比べられます。',
      precise:'音源–フィルタ理論では、音声を音源と声道フィルタの働きに分けて記述します。有声音では声帯振動が主要な音源となり、声道の共鳴がスペクトル包絡を形づくります。FormantasiaのF0／F1〜F3の対応は学習用の単純化で、実際の発声では相互作用もあります。',
      sources:[
        {label:'Oxford Research Encyclopedia — Source–Filter Theory',url:'https://doi.org/10.1093/acrefore/9780199384655.013.894'},
        {label:'Praat Manual — Source-filter synthesis',url:'https://www.fon.hum.uva.nl/praat/manual/Source-filter_synthesis.html'}
      ]
    },
    praat: {
      title:'Praat（プラート）',
      one:'声を録音して、見て、測って、加工できる音声学ソフトです。',
      more:'ピッチ、フォルマント、スペクトログラムなどを調べるときによく使われます。',
      tryIt:'Formantasiaの「Praatへ書き出し」を使うと、描いたF1〜F3の軌跡をPraat側でも扱えます。',
      precise:'Praatは音声の録音・表示・分析・合成・加工などを行うためのソフトウェアです。University of Amsterdamで開発され、音声学・音韻論の研究や教育で広く利用されています。',
      sources:[
        {label:'Praat official site',url:'https://praat.org/'},
        {label:'Praat Manual — Intro',url:'https://www.fon.hum.uva.nl/praat/manual/Intro.html'}
      ]
    },
    bandwidth: {
      title:'Bandwidth（帯域幅）',
      one:'フォルマントの「山の太さ」を表す値です。',
      more:'小さいほど細く鋭い山、大きいほど広くなだらかな山になります。',
      tryIt:()=>usingEmpiricalBandwidth()
        ? 'いまは文献由来の帯域幅を使っています。Manual Qへ切り替えると、「山の鋭さ」を自分で動かして聴き比べられます。'
        : `いまは Manual Q ${Number(qEl.value)}。Qを動かして、フォルマントの位置を変えずに響き方がどう変わるか聴いてみよう。`,
      precise:'各フォルマントには中心となる周波数だけでなく、その共鳴が周波数方向にどれくらい広がるかを表す帯域幅があります。帯域幅が狭いほど共鳴ピークは鋭く、広いほどなだらかになります。PraatのFormantデータも中心周波数と帯域幅を持ちます。',
      sources:[
        {label:'Praat Manual — Formant',url:'https://www.fon.hum.uva.nl/praat/manual/Formant.html'},
        {label:'Praat Manual — smoothest formant tracks',url:'https://www.fon.hum.uva.nl/praat/manual/Formants__Extract_smoothest_part___.html'}
      ]
    },
    q: {
      title:'Q（quality factor）',
      one:'フォルマントの「山のとがり具合」を表す数字です。',
      more:'Qが大きいほど細く鋭く、小さいほど幅広い共鳴になります。',
      tryIt:()=>usingEmpiricalBandwidth()
        ? 'いまは文献由来の帯域幅からQを自動計算しています。Manual Qへ切り替えると、自分でQを動かせます。'
        : `いまは Q=${Number(qEl.value)}。Qを上げ下げして、F1〜F3の位置を変えずに響き方だけがどう変わるか聴いてみよう。`,
      precise:'Qは共鳴の鋭さを表す無次元の指標です。Formantasiaのband-passフィルタでは中心周波数Fと帯域幅BからQ=F/Bとして扱い、Qが高いほど帯域が狭くなります。',
      sources:[
        {label:'OpenStax University Physics — Resonance and Q',url:'https://openstax.org/books/university-physics-volume-2/pages/15-5-resonance-in-an-ac-circuit'},
        {label:'Web Audio API — BiquadFilterNode',url:'https://webaudio.github.io/web-audio-api/#BiquadFilterNode'}
      ]
    },
    evidence: {
      title:'● 実測・△ 借用・┄ モデル',
      one:'その線が「どこまで実測で、どこからアプリのモデルか」を示す印です。',
      more:'●は採用した資料の値、△は別条件などから借りた値、破線はアプリが作った区間です。',
      tryIt:()=>presetDirty
        ? 'いまは編集済み。元プリセットの根拠が灰色のゴーストとして残るので、「文献・モデル」と「自分の編集」を比べてみよう。'
        : 'プリセットを選び替えて、●・△・破線の割合がどう違うか見比べてみよう。',
      precise:'●・△・破線はFormantasia独自の表示規約です。学界共通の記号ではありません。●は採用した文献・データセットから直接得た値、△は別条件や別研究から借用した値、破線は補間・合成などアプリがモデル化した区間を示します。',
      sources:[{label:'Formantasia — Evidence表示規約（アプリ内定義）'}]
    }
  };

  const GLOSSARY_SOURCE_DETAILS = {'''
new_s, n = re.subn(pattern,new_topics,s,flags=re.S)
if n != 1:
    raise SystemExit(f'learning topics: expected 1 replacement, found {n}')
s=new_s

# Update lower-card rendering to four layers.
replace_once(
"""    learningExplainTitle.textContent=item.title;
    learningExplainText.textContent=item.text;
    learningExplainExample.textContent=typeof item.example==='function'?item.example():item.example;
    renderLearningReferences(learningExplainSources,item);""",
"""    learningExplainTitle.textContent=item.title;
    learningExplainText.textContent=typeof item.one==='function'?item.one():item.one;
    learningExplainExample.textContent=typeof item.tryIt==='function'?item.tryIt():item.tryIt;
    learningExplainPrecise.textContent=typeof item.precise==='function'?item.precise():item.precise;
    renderLearningReferences(learningExplainSources,item);""",
'lower layered rendering')

# Popover: only one-line + one extra sentence + short citation.
replace_once(
"learningInfoPopover.innerHTML='<strong class=\"learning-popover-title\"></strong><p class=\"learning-popover-text\"></p><p class=\"learning-popover-example\"></p><div class=\"learning-popover-source\"></div>';",
"learningInfoPopover.innerHTML='<strong class=\"learning-popover-title\"></strong><span class=\"learning-popover-kicker\">ひとことで</span><p class=\"learning-popover-text\"></p><span class=\"learning-popover-kicker\">もう少し</span><p class=\"learning-popover-example\"></p><div class=\"learning-popover-source\"></div>';",
'popover layered markup')

replace_once(
"""    learningPopoverTitle.textContent=item.title;
    learningPopoverText.textContent=item.text;
    learningPopoverExample.textContent=typeof item.example==='function'?item.example():item.example;
    renderLearningSourceShort(learningPopoverSources,item);""",
"""    learningPopoverTitle.textContent=item.title;
    learningPopoverText.textContent=typeof item.one==='function'?item.one():item.one;
    learningPopoverExample.textContent=typeof item.more==='function'?item.more():item.more;
    renderLearningSourceShort(learningPopoverSources,item);""",
'popover layered rendering')

path.write_text(s,encoding='utf-8')
print('Applied layered beginner-friendly learning explanations to all 13 glossary topics.')
