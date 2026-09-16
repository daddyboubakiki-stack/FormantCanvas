# Articulation Lab — v0.5-alpha.18 staging checkpoint

Articulation Lab is a proposed sister app to Formant Canvas.

- **Formant Canvas:** manipulate acoustic space and hear the result.
- **Articulation Lab:** manipulate vocal-tract articulation and hear the result.

The app deliberately separates two experiences:

1. **Vowel Buttons** — tap IPA buttons. A short **human recording** plays while a separate pedagogical articulation target is visualized.
2. **Mouth Synth** — turn on continuous synthesis and manipulate a pedagogical articulation model like an instrument.

This prevents real recorded vowel evidence and freely generated articulatory synthesis from pretending to be the same scientific object.

## v0.5-alpha.18 checkpoint

### Simple / Cute skin switch

The frontal teaching model now has two visual skins driven by the same articulation state. `Simple` preserves the alpha.17 schematic face. `Cute` adds an original small-monkey exterior with a round silhouette, large ears and eyes, a squirrel-monkey-inspired face patch, and thinner lips. The skin changes presentation only; articulation targets, mouth-state semantics, recordings, synthesis, coordination, and IPA estimation are unchanged.

The current checkpoint consolidates the visual-articulation work that was user-reviewed through alpha.3–alpha.17.

### Shared side + front articulation

Both views are driven by the same articulation state. Shared axes currently include:

- tongue-body front/back
- tongue-body high/low
- tongue-root retraction
- independent jaw opening
- lip rounding
- lip spreading

`Side / Front / Both` switching remains available.

### Frontal Simple skin

The current frontal renderer is intentionally schematic rather than photorealistic. It now includes:

- a neutral-gray UI/background rather than the earlier warm yellow cast
- stronger visual narrowing/protrusion for rounded vowels, especially `/u/`
- a smoother single-color lip contour
- a short-midface, friendly schematic face
- round eyes with short, soft brows
- the earlier simple line nose
- teeth clipped inside the mouth aperture
- upper/lower tooth widths kept close, with the upper row slightly wider
- a state-dependent choice between showing lower teeth or the tongue so the lower oral slot does not become visually crowded
- intentionally **no gum layer** in Simple skin, after testing showed that gums added complexity without reliably improving the teaching view across narrow/open postures

The renderer remains a teaching model, not measured anatomy.

### Close front vowels and lower teeth

For close, spread postures such as `/i/` and `/ɪ/`, the renderer can prioritize lower teeth to suggest the familiar front-view “ee/grin” appearance. More open front vowels such as `/ɛ/` and `/æ/` prioritize the tongue instead.

This is a display heuristic for clarity, not a claim that one structure is literally invisible in all speakers.

### Natural / Independent free articulation

Mouth Synth has two coordination modes:

- **Natural** (default): dragging the tongue also moves jaw opening, lip spread, lip rounding and tongue-root retraction using a smooth interpolation field built from the shared vowel teaching targets.
- **Independent**: tongue, jaw and lips can be manipulated separately, including deliberately unusual combinations.

Natural coordination is a pedagogical interpolation, not an anatomical inverse solver. Tongue position does not uniquely determine all other articulators in real speech.

### Approximate IPA while Mouth Synth is sounding

Mouth Synth displays `≈ [IPA]` while VOICE is on.

The estimator compares the current synth's modeled F1/F2/F3 values with the same synth model evaluated at the English/Japanese vowel anchors. It is explicitly a **pedagogical synth estimate**, not automatic transcription of a human speaker.

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
- continuous synthesis retained for Mouth Synth
- retained v0.4.2 Japanese/loudness repair
- retained v0.4.3 natural KIT `/ɪ/` nucleus from US-English `kid`, with no time-stretch
- explicit provenance and redistribution boundaries

## Scientific / educational precedents

The design is informed by established articulatory resources without copying their artwork or restricted materials.

- **Seeing Speech / STAR:** imaging-backed 2-D articulator animation and independent jaw/tongue-region control
- **Sounds of Speech (University of Iowa):** articulatory animation + audio + teaching material
- **Dynamic Dialects:** synchronized lip video and ultrasound tongue imaging
- **VocalTractLab:** higher-level phonetic controls separated from a richer tract model; area-function work is a future direction

Restricted artwork/video from reference resources is not modified or bundled here.

## Scientific boundary

Articulation Lab intentionally separates:

- **recorded audio evidence** — a human sample with documented preprocessing
- **articulatory teaching target** — modeled tongue/jaw/lip posture
- **Mouth Synth acoustics** — continuous pedagogical synthesis

A human recording tells us how that recorded person sounded. It does not uniquely determine the anatomy that produced the sound. Multiple articulations can produce similar acoustics.

The cavity shading is a teaching visualization, not a measured area function.

## Audio licensing policy

Only recordings with sufficiently explicit redistribution permission are bundled. “Publicly downloadable” or “usable for research” is not treated as redistribution permission.

## Distribution build

`.github/workflows/articulation-v04-preview.yml` is a historical filename. It validates the current alpha checkpoint and builds:

- `ArticulationLab_v0.5-alpha.18.html` — self-contained preview with CSS, JavaScript and vetted WAV samples embedded
- `ArticulationLab_v0.5-alpha.18_source.zip` — modular source bundle

Validation includes JavaScript syntax, articulation-target / recording-data separation, Natural coordination behavior, strong `/u/` rounding geometry, nearest-modeled-IPA checks, retained real-voice provenance/duration/loudness checks, and standalone packaging.

## Next stages

- design exploration in a separate MetaAI/Cute branch
- Anatomy skin
- additional Cute characters driven by the same articulation state
- Compare A/B overlay
- richer tract acoustics / area-function exploration
- consonant-ready tongue-tip, constriction, velum, airflow and voicing controls

## Repository status

This folder lives in the Formant Canvas repository as a **staging implementation**. The original staging branch name, `design/articulation-lab-v0.1`, is historical. The current Cute-skin checkpoint is **v0.5-alpha.18**.

The draft staging PR should **not** be merged into Formant Canvas `main` merely to ship this sister-app prototype.
