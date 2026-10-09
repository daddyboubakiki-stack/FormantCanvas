from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

# Make the three setting info buttons explicitly operation-help controls.
replacements = {
    'aria-label="F0の説明"': 'aria-label="F0を変えるとどうなる？"',
    'aria-label="帯域幅の説明"': 'aria-label="帯域幅モードを変えるとどうなる？"',
    'aria-label="Qの説明"': 'aria-label="Qを変えるとどうなる？"',
}
for old, new in replacements.items():
    if old not in html:
        raise SystemExit(f'missing marker: {old}')
    html = html.replace(old, new, 1)

# Add operation-specific copy. The lower glossary remains scientifically layered and unchanged.
marker = "  const LEARNING_POPOVER_MS=10000;\n"
if marker not in html:
    raise SystemExit('popover marker not found')

control_help = r'''  // Operation help is intentionally separate from glossary definitions.
  // The round (i) answers "what happens if I change this control?";
  // the lower learning card answers "what does this term mean?".
  const CONTROL_HELP = {
    f0: {
      title:'基本周波数 F0',
      lead:'声の高さが変わります。',
      detail:()=>`上げる → 高い声 ／ 下げる → 低い声。いまは ${Math.round(Number(f0El.value))} Hz です。F1〜F3の線そのものは動きません。`,
      deepLabel:'F0のしくみを詳しく'
    },
    bandwidth: {
      title:'帯域幅モード',
      lead:'声の「響きの鋭さ」を、文献値に任せるか自分で調整するかを切り替えます。',
      detail:()=>usingEmpiricalBandwidth()
        ? 'いまは Empirical bandwidth。文献由来の帯域幅を使い、Qは自動で決まります。Manual Qにすると下のQつまみを動かせます。'
        : 'いまは Manual Q。下のQつまみで響きの鋭さを自分で変えられます。Empirical bandwidthにすると文献由来の値へ戻ります。',
      deepLabel:'Bandwidthのしくみを詳しく'
    },
    q: {
      title:'Manual Q',
      lead:'声の響きが、キュッと鋭くなったり、ふわっと広がったりします。',
      detail:()=>usingEmpiricalBandwidth()
        ? 'いまは Empirical bandwidth なので、このつまみは自動計算になっていて動かせません。Manual Qへ切り替えると調整できます。'
        : `Qを上げる → 鋭く ／ 下げる → 広くなだらかに。いまは Q=${Number(qEl.value)} です。`,
      deepLabel:'Qのしくみを詳しく'
    }
  };

'''
html = html.replace(marker, control_help + marker, 1)

old_inner = '''  learningInfoPopover.innerHTML='<strong class="learning-popover-title"></strong><span class="learning-popover-kicker">ひとことで</span><p class="learning-popover-text"></p><span class="learning-popover-kicker">もう少し</span><p class="learning-popover-example"></p><div class="learning-popover-source"></div>';'''
new_inner = '''  learningInfoPopover.innerHTML='<strong class="learning-popover-title"></strong><span class="learning-popover-kicker">ここを変えると？</span><p class="learning-popover-text"></p><p class="learning-popover-example"></p><button class="learning-popover-deep" type="button">📘 しくみを詳しく</button><div class="learning-popover-source"></div>';'''
if old_inner not in html:
    raise SystemExit('old popover innerHTML not found')
html = html.replace(old_inner, new_inner, 1)

old_const = "  const learningPopoverSources=learningInfoPopover.querySelector('.learning-popover-source');\n  let learningPopoverAnchor=null;\n  let learningPopoverTimer=null;\n"
new_const = "  const learningPopoverSources=learningInfoPopover.querySelector('.learning-popover-source');\n  const learningPopoverDeep=learningInfoPopover.querySelector('.learning-popover-deep');\n  let learningPopoverAnchor=null;\n  let learningPopoverTopic=null;\n  let learningPopoverTimer=null;\n"
if old_const not in html:
    raise SystemExit('popover const marker not found')
html = html.replace(old_const, new_const, 1)

