# Formantasia 統合・開発資産回収の記録（2026-10-09）

ユーザー決定（2026-10-09）: **Cloudflare Pages 版 `https://formantasia.pages.dev/` を Formantasia の正本・完成形の基準とする。** 本書はその決定に基づき、(A) 公開版の実態、(B) 全ブランチの回収判断、(C) Netlify→Cloudflare 統一の変更候補 を記録する。作業者: Claude Code。

確認方法の区別: **確認済み** = GitHub上の記録・コード・自動テストで直接確認 / **他者記録** = 別AIのQA記録による / **未確認** = 本セッションの環境から到達できず確認していない。

## A. 公開版の実態

| 項目 | Cloudflare Pages（基準） | Netlify（旧公開先） |
| --- | --- | --- |
| 配信元 | GitHub `main`。Cloudflare Pages GitHub連携。main のビルドには Branch Preview URL が付かず、PR ブランチには付く → 本番ブランチは `main`（確認済み: check run 出力） | Netlify GitHub連携。PRには deploy-preview の status が付く（確認済み） |
| 最新本番デプロイ | `ff9f5c1`（PR #20, おたよりポスト導線）→ デプロイ `b28caca4`、2026-10-09T10:30:50Z 成功（確認済み: Cloudflare Pages check run） | 9/17 以降の main コミットに Netlify 本番ビルドの記録なし。9/17 の UI 改善コミットは `[skip netlify]` 付き（確認済み）。本番が指すコミットは **未確認**（Netlify管理画面 → Deploys で要確認） |
| ビルド設定 | repo に build 設定なし（`package.json` / `wrangler.*` / `_headers` / `_redirects` なし）→ repo ルートをそのまま配信（確認済み: ファイル構成から。ダッシュボードの output dir 設定は **未確認**） | `netlify.toml` なし。Netlify 側 UI 設定は **未確認** |
| 実画面 | 3モードすべてでおたよりポスト導線あり（他者記録: Chibichan-Sketchbook `docs/OTAYORI_POST_MVP_QA_2026-10-08.md`, 2026-10-09） | 通常の画面は出るが、おたよりポスト導線なし（同上）→ `ff9f5c1` より古い |
| 作品集からのリンク | Chibichan-Sketchbook `public/index.html` は `https://formantasia.pages.dev/` を指す（確認済み） | — |

**結論**: Cloudflare 本番の実装の土台は `main`（`ff9f5c1`）。統合ブランチはすべて `main` から作成した。

**本セッションで未確認のこと**: 本セッションのクラウド環境はネットワーク制限で `*.pages.dev` / `*.netlify.app` に接続できず、配信中の HTML を直接取得・バイト比較していない。Cloudflare ダッシュボードで「Production branch = main」「Build output directory = /（ルート）」を一度確認すれば、上記の推定は確定する。

**補足（低優先）**: ルート配信のため、`AGENTS.md`・`tools/`・`data/` なども公開URLから読める状態のはず（未確認）。秘密情報は含まれていないが、気になる場合は将来 `public/` 等への出力分離を検討。

## B. ブランチ・PR の回収判断

判断は ahead/behind ではなく、**各ブランチの変更（merge-base→先端）が main に含まれているか**をファイル単位・追加行単位で照合した。

### 1. すでに Cloudflare 版（main）に存在 → 移植不要

