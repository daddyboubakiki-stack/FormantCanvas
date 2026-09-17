from pathlib import Path
import re

INDEX = Path('index.html')
STATE = Path('PROJECT_STATE.md')
DECISIONS = Path('DECISIONS.md')

html = INDEX.read_text(encoding='utf-8')
original = html


def replace_once(text, old, new, label):
    if old not in text:
        raise AssertionError(f'missing target for {label}')
    if text.count(old) != 1:
        raise AssertionError(f'expected exactly one target for {label}, found {text.count(old)}')
    return text.replace(old, new, 1)


# Protect the research-value/data block during this UI-only task.
protected_match = re.search(r"  const JA_MT_BW = \{.*?\n  let YK2019_DATA = null;", html, flags=re.S)
if not protected_match:
    raise AssertionError('protected research block not found')
protected_before = protected_match.group(0)

# 1) Research Preview: compact in casual/learning, full notice in research.
old_preview = '''  <div class="public-preview-banner" role="note" aria-label="Research preview notice">
    <span class="preview-pill">Research Preview</span>
    <strong>Development Version</strong>
    <span>教育・実験用。プリセットには公表された文献値とアプリによるモデル区間が含まれます。根拠の詳細は🔬研究モードで確認できます。</span>
  </div>'''
new_preview = '''  <div class="public-preview-banner research-only" role="note" aria-label="Research preview notice">
    <span class="preview-pill">Research Preview</span>
    <strong>Development Version</strong>
    <span>教育・実験用。プリセットには公表された文献値とアプリによるモデル区間が含まれます。この研究モードでは、各プリセットの根拠と近似方法を確認できます。</span>
  </div>
  <details class="public-preview-compact">
    <summary>Research Preview ⓘ</summary>
    <p>Formantasiaは現在開発中の教育・実験用アプリです。プリセットには公表された文献値とアプリによるモデル区間が含まれます。詳しい根拠は🔬研究モードで確認できます。</p>
  </details>'''
html = replace_once(html, old_preview, new_preview, 'research preview')

# 2) Friendlier casual-only preset labels without changing IDs or behavior.
html = replace_once(
    html,
    '      <label for="presetLanguage">言語</label>',
    '      <label for="presetLanguage"><span class="casual-only">ことば</span><span class="learning-plus">言語</span></label>',
    'language label',
)
html = replace_once(
    html,
    '      <label for="voiceType">話者</label>',
    '      <label for="voiceType"><span class="casual-only">だれの声？</span><span class="learning-plus">話者</span></label>',
    'voice label',
)
html = replace_once(
    html,
    '      <label for="vowelPreset">母音 <span class="research-only" style="font-size:10px;color:var(--muted)">auto</span></label>',
    '      <label for="vowelPreset"><span class="casual-only">どの音？</span><span class="learning-plus">母音 <span class="research-only" style="font-size:10px;color:var(--muted)">auto</span></span></label>',
    'vowel label',
)

# 3) Canvas hero: preset selector + canvas become one primary workspace.
selector_anchor = '  <div class="selector-bar" aria-label="Voice preset controls">'
html = replace_once(
    html,
    selector_anchor,
    '  <section class="canvas-hero" aria-label="声をえがくキャンバス">\n' + selector_anchor,
    'canvas hero opening',
)

compare_pattern = re.compile(
    r'\n  <section class="beginner-compare" id="beginnerCompareWrap" hidden aria-label="同じ母音のくらべ聴き">.*?\n  </section>\n',
    flags=re.S,
)
compare_match = compare_pattern.search(html)
if not compare_match:
    raise AssertionError('beginner comparison section not found')
compare_block = compare_match.group(0).strip('\n')
html = html[:compare_match.start()] + '\n' + html[compare_match.end():]

canvas_tail = '''    <div class="canvas-wrap" id="canvasWrap">
      <canvas id="gridCanvas"></canvas>
      <canvas id="drawCanvas"></canvas>
    </div>
  </div>

  <div class="settings">'''
