#!/usr/bin/env python3
from pathlib import Path
import re

path=Path('index.html')
s=path.read_text(encoding='utf-8')

if 'Sourced learning glossary v1' in s:
    print('Sourced learning glossary already present; no changes.')
    raise SystemExit(0)

def replace_once(old,new,label):
    global s
    count=s.count(old)
    if count!=1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    s=s.replace(old,new,1)

# Marker + source styling.
replace_once('  .learning-example { margin-top:7px!important; padding-top:7px; border-top:1px dashed #ccd4e0; color:#667085!important; }', '''  .learning-example { margin-top:7px!important; padding-top:7px; border-top:1px dashed #ccd4e0; color:#667085!important; }
  /* Sourced learning glossary v1 */
  .learning-source { margin-top:8px; padding-top:8px; border-top:1px solid #e1e6ef; color:#788194; font-size:10.5px; line-height:1.55; }
  .learning-source a, .learning-popover-source a { color:#315fc4; text-decoration:none; font-weight:750; }
  .learning-source a:hover, .learning-popover-source a:hover { text-decoration:underline; }
  .learning-source-sep { margin:0 4px; color:#a0a7b4; }
  .learning-citation-note { margin-top:5px!important; color:#9299a7!important; font-size:9.5px!important; line-height:1.45!important; }''', 'learning source css')
replace_once('  .learning-popover-example { margin-top:7px; padding-top:7px; border-top:1px dashed #d2d9e5; color:#687489; }', '''  .learning-popover-example { margin-top:7px; padding-top:7px; border-top:1px dashed #d2d9e5; color:#687489; }
  .learning-popover-source { margin-top:8px; padding-top:7px; border-top:1px solid #e1e6ef; color:#7b8495; font-size:9.8px; line-height:1.5; }''', 'popover source css')

# Expand topic buttons.
replace_once('''      <button class="learning-topic" type="button" data-learn-topic="f3">F3</button>
      <button class="learning-topic" type="button" data-learn-topic="bandwidth">Bandwidth</button>''', '''      <button class="learning-topic" type="button" data-learn-topic="f3">F3</button>
      <button class="learning-topic" type="button" data-learn-topic="formant">フォルマント</button>
      <button class="learning-topic" type="button" data-learn-topic="resonance">共鳴</button>
      <button class="learning-topic" type="button" data-learn-topic="hz">Hz</button>
      <button class="learning-topic" type="button" data-learn-topic="spectrogram">スペクトログラム</button>
      <button class="learning-topic" type="button" data-learn-topic="sourcefilter">音源–フィルタ</button>
      <button class="learning-topic" type="button" data-learn-topic="praat">Praat</button>
      <button class="learning-topic" type="button" data-learn-topic="bandwidth">Bandwidth</button>''', 'topic buttons')

replace_once('''      <p class="learning-example" id="learningExplainExample">線を上下に動かして、音の変化を聴いてみよう。</p>
    </div>''', '''      <p class="learning-example" id="learningExplainExample">線を上下に動かして、音の変化を聴いてみよう。</p>
      <div class="learning-source" id="learningExplainSources" aria-label="この用語の出典"></div>
      <p class="learning-citation-note">本文は出典を踏まえたFormantasiaによる要約です。原文の直接引用ではありません。</p>
    </div>''', 'learning source container')

