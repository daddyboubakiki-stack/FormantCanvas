#!/usr/bin/env python3
from pathlib import Path
import re

path=Path('index.html')
s=path.read_text(encoding='utf-8')

if 'learningInfoPopover' in s:
    print('Learning info popover already present; no changes.')
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

# 1) Make the inline info controls unmistakably circular buttons and add a floating explanation card.
pattern=r'''  \.info-dot \{\n    display:inline-grid; place-items:center; width:17px; height:17px; margin-left:4px; border-radius:50%;\n    border:1px solid #bdc7d7; color:#5a6780; background:#fff; font-size:10px; font-weight:900; cursor:pointer; vertical-align:middle;\n  \}\n  \.info-dot:hover \{ background:#eef3fa; \}'''
repl='''  .info-dot {
    display:inline-grid; place-items:center; width:27px; height:27px; min-width:27px; min-height:27px;
    margin:-5px 0 -5px 5px; padding:0; border-radius:50%; border:1px solid #aebbd0;
    color:#465673; background:#fff; font-size:13px; line-height:1; font-weight:900; cursor:pointer;
    vertical-align:middle; box-shadow:0 2px 7px rgba(36,54,88,.10); transform:none!important;
  }
  .info-dot:hover { background:#eef3fa; border-color:#8fa1be; box-shadow:0 4px 10px rgba(36,54,88,.14); }
  .info-dot:focus-visible { outline:3px solid rgba(79,140,255,.28); outline-offset:2px; }
  .info-dot[aria-expanded="true"] { background:#e7eefb; border-color:#7f94b8; color:#253b61; }

  .learning-popover {
    position:fixed; z-index:120; width:min(320px,calc(100vw - 24px)); padding:12px 14px;
    border:1px solid #d5ddeb; border-radius:15px; background:rgba(255,255,255,.98);
    box-shadow:0 16px 42px rgba(28,42,71,.18); backdrop-filter:blur(12px);
    opacity:0; transform:translateY(5px) scale(.985); pointer-events:none;
    transition:opacity .22s ease, transform .22s ease; color:var(--text);
  }
  .learning-popover.visible { opacity:1; transform:translateY(0) scale(1); pointer-events:auto; }
  .learning-popover-title { display:block; margin:0 0 5px; font-size:13px; }
  .learning-popover-text, .learning-popover-example { margin:0; font-size:11.5px; line-height:1.6; color:#515c70; }
  .learning-popover-example { margin-top:7px; padding-top:7px; border-top:1px dashed #d2d9e5; color:#687489; }
  @media (prefers-reduced-motion: reduce) {
    .learning-popover { transition:none; }
  }'''
regex_once(pattern,repl,'replace info-dot CSS')

# 2) Use real button elements instead of span elements pretending to be buttons.
pattern=r'<span class="info-dot learning-only" tabindex="0" role="button" data-learn-topic="([^"]+)" aria-label="([^"]+)">i</span>'
s,n=re.subn(pattern,r'<button class="info-dot learning-only" type="button" data-learn-topic="\1" aria-label="\2" aria-expanded="false">i</button>',s)
if n<1:
    raise SystemExit('convert info dots to buttons: expected at least 1 match')

# 3) Add floating popover behavior while preserving the existing lower learning card.
old='''  document.querySelectorAll('[data-learn-topic]').forEach(el=>{
    const activate=()=>{
      chooseLearningTopic(el.dataset.learnTopic);
      if(el.classList.contains('info-dot') && learningCard) learningCard.scrollIntoView({behavior:'smooth',block:'nearest'});
    };
    el.addEventListener('click',activate);
    if(el.classList.contains('info-dot')) el.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); activate(); } });
  });'''
new='''  const LEARNING_POPOVER_MS=10000;
  const learningInfoPopover=document.createElement('aside');
  learningInfoPopover.id='learningInfoPopover';
  learningInfoPopover.className='learning-popover';
  learningInfoPopover.setAttribute('role','status');
  learningInfoPopover.setAttribute('aria-live','polite');
  learningInfoPopover.innerHTML='<strong class="learning-popover-title"></strong><p class="learning-popover-text"></p><p class="learning-popover-example"></p>';
  document.body.appendChild(learningInfoPopover);
  const learningPopoverTitle=learningInfoPopover.querySelector('.learning-popover-title');
  const learningPopoverText=learningInfoPopover.querySelector('.learning-popover-text');
  const learningPopoverExample=learningInfoPopover.querySelector('.learning-popover-example');
  let learningPopoverAnchor=null;
  let learningPopoverTimer=null;

  function positionLearningPopover(){
    if(!learningPopoverAnchor || !learningInfoPopover.classList.contains('visible')) return;
    const r=learningPopoverAnchor.getBoundingClientRect();
    const p=learningInfoPopover.getBoundingClientRect();
    const gap=12, margin=12;
    let left, top=r.top + r.height/2 - p.height/2;
    const roomRight=window.innerWidth-r.right;
    const roomLeft=r.left;
    if(roomRight>=p.width+gap+margin){
      left=r.right+gap;
    }else if(roomLeft>=p.width+gap+margin){
      left=r.left-p.width-gap;
    }else{
      left=r.left+r.width/2-p.width/2;
      top=r.bottom+gap;
      if(top+p.height>window.innerHeight-margin) top=r.top-p.height-gap;
    }
    left=Math.max(margin,Math.min(left,window.innerWidth-p.width-margin));
    top=Math.max(margin,Math.min(top,window.innerHeight-p.height-margin));
    learningInfoPopover.style.left=`${Math.round(left)}px`;
    learningInfoPopover.style.top=`${Math.round(top)}px`;
  }

  function hideLearningPopover(){
    if(learningPopoverTimer){ clearTimeout(learningPopoverTimer); learningPopoverTimer=null; }
    if(learningPopoverAnchor) learningPopoverAnchor.setAttribute('aria-expanded','false');
    learningPopoverAnchor=null;
    learningInfoPopover.classList.remove('visible');
  }

  function showLearningPopover(anchor,topic){
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
    learningPopoverText.textContent=item.text;
    learningPopoverExample.textContent=typeof item.example==='function'?item.example():item.example;
    learningInfoPopover.classList.add('visible');
    positionLearningPopover();
    requestAnimationFrame(positionLearningPopover);
    if(learningPopoverTimer) clearTimeout(learningPopoverTimer);
    learningPopoverTimer=setTimeout(hideLearningPopover,LEARNING_POPOVER_MS);
  }

  document.querySelectorAll('[data-learn-topic]').forEach(el=>{
    el.addEventListener('click',()=>{
      const topic=el.dataset.learnTopic;
      chooseLearningTopic(topic);
      if(el.classList.contains('info-dot')) showLearningPopover(el,topic);
    });
  });
  document.addEventListener('keydown',e=>{ if(e.key==='Escape') hideLearningPopover(); });
  window.addEventListener('resize',positionLearningPopover);
  window.addEventListener('scroll',positionLearningPopover,true);'''
replace_once(old,new,'replace learning topic event behavior')

# 4) Never leave a learning popover floating when the user leaves Learning mode.
old="""    uiMode = ['casual','learning','research'].includes(next) ? next : 'casual';
    document.body.dataset.uiMode=uiMode;"""
new="""    uiMode = ['casual','learning','research'].includes(next) ? next : 'casual';
    if(uiMode!=='learning') hideLearningPopover();
    document.body.dataset.uiMode=uiMode;"""
replace_once(old,new,'hide popover outside learning mode')

path.write_text(s,encoding='utf-8')
print(f'Upgraded {n} learning info controls with circular buttons and 10-second side popovers.')