canvas_tail_new = '''    <div class="canvas-wrap" id="canvasWrap">
      <canvas id="gridCanvas"></canvas>
      <canvas id="drawCanvas"></canvas>
      <div id="canvasEmptyHint" class="canvas-empty-hint casual-only" aria-hidden="true">
        <span class="canvas-empty-hint-mark">✏️</span>
        <span>ここに線をかいて、声のひびきを聴いてみよう</span>
      </div>
    </div>
  </div>
  </section>

''' + compare_block + '''

  <div class="settings">'''
html = replace_once(html, canvas_tail, canvas_tail_new, 'canvas hero closing and empty hint')

# 4) Visual overrides live in one clearly marked block so the monolithic file stays reviewable.
design_css = r'''

  /* Design polish v1 — 2026-09-17
     Warm casual mode, canvas-as-hero hierarchy, mobile two-row controller,
     readable type scale, and compact Research Preview. */
  .public-preview-compact {
    margin:0 0 10px; padding:7px 10px; border:1px solid rgba(216,221,234,.8);
    border-radius:12px; background:rgba(255,255,255,.58); color:#667085;
    font-size:12px; line-height:1.55;
  }
  .public-preview-compact summary { width:max-content; max-width:100%; cursor:pointer; font-weight:800; color:#697184; }
  .public-preview-compact summary:hover { color:#404756; }
  .public-preview-compact p { margin:7px 2px 2px; max-width:760px; }
  body[data-ui-mode="research"] .public-preview-compact { display:none; }

  .canvas-hero {
    position:relative; margin:0 0 14px; border:1px solid var(--border); border-radius:24px;
    background:#fff; box-shadow:0 18px 46px rgba(30,42,75,.10);
    transition:box-shadow .18s ease, border-color .18s ease;
  }
  .canvas-hero .selector-bar {
    margin:0; border:0; border-radius:23px 23px 0 0; border-bottom:1px solid var(--border);
    box-shadow:none; background:rgba(255,255,255,.94); position:sticky; top:10px; z-index:45;
  }
  .canvas-hero .canvas-card { border:0; border-radius:0 0 23px 23px; box-shadow:none; overflow:hidden; }
  .canvas-hero .canvas-top { background:rgba(249,250,253,.72); }
  .canvas-hero .canvas-wrap { min-height:380px; }
  .canvas-hero:focus-within { box-shadow:0 20px 52px rgba(30,42,75,.13); }

  .canvas-empty-hint {
    position:absolute; left:50%; top:50%; z-index:4; width:min(420px,78%);
    transform:translate(-50%,-50%); text-align:center; color:#9b837d;
    font-size:14px; font-weight:700; line-height:1.7; pointer-events:none;
    opacity:0; visibility:hidden; transition:opacity .18s ease, transform .18s ease;
  }
  .canvas-empty-hint.is-visible { opacity:1; visibility:visible; transform:translate(-50%,-50%) scale(1); }
  .canvas-empty-hint-mark { display:block; margin-bottom:5px; font-size:20px; opacity:.8; }

  body[data-ui-mode="casual"] {
    background:linear-gradient(180deg,#fdfbf7,#f8f4ee);
  }
  body[data-ui-mode="casual"] .toolbar,
  body[data-ui-mode="casual"] .settings,
  body[data-ui-mode="casual"] .bottom,
  body[data-ui-mode="casual"] .selector-bar,
  body[data-ui-mode="casual"] .casual-export-panel {
    background:rgba(255,252,248,.94); border-color:#eadfda;
    box-shadow:0 10px 32px rgba(112,82,68,.065);
  }
  body[data-ui-mode="casual"] .mode-switch { background:rgba(255,250,246,.96); border-color:#eadfda; }
  body[data-ui-mode="casual"] .mode-btn.active { background:#a85f71; color:#fff; }
  body[data-ui-mode="casual"] .canvas-hero {
    border-color:#eadfda; background:#fffdf9; box-shadow:0 18px 46px rgba(112,82,68,.09);
  }
  body[data-ui-mode="casual"] .canvas-hero:focus-within { box-shadow:0 20px 52px rgba(112,82,68,.12); }
  body[data-ui-mode="casual"] .canvas-hero .selector-bar {
    background:rgba(255,252,248,.96); border-bottom-color:#eadfda;
  }
  body[data-ui-mode="casual"] .canvas-hero .canvas-card { background:#fffdf9; }
  body[data-ui-mode="casual"] .canvas-hero .canvas-top { background:rgba(253,249,245,.82); }
  body[data-ui-mode="casual"] .canvas-wrap { background:#fffdf9; }
  body[data-ui-mode="casual"] .casual-tip { color:#7c6b68; }
  body[data-ui-mode="casual"] .public-preview-compact {
    background:rgba(255,252,248,.62); border-color:#eadfda; color:#7c706c;
  }

  /* Readability: explanatory and interactive text should not be metadata-sized. */
  .mode-export-copy p, .casual-export-copy p { font-size:12px; line-height:1.6; }
  .ev-key, .evidence-toggle { font-size:12px; }
  .advanced-panel::before { font-size:11px; }
  .reset-preset { padding:7px 10px; font-size:12px; }
  .setting-note { font-size:11px; line-height:1.45; }
  .compare-choice .kicker { font-size:11px; }
  .compare-choice .metric, .compare-choice .listen { font-size:12px; }
  .compare-note { font-size:11.5px; line-height:1.6; }
  .learning-source, .learning-source-heading { font-size:11.5px; }
  .learning-citation-note { font-size:10.5px!important; }
  .learning-popover-kicker { font-size:10px; }
  .learning-popover-text, .learning-popover-example { font-size:12px; }
  .learning-popover-source { font-size:10.5px; }
  .learning-popover-deep { font-size:11.5px; }

  @media (prefers-reduced-motion: reduce) {
    .canvas-hero, .canvas-empty-hint { transition:none; }
  }

  @media (max-width:820px) {
    body { padding-bottom:210px; }
    .mode-btn { padding:7px 10px; font-size:12px; white-space:nowrap; }
    .canvas-hero { border-radius:20px; }
    .canvas-hero .canvas-card { border-radius:19px; }
    .canvas-hero .selector-bar {
      position:fixed; left:10px; right:10px; top:auto; bottom:10px; z-index:50; margin:0 auto;
      max-width:calc(1120px - 20px); padding:10px; border:1px solid var(--border); border-radius:18px;
      grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr) 48px;
      grid-template-rows:auto auto; gap:7px 8px;
      box-shadow:0 14px 40px rgba(20,30,55,.20);
    }
    body[data-ui-mode="casual"] .canvas-hero .selector-bar { border-color:#eadfda; }
    .canvas-hero .selector-bar::before { display:none; }
    .canvas-hero .selector-bar .mini-control:nth-of-type(1) { grid-column:1; grid-row:1; }
    .canvas-hero .selector-bar .mini-control:nth-of-type(2) { grid-column:2 / 4; grid-row:1; }
    .canvas-hero .selector-bar .mini-control:nth-of-type(3) { grid-column:1 / 3; grid-row:2; }
    .canvas-hero .selector-bar .selector-actions { grid-column:3; grid-row:2; align-self:end; }
    .mini-control label { font-size:11px; margin-bottom:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .mini-control select { min-height:42px; padding:7px 9px; font-size:12px; }
  }

  @media (max-width:520px) {
    .canvas-hero .selector-bar { left:8px; right:8px; bottom:8px; padding:9px; gap:6px 7px; }
    .canvas-hero .transport-btn { width:44px; height:44px; min-width:44px; min-height:44px; }
  }
'''
if '/* Design polish v1 — 2026-09-17' in html:
    raise AssertionError('design polish CSS already present')