# Replace glossary data with sourced entries.
pattern=r"  const LEARNING_TOPICS = \{.*?\n  \};\n\n  function learningEvidenceLabel"
repl=r'''  const LEARNING_TOPICS = {
    f0: {
      title:'F0（基本周波数）',
      text:'周期的な声帯振動の基本的な繰り返し周波数です。Hzで表し、知覚される声の高さと強く関係します。ただし、声道の共鳴を表すF1〜F3とは別の量です。',
      example:()=>`いまのF0は ${Math.round(Number(f0El.value))} Hz。スライダーを動かして、母音らしさをなるべく保ったまま高さがどう変わるか聴いてみよう。`,
      sources:[
        {label:'Praat Manual — frequency',url:'https://www.fon.hum.uva.nl/praat/manual/frequency.html'},
        {label:'Oxford — Source–Filter Theory',url:'https://doi.org/10.1093/acrefore/9780199384655.013.894'}
      ]
    },
    f1: {
      title:'F1（第1フォルマント）',
      text:'第1フォルマントの中心周波数です。母音では母音の高さと逆方向に強く関係し、一般にF1が高いほど低い舌位置・大きい口の開きに対応する傾向があります。ただし、声道全体の共鳴の結果なので単純な1対1対応ではありません。',
      example:()=>{ const v=interpolate('F1',duration()/2); return `中央付近のF1は ${v==null?'—':Math.round(v)+' Hz'}。F1の線だけ上下に動かして比較してみよう。`; },
      sources:[
        {label:'MIT OCW 24.901 — Lecture 8',url:'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/resources/mit24_901f10_lec08/'},
        {label:'Macquarie — Vocal Tract Resonance',url:'https://www.mq.edu.au/faculty-of-medicine-health-and-human-sciences/departments-and-schools/department-of-linguistics/our-research/phonetics-and-phonology/speech/acoustics/acoustic-theory-of-speech-production/vocal-tract-resonance'}
      ]
    },
    f2: {
      title:'F2（第2フォルマント）',
      text:'第2フォルマントの中心周波数です。母音では舌の前後位置や唇の丸めと強く関係します。一般にF2が低いほど後寄り、または円唇化した母音になりやすいですが、F1と同様に声道全体の共鳴の結果です。',
      example:()=>{ const v=interpolate('F2',duration()/2); return `中央付近のF2は ${v==null?'—':Math.round(v)+' Hz'}。F2だけを動かして、母音の聞こえ方がどう変わるか試そう。`; },
      sources:[
        {label:'MIT OCW 24.901 — Lecture 8',url:'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/resources/mit24_901f10_lec08/'},
        {label:'Macquarie — Vocal Tract Resonance',url:'https://www.mq.edu.au/faculty-of-medicine-health-and-human-sciences/departments-and-schools/department-of-linguistics/our-research/phonetics-and-phonology/speech/acoustics/acoustic-theory-of-speech-production/vocal-tract-resonance'}
      ]
    },
    f3: {
      title:'F3（第3フォルマント）',
      text:'第3フォルマントの中心周波数です。F1・F2とともに低い周波数側のスペクトル構造を記述する重要な値で、多くの母音では最初の3フォルマントがよく参照されます。F3の解釈は音・話者・文脈に依存するため、単純な舌位置の対応にはしません。',
      example:()=>{ const v=interpolate('F3',duration()/2); return `中央付近のF3は ${v==null?'—':Math.round(v)+' Hz'}。F1/F2をそのままにしてF3だけ変え、聞こえ方の違いを探してみよう。`; },
      sources:[
        {label:'MIT OCW 24.901 — Lecture 8',url:'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/resources/mit24_901f10_lec08/'},
        {label:'Praat Manual — Formant',url:'https://www.fon.hum.uva.nl/praat/manual/Formant.html'}
      ]
    },
    formant: {
      title:'フォルマント（formant）',
      text:'声道の共鳴によって音のスペクトルに現れる特徴的なピーク／共鳴周波数です。F1、F2、F3…は低い周波数側から順に数えます。Praatでは各フォルマントを中心周波数と帯域幅の組として時間ごとに扱います。',
      example:'Formantasiaの色つきのF1〜F3の線は、時間とともにフォルマント中心周波数がどう変わるかを描いたものです。',
      sources:[
        {label:'Oxford Phonetics — Source-Filter Model',url:'https://www.phon.ox.ac.uk/jcoleman/source_filter'},
        {label:'Praat Manual — Formant',url:'https://www.fon.hum.uva.nl/praat/manual/Formant.html'}
      ]
    },
    resonance: {
      title:'共鳴（resonance）',
      text:'ある周波数付近の振動に強く応答する性質です。声道は形によって複数の共鳴を持ち、その位置が音源のスペクトルを選択的に強めたり弱めたりします。声道の共鳴はフォルマントを理解する土台です。',
      example:'同じF0の音源でも、F1〜F3の位置を変えると聞こえる母音が変わるのは、声道フィルタの共鳴を変えたと考えると理解しやすいです。',
      sources:[
        {label:'Oxford Phonetics — Source-Filter Model',url:'https://www.phon.ox.ac.uk/jcoleman/source_filter'},
        {label:'Macquarie — Vocal Tract Resonance',url:'https://www.mq.edu.au/faculty-of-medicine-health-and-human-sciences/departments-and-schools/department-of-linguistics/our-research/phonetics-and-phonology/speech/acoustics/acoustic-theory-of-speech-production/vocal-tract-resonance'}
      ]
    },
    hz: {
      title:'Hz（ヘルツ）',
      text:'周波数のSI単位です。1 Hzは1秒あたり1回の周期・繰り返しに相当します。F0もフォルマント周波数もHzで表せますが、同じ単位でも表している現象は異なります。',
      example:()=>`いまF0は ${Math.round(Number(f0El.value))} Hz。たとえば140 Hzなら、周期的な音源が1秒あたり約140回くり返すという意味です。`,
      sources:[
        {label:'NIST — SI Units: Time / Frequency',url:'https://www.nist.gov/pml/owm/si-units-time'},
        {label:'Praat Manual — frequency',url:'https://www.fon.hum.uva.nl/praat/manual/frequency.html'}
      ]
    },
    spectrogram: {
      title:'スペクトログラム（spectrogram）',
      text:'音を「いつ・どの周波数に・どれくらいエネルギーがあるか」で表す時間–周波数表示です。一般に横軸が時間、縦軸が周波数で、濃さなどがエネルギーの強さを表します。',
      example:'Praatではスペクトログラムの暗い帯を見ながら母音のフォルマントを観察できます。Formantasiaはスペクトログラムそのものではなく、F1〜F3の軌跡を直接描く設計です。',
      sources:[
        {label:'Praat Manual — Spectrogram',url:'https://www.fon.hum.uva.nl/praat/manual/Spectrogram.html'},
        {label:'Praat Tutorial — Viewing a spectrogram',url:'https://www.fon.hum.uva.nl/praat/manual/Intro_3_1__Viewing_a_spectrogram.html'}
      ]
    },
    sourcefilter: {
      title:'音源–フィルタ理論（source–filter theory）',
      text:'音声を、まず音源を作る段階と、その音を声道の共鳴でフィルタする段階に分けて考えるモデルです。有声音では声帯振動が主要な音源となり、声道フィルタがスペクトルを形づくります。',
      example:'FormantasiaではF0が主に「音源」側、F1〜F3と帯域幅が主に「フィルタ」側の操作に対応します。これは学習用の単純化で、実際の発声では音源と声道が相互作用する場合もあります。',
      sources:[
        {label:'Oxford Research Encyclopedia — Source–Filter Theory',url:'https://doi.org/10.1093/acrefore/9780199384655.013.894'},
        {label:'Praat Manual — Source-filter synthesis',url:'https://www.fon.hum.uva.nl/praat/manual/Source-filter_synthesis.html'}
      ]
    },
    praat: {
      title:'Praat（プラート）',
      text:'音声の録音・表示・分析・合成・加工などを行える音声学用ソフトウェアです。University of AmsterdamのPaul Boersmaらによって開発・保守され、音声研究や教育で広く使われています。',
      example:'Formantasiaの「Praatへ書き出し」は、描いたF1〜F3の軌跡をPraat側でも扱いやすくするための連携機能です。',
      sources:[
        {label:'Praat official site',url:'https://praat.org/'},
        {label:'Praat Manual — Intro',url:'https://www.fon.hum.uva.nl/praat/manual/Intro.html'}
      ]
    },
    bandwidth: {
      title:'Bandwidth（帯域幅）',
      text:'各フォルマントの共鳴ピークが周波数方向にどれくらい広がっているかを表す量です。帯域幅が小さいほどピークは鋭く、帯域幅が大きいほど幅広い共鳴になります。PraatのFormantデータは中心周波数と帯域幅を持ちます。',
      example:()=>usingEmpiricalBandwidth()
        ? `いまは Empirical bandwidth。文献由来のB1〜B3を使い、QはF/Bから自動計算しています。`
        : `いまは Manual Q ${Number(qEl.value)}。この場合は bandwidth = F ÷ Q として合成しています。`,
      sources:[
        {label:'Praat Manual — Formant',url:'https://www.fon.hum.uva.nl/praat/manual/Formant.html'},
        {label:'Praat Manual — smoothest formant tracks',url:'https://www.fon.hum.uva.nl/praat/manual/Formants__Extract_smoothest_part___.html'}
      ]
    },
    q: {
      title:'Q（quality factor）',
      text:'共鳴の鋭さを表す無次元の指標です。2次の共振・バンドパス系では、中心周波数を帯域幅で割った比として扱え、高いQほど狭い帯域になります。Formantasiaのband-passフィルタでもQが大きいほど帯域が狭くなります。',
      example:()=>usingEmpiricalBandwidth()
        ? 'Empirical bandwidthでは各時点の中心周波数Fと帯域幅Bから Q=F/B を計算します。Manual Qでは共通Qを直接変えられます。'
        : `いまは Q=${Number(qEl.value)}。Qを上げ下げして、同じフォルマント位置でも共鳴の鋭さが変わるか聴き比べよう。`,
      sources:[
        {label:'OpenStax University Physics — Resonance and Q',url:'https://openstax.org/books/university-physics-volume-2/pages/15-5-resonance-in-an-ac-circuit'},
        {label:'Web Audio API — BiquadFilterNode',url:'https://webaudio.github.io/web-audio-api/#BiquadFilterNode'}
      ]
    },
    evidence: {
      title:'● 実測・△ 借用・┄ モデル',
      text:'これはFormantasia独自の表示規約です。●は採用した文献・データセットから直接得た値、△は別条件や別研究から借用した値、破線は補間・合成などアプリがモデル化した区間を示します。',
      example:()=>presetDirty
        ? 'いまは編集済み。元プリセットの根拠が灰色のゴーストとして残るので、「文献・モデル」と「自分の編集」を比べられます。'
        : 'プリセットを選び替えて、●の数や△・破線の割合がどう違うか見比べてみよう。',
      sources:[{label:'Formantasia — Evidence表示規約（アプリ内定義）'}]
    }
  };

  function learningEvidenceLabel'''
