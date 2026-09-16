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


def replace_count(old: str, new: str, expected: int, label: str) -> None:
    global s
    count = s.count(old)
    if count != expected:
        raise SystemExit(f'{label}: expected {expected} matches, found {count}')
    s = s.replace(old, new)


# 1) Do not block browser zoom / pinch zoom.
replace_once(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0" />',
    'viewport zoom',
)

# 2) Improve text contrast without changing research data or synthesis values.
replace_once('    --muted: #747b8c;', '    --muted: #667085;', 'muted color')
replace_count('color:#9097a6', 'color:#667085', 2, 'section kicker colors')
replace_once('color:#9299a7!important', 'color:#667085!important', 'citation note color')
replace_once('color:#8a91a0', 'color:#667085', 'site signature color')
replace_once('color:#778198', 'color:#667085', 'compare kicker color')
replace_once('color:#7a8497', 'color:#667085', 'compare note color')
replace_once('color:#7b8495', 'color:#667085', 'popover source color')
replace_count("gctx.fillStyle = '#81889a';", "gctx.fillStyle = '#667085';", 2, 'canvas axis label color')
replace_once("dctx.fillStyle='rgba(89,97,116,.72)';", "dctx.fillStyle='#596174';", 'canvas timing label color')

# Keep the F1/F2/F3 line colors, but use darker same-hue fills for selected buttons
# so their white labels meet normal-text contrast requirements.
replace_once('.track-btn[data-track="F1"].active { background:var(--f1); }', '.track-btn[data-track="F1"].active { background:#c92f4e; }', 'F1 active button')
replace_once('.track-btn[data-track="F2"].active { background:var(--f2); }', '.track-btn[data-track="F2"].active { background:#2563eb; }', 'F2 active button')
replace_once('.track-btn[data-track="F3"].active { background:var(--f3); }', '.track-btn[data-track="F3"].active { background:#7c3aed; }', 'F3 active button')

# 3) Give all ordinary interactive controls a strong, consistent keyboard focus ring.
replace_once(
    '  button:active { transform:translateY(0); }\n  button.active { color:#fff; border-color:transparent; }',
    '  button:active { transform:translateY(0); }\n  button:focus-visible, select:focus-visible, input:focus-visible, summary:focus-visible, a:focus-visible {\n    outline:3px solid #1d4ed8; outline-offset:3px;\n  }\n  button.active { color:#fff; border-color:transparent; }',
    'global focus ring',
)
replace_once(
    '  .info-dot:focus-visible { outline:3px solid rgba(79,140,255,.28); outline-offset:2px; }',
    '  .info-dot:focus-visible { outline:3px solid #1d4ed8; outline-offset:3px; }',
    'info focus ring',
)

# 4) Give settings controls explicit accessible names.
replace_once(
    '<input id="duration" type="range" min="0.04" max="8" step="0.001" value="0.600" />',
    '<input id="duration" type="range" min="0.04" max="8" step="0.001" value="0.600" aria-label="再生時間" />',
    'duration label',
)
replace_once(
    '<input id="f0" type="range" min="70" max="500" step="1" value="140" />',
    '<input id="f0" type="range" min="70" max="500" step="1" value="140" aria-label="声の高さ・基本周波数 F0" />',
    'F0 label',
)
replace_once(
    '<input id="maxHz" type="range" min="2500" max="6000" step="250" value="4000" />',
    '<input id="maxHz" type="range" min="2500" max="6000" step="250" value="4000" aria-label="最大周波数" />',
    'max Hz label',
)
replace_once(
    '<select id="bandwidthMode">',
    '<select id="bandwidthMode" aria-label="帯域幅モード">',
    'bandwidth mode label',
)
replace_once(
    '<input id="q" type="range" min="2" max="25" step="1" value="10" />',
    '<input id="q" type="range" min="2" max="25" step="1" value="10" aria-label="Manual Q" />',
    'Q label',
)
replace_once(
    '<input id="stabilize" type="range" min="0" max="100" step="1" value="72" />',
    '<input id="stabilize" type="range" min="0" max="100" step="1" value="72" aria-label="手ブレ補正" />',
    'stabilize label',
)