html = replace_once(html, '</style>', design_css + '\n</style>', 'design CSS insertion')

# 5) Casual canvas uses the warm surface actually painted by the grid canvas.
html = replace_once(
    html,
    "    gctx.fillStyle = '#fbfcff';",
    "    gctx.fillStyle = uiMode==='casual' ? '#fffdf9' : '#fbfcff';",
    'casual grid background',
)

# 6) Empty-canvas hint follows the single render path so every editing operation stays in sync.
empty_hint_fn = '''  function updateCanvasEmptyHint(){
    const hint=document.getElementById('canvasEmptyHint');
    if(!hint) return;
    const empty=tracks.F1.length===0 && tracks.F2.length===0 && tracks.F3.length===0;
    hint.classList.toggle('is-visible',empty);
  }

'''
html = replace_once(html, '  function render(){\n    drawGrid();', empty_hint_fn + '  function render(){\n    updateCanvasEmptyHint();\n    drawGrid();', 'empty hint render hook')

# Protected research content must be byte-for-byte unchanged.
protected_after_match = re.search(r"  const JA_MT_BW = \{.*?\n  let YK2019_DATA = null;", html, flags=re.S)
if not protected_after_match:
    raise AssertionError('protected research block disappeared')
if protected_after_match.group(0) != protected_before:
    raise AssertionError('protected research data changed during UI patch')

