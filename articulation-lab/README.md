# Articulation Lab — v0.3.1 staging build

Articulation Lab is a proposed sister app to Formant Canvas.

- **Formant Canvas:** manipulate acoustic space and hear the result.
- **Articulation Lab:** manipulate vocal-tract articulation and hear the result.

The app now has two deliberately separate play experiences.

1. **Vowel Buttons** — tap IPA buttons on a simplified vowel quadrilateral; each tap moves the modeled tongue/lips and plays a short ~0.5 s vowel burst.
2. **Mouth Synth** — turn on continuous voicing and drag the tongue directly like an instrument.

This separation keeps the educational selection task and the free-play instrument task from competing for the same screen space.

## Product goals

1. Direct manipulation: in Mouth Synth, the tongue itself is the primary control.
2. Immediate playful sound: in Vowel Buttons, one tap should immediately produce a short sound.
3. Clear mode semantics: short triggered sounds and continuous synthesis are different modes, not overloaded controls.
4. Human constraints: unlike Formant Canvas, impossible articulatory positions should be constrained.
5. Honest science: acoustic targets and articulatory targets are separate datasets; no claim that F1/F2 uniquely determines tongue shape.
6. Handoff-safe design: data, acoustics, articulation state, vowel map, and mouth graphics are separate modules so another model/developer can redesign the visual layer without silently changing the science.
7. Skinning: Simple, Anatomy, and Cute mouth renderers can visualize the same underlying articulation state.

## v0.3.1 implementation status

Implemented:

- 2D midsagittal **Simple** mouth skin
- separate **Vowel Buttons** and **Mouth Synth** modes
- simplified vowel quadrilateral rendered independently from the mouth
- translucent circular IPA buttons
- English / Japanese / Both display switching
- English demo vowel set `/i ɪ ɛ æ ʌ ə ɑ ɔ ʊ u/`
- Japanese demo vowel set `/i e a o ɯ/`
- short retriggerable ~0.5 s steady-vowel bursts in Vowel Buttons mode
- visual tongue morphing separated from button-mode audio targets
- softer short-note attack/release to reduce consonant-like transients
- brief source reuse across repeated taps to reduce oscillator onset clicks
- pointer/touch dragging of the tongue body in Mouth Synth mode
- keyboard arrow-key alternative for the tongue handle
- Child / Teen / Adult / Soft-airy voice-rendering presets
- Child voice as the default
- F0 control
- lip-rounding control in Mouth Synth mode
- `VOICE ON/OFF` only for continuous Mouth Synth use
- live F1/F2/F3 synthesis estimates
- responsive phone/tablet/desktop layout
- separate state, constraint, audio, mouth renderer, vowel-map renderer, data, and app-controller files

### v0.3.1 button-audio fix

Vowel Buttons now synthesizes the selected target vowel from note onset instead of first sounding the previous articulation and then following the visual tongue animation. The mouth may still animate into its new position for clarity, but that visual morph is not sent to the audio engine in button mode. This prevents the accidental formant transition that could make isolated vowels sound like consonant-vowel syllables such as /pa pi pu pe po/.

### Important evidence status

The current vowel-map positions, tongue targets, and formant mapping are explicitly a **pedagogical/demo model**. They are **not yet source-backed empirical English/Japanese normative values or measured anatomy**.

The simplified vowel quadrilateral is a phonetic teaching map. It must not be described as a literal anatomical coordinate system.

The next scientific-data milestone is to port verified Formant Canvas vowel values into the versioned target schema while preserving population, context, source, and evidence type.

## Current file layout

```text
articulation-lab/
  index.html
  data/
    voice-profiles.js
    vowel-presets.js
    source-registry.json
  src/
    state-store.js
    constraint-mapper.js
    audio/
      formant-engine.js
    renderers/
      simple-renderer.js
      vowel-map.js
    app.js
  styles/
    base.css
  contracts/
  docs/
```

The mouth renderer does not own tongue position. `ArticulationState` is the source of truth. The vowel map is a separate selection renderer that points to presets. A future `CuteRenderer` or `AnatomyRenderer` should consume the same state and must not alter scientific/acoustic data merely to fit a visual design.

## Interaction contract

### Vowel Buttons

- mouth handle is visually subdued and non-interactive
- vowel buttons live on the separate vowel quadrilateral, not on top of the tongue
- one tap selects a preset, animates the modeled articulation, and triggers ~0.5 s of steady vowel sound
- visual tongue animation does not create an audible formant-transition path in button mode
- rapid taps may retrigger/change the sound without requiring a separate VOICE button
- language filter supports English, Japanese, or Both

### Mouth Synth

- vowel quadrilateral is hidden
- tongue handle becomes fully interactive
- VOICE ON/OFF controls continuous sound
- dragging the tongue updates sound continuously

## Non-goals for v0.3.1

- 3D rendering
- microphone-based pronunciation scoring
- consonants
- nasal coupling
- full jaw/tongue-tip control
- claiming a unique inverse mapping from acoustics to anatomy
- claiming the current demo vowel values are empirical language norms
- treating the vowel quadrilateral as measured tongue geometry

## Planned educational modes

- **COMPARE** — A/B and morph comparison, especially Japanese vs English vowels
- **LEARN** — move from a familiar Japanese vowel toward an English target zone
- **PHONETICS** — show acoustic values, population, source, and evidence type

## Handoff rule

A graphics/UI contributor should normally edit renderer/style/UI files, not scientific data or acoustic mappings. See `docs/META_AI_HANDOFF.md` and `docs/SCIENTIFIC_CONTRACT.md`.

## Repository status

This folder currently lives in the Formant Canvas repository as a **staging implementation** on branch `design/articulation-lab-v0.1`. The branch name is historical; the staged app itself is now v0.3.1. It remains intentionally isolated from Formant Canvas `main`. The intended end state is a separate Articulation Lab repository, with shared data contracts between the two apps.
