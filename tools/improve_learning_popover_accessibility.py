#!/usr/bin/env python3
from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def replace_once(old: str, new: str, label: str) -> None:
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    s = s.replace(old, new, 1)


# Give the popover room for a visible close button.
replace_once(
    '    position:fixed; z-index:120; width:min(320px,calc(100vw - 24px)); padding:12px 14px;',
    '    position:fixed; z-index:120; width:min(320px,calc(100vw - 24px)); padding:12px 44px 12px 14px;',
    'popover padding',
)

# Add a clear, 30x30 close target. The visible glyph stays compact; aria-label supplies the name.
replace_once(
    '  .learning-popover.visible { opacity:1; transform:translateY(0) scale(1); pointer-events:auto; }\n  .learning-popover-title { display:block; margin:0 0 5px; font-size:13px; }',
    '  .learning-popover.visible { opacity:1; transform:translateY(0) scale(1); pointer-events:auto; }\n  .learning-popover-close {\n    position:absolute; top:8px; right:8px; width:30px; height:30px; min-width:30px; min-height:30px;\n    display:grid; place-items:center; padding:0; border-radius:50%; border:1px solid #cfd7e5;\n    background:#fff; color:#344054; font-size:20px; line-height:1; font-weight:700; box-shadow:none;\n  }\n  .learning-popover-close:hover { background:#eef3fa; transform:none; box-shadow:none; }\n  .learning-popover-title { display:block; margin:0 0 5px; font-size:13px; }',
    'close button css',
)

# Replace the timed status message with a non-modal dialog that has a labelled close button.
replace_once(
    "  const LEARNING_POPOVER_MS=10000;\n  const learningInfoPopover=document.createElement('aside');\n  learningInfoPopover.id='learningInfoPopover';\n  learningInfoPopover.className='learning-popover';\n  learningInfoPopover.setAttribute('role','status');\n  learningInfoPopover.setAttribute('aria-live','polite');\n  learningInfoPopover.innerHTML='<strong class=\"learning-popover-title\"></strong><span class=\"learning-popover-kicker\">ここを変えると？</span><p class=\"learning-popover-text\"></p><p class=\"learning-popover-example\"></p><button class=\"learning-popover-deep\" type=\"button\">📘 しくみを詳しく</button><div class=\"learning-popover-source\"></div>';\n  document.body.appendChild(learningInfoPopover);\n  const learningPopoverTitle=learningInfoPopover.querySelector('.learning-popover-title');",
    "  const learningInfoPopover=document.createElement('aside');\n  learningInfoPopover.id='learningInfoPopover';\n  learningInfoPopover.className='learning-popover';\n  learningInfoPopover.setAttribute('role','dialog');\n  learningInfoPopover.setAttribute('aria-modal','false');\n  learningInfoPopover.setAttribute('aria-labelledby','learningPopoverTitle');\n  learningInfoPopover.hidden=true;\n  learningInfoPopover.innerHTML='<button class=\"learning-popover-close\" type=\"button\" aria-label=\"閉じる\">×</button><strong class=\"learning-popover-title\" id=\"learningPopoverTitle\"></strong><span class=\"learning-popover-kicker\">ここを変えると？</span><p class=\"learning-popover-text\"></p><p class=\"learning-popover-example\"></p><button class=\"learning-popover-deep\" type=\"button\">📘 しくみを詳しく</button><div class=\"learning-popover-source\"></div>';\n  document.body.appendChild(learningInfoPopover);\n  const learningPopoverClose=learningInfoPopover.querySelector('.learning-popover-close');\n  const learningPopoverTitle=learningInfoPopover.querySelector('.learning-popover-title');",
    'popover dialog markup',
)

replace_once(
    "  let learningPopoverAnchor=null;\n  let learningPopoverTopic=null;\n  let learningPopoverTimer=null;",
    "  let learningPopoverAnchor=null;\n  let learningPopoverTopic=null;",
    'remove timer state',
)

replace_once(
    "  function hideLearningPopover(){\n    if(learningPopoverTimer){ clearTimeout(learningPopoverTimer); learningPopoverTimer=null; }\n    if(learningPopoverAnchor) learningPopoverAnchor.setAttribute('aria-expanded','false');\n    learningPopoverAnchor=null;\n    learningPopoverTopic=null;\n    learningInfoPopover.classList.remove('visible');\n  }",
    "  function hideLearningPopover(){\n    if(learningPopoverAnchor) learningPopoverAnchor.setAttribute('aria-expanded','false');\n    learningPopoverAnchor=null;\n    learningPopoverTopic=null;\n    learningInfoPopover.classList.remove('visible');\n    learningInfoPopover.hidden=true;\n  }",
    'remove timed hide logic',
)

replace_once(
    "    renderLearningSourceShort(learningPopoverSources,item);\n    learningInfoPopover.classList.add('visible');\n    positionLearningPopover();\n    requestAnimationFrame(positionLearningPopover);\n    if(learningPopoverTimer) clearTimeout(learningPopoverTimer);\n    learningPopoverTimer=setTimeout(hideLearningPopover,LEARNING_POPOVER_MS);",
    "    renderLearningSourceShort(learningPopoverSources,item);\n    learningInfoPopover.hidden=false;\n    learningInfoPopover.classList.add('visible');\n    positionLearningPopover();\n    requestAnimationFrame(()=>{\n      positionLearningPopover();\n      learningPopoverClose.focus();\n    });",
    'remove auto-dismiss and focus dialog',
)

# Explicit close returns focus to the triggering info button.
replace_once(
    "  learningPopoverDeep.addEventListener('click',()=>{",
    "  learningPopoverClose.addEventListener('click',()=>{\n    const anchor=learningPopoverAnchor;\n    hideLearningPopover();\n    if(anchor) anchor.focus();\n  });\n\n  learningPopoverDeep.addEventListener('click',()=>{",
    'close button handler',
)

# Escape also closes and returns focus to the trigger.
replace_once(
    "  document.addEventListener('keydown',e=>{ if(e.key==='Escape') hideLearningPopover(); });",
    "  document.addEventListener('keydown',e=>{\n    if(e.key!=='Escape' || learningInfoPopover.hidden) return;\n    const anchor=learningPopoverAnchor;\n    hideLearningPopover();\n    if(anchor) anchor.focus();\n  });",
    'escape focus restoration',
)

path.write_text(s, encoding='utf-8')
print('Improved learning popover accessibility: no timeout, dialog semantics, explicit close button.')