# Sanity checks for intended structure.
for required in [
    'class="public-preview-banner research-only"',
    'class="public-preview-compact"',
    'class="canvas-hero"',
    'id="canvasEmptyHint"',
    'ことば',
    'だれの声？',
    'どの音？',
    'grid-template-rows:auto auto',
    "updateCanvasEmptyHint();",
]:
    if required not in html:
        raise AssertionError(f'missing expected design marker: {required}')

INDEX.write_text(html, encoding='utf-8')

# Durable repository memory: record the implementation state and rationale.
state = STATE.read_text(encoding='utf-8')
state = state.replace('Snapshot date: 2026-09-16', 'Snapshot date: 2026-09-17', 1)
state_anchor = '- Mobile-specific presentation rules.\n'
state_add = '''- Casual mode now uses a warmer, softer visual treatment and friendlier preset labels while preserving the research/learning information model.\n- The preset selector and drawing canvas are grouped as the primary canvas workspace on larger screens; mobile keeps the selector as a fixed two-row controller.\n- Research Preview disclosure is compact in Casual/Learning and fully visible in Research mode.\n- A casual-only empty-canvas hint appears when all three formant tracks are empty.\n'''
if 'The preset selector and drawing canvas are grouped as the primary canvas workspace' not in state:
    if state_anchor not in state:
        raise AssertionError('PROJECT_STATE insertion anchor missing')
    state = state.replace(state_anchor, state_anchor + state_add, 1)
STATE.write_text(state, encoding='utf-8')

decisions = DECISIONS.read_text(encoding='utf-8')
decision_entry = '''## D-011 — Make the canvas workspace the visual hero and adapt density by mode/device\n\n**Status:** Accepted  \n**Date:** 2026-09-17\n\n### Decision\nTreat the preset selector plus drawing canvas as Formantasia's primary interactive workspace. Casual mode should feel warmer and more approachable, while Learning and Research retain progressively denser explanatory information. On mobile, keep the preset selector reachable as a fixed two-row controller rather than compressing all controls into one row.\n\n### Rationale\nThe core product loop is choose a sound → draw/edit → listen. Giving the canvas workspace stronger hierarchy reduces competition from surrounding cards and makes the app easier to understand at a glance. Mode-specific disclosure preserves scientific detail without forcing research-level density into casual exploration. The two-row mobile controller improves label and option readability without sacrificing thumb reach.\n\n### Consequence\nFuture UI changes should preserve the canvas as the primary visual/interaction target, avoid making every panel equally prominent, and verify Casual/Learning/Research plus desktop/mobile separately. Research provenance remains fully available even when its preview notice is visually quieter outside Research mode.\n\n---\n\n'''
if '## D-011 — Make the canvas workspace the visual hero' not in decisions:
    anchor = '## Entry template\n'
    if anchor not in decisions:
        raise AssertionError('DECISIONS insertion anchor missing')
    decisions = decisions.replace(anchor, decision_entry + anchor, 1)
DECISIONS.write_text(decisions, encoding='utf-8')

print('DESIGN_POLISH_PATCH_OK')
