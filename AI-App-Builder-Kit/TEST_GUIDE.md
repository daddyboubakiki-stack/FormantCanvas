# Clean-room Test Guide v0.1

このv0.1を初見の第三者と新しいAIチャットで壊してみるためのガイドです。販売品質の証明ではなく、分かりにくさ、過剰さ、漏れ、誤作動を見つけることが目的です。

## 1. テスト条件を記録する

- AIサービス / モデル / プラン（分かる範囲）
- ファイル添付の可否と添付数上限
- 使用端末
- テスターの開発経験
- 渡したファイルと順序
- 使用した企画シナリオ

Freeプランでは、長い会話や多数ファイルを前提にしません。まず`MASTER_PROMPT.md`、`APP_KICKOFF.md`、`DEVELOPMENT_METHOD.md`、`PROJECT_BRIEF_TEMPLATE.md`の4ファイル、または順次貼り付けで試します。

## 2. 基本シナリオ

1. 新規チャットを開始する。
2. 指定ファイルと、曖昧さを少し含むアプリ案を渡す。
3. 「このキットを使って企画を始めて」とだけ依頼する。
4. Kickoff終了までは実装を許可しない。
5. 生成されたBriefと質問過程を記録する。
6. 次に小さな変更依頼、バグ報告、保護対象を含む変更依頼を試す。

`examples/CLEAN_ROOM_SCENARIOS.md`に異なる用途の短い課題があります。

## 3. 導入テスト

- [ ] `START_HERE.md`だけで最初の操作が分かる。
- [ ] AIに何を、どの順で渡すか迷わない。
- [ ] ファイル添付なしでも開始できる。
- [ ] Freeプランで現実的な長さとファイル数である。
- [ ] 特定AIサービスの公式製品だと誤解しない。

## 4. Kickoffテスト

- [ ] AIが実装前にKickoffを行う。
- [ ] 既知情報を先に埋める。
- [ ] 回答済み情報を聞き直さない。
- [ ] 一度に質問しすぎない。
- [ ] 複数選択が自然な項目で複数選択できる。
- [ ] 「未定」「AIに提案してもらう」を認める。
- [ ] Target、Age、Experience、Purpose、Core actionを扱う。
- [ ] Context、Devices、Session length、Frequencyを扱う。
- [ ] Art direction、Gamification、Network、Storage/Login、Visibilityを扱う。
- [ ] Maturity goal、Priorities、Must-have / Must-notを扱う。
- [ ] 決定と仮説を区別する。
- [ ] 複雑・高リスクな企画だけDeep Kickoffへ進む。
- [ ] Brief確認前に勝手に実装を始めない。

## 5. Core動作テスト

- [ ] 利用者の目的を短く構造化する。
- [ ] 変更可能な実装と保護対象を分ける。
- [ ] 指示へ盲従せず、必要な改善案を理由付きで示す。
- [ ] 低影響の曖昧さで止まりすぎない。
- [ ] 変更を小さく検証可能に分ける。
- [ ] バグの再現条件を整理してから修正案を出す。
- [ ] 完成条件と近接回帰を扱う。
- [ ] プロジェクト記憶をチャットだけに依存させない。
- [ ] 保存と本番公開を区別する。

## 6. 安全性・アクセシビリティテスト

- [ ] 保護対象を別作業のついでに変更しない。
- [ ] 研究値、出典、区分の変更に根拠と承認を求める。
- [ ] 不要な個人データ取得を提案しない。
- [ ] 子ども向けで課金、共有、外部リンク、誤操作を検討する。
- [ ] 色だけ、音だけ、細かいドラッグだけへ依存しない。
- [ ] キーボード、フォーカス、読み上げ名、Reduce Motionを検討する。
- [ ] ダークパターン、FOMO、恥、過剰な通知を避ける。
- [ ] 未検証の規格適合を断言しない。

## 7. Personalization / Presetテスト

- [ ] 利用者の美的好みを勝手に仮定しない。
- [ ] 「かわいい」「柔らかい」「アナログ」がCore扱いされない。
- [ ] PresetがCoreの安全性・アクセシビリティを弱めない。
- [ ] Research / Education / Creativeで提案内容が適切に変わる。
- [ ] Research / Technicalでゲーム性が原則Level 0〜1になる。
- [ ] Kids Educationでも自動的にランキングやstreakを追加しない。
- [ ] ゲーム要素を後から弱める・外す設計を提案できる。

## 8. APP_KICKOFF.htmlテスト

- [ ] ローカルで開ける。
- [ ] キーボードだけで入力・生成・コピーできる。
- [ ] ラベルとfieldsetが分かる。
- [ ] 狭い画面、200%拡大で主要操作が使える。
- [ ] 必須項目が未入力のとき説明が出る。
- [ ] 入力がBriefへ正しく反映される。
- [ ] HTML入力が実行されず、文字として出力される。
- [ ] コピー失敗時にも手動コピーできる。
- [ ] Markdown保存を開始し、保存完了を断定しない説明が出る。
- [ ] 複数回生成すると直近5件の履歴が表示される。
- [ ] 履歴から過去の生成版を復元できる。
- [ ] 履歴は外部送信・永続保存されず、再読み込みで消える。
- [ ] 外部通信を行わない。

## 9. 合格の目安

v0.1では満点を求めません。次を満たせば第三者テスト可能とします。

- 初見の人が10分以内にKickoffを開始できる。
- AIが回答済み情報を大量に聞き直さない。
- Brief確認前に実装を始めない。
- 保護対象と仮説が明記される。
- 用途が変わってもCoreが保たれ、見た目やゲーム性だけが適応する。
- 失敗を再現できるログが残る。

## 10. テストログ・テンプレート

```md
# Clean-room Test Log

Date:
Tester:
AI / plan / model:
Device:
Files provided:
Scenario:

## Outcome

Could start without help: Yes / Partly / No
Time to first Kickoff:
Question count:
Repeated questions:
Started implementation too early: Yes / No
Brief quality: 1–5
Protected artifacts handled correctly: Yes / Partly / No

## Failure

Step:
Expected:
Actual:
Impact:
Exact prompt / response excerpt:
Reproducible: Always / Sometimes / Once

## Classification

Area: Onboarding / Prompt / Kickoff / Core / Design / Gamification / HTML / Other
Severity: Blocker / Major / Minor / Note
Likely cause:

## Proposed change

Smallest useful fix:
Files affected:
Risk of regression:
Retest scenario:
```
