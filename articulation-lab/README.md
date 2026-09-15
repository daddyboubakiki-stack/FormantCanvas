# Articulation Lab — v0.5-alpha staging build

Articulation Lab is a proposed sister app to Formant Canvas.

- **Formant Canvas:** manipulate acoustic space and hear the result.
- **Articulation Lab:** manipulate vocal-tract articulation and hear the result.

The app deliberately separates two play experiences.

1. **Vowel Buttons** — tap IPA buttons. A short **human recording** plays while a separate pedagogical articulation target is visualized.
2. **Mouth Synth** — turn on continuous synthesis and manipulate the teaching model like an instrument.

This keeps “hear a real vowel example” and “freely play an articulatory model” from pretending to be the same scientific object.

## v0.5-alpha visual foundation

The v0.5 work starts moving the app from a single tongue-point diagram toward a reusable whole-vocal-tract teaching model.

Implemented in the alpha foundation:

- articulation targets separated from recording metadata (`data/articulation-targets.js`)
- shared normalized axes for:
  - tongue body front/back
  - tongue body high/low
  - tongue-root retraction
  - independent jaw opening
  - lip rounding
  - lip spreading
- upgraded sagittal Simple renderer:
  - jaw rotation/translation
  - lower jaw/lip/teeth move together
  - tongue root responds separately from tongue body
  - schematic visible airway/cavity fill
- new frontal Simple renderer:
  - vertical mouth opening follows jaw opening
  - horizontal width follows lip spread
  - rounding narrows/rounds the aperture
  - teeth/tongue visibility changes with the shared state
  - lower face/chin visibly follows jaw opening
- Side / Front / Both view switching
- Mouth Synth jaw-opening and lip-spread controls
- initial `/æ/` versus `/ɑ/` visual teaching contrast
- CI validation that recording presets do not silently embed a second articulation geometry

The initial visual target values are **pedagogical models**, not measured anatomy. See `docs/V0_5_ALPHA_IMPLEMENTATION.md` for implementation rationale and scientific/educational precedents.

## Scientific precedents for the visual architecture

- Seeing Speech / STAR uses imaging-backed 2-D head animation with jaw translation/rotation and multiple tongue control regions. Articulation Lab uses that as a conceptual validation for treating jaw and tongue regions as separate controls, without copying its artwork.
- VocalTractLab demonstrates a useful separation between higher-level phonetic controls and a much richer tract model. Its full model derives an area function from tract geometry; Articulation Lab's current cavity shading is only a schematic teaching hint, not a computed area function.

## `/æ/` versus `/ɑ/` alpha target

The first acceptance pair deliberately makes more than the tongue point change.

### `/æ/` TRAP

- front-low tongue-body target
- lower tongue-root retraction target
- strongly open jaw
- very little rounding
- stronger lateral lip spread

### `/ɑ/` PALM

- back-low tongue-body target
- more posterior/retracted tongue-root target
- slightly larger vertical jaw opening
- very little rounding
- much less lateral lip spread

This is meant to make the user's observation visible: the two low vowels can differ in **how the mouth opens**, not only where a dot sits on a vowel quadrilateral. The implementation does not claim that `/ɑ/` simply creates a uniformly larger pharyngeal cavity; tongue-root retraction can locally narrow/reshape the pharyngeal airway.

## Existing v0.4 real-voice foundation retained

- English / Japanese / Both switching
- English button set `/i ɪ ɛ æ ʌ ə ɑ ɔ ʊ u/`
- Japanese button set `/i e a o ɯ/`
- locally bundled real-human WAV playback for Vowel Buttons
- cached/retriggerable sample playback with short fades
- continuous source-filter synthesis retained for Mouth Synth
- Child / Teen / Adult / Soft-airy synth-rendering profiles
- synth F1/F2/F3 estimates shown only in Mouth Synth
- fail-closed duration/loudness validation for processed teaching samples

### Japanese/loudness repair (v0.4.2)

User-device listening exposed that the first real-voice bundle made Japanese vowels feel much too short, Japanese `/i/` was effectively inaudible, and English `/ɔ/` was quieter than its neighbors. v0.4.2 changed Japanese preprocessing from fixed midpoint cropping to voiced-token detection, added pitch-preserving duration adjustment for unusually short Japanese source tokens, and active-RMS matched the button recordings with peak-headroom protection.

