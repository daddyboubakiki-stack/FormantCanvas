# Example Brief — 専門用語フラッシュカード

これは形式を示す架空の例です。

## Product summary

- **Working title:** Term Deck
- **Purpose:** 大学生が、授業前の短時間に専門用語と定義を復習できるWebアプリ。
- **Success:** 3分以内に復習を開始でき、分からなかった語だけを再確認できる。
- **Out of scope:** 教員による成績評価、公開ランキング、SNS共有。

## Audience and context

- **Target:** 大学生、初級〜中級
- **Context:** 通学中と授業前
- **Devices:** スマートフォン中心、PCも対応
- **Session / frequency:** 1〜5分、週2〜4回（仮説）

## Core experience

- **Core action:** 用語を見て意味を思い出し、答えを開いて自己評価する。
- **Art direction:** Clean & Professional 70% + Warm & Playful 30%
- **Gamification:** Level 1。学習済み数と復習対象だけを静かに表示する。

## Technical assumptions

- **Network:** 初回読込後はオフラインでも使える案を検証する。
- **Storage / login:** v0.1は端末内保存、ログインなし。
- **Visibility:** 自分だけ。
- **Maturity:** 動く試作。

## Priorities and boundaries

- **Priorities:** 分かりやすさ、起動の速さ、アクセシビリティ。
- **Must-have:** キーボード操作、用語データのインポート、復習対象の絞り込み。
- **Must-not:** streak、公開ランキング、学習を急かす通知。
- **Protected:** インポート済みの用語本文と出典。UI修正のついでに書き換えない。

## First prototype

- 10件の架空データで、一覧 → カード → 自己評価 → 復習一覧を試す。
- 受け入れ条件：スマートフォン幅とキーボードのみの両方で、一連の復習を完了できる。

## Open questions

- **高影響:** インポート形式をCSVとJSONのどちらにするか。
- **低影響:** 完了表示の文言とアクセント色。