s2,n=re.subn(pattern,repl,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'learning topics: expected 1 match, found {n}')
s=s2

# Add source rendering to lower card.
replace_once("""    learningExplainExample.textContent=typeof item.example==='function'?item.example():item.example;
    if(learningPresetBadge) learningPresetBadge.textContent=learningEvidenceLabel();""", """    learningExplainExample.textContent=typeof item.example==='function'?item.example():item.example;
    renderLearningSources(learningExplainSources,item);
    if(learningPresetBadge) learningPresetBadge.textContent=learningEvidenceLabel();""", 'update lower sources')

# Add source renderer before panel updater.
replace_once('''  function updateLearningPanel(){''', '''  function renderLearningSources(container,item){
    if(!container) return;
    container.textContent='';
    const sources=(item && item.sources) || [];
    if(!sources.length){ container.hidden=true; return; }
    container.hidden=false;
    const prefix=document.createElement('span');
    prefix.textContent='出典：';
    container.appendChild(prefix);
    sources.forEach((source,index)=>{
      if(index){ const sep=document.createElement('span'); sep.className='learning-source-sep'; sep.textContent='·'; container.appendChild(sep); }
      if(source.url){
        const a=document.createElement('a'); a.href=source.url; a.target='_blank'; a.rel='noreferrer'; a.textContent=source.label; container.appendChild(a);
      }else{
        const span=document.createElement('span'); span.textContent=source.label; container.appendChild(span);
      }
    });
  }

  function updateLearningPanel(){''', 'source render function')

# Popover gets sources too.
replace_once("learningInfoPopover.innerHTML='<strong class=\"learning-popover-title\"></strong><p class=\"learning-popover-text\"></p><p class=\"learning-popover-example\"></p>';", "learningInfoPopover.innerHTML='<strong class=\"learning-popover-title\"></strong><p class=\"learning-popover-text\"></p><p class=\"learning-popover-example\"></p><div class=\"learning-popover-source\"></div>';", 'popover source markup')
replace_once("  const learningPopoverExample=learningInfoPopover.querySelector('.learning-popover-example');", "  const learningPopoverExample=learningInfoPopover.querySelector('.learning-popover-example');\n  const learningPopoverSources=learningInfoPopover.querySelector('.learning-popover-source');", 'popover source reference')
replace_once("""    learningPopoverExample.textContent=typeof item.example==='function'?item.example():item.example;
    learningInfoPopover.classList.add('visible');""", """    learningPopoverExample.textContent=typeof item.example==='function'?item.example():item.example;
    renderLearningSources(learningPopoverSources,item);
    learningInfoPopover.classList.add('visible');""", 'popover render sources')

path.write_text(s,encoding='utf-8')
print('Expanded sourced learning glossary with 13 terms.')
