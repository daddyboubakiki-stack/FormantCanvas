# AI App Builder Kit — Public Edition v0.1

AIを、コード生成だけでなく、企画・UX・設計・安全性・アクセシビリティ・検証まで一緒に考える共同開発者として使うためのスターターキットです。

これは特定のAIサービスの公式製品ではありません。ChatGPTを含む、ファイルまたは長文指示を読める対話型AIで使うことを想定しています。v0.1は、第三者によるClean-room Testのための試作版です。

## 最短の始め方

### ファイルを添付できる場合

1. このフォルダをダウンロードする。
2. 新しいAIチャットに、このフォルダのMarkdownファイルを添付する。
3. [`MASTER_PROMPT.md`](MASTER_PROMPT.md) の本文を送る。
4. AIが既知情報を先に埋めたApp Kickoffを開始する。

最初から全ファイルを添付できない場合は、まず次の4ファイルで開始できます。

1. `MASTER_PROMPT.md`
2. `APP_KICKOFF.md`
3. `DEVELOPMENT_METHOD.md`
4. `PROJECT_BRIEF_TEMPLATE.md`

UIやゲーム要素を検討するときに、`DESIGN_PROTOCOL.md`、`GAMIFICATION_PROTOCOL.md`、`PERSONALIZATION.md`を追加してください。

### ファイルを添付できない場合

1. `MASTER_PROMPT.md`を貼り付ける。
2. `APP_KICKOFF.md`を続けて貼り付ける。
3. AIに「まず企画カルテだけ行い、まだ実装しないでください」と伝える。
4. Briefができたら、必要なCore文書を追加する。

### クリック式で企画を整理したい場合

`APP_KICKOFF.html`をブラウザで開き、選択肢を埋めてProject Briefを生成します。生成結果をコピーし、AIへ渡してください。入力内容はブラウザ内で処理され、外部送信機能はありません。

## 3層の構成

| 層 | 役割 | 上書きできるもの |
|---|---|---|
| Core | 安全性、保護対象、共同開発、検証、アクセシビリティ等の共通原則 | 原則として上書きしない |
| Personalization | 話し方、説明量、提案の積極性、確認頻度、速度と品質の配分 | 利用者が調整できる |
| Preset | Research、Kids Education、Creative等の用途別初期値 | Coreを弱めない範囲で調整できる |

優先順位は、`Core > プロジェクト固有の保護ルール > Personalization / Preset > 個別の実装案`です。

## ファイル一覧

| ファイル | 誰が読むか | 役割 |
|---|---|---|
| `START_HERE.md` | 人間 | 導入と読み順 |
| `MASTER_PROMPT.md` | AI | 入口となる短い指示 |
| `APP_KICKOFF.md` | 人間・AI | Mini / Deep Kickoffの進め方 |
| `APP_KICKOFF.html` | 人間 | クリック式企画カルテ |
| `DEVELOPMENT_METHOD.md` | 人間・AI | Coreの開発・安全・記憶原則 |
| `DESIGN_PROTOCOL.md` | 人間・AI | 一般化した視覚・感覚設計 |
| `GAMIFICATION_PROTOCOL.md` | 人間・AI | 用途適応型ゲーミフィケーション |
| `PERSONALIZATION.md` | 人間・AI | 好みの設定と用途別Preset |
| `PROJECT_BRIEF_TEMPLATE.md` | 人間・AI | 企画・保護対象・判断の記録 |
| `TEST_GUIDE.md` | テスター | Clean-room Testと失敗ログ |
| `examples/` | 人間・AI | 記入例とテスト例 |

## この版で意図的にしないこと

- 特定の人格や会話関係を再現しない。
- 特定の色、素材、かわいさ、柔らかさをCoreとして強制しない。
- すべてのプロジェクトへ同じゲーム性を付けない。
- 法令・規格への適合を、検証なしに宣言しない。
- 完璧な長期仕様を作ってから実装を始めようとしない。

## 推奨する最初の実験

小さなアプリ案を一つ選び、Mini Kickoff → Brief生成 → 最小試作の提案までを試してください。初回は実装させず、質問数、聞き直し、勝手な仮定、保護対象の扱いを観察すると、キット自体の問題を見つけやすくなります。