old_hide = """    if(learningPopoverAnchor) learningPopoverAnchor.setAttribute('aria-expanded','false');
    learningPopoverAnchor=null;
    learningInfoPopover.classList.remove('visible');
"""
new_hide = """    if(learningPopoverAnchor) learningPopoverAnchor.setAttribute('aria-expanded','false');
    learningPopoverAnchor=null;
    learningPopoverTopic=null;
    learningInfoPopover.classList.remove('visible');
"""
if old_hide not in html:
    raise SystemExit('hide marker not found')
html = html.replace(old_hide, new_hide, 1)

old_show = """  function showLearningPopover(anchor,topic){
    if(uiMode!=='learning' || !LEARNING_TOPICS[topic]) return;
    if(learningPopoverAnchor===anchor && learningInfoPopover.classList.contains('visible')){
      hideLearningPopover();
      return;
    }
    if(learningPopoverAnchor) learningPopoverAnchor.setAttribute('aria-expanded','false');
    const item=LEARNING_TOPICS[topic];
    learningPopoverAnchor=anchor;
    anchor.setAttribute('aria-expanded','true');
    learningPopoverTitle.textContent=item.title;
    learningPopoverText.textContent=typeof item.one==='function'?item.one():item.one;
    learningPopoverExample.textContent=typeof item.more==='function'?item.more():item.more;
    renderLearningSourceShort(learningPopoverSources,item);
    learningInfoPopover.classList.add('visible');
    positionLearningPopover();
    requestAnimationFrame(positionLearningPopover);
    if(learningPopoverTimer) clearTimeout(learningPopoverTimer);
    learningPopoverTimer=setTimeout(hideLearningPopover,LEARNING_POPOVER_MS);
  }
"""
new_show = """  function showLearningPopover(anchor,topic){
    if(uiMode!=='learning' || !LEARNING_TOPICS[topic] || !CONTROL_HELP[topic]) return;
    if(learningPopoverAnchor===anchor && learningInfoPopover.classList.contains('visible')){
      hideLearningPopover();
      return;
    }
    if(learningPopoverAnchor) learningPopoverAnchor.setAttribute('aria-expanded','false');
    const item=LEARNING_TOPICS[topic];
    const help=CONTROL_HELP[topic];
    learningPopoverAnchor=anchor;
    learningPopoverTopic=topic;
    anchor.setAttribute('aria-expanded','true');
    learningPopoverTitle.textContent=help.title;
    learningPopoverText.textContent=typeof help.lead==='function'?help.lead():help.lead;
    learningPopoverExample.textContent=typeof help.detail==='function'?help.detail():help.detail;
    learningPopoverDeep.textContent=`📘 ${help.deepLabel || 'しくみを詳しく'}`;
    renderLearningSourceShort(learningPopoverSources,item);
    learningInfoPopover.classList.add('visible');
    positionLearningPopover();
    requestAnimationFrame(positionLearningPopover);
    if(learningPopoverTimer) clearTimeout(learningPopoverTimer);
    learningPopoverTimer=setTimeout(hideLearningPopover,LEARNING_POPOVER_MS);
  }

  learningPopoverDeep.addEventListener('click',()=>{
    const topic=learningPopoverTopic;
    if(!topic) return;
    chooseLearningTopic(topic);
    hideLearningPopover();
    if(learningCard) learningCard.scrollIntoView({behavior:'smooth',block:'start'});
  });
"""
if old_show not in html:
    raise SystemExit('showLearningPopover block not found')
html = html.replace(old_show, new_show, 1)

# Add styling for the bridge from operation help to glossary.
style_marker = "  .learning-popover-source { margin-top:8px; padding-top:7px; border-top:1px solid #e1e6ef; color:#7b8495; font-size:9.8px; line-height:1.5; }\n"
style_add = """  .learning-popover-deep {
    margin-top:9px; padding:6px 9px; border-radius:10px; border:1px solid #d8e0ed;
    background:#f7f9fc; color:#44516a; font-size:10.5px; font-weight:800; box-shadow:none;
  }
  .learning-popover-deep:hover { background:#eef3fa; transform:none; box-shadow:none; }
"""
if style_marker not in html:
    raise SystemExit('popover style marker not found')
html = html.replace(style_marker, style_marker + style_add, 1)

path.write_text(html, encoding='utf-8')
print('Separated round info-button operation help from the lower glossary.')
