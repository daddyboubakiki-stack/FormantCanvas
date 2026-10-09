# Architecture

## Core principle

Treat **state**, **science/data**, **audio**, and **graphics** as different layers.

```text
User pointer / preset
        ↓
ArticulationState
        ↓
Constraint + mapping layer
   ↙                 ↘
Renderer              AcousticEngine
(Simple/Anatomy/Cute)      ↓
                         Audio
        ↓
AcousticTarget / evidence UI
```

The renderer must never become the source of truth for tongue position. The SVG/path is a visualization of state, not the state itself.

## 1. ArticulationState

Normalized values are preferred for the UI-facing state so skins can share one contract.

```js
{
  tongueBodyFrontBack: 0.0..1.0, // front → back
  tongueBodyHeight:    0.0..1.0, // high → low (UI convention; document explicitly)
  tongueTipFrontBack:  0.0..1.0, // reserved in v0.1
  tongueTipHeight:     0.0..1.0, // reserved in v0.1
  lipRounding:         0.0..1.0,
  lipAperture:         0.0..1.0, // reserved/derived initially
  jawOpening:          0.0..1.0, // reserved/derived initially
  velumOpening:        0.0..1.0, // reserved; 0 for oral-vowel MVP
  f0Hz:                number,
  voicing:             boolean
}
```

### Why normalized state?

A Cute renderer and an Anatomy renderer should be able to draw different geometry for the same articulatory intention. Physical units can be introduced later in an additional calibrated model layer without breaking UI skins.

## 2. ConstraintMapper

Responsibilities:

- clamp state to supported human-like ranges
- prevent visual tongue paths from crossing hard palate / teeth boundaries
- map high-level tongue controls to the synthesis engine's tract controls
- optionally derive jaw/lip aperture from vowel configuration in the MVP
- expose an explicit `modelVersion`

Do **not** infer one unique anatomical posture from F1/F2. When moving from an acoustic target to articulation, return one or more labeled candidate postures or a target zone.

## 3. AcousticEngine interface

The UI should call a narrow interface rather than a specific synthesizer implementation.

```js
engine.start()
engine.stop()
engine.setArticulation(state)
engine.setF0(hz)
engine.getAcousticEstimate() // { f1Hz, f2Hz, f3Hz, method, confidence }
```

### MVP backend

A lightweight Web Audio / formant-filter engine is acceptable for the first playable build if it reacts immediately and is clearly labeled as an approximation.

### Preferred later backend

A Pink-Trombone-derived or compatible tract model is a good candidate because the model exposes a vocal-tract diameter representation and continuous target diameters. Keep third-party code isolated under `src/audio/backends/` with license notices.

## 4. Renderer interface

```js
renderer.mount(container)
renderer.render(articulationState)
renderer.pointerToIntent(pointerEvent) // returns partial state update
renderer.destroy()
```

Planned implementations:

- `SimpleRenderer`
- `AnatomyRenderer`
- `CuteRenderer`

All renderers consume the same state. Switching skin must not alter the sound or scientific dataset.

## 5. Vowel data model

Separate three concepts:

### AcousticTarget
Measured or modeled acoustic information.

- language
- phoneme / label
- speaker population
- context
- F1/F2/F3
- unit
- evidence type (`measured_group_mean`, `measured_single_speaker`, `model_prediction`, `pedagogical_model`, etc.)
- source ID

### ArticulatoryTarget
A suggested configuration or region.

- normalized tongue/lip/jaw state
- `targetType`: point | zone | alternatives
- evidence type
- source ID
- notes about uncertainty

### Pairing
A UI preset may point to one AcousticTarget and one ArticulatoryTarget, but they are never assumed to be mathematically equivalent evidence.

## 6. English/Japanese comparison

COMPARE should support:

- language A + vowel A
- language B + vowel B
- A/B audio toggle
- animated morph between articulatory targets
- F1/F2 plot with both acoustic targets
- plain-language directional cue, e.g. `more front`, `lower`, `more rounded`
- population/source badge

For classroom mode, hide raw numbers by default. PHONETICS mode reveals F1/F2/F3, source, population, context, and evidence type.

## 7. Shared data with Formant Canvas

Long term, both apps should consume the same versioned vowel-data package rather than copy-pasting numeric constants.

Suggested future package boundary:

```text
shared-vowel-data/
  schema/
  sources.json
  acoustic-targets.json
  trajectories.json
```

Articulation Lab adds its own `articulatory-targets.json` because Formant Canvas does not need anatomical targets.

## 8. Event flow for PLAY

1. pointer moves tongue handle
2. renderer converts pointer to articulatory intent
3. constraints normalize/update `ArticulationState`
4. state store emits update
5. renderer redraws tongue
6. acoustic engine updates continuously
7. acoustic estimate/readout updates at a throttled visual rate

Audio updates should be smoother/faster than UI text updates.

## 9. Event flow for COMPARE morph

1. load two preset records
2. interpolate **articulation state**, not F1/F2 alone
3. feed each intermediate state to engine
4. animate both anatomy and sound
5. independently plot source-backed acoustic target points/ranges

The morph is a pedagogical path unless a measured articulatory trajectory exists. Label it accordingly.

## 10. Failure-safe rule

If a value lacks a recoverable source/provenance record, the app may still use it as a clearly labeled model/demo value, but must not display it as empirical or normative.