# 5) Expose selected tool/topic state to assistive technology.
replace_once(
    '  <div class="toolbar">',
    '  <div class="toolbar" role="group" aria-label="描画ツール">',
    'toolbar group label',
)
replace_once(
    '    <button class="track-btn active" data-track="F1"><span class="casual-only">F1 低め</span><span class="learning-plus">F1 を描く</span></button>',
    '    <button class="track-btn active" data-track="F1" type="button" aria-pressed="true"><span class="casual-only">F1 低め</span><span class="learning-plus">F1 を描く</span></button>',
    'F1 pressed state',
)
replace_once(
    '    <button class="track-btn" data-track="F2"><span class="casual-only">F2 まんなか</span><span class="learning-plus">F2 を描く</span></button>',
    '    <button class="track-btn" data-track="F2" type="button" aria-pressed="false"><span class="casual-only">F2 まんなか</span><span class="learning-plus">F2 を描く</span></button>',
    'F2 pressed state',
)
replace_once(
    '    <button class="track-btn" data-track="F3"><span class="casual-only">F3 高め</span><span class="learning-plus">F3 を描く</span></button>',
    '    <button class="track-btn" data-track="F3" type="button" aria-pressed="false"><span class="casual-only">F3 高め</span><span class="learning-plus">F3 を描く</span></button>',
    'F3 pressed state',
)
replace_once(
    '    <button id="eraserBtn" class="eraser">消しゴム</button>',
    '    <button id="eraserBtn" class="eraser" type="button" aria-pressed="false">消しゴム</button>',
    'eraser pressed state',
)
replace_once(
    "    document.querySelectorAll('.track-btn').forEach(b=>b.classList.toggle('active', b.dataset.track===name));\n    document.getElementById('eraserBtn').classList.remove('active');",
    "    document.querySelectorAll('.track-btn').forEach(b=>{\n      const selected=b.dataset.track===name;\n      b.classList.toggle('active',selected);\n      b.setAttribute('aria-pressed',String(selected));\n    });\n    const eraserBtn=document.getElementById('eraserBtn');\n    eraserBtn.classList.remove('active');\n    eraserBtn.setAttribute('aria-pressed','false');",
    'setActiveTrack aria state',
)
replace_once(
    "    document.querySelectorAll('.track-btn').forEach(b=>b.classList.remove('active'));\n    document.getElementById('eraserBtn').classList.add('active');",
    "    document.querySelectorAll('.track-btn').forEach(b=>{ b.classList.remove('active'); b.setAttribute('aria-pressed','false'); });\n    const eraserBtn=document.getElementById('eraserBtn');\n    eraserBtn.classList.add('active');\n    eraserBtn.setAttribute('aria-pressed','true');",
    'eraser aria state',
)
replace_once(
    "    document.querySelectorAll('[data-learn-topic].learning-topic').forEach(btn=>btn.classList.toggle('active',btn.dataset.learnTopic===learningTopic));",
    "    document.querySelectorAll('[data-learn-topic].learning-topic').forEach(btn=>{\n      const selected=btn.dataset.learnTopic===learningTopic;\n      btn.classList.toggle('active',selected);\n      btn.setAttribute('aria-pressed',String(selected));\n    });",
    'learning topic aria state',
)
replace_once(
    '    return `<button class="compare-choice${active}" type="button" data-compare-key="${key}"><strong>${title}</strong><span class="metric">${metric}</span><span class="listen">▶ 聴く</span></button>`;',
    '    return `<button class="compare-choice${active}" type="button" data-compare-key="${key}" aria-pressed="${compareCurrentKey===key}"><strong>${title}</strong><span class="metric">${metric}</span><span class="listen">▶ 聴く</span></button>`;',
    'compare card aria state',
)

path.write_text(s, encoding='utf-8')
print('Applied Formantasia accessibility quick fixes.')