| ブランチ / PR | 根拠 |
| --- | --- |
| `casual-age8-copy-20260917`, `casual-child-copy-20260917`, `casual-language-audit-20260917`, `casual-parent-preview-v2-20260917`, `design-polish-20260917`, `fix-mode-labels-20260917`, `seo-canonical-formantasia` (#10), `seo-formantasia-discovery` (#9), `docs/ai-development-method` (#12), `docs/app-kickoff-mini` (#16), `docs/gamification-principles` (#15), `maintenance/repo-cleanup-2026-10-03` (#19), `feature/otayori-link-20261008` (#20), `fix-learning-display-fragments` (#8), `codex/inspect-formantcanvas-repository-and-summarize` (#1) | 正味の差分が 0、または変更ファイルが main と同一 |
| `casual-parent-preview-20260917` | 追加33行すべて main に存在（v2 として統合済み） |
| `feat/export-controls-by-mode` (#14) | 追加51行すべて main に存在 |
| `fix-casual-mobile-copy` (#7) | 追加行すべて main に存在 |
| `feat/beginner-vowel-compare-ui` (#13) | main にない17行は、学習ポップオーバーの**10秒自動消去タイマー**と旧CSS。`c2e10b2 Improve learning popover accessibility` で意図的に置換済み（自動で消える説明はアクセシビリティ上の問題）。**復活させない** |
| `feat/yazawa-kondo-ui-integration` (#11) | main にない16行は、Yazawa–Kondo 条件を母音ドロップダウンの optgroup に並べる旧方式。main は比較行（`data-compare-key`）方式に置換済み（コード内コメント: "same-vowel conditions live in the comparison row, not the dropdown"）。**復活させない** |
| `rebrand-formantasia` (#6) | main にない5行は改名直後の旧文言。後の UI 改善で置換済み |

### 2. Cloudflare 版に存在せず、移植する価値あり → 今回移植

| 資産 | 移植先 | 内容 |
| --- | --- | --- |
| `feat/hillenbrand-trajectories`（PR #2） | `feat/hillenbrand-port-20261009` | 研究モードの成人男女 /eɪ/ /oʊ/ に Hillenbrand 1995 の10–80% 8点実測群平均。データJSON・生成スクリプトは無変更で移植。独立検証スクリプト `tools/verify_hillenbrand_1995.py` を追加。一回限りの patch スクリプトと workflow 3本は移植しない（PR #2 に履歴として残す） |
| 同上の UI 発見性 | `feat/integration-ui-20261009` | 「プリセットに戻す」を常時表示（未変更時は無効）、根拠カード内に実測軌跡への切替を追加（既存チェックボックスと同じ処理） |
| `feat/yazawa-kondo-adult-presets`（PRなし） | `feat/yazawa-generator-20261009` | main の Yazawa–Kondo データを生成したスクリプト。PR #11 はデータとUIだけを統合し、生成スクリプトは取り残されていた。CI（`9c57558`）がこのスクリプトで生成したJSONは main と sha256 一致、要約スクリプトは今日の再実行で main のCSVとバイト一致 |

### 3. 参考資料として保管（今回は移植しない）

| ブランチ / PR | 理由 |
| --- | --- |
| `feat/japanese-vv-evidence-audit`（PR #4） | 日本語VVの証拠マニフェストと検証スクリプト。監査の結論が未確定で、LOG HOUSE の別タスク（`formant-japanese`）として扱う。研究データの扱いを決める作業なので統合と混ぜない |
| PR #2 の one-shot workflow / patch スクリプト | 生成の経緯を示す履歴。PR #2 ブランチに残す |

### 4. 方針と競合する・別プロジェクトの成果 → Formantasia には移植しない

| ブランチ / PR | 理由 |
| --- | --- |
| `design/articulation-lab-v0.1`（PR #5）, `design/codex-cute-monkey`, `design/metaai-cute-exploration` | `articulation-lab/` 以下47–48ファイルの**別アプリ**（Articulation Lab、実音声WAV・ソース台帳つき）。現在のベロちゃん（`bero-chan_articulation-lab`、単一HTMLの v11 系）とは別系統で、Formantasia の機能ではない。ベロちゃん側で参考にするかは別判断。ブランチは削除しない |
| PR #17 `docs/public-edition-v0.1`（クローズ・未マージ） | AI App Builder Kit 側の成果物。Formantasia の対象外 |

## C. Netlify → Cloudflare 統一の変更候補（未実施）

実際の配信設定を確認する前には書き換えない。ユーザーが Cloudflare ダッシュボードの本番設定を確認し、Netlify の扱いを決めた後に、1つの小さなPRで行う。

| 対象 | 現状 | 変更候補 |
| --- | --- | --- |
| `index.html` `<link rel="canonical">`, `og:url`, JSON-LD `url` | `https://formantasia.netlify.app/` | `https://formantasia.pages.dev/` |
| `robots.txt` の `Sitemap:` / `sitemap.xml` の `<loc>` | netlify.app | pages.dev（`lastmod` も更新） |
| `AGENTS.md` 146行「Canonical public URL」, `README.md` 5行「Live app」, `PROJECT_STATE.md` 13行・115行 | netlify.app を正式公開先と記載 | pages.dev に変更し、Netlify は旧公開先と明記 |
| DaddyBoubakiki-Development-Method `GITHUB_MAP.md` / `ATELIER_REPOS.json` | 公開URLの記載なし（確認済み） | 変更不要 |
| Netlify サイト本体 | 古いビルドを配信中 | 選択肢: (a) pages.dev への 301 リダイレクトだけを置く、(b) 公開停止、(c) 当面放置（canonical だけ pages.dev）。検索エンジン登録の有無で判断 |
| コミットメッセージの `[skip netlify]` 慣習 | 9/17 に使用 | Netlify 停止後は不要 |

canonical の変更は検索結果に影響するため、(a)〜(c) の決定と同時に行うのが安全。
