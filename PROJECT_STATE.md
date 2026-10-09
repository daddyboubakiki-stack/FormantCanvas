# PROJECT_STATE.md — Formantasia

> Latest observation: see the dated 2026-10-03 maintenance section below. The original 2026-09-17 snapshot is retained as history; it is not a fresh browser QA result.

Snapshot date: 2026-09-17

This file records the current repository state so that a new human or AI collaborator can understand the project without relying on chat history.

## Product

**Formantasia（フォルマンタジア） — 声をえがくキャンバス · Draw Your Voice**

Public app: `https://formantasia.netlify.app/`

Purpose: an educational and experimental Web app for drawing F1/F2/F3 formant trajectories, listening to the resulting sound, exploring vowel presets, and inspecting the literature sources and modeling assumptions behind reference data.

The public build is currently described as a **Research Preview**.

## Repository shape

Current root files:
- `index.html` — main application; currently a large single-file implementation containing styling, UI, data, and behavior.
- `README.md` — public project description.
- `robots.txt`
- `sitemap.xml`
- `AGENTS.md` — standing development rules.
- `PROJECT_STATE.md` — this snapshot.
- `DECISIONS.md` — durable design/research decisions.

There is currently no root-level package manifest or multi-module application structure. Treat the monolithic `index.html` as a regression risk: inspect surrounding code before making local changes.

## Confirmed current UI / behavior

The current `index.html` contains:
- Casual, Learning, and Research UI modes.
- F1, F2, and F3 drawing/visualization controls.
- Voice/preset selection UI.
- Playback controls.
- WAV download support in the interface.
- Research tools and evidence display.
- Evidence categories visually distinguishing empirical, borrowed, and modeled information.
- Mobile-specific presentation rules.
- Casual mode now uses a warmer, softer visual treatment and friendlier preset labels while preserving the research/learning information model.
- The preset selector and drawing canvas are grouped as the primary canvas workspace on larger screens; mobile keeps the selector as a fixed two-row controller.
- Research Preview disclosure is compact in Casual/Learning and fully visible in Research mode.
- A casual-only empty-canvas hint appears when all three formant tracks are empty.
- SEO/canonical metadata for the Formantasia public site.

## Research-data policy currently represented in the app

The app explicitly distinguishes confidence/provenance levels rather than presenting every preset as equally empirical.

Current research-note principles include:
- published numerical averages and public materials are preferred;
- non-public or researcher-provided raw audio should not be bundled casually;
- derived statistics may be used when clearly documented as derived;
- empirical, borrowed, and app-modeled information should remain visibly distinguishable;
- display-only straight lines for monophthongs are not to be misrepresented as measured time-series trajectories.

The current app text identifies Hillenbrand et al. (1995) public 10% trajectories as a future integration candidate rather than as already integrated trajectory data.

## Recent repository-level decisions / changes

Recent merged work includes:
- public-facing rebrand from FormantCanvas to Formantasia while preserving selected internal/legacy identifiers;
- mobile display fixes for mode-specific content;
- search-discovery / SEO improvements;
- canonical site declaration and sitemap support.

See `DECISIONS.md` for durable rationale rather than relying only on commit history.

## Known engineering risks

1. **Monolithic implementation** — unrelated concerns live close together in `index.html`, so broad edits can create regressions.
2. **Multiple UI modes** — a change that looks correct in one mode can hide or alter content in another.
3. **Research provenance** — changing a value without updating its source/evidence classification can make the UI scientifically misleading.
4. **Legacy identifiers** — public branding is Formantasia, but internal names or persisted keys may intentionally retain older naming.
5. **Visual / interaction acceptance** — some important correctness criteria are perceptual and require manual UI review, not only code inspection.

## Working method

For all new work:
1. Read `AGENTS.md` first.
2. Inspect the relevant code before proposing a patch.
3. Define acceptance criteria and protected behavior.
4. Prefer small, reviewable changes.
5. Update this file when the current implementation state materially changes.

## Near-term documentation TODO

- Add concrete manual regression checks as recurring behavior stabilizes.
- Add project-specific test commands if/when a test/build system is introduced.
- Keep this snapshot focused on what is actually merged into the repository; exploratory ideas should not be described as implemented features.


---

# 2026-10-03 maintenance observation

最終確認日: 2026-10-03（JST）
状態: 🟡 要整理 / MAINTENANCE_REVIEW_READY

## 目的と確認範囲

Formantasia（旧FormantCanvas）。F1/F2/F3軌跡・合成・根拠表示の教育/研究preview。既存2026-09-17 snapshotを保持。

これは確認日の記録です。着手時はremoteのmain・branch・PRを再確認してください。通常のcloneはこの環境の認証制約で利用できず、GitHub接続からmainのcommitを固定して取得した検証用snapshotを使用しました。snapshotの初期git statusはcleanです。利用者のPC上の未コミット変更・local branchは未確認であり、変更なしとは判断していません。

