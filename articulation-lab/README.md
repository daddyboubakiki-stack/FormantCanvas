# Articulation Lab — v0.5-alpha.2 staging build

Articulation Lab is a proposed sister app to Formant Canvas.

- **Formant Canvas:** manipulate acoustic space and hear the result.
- **Articulation Lab:** manipulate vocal-tract articulation and hear the result.

The app deliberately separates two experiences:

1. **Vowel Buttons** — tap IPA buttons. A short **human recording** plays while a separate pedagogical articulation target is visualized.
2. **Mouth Synth** — turn on continuous synthesis and manipulate a pedagogical articulation model like an instrument.

This prevents “real recorded vowel evidence” and “freely generated articulatory synthesis” from pretending to be the same scientific object.

## v0.5-alpha.2 — front-view refinement, stronger rounding, approximate IPA

### More human-looking frontal Simple skin

The frontal mouth is no longer built from two plain concentric ellipses. The renderer now uses shaped Bezier contours with:

- a simplified Cupid's-bow upper-lip contour
- a fuller lower-lip contour
- distinct mouth-corner geometry
- a separate darker oral cavity
- more subdued, anatomically distinct colors for lips, tongue, teeth and skin
- small nostril cues
- subtle upper-incisor separators
- reduced lower-incisor prominence

This remains a schematic teaching face, not photorealistic anatomy.

### Stronger visible rounding

User review found the /u/-like rounded posture visually too open. alpha.2 therefore makes strong rounding visibly reduce **both horizontal and vertical aperture** while increasing side-view protrusion.

The CI now explicitly checks that the pedagogical English `/u/` target has a much smaller frontal aperture than `/æ/`.

### Approximate IPA while Mouth Synth is sounding

Mouth Synth now displays a prominent `≈ [IPA]` hint while VOICE is on.

The estimator does **not** infer IPA from the drawing alone. It compares the current synth's modeled F1/F2/F3 values with the same synth model evaluated at the 15 English/Japanese vowel anchors, and reports the nearest anchor.

This means:

- jaw-opening effects already represented in the synth can affect the estimate
- lip-rounding effects already represented in the synth can affect the estimate
- visual-only axes such as `lipSpread` do not falsely count as audible evidence

The readout is explicitly a **pedagogical synth estimate**, not automatic phonetic transcription of a human speaker.

## v0.5-alpha.1 — Natural / Independent free articulation

Mouth Synth has two coordination modes:

- **Natural** (default): dragging the tongue also moves jaw opening, lip spread, lip rounding and tongue-root retraction using a smooth interpolation field built from the shared vowel teaching targets.
- **Independent**: tongue, jaw and lips can be manipulated separately, including deliberately unusual combinations.

Natural coordination is a pedagogical interpolation, not an anatomical inverse solver. Tongue position does not uniquely determine all other articulators in real speech.

## v0.5 visual foundation

Articulation targets are stored separately from recording metadata in `data/articulation-targets.js`.

Shared normalized articulation axes currently include:

- tongue body front/back
- tongue body high/low
- tongue-root retraction
- independent jaw opening
- lip rounding
- lip spreading

The sagittal Simple renderer includes jaw movement, tongue-root response, lip rounding/spreading and schematic airway shading. The frontal Simple renderer shows vertical/horizontal aperture, rounding, teeth/tongue visibility and jaw/chin movement from the **same articulation state**.

Side / Front / Both switching is available.

## First visual acceptance pair: `/æ/` vs `/ɑ/`

### `/æ/` TRAP

- front-low tongue-body target
- lower tongue-root retraction
- strongly open jaw
- very little rounding
- stronger lateral lip spread

### `/ɑ/` PALM

- back-low tongue-body target
- greater tongue-root retraction
- slightly larger vertical jaw opening
- very little rounding
- much less lateral lip spread

These are teaching targets, not measured anatomy or claims about every English speaker.

## Scientific / educational precedents

The design is informed by established articulatory resources without copying their artwork or restricted materials.

- **Seeing Speech / STAR**: useful precedent for imaging-backed 2-D articulator animation, independent jaw motion and multiple tongue regions.
- **Sounds of Speech (University of Iowa)**: useful precedent for combining articulatory animation, real-speaker visual material, audio and explanatory teaching content.
- **Dynamic Dialects**: useful reference for synchronized lip video and ultrasound tongue imaging.
- **VocalTractLab**: useful precedent for separating higher-level phonetic controls from a richer tract model and for future area-function-based acoustics.

