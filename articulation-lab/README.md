# Articulation Lab — v0.1 staging build

Articulation Lab is a proposed sister app to Formant Canvas.

- **Formant Canvas:** manipulate acoustic space and hear the result.
- **Articulation Lab:** manipulate the vocal tract and hear the result.

The first public-facing idea is a **playable 2D mouth instrument**: drag the tongue directly, change lip rounding, and hear the vowel-like sound change continuously. Educational features are layered on top after the instrument itself feels responsive and fun.

## Product goals

1. Direct manipulation: the tongue itself is the primary control.
2. Continuous sound: moving an articulator changes sound immediately, not only after releasing a control.
3. Human constraints: unlike Formant Canvas, impossible articulatory positions should be constrained.
4. Honest science: acoustic targets and articulatory targets are separate datasets; no claim that F1/F2 uniquely determines tongue shape.
5. Handoff-safe design: data, acoustics, articulation state, and graphics are separate modules so another model/developer can redesign the visual layer without silently changing the science.
6. Skinning: Simple, Anatomy, and Cute renderers can visualize the same underlying articulation state.

## v0.1 implementation status

A first playable implementation is now present in this folder.

Implemented:

- 2D midsagittal **Simple** skin
- pointer/touch dragging of the tongue body
- keyboard arrow-key alternative for the tongue handle
- live lip-rounding control
- F0 control
- `VOICE ON/OFF` using a lightweight Web Audio source-filter/formant backend
- continuously updated F1/F2/F3 estimates
- vowel presets `/i æ ɑ ə u/`
- responsive phone/tablet/desktop layout
- separate state, constraint, audio, renderer, data, and app-controller files

### Important evidence status

The acoustic values and tongue targets in the current v0.1 are explicitly marked as a **pedagogical/demo model**. They are **not yet the source-backed English/Japanese normative dataset** planned for COMPARE/LEARN.

The next scientific-data milestone is to port verified Formant Canvas vowel values into the versioned target schema while preserving population, context, source, and evidence type.

## Current file layout

```text
articulation-lab/
  index.html
  data/
    vowel-presets.js
    source-registry.json
  src/
    state-store.js
    constraint-mapper.js
    audio/
      formant-engine.js
    renderers/
      simple-renderer.js
    app.js
  styles/
    base.css
  contracts/
  docs/
```

The renderer does not own the tongue position. `ArticulationState` is the source of truth. A future `CuteRenderer` or `AnatomyRenderer` should consume the same state and must not alter scientific/acoustic data merely to fit a visual design.

## Non-goals for v0.1

- 3D rendering
- microphone-based pronunciation scoring
- consonants
- nasal coupling
- full jaw/tongue-tip control
- claiming a unique inverse mapping from acoustics to anatomy
- claiming the current demo vowel values are empirical language norms

## Planned modes

- **PLAY** — free mouth instrument
- **COMPARE** — A/B and morph comparison, especially Japanese vs English vowels
- **LEARN** — move from a familiar Japanese vowel toward an English target zone
- **PHONETICS** — show acoustic values, population, source, and evidence type

## Handoff rule

A graphics/UI contributor should normally edit renderer/style/UI files, not scientific data or acoustic mappings. See `docs/META_AI_HANDOFF.md` and `docs/SCIENTIFIC_CONTRACT.md`.

## Repository status

This folder currently lives in the Formant Canvas repository as a **staging implementation** on branch `design/articulation-lab-v0.1`. It is intentionally isolated from Formant Canvas `main`. The intended end state is a separate Articulation Lab repository, with shared data contracts between the two apps.