Current Japanese outputs contain about **0.39–0.41 s of audible vowel material**. The duration adjustment is intentionally disclosed: they remain recordings of a real speaker, but the button duration is not the speaker’s untouched token duration.

### Natural KIT `/ɪ/` (v0.4.3)

A listening review found that the isolated generic IPA-reference `/ɪ/` could sound unlike a familiar English KIT vowel when heard alone. v0.4.3 replaces that button with a language-specific US-English source.

- word: `kid`
- recording: `En-us-kid.ogg`
- speaker/author: Dvortygirl
- source: Wikimedia Commons
- license used: **CC BY-SA 2.5**
- selected interval: approximately `0.205–0.315 s`
- exported vowel length: approximately `0.110 s`
- no time-stretch
- 6 ms fade-in + 10 ms fade-out
- mono 24 kHz conversion + active-RMS matching

The `/k/` release/aspiration and `/d/` closure are excluded. Preserving the naturally short KIT duration is deliberate.

## Real-voice sets currently bundled

### Japanese reference voice

- five Japanese vowels: あ・い・う・え・お
- one speaker
- Public Domain (PD-self)
- voiced-token detection + documented duration adjustment
- example voice, not a population norm

### Generic IPA reference

Nine current English-labelled buttons still use vowels extracted from the human “All IPA Vowels” reference recording:

- CC0 1.0
- active-RMS level matched
- generic IPA reference, **not** a General American population norm

### US-English KIT reference

- `/ɪ/` extracted from `kid`
- Dvortygirl
- CC BY-SA 2.5
- no time-stretch
- language-specific US-English word evidence

## Scientific boundary

Articulation Lab intentionally separates:

- **recorded audio evidence** — a human sample with documented preprocessing
- **articulatory teaching target** — modeled tongue/jaw/lip posture
- **Mouth Synth acoustics** — continuous pedagogical synthesis model

A human recording tells us how **that recorded person** sounded. It does not tell us the unique tongue position that produced the recording. Multiple articulations can produce similar acoustics, and F1/F2 do not uniquely determine anatomy.

The new `lipSpread` and `tongueRootRetraction` axes are primarily visual/model-state parameters in this alpha. The existing synth already uses `jawOpening` in its pedagogical F1 mapping. The project deliberately avoids inventing strong acoustic coefficients for every new visual axis without a more principled tract/area-function model.

## Audio licensing policy

Only recordings with sufficiently explicit redistribution permission are bundled. “Publicly downloadable” or “usable for research” is **not** treated as redistribution permission.

Research corpora such as JVPD are not copied into the app unless their terms explicitly permit the intended redistribution. Male / female / child language-matched recording sets remain a future addition and should be added only when both recording rights and speaker metadata are explicit.

## Distribution build

`.github/workflows/articulation-v04-preview.yml` (historical filename) now validates the v0.5-alpha code/data split, retains the v0.4.3 audio-bundle checks, and builds:

- `ArticulationLab_v0.5-alpha.html` — self-contained preview with CSS, JavaScript, and vetted WAV samples embedded
- `ArticulationLab_v0.5-alpha_source.zip` — modular source bundle

The self-contained build contains no local external script, stylesheet, or audio-file dependency.

## Current non-goals for this alpha

- 3D rendering
- microphone-based pronunciation scoring
- claiming current teaching postures are measured anatomy
- claiming a unique inverse mapping from acoustics to anatomy
- pretending the schematic cavity fill is an area function
- full consonant synthesis in this alpha

## Next visual stages

1. user-device review of the v0.5 side/front geometry
2. tune the `/æ/` versus `/ɑ/` contrast from visual feedback
3. add renderer/skin registry
4. Anatomy skin
5. Cute exterior skins (e.g. monkey/cat) driven by exactly the same articulation state
6. Compare A/B overlay
7. consonant-ready controls: tongue tip, constriction degree/location, velum, airflow and voicing visualization

## Repository status

This folder lives in the Formant Canvas repository as a **staging implementation** on branch `design/articulation-lab-v0.1`. The branch name is historical; the staged app itself is now v0.5-alpha. It remains intentionally isolated from Formant Canvas `main` and should not be merged merely to ship this staging folder.
