# Articulation Lab — v0.4 staging build

Articulation Lab is a proposed sister app to Formant Canvas.

- **Formant Canvas:** manipulate acoustic space and hear the result.
- **Articulation Lab:** manipulate vocal-tract articulation and hear the result.

The app deliberately separates two play experiences.

1. **Vowel Buttons** — tap IPA buttons on a simplified vowel quadrilateral. The mouth moves toward a pedagogical posture while a short **human recording** plays.
2. **Mouth Synth** — turn on continuous synthesis and drag the tongue directly like an instrument.

This keeps “hear a real vowel example” and “freely play an articulatory model” from pretending to be the same scientific object.

## v0.4 implementation status

Implemented:

- 2D midsagittal **Simple** mouth skin
- separate **Vowel Buttons** and **Mouth Synth** modes
- simplified vowel quadrilateral independent from the mouth drawing
- English / Japanese / Both switching
- English button set `/i ɪ ɛ æ ʌ ə ɑ ɔ ʊ u/`
- Japanese button set `/i e a o ɯ/`
- **locally bundled real-human WAV playback** for Vowel Buttons
- preloading, decoding cache, retriggering, and short attack/release fades for stable button playback
- synth fallback if a recording cannot be decoded
- real-audio playback kept independent from the visual tongue morph
- continuous source-filter synthesis retained for Mouth Synth
- pointer/touch and keyboard tongue control in Mouth Synth
- Child / Teen / Adult / Soft-airy **synth-rendering** profiles
- F0 and lip-rounding controls in Mouth Synth
- live synth F1/F2/F3 estimates shown only in Mouth Synth
- responsive phone/tablet/desktop layout
- automated real-voice bundle build and automated self-contained preview build

## Real-voice sets currently bundled

### Japanese reference voice

- five language-specific Japanese vowel recordings: あ・い・う・え・お
- locally trimmed to short stable-vowel samples
- source license recorded as **Public Domain (PD-self)**
- these are examples of one recorded Japanese speaker, not a population norm

### English-labelled IPA reference

- ten vowels extracted from a human “All IPA Vowels” reference recording
- source license recorded as **CC0 1.0**
- this is a generic human IPA reference set, **not** a General American population norm and not a matched male/female/child corpus

`assets/audio/real/real-voice-sources.json` and `build-report.json` preserve provenance/build information for the bundled samples.

## Scientific boundary

A human recording tells us how **that recorded person** sounded. The mouth pose drawn above it is a pedagogical model unless measured articulatory data says otherwise.

Therefore v0.4 intentionally separates:

- **recorded audio evidence** — human voice sample
- **articulatory teaching target** — modeled tongue/lip posture
- **Mouth Synth acoustics** — continuous pedagogical synthesis model

The vowel quadrilateral is a phonetic teaching map, not literal measured tongue geometry. F1/F2 do not uniquely determine a tongue posture.

## Interaction contract

### Vowel Buttons

- mouth handle is subdued and non-interactive
- buttons live on the separate vowel quadrilateral
- tapping a button plays a short locally bundled human recording when available
- the mouth may animate toward the teaching posture, but this visual morph does not modify the recording
- rapid taps retrigger without a separate VOICE switch
- English / Japanese / Both filtering remains
- synth formant readouts are hidden in this mode to avoid presenting model estimates as measurements of the recording

### Mouth Synth

- vowel quadrilateral is hidden
- tongue handle becomes interactive
- VOICE ON/OFF controls continuous synthesis
- dragging the tongue changes the synthesized sound continuously
- synth F1/F2/F3 estimates remain explicitly labeled as model output

## Audio licensing policy

Only recordings with sufficiently explicit permission for redistribution are bundled. “Publicly downloadable” or “usable for research” is **not** treated as equivalent to redistribution permission.

For that reason, corpora such as JVPD or other research datasets are not copied into the app unless their terms explicitly permit the intended redistribution. Hillenbrand material remains scientifically useful for analysis, but recordings are not bundled merely because a mirror repository has a software license.

Male / female / child language-matched recording sets remain a future addition and should be added only when both the recording license and speaker metadata are explicit.

## Current file layout

```text
articulation-lab/
  index.html
  assets/audio/real/
    jp_reference/
    ipa_reference/
    real-voice-sources.json
    build-report.json
  data/
    voice-profiles.js
    vowel-presets.js
    source-registry.json
  src/
    state-store.js
    constraint-mapper.js
    audio/
      formant-engine.js
      sample-player.js
    renderers/
      simple-renderer.js
      vowel-map.js
    app.js
  styles/
    base.css
  tools/
    build_real_voice_bundle.py
    build_standalone_preview.py
  contracts/
  docs/
```

## Distribution build

`.github/workflows/articulation-v04-preview.yml` validates JavaScript syntax and builds:

- `ArticulationLab_v0.4.html` — self-contained single-file preview with CSS, JavaScript, and the vetted WAV samples embedded
- `ArticulationLab_v0.4_source.zip` — modular source bundle

The self-contained build contains no local external script, stylesheet, or audio-file dependency.

## Non-goals for v0.4

- 3D rendering
- microphone-based pronunciation scoring
- consonants
- nasal coupling
- full jaw/tongue-tip control
- claiming a unique inverse mapping from acoustics to anatomy
- claiming current teaching postures are measured anatomy
- claiming the English IPA reference voice is a population norm

## Planned educational modes

- **COMPARE** — A/B comparison, especially Japanese vs English vowels
- **LEARN** — move from a familiar Japanese vowel toward an English target zone
- **PHONETICS** — show acoustic values, population, source, and evidence type when source-backed data exists

## Repository status

This folder currently lives in the Formant Canvas repository as a **staging implementation** on branch `design/articulation-lab-v0.1`. The branch name is historical; the staged app itself is now v0.4. It remains intentionally isolated from Formant Canvas `main` and should not be merged merely to ship this staging folder.