Seeing Speech and Dynamic Dialects are treated as reference/validation resources; their restricted artwork/video is not modified or bundled into this app.

## Current Mouth Synth acoustic boundary

The current pedagogical formant mapping responds directly to:

- tongue-body front/back
- tongue-body high/low
- jaw opening
- lip rounding

`lipSpread` and `tongueRootRetraction` are currently primarily visual/model-state axes. Strong acoustic coefficients are intentionally deferred until a more principled vocal-tract / area-function model is introduced.

## Existing real-voice foundation retained

- English / Japanese / Both switching
- English buttons `/i ɪ ɛ æ ʌ ə ɑ ɔ ʊ u/`
- Japanese buttons `/i e a o ɯ/`
- locally bundled human recordings for Vowel Buttons
- cached/retriggerable playback with short fades
- continuous synthesis retained for Mouth Synth
- Child / Teen / Adult / Soft-airy synth-rendering profiles
- synth F1/F2/F3 estimates shown only in Mouth Synth
- fail-closed duration/loudness validation

### Japanese/loudness repair (v0.4.2)

Japanese source recordings contain unusually short repeated kana tokens. The build detects an actual voiced token, retains onset/offset margin, applies documented pitch-preserving duration adjustment, and active-RMS matches the resulting samples while respecting peak headroom.

Current Japanese outputs contain about **0.39–0.41 s** of audible vowel material.

### Natural KIT `/ɪ/` (v0.4.3)

The generic isolated IPA `/ɪ/` was replaced after listening review with the vowel nucleus from a US-English `kid` recording.

- source: `En-us-kid.ogg`
- author/speaker attribution: Dvortygirl
- Wikimedia Commons
- CC BY-SA 2.5
- selected interval approximately `0.205–0.315 s`
- exported length approximately `0.110 s`
- no time-stretch
- 6 ms fade-in / 10 ms fade-out
- mono 24 kHz conversion + active-RMS matching

## Scientific boundary

Articulation Lab intentionally separates:

- **recorded audio evidence** — a human sample with documented preprocessing
- **articulatory teaching target** — modeled tongue/jaw/lip posture
- **Mouth Synth acoustics** — continuous pedagogical synthesis

A human recording tells us how that recorded person sounded. It does not uniquely determine the anatomy that produced the sound. Multiple articulations can produce similar acoustics.

The cavity shading is a teaching visualization, not a measured area function.

## Audio licensing policy

Only recordings with sufficiently explicit redistribution permission are bundled. “Publicly downloadable” or “usable for research” is not treated as redistribution permission.

Research corpora such as JVPD are not copied into the app unless their terms explicitly permit the intended redistribution.

## Distribution build

`.github/workflows/articulation-v04-preview.yml` is a historical filename. It now validates alpha.2 and builds:

- `ArticulationLab_v0.5-alpha.2.html` — self-contained preview with CSS, JavaScript and vetted WAV samples embedded
- `ArticulationLab_v0.5-alpha.2_source.zip` — modular source bundle

Validation includes:

- JavaScript syntax
- articulation-target / recording-data separation
- Natural coordination behavior
- strong `/u/` rounding geometry relative to `/æ/`
- nearest-modeled-IPA checks for `/u/` and `/æ/`
- retained v0.4.3 audio provenance/duration/loudness checks
- self-contained distribution packaging

## Next stages

- user-device review of alpha.2 mouth geometry and approximate IPA behavior
- further tune teeth, lip contour and face proportions
- renderer/skin registry
- Anatomy skin
- Cute exterior skins (monkey/cat/etc.) driven by exactly the same articulation state
- Compare A/B overlay
- richer tract acoustics / area-function exploration
- consonant-ready tongue-tip, constriction, velum, airflow and voicing controls

## Repository status

This folder lives in the Formant Canvas repository as a **staging implementation** on branch `design/articulation-lab-v0.1`. The branch name is historical. The current staged app is v0.5-alpha.2.

The draft staging PR should **not** be merged into Formant Canvas `main` merely to ship this sister-app prototype.
