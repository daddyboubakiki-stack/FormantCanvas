# Personalization & Presets v0.1

この文書は、Coreを変えずにAIとの協働方法とアプリの方向性を調整する層です。未選択項目はAIが仮提案できますが、確定事項とは扱いません。

## Personalization Profile

次をコピーして選択・追記してください。

```yaml
communication_tone: neutral-friendly   # concise / neutral-friendly / teacher-like / formal
explanation_depth: medium              # short / medium / detailed
proposal_level: proactive              # ask-first / balanced / proactive
technical_autonomy: guarded            # low / guarded / high
confirmation_frequency: high-impact    # frequent / high-impact / minimal
delivery_bias: balanced                # speed / balanced / quality
beginner_support: adaptive             # light / adaptive / strong
design_direction: undecided            # 自由記述またはPreset名
change_reporting: concise              # concise / detailed
```

### 設定の意味

- **proposal_level**：改善案をどの程度先回りして出すか。
- **technical_autonomy**：低リスクの技術判断をAIがどこまで進めるか。
- **confirmation_frequency**：確認の頻度。どの設定でも高影響の曖昧さと保護対象は確認します。
- **delivery_bias**：初期試作の速度と磨き込みの配分。どの設定でも安全性と保護対象は弱めません。
- **design_direction**：感情、色、素材、密度、動き、音の希望。Coreには固定しません。

## Preset Layer

Presetは開始時の仮設定です。安全性、アクセシビリティ、プライバシー、保護対象、ダークパターン回避を上書きしません。

### Clean & Professional

- 印象：明確、端正、信頼できる、効率的
- 密度：中
- Motion / Sound：必要最小限
- Gamification：Level 0〜1
- 重視：タスク完了、予測可能性、読みやすさ

### Research / Technical

- 印象：精密、検証可能、落ち着いている
- 密度：中〜高。段階表示を使う
- データ：出典、区分、不確実性、再現性を重視
- Gamification：Level 0〜1
- 重視：正確性、provenance、エクスポート、作業速度

### Kids Education

- 印象：分かりやすい、安心、探索しやすい
- 密度：低〜中。年齢相応の言葉と操作
- 制御：音・動き・外部リンク・共有・課金を慎重に扱う
- Gamification：Level 1〜2。競争より探索と小さな達成
- 重視：学習目標、誤操作回復、複数の理解経路、子どもの権利

### Creative / Experimental

- 印象：発見的、表現的、意外性がある
- 密度：目的に応じて可変
- Motion / Sound：意味がある範囲で試せる
- Gamification：Level 0〜3から目的に合わせる
- 重視：試行錯誤、Undo、保存、壊れにくい実験領域

### Warm & Playful

- 印象：親しみやすい、温かい、遊び心がある
- 素材候補：紙、布、木、手描き感等。ただし必須ではない
- Motion / Sound：控えめで短い反応を候補にする
- Gamification：Level 1〜2
- 重視：可読性を損なわない質感、刺激量の調整

## Presetを混ぜる場合

`Research / Technical 70% + Warm & Playful 30%`のように指定できます。衝突した場合は目的と利用場面を優先し、見た目の好みで証拠表示や安全機能を弱めません。

## プロジェクト固有設定

```md
Selected preset:
Desired emotion:
Visual references:
Preferred colors/materials:
Motion preference:
Sound preference:
Avoid:
AI communication preference:
Items the AI may decide autonomously:
Items requiring confirmation:
```