## Current main

- 確認したmain: [1d7c2d4](https://github.com/daddyboubakiki-stack/FormantCanvas/commit/1d7c2d41464d881aff697e3f7505c413ba032ffc)
- 主要commit: Remove obsolete App Kickoff copy after Public repo migration（2026-09-19T12:41:56Z）
- 掃除branch: maintenance/repo-cleanup-2026-10-03（mainには未反映）
- 使用技術: 単一HTMLアプリ・Python整備tools・GitHub Actions。package/dependency manifestなし。
- deploy先: mainのREADME・AGENTS・canonical/SEOは https://formantasia.netlify.app/ 。作品集は https://formantasia.pages.dev/ を指す。到達性未確認でどちらかへ統一しない。

## 実装済み・未完了

**mainで確認したもの**

- Casual / Learning / Research、formant描画・再生・WAV export、preset・比較UI・根拠表示。
- Yazawa–Kondoデータ・関連UIのmerged PRとmainのファイルを確認。データは保護。
- 共通本文を独立コピーせず参照する構造が既にある。

**未完了・既知の問題・未確認**

- 共通参照がDevelopment-Methodの移行元資料を正本として案内していた（今回修正）。
- 本番originの記録が作品集と不一致。NEEDS_USER_REVIEW。SEO/アプリ設定は今回変更しない。
- open PR #2 Hillenbrand / #4 Japanese VV / #5 Articulation Labは未マージ。取得時mergeable=true / cleanだが、研究根拠・保護資産・実装QAの完了とは別。
- FormantCanvas内Articulation Lab枝と別ベロちゃんrepoの関係・保護資産の同等性を未確定のままmergeしない。

## Branch / PR

remote branchの判定は確認時のmainとの比較とPR記録に基づきます。長期未更新だけでSTALEや削除可とは断定しません。

| Branch | 判定 | main比較・根拠 |
| --- | --- | --- |
| main | ACTIVE | 1d7c2d4 |
| `casual-age8-copy-20260917` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 14; mainの祖先（ahead 0） |
| `casual-child-copy-20260917` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 26; mainの祖先（ahead 0） |
| `casual-language-audit-20260917` | UNKNOWN | ahead 2 / behind 26; GitHub compareの分岐点→headはfiles 0。main tree同一の証明ではなく、等価性・削除を保留。 |
| `casual-parent-preview-20260917` | UNKNOWN | ahead 4 / behind 26; 確証不足 |
| `casual-parent-preview-v2-20260917` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 19; mainの祖先（ahead 0） |
| `codex/inspect-formantcanvas-repository-and-summarize` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 89; mainの祖先（ahead 0）・PR merged |
| `design/articulation-lab-v0.1` | PR_OPEN | ahead 111 / behind 88; open PR #5 |
| `design/codex-cute-monkey` | UNKNOWN | ahead 131 / behind 88; 確証不足 |
| `design/metaai-cute-exploration` | UNKNOWN | ahead 112 / behind 88; 確証不足 |
| `design-polish-20260917` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 34; mainの祖先（ahead 0） |
| `docs/ai-development-method` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 53; mainの祖先（ahead 0）・PR merged |
| `docs/app-kickoff-mini` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 23; mainの祖先（ahead 0）・PR merged |
| `docs/gamification-principles` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 38; mainの祖先（ahead 0）・PR merged |
| `feat/beginner-vowel-compare-ui` | COMPLETED | ahead 1 / behind 73; 同じhead SHAのPRがmerge済み（squash等のためaheadは残り得る）。等価性・削除は個別確認 |
| `feat/export-controls-by-mode` | COMPLETED | ahead 4 / behind 72; 同じhead SHAのPRがmerge済み（squash等のためaheadは残り得る）。等価性・削除は個別確認 |
| `feat/hillenbrand-trajectories` | PR_OPEN | ahead 11 / behind 88; open PR #2 |
| `feat/japanese-vv-evidence-audit` | PR_OPEN | ahead 4 / behind 88; open PR #4 |
| `feat/yazawa-kondo-adult-presets` | UNKNOWN | ahead 13 / behind 88; 確証不足 |
| `feat/yazawa-kondo-ui-integration` | COMPLETED | ahead 15 / behind 74; 同じhead SHAのPRがmerge済み（squash等のためaheadは残り得る）。等価性・削除は個別確認 |
| `fix-casual-mobile-copy` | COMPLETED | ahead 3 / behind 85; 同じhead SHAのPRがmerge済み（squash等のためaheadは残り得る）。等価性・削除は個別確認 |
| `fix-learning-display-fragments` | COMPLETED | ahead 3 / behind 84; 同じhead SHAのPRがmerge済み（squash等のためaheadは残り得る）。等価性・削除は個別確認 |
| `fix-mode-labels-20260917` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 11; mainの祖先（ahead 0） |
| `rebrand-formantasia` | COMPLETED | ahead 7 / behind 88; 同じhead SHAのPRがmerge済み（squash等のためaheadは残り得る）。等価性・削除は個別確認 |
| `seo-canonical-formantasia` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 75; mainの祖先（ahead 0）・PR merged |
| `seo-formantasia-discovery` | COMPLETED / DELETE_CANDIDATE | ahead 0 / behind 79; mainの祖先（ahead 0）・PR merged |

Open PR: [#5](https://github.com/daddyboubakiki-stack/FormantCanvas/pull/5) Prototype Articulation Lab v0.5-alpha.17 visual-articulation checkpoint（draft; mergeable=true / clean）; [#2](https://github.com/daddyboubakiki-stack/FormantCanvas/pull/2) Add Hillenbrand 1995 measured diphthong trajectories（draft; mergeable=true / clean）; [#4](https://github.com/daddyboubakiki-stack/FormantCanvas/pull/4) Audit Japanese VV trajectory evidence（draft; mergeable=true / clean）

最近mergeされたPR: [#18](https://github.com/daddyboubakiki-stack/FormantCanvas/pull/18) Publish App Kickoff v0.1; [#16](https://github.com/daddyboubakiki-stack/FormantCanvas/pull/16) Add App Kickoff questionnaire and mini brief preset; [#15](https://github.com/daddyboubakiki-stack/FormantCanvas/pull/15) Add adaptive gamification design principles; [#12](https://github.com/daddyboubakiki-stack/FormantCanvas/pull/12) Add shared AI development method and project memory; [#14](https://github.com/daddyboubakiki-stack/FormantCanvas/pull/14) Add export controls to Casual and Learning modes

PRのmerge・close・force update、既存branchへの書き込み・削除は行っていません。

## 文書の正本と分類

| 文書 | 分類 | 読み方 |
| --- | --- | --- |
| [README.md](README.md) | CURRENT | 製品説明・現行正本参照 |
| [AGENTS.md](AGENTS.md) | CURRENT | 研究保護の正本 |
| [PROJECT_STATE.md](PROJECT_STATE.md) | CURRENT / HISTORICAL | 日付付きsnapshotと最新観察 |
| [DECISIONS.md](DECISIONS.md) | CURRENT / HISTORICAL | 決定の根拠 |
| [GLOBAL_APP_PRINCIPLES.md](GLOBAL_APP_PRINCIPLES.md) | CURRENT | 運用入口への参照 |
| [DEVELOPMENT_METHOD.md](DEVELOPMENT_METHOD.md) | CURRENT | Coreへの参照 |
| [GAMIFICATION_DESIGN.md](GAMIFICATION_DESIGN.md) | CURRENT | Coreへの参照 |
| [APP_KICKOFF.md](APP_KICKOFF.md) | CURRENT | Overlay参照 |
| [VISUAL_SENSORY_DESIGN.md](VISUAL_SENSORY_DESIGN.md) | CURRENT | Overlay参照 |
| [TOOLS_AND_DEPLOYMENT.md](TOOLS_AND_DEPLOYMENT.md) | CURRENT | 工房運用参照 |

## 今回の整理と残すもの

- AUTO_FIXED: README・AGENTS・3 pointer文書を現行Core/Overlay構造へ接続。
- AUTO_FIXED: 既存PROJECT_STATEへmain/branch/PR/公開URL不一致/未確認を追記。
- LEFT_UNTOUCHED: 研究数値、出典、evidence、CSV/JSON、index、Python tools、CI、SEO、全feature branchとPR。

削除候補はこの記録のbranch分類と下記に限定し、自動削除しません。
- DELETE_CANDIDATES: main祖先のbranchは表の削除候補。分岐点比の差分なしbranchはmainとの等価性を未確定として削除保留。
- DELETE_CANDIDATES: Articulation Lab・cute系branchはUNKNOWN/PR_OPENのまま保護。

## 検証

- 正式なpackage scriptなし。WorkflowのSelenium smokeはSelenium/Chrome/driverがこの環境に揃わず未実施（環境依存）。新規toolは導入しない。
- 相対リンク・候補スキャン: broken link/秘密候補/完全一致重複なし。
- 値・UI挙動のQAは今回再実行していない。
- Markdown相対リンク・git diff --check・変更範囲はコミット前に確認。runtimeコード、研究値、ユーザーデータ、dependency、デプロイ設定は今回変更しない。

## 次の一手

- 本番originを管理設定と未認証画面で確定し、作品集/README/SEOの一致を別作業で整える。
- 研究系PR #2/#4と独立ベロちゃん移行に関係するPR #5を個別に根拠監査する。
