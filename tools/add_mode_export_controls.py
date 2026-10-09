from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Keep this patch idempotent.
if 'id="casualDownloadWavBtn"' in text and 'id="modeExportPanel"' in text:
    print('Mode export controls already present.')
    raise SystemExit(0)

css_anchor = "  .check-wrap { display:flex; align-items:center; gap:8px; min-height:38px; padding:8px 10px; border:1px solid var(--border); background:#fff; border-radius:12px; font-size:13px; font-weight:700; cursor:pointer; user-select:none; }"
css_insert = """  .mode-export-panel {
    margin-top:12px; padding:12px 14px; display:flex; flex-wrap:wrap; gap:10px 14px; align-items:center;
    background:var(--panel); border:1px solid var(--border); border-radius:18px;
    box-shadow:0 10px 35px rgba(30,42,75,.05); backdrop-filter:blur(10px);
  }
  .mode-export-copy { flex:1 1 280px; min-width:0; }
  .mode-export-copy strong { display:block; font-size:13px; margin-bottom:3px; }
  .mode-export-copy p { margin:0; color:var(--muted); font-size:11px; line-height:1.55; }
  .mode-export-panel .io-group { flex:0 1 auto; }
  .casual-export-panel {
    display:none; margin-top:12px; padding:12px 14px; align-items:center; gap:12px;
    background:linear-gradient(180deg,#ffffff,#f7fbff); border:1px solid var(--border); border-radius:18px;
    box-shadow:0 10px 35px rgba(30,42,75,.05);
  }
  body[data-ui-mode=\"casual\"] .casual-export-panel { display:flex; }
  .casual-export-copy { flex:1 1 220px; min-width:0; }
  .casual-export-copy strong { display:block; font-size:13px; margin-bottom:3px; }
  .casual-export-copy p { margin:0; color:var(--muted); font-size:11px; line-height:1.55; }
  .casual-download-btn { min-height:46px; padding:10px 15px; white-space:nowrap; }
""" + css_anchor
if css_anchor not in text:
    raise RuntimeError('CSS anchor not found')
text = text.replace(css_anchor, css_insert, 1)

mobile_anchor = "    .advanced-panel .io-group button { flex:1 1 auto; }"
mobile_insert = mobile_anchor + "\n    .mode-export-panel .io-group { flex:1 1 100%; }\n    .mode-export-panel .io-group button { flex:1 1 auto; }\n    .casual-export-panel { flex-direction:column; align-items:stretch; }\n    .casual-download-btn { width:100%; }"
if mobile_anchor not in text:
    raise RuntimeError('Mobile CSS anchor not found')
text = text.replace(mobile_anchor, mobile_insert, 1)

bottom_anchor = """  </div>\n\n  <div class=\"casual-tip casual-only\">✏️ F1・F2・F3を好きに曲げて、▶ で聴き比べよう。学習モードでは、F1/F2/F3や音のしくみも確かめられます。</div>"""
exports = """  </div>

  <section class=\"mode-export-panel learning-plus\" id=\"modeExportPanel\" aria-label=\"保存・書き出し・読み込み\">
    <div class=\"mode-export-copy\">
      <strong><span class=\"learning-only\">📥 保存・読み込み</span><span class=\"research-only\">Export / import</span></strong>
      <p class=\"learning-only\">いまの音をWAV、F1〜F3のデータをCSV、Praat用スクリプトとして保存できます。CSVを読み込んで続きから触ることもできます。</p>
      <p class=\"research-only\">現在の合成音・F1〜F3軌跡を保存し、CSVデータを読み込めます。</p>
    </div>
    <div class=\"io-group\">
      <button id=\"downloadWavBtn\" class=\"wav-download\" title=\"現在の合成音を48 kHz / 16-bit PCM WAVで保存\"><span class=\"learning-only\">WAVを保存</span><span class=\"research-only\">WAV書き出し</span></button>
      <button id=\"exportPraat\"><span class=\"learning-only\">Praat用に保存</span><span class=\"research-only\">Praatへ書き出し</span></button>
      <button id=\"exportCsv\"><span class=\"learning-only\">CSVを保存</span><span class=\"research-only\">CSV書き出し</span></button>
      <button id=\"importCsvBtn\"><span class=\"learning-only\">CSVを読み込む</span><span class=\"research-only\">CSV読込</span></button>
      <input id=\"importCsv\" type=\"file\" accept=\".csv,.txt\" hidden />
    </div>
  </section>

  <section class=\"casual-export-panel casual-only\" id=\"casualExportPanel\" aria-label=\"音を保存\">
    <div class=\"casual-export-copy\">
      <strong>できた音をのこしておこう 🎵</strong>
      <p>いま作った音をWAVファイルでスマホやパソコンに保存できます。</p>
    </div>
    <button id=\"casualDownloadWavBtn\" class=\"wav-download casual-download-btn\" type=\"button\" title=\"いま作った音をWAVファイルで保存\">🔊 おとを保存する</button>
  </section>

  <div class=\"casual-tip casual-only\">✏️ F1・F2・F3を好きに曲げて、▶ で聴き比べよう。学習モードでは、F1/F2/F3や音のしくみも確かめられます。</div>"""
if bottom_anchor not in text:
    raise RuntimeError('Bottom anchor not found')
text = text.replace(bottom_anchor, exports, 1)

old_io = """    <div class=\"io-group\">\n      <button id=\"downloadWavBtn\" class=\"wav-download\" title=\"現在の合成音を48 kHz / 16-bit PCM WAVで保存\">WAV書き出し</button>\n      <button id=\"exportPraat\">Praatへ書き出し</button>\n      <button id=\"exportCsv\">CSV書き出し</button>\n      <button id=\"importCsvBtn\">CSV読込</button>\n      <input id=\"importCsv\" type=\"file\" accept=\".csv,.txt\" hidden />\n    </div>\n"""
if old_io not in text:
    raise RuntimeError('Research export group not found')
text = text.replace(old_io, '', 1)

text = text.replace('  async function downloadWav(){', '  async function downloadWav(triggerBtn){', 1)
text = text.replace("    const btn=document.getElementById('downloadWavBtn');\n    const old=btn.textContent;\n    btn.disabled=true; btn.textContent='書き出し中…';", "    const btn=triggerBtn || document.getElementById('downloadWavBtn');\n    const old=btn.innerHTML;\n    btn.disabled=true; btn.textContent=uiMode==='casual'?'保存中…':'書き出し中…';", 1)
text = text.replace('      btn.disabled=false; btn.textContent=old;', '      btn.disabled=false; btn.innerHTML=old;', 1)
text = text.replace("  document.getElementById('downloadWavBtn').onclick=downloadWav;", "  document.getElementById('downloadWavBtn').onclick=e=>downloadWav(e.currentTarget);\n  document.getElementById('casualDownloadWavBtn').onclick=e=>downloadWav(e.currentTarget);", 1)

path.write_text(text, encoding='utf-8')
print('Added mode-specific export controls.')
