# Articulation Lab — v0.4.3 staging build

Articulation Lab is a proposed sister app to Formant Canvas.

- **Formant Canvas:** manipulate acoustic space and hear the result.
- **Articulation Lab:** manipulate vocal-tract articulation and hear the result.

The app deliberately separates two play experiences.

1. **Vowel Buttons** — tap IPA buttons on a simplified vowel quadrilateral. The mouth moves toward a pedagogical posture while a short **human recording** plays.
2. **Mouth Synth** — turn on continuous synthesis and drag the tongue directly like an instrument.

This keeps “hear a real vowel example” and “freely play an articulatory model” from pretending to be the same scientific object.

## v0.4.3 implementation status

Implemented:

- 2D midsagittal **Simple** mouth skin
- separate **Vowel Buttons** and **Mouth Synth** modes
- English / Japanese / Both switching
- English button set `/i ɪ ɛ æ ʌ ə ɑ ɔ ʊ u/`
- Japanese button set `/i e a o ɯ/`
- locally bundled real-human WAV playback for Vowel Buttons
- cached/retriggerable sample playback with short fades
- continuous source-filter synthesis retained for Mouth Synth
- Child / Teen / Adult / Soft-airy synth-rendering profiles
- synth F1/F2/F3 estimates shown only in Mouth Synth
- automated real-voice bundle and self-contained preview builds
- fail-closed duration/loudness validation for processed teaching samples

## v0.4.2 Japanese/loudness repair

User-device listening exposed that the first real-voice bundle made Japanese vowels feel much too short, Japanese `/i/` was effectively inaudible, and English `/ɔ/` was quieter than its neighbors. v0.4.2 therefore changed Japanese preprocessing from fixed midpoint cropping to voiced-token detection, added pitch-preserving duration adjustment for the unusually short Japanese source tokens, and active-RMS matched the button recordings with peak-headroom protection.

Current Japanese outputs contain about **0.39–0.41 s of audible vowel material**. The duration adjustment is intentionally disclosed: they remain recordings of a real speaker, but the button duration is not the speaker’s untouched token duration.

## v0.4.3 KIT `/ɪ/` replacement

A second listening review found that the isolated IPA-reference `/ɪ/` could sound unlike a familiar English KIT vowel when heard by itself. Rather than treating a generic isolated IPA production as if it were automatically the best English-teaching example, v0.4.3 replaces only the KIT button with a language-specific US-English source.

Source:

- **word:** `kid`
- **recording:** `En-us-kid.ogg`
- **speaker/author:** Dvortygirl
- **variety:** US English, as described by the source page
- **source:** Wikimedia Commons
- **license used by this app:** **CC BY-SA 2.5** (the original is dual-licensed with GFDL 1.2+)

Acoustic inspection of the source gives a clean segmentation:

- approximately **0.09–0.20 s:** `/k/` release and aspiration
- approximately **0.205–0.315 s:** voiced KIT vowel nucleus
- after approximately **0.32 s:** transition into `/d/` closure

The app therefore exports the approximately **0.110 s** vowel interval from `0.205–0.315 s`. It receives only:

- mono 24 kHz conversion
- 6 ms fade-in
- 10 ms fade-out
- active-RMS level matching

It receives **no time-stretch**. Preserving this short duration is deliberate: duration is part of the natural English realization rather than a defect to be equalized away.

The adapted KIT clip remains attributed to Dvortygirl and is distributed under CC BY-SA 2.5. Source/provenance metadata are also preserved in `assets/audio/real/real-voice-sources.json` and `build-report.json`.

## Real-voice sets currently bundled

### Japanese reference voice

- five language-specific Japanese vowel recordings: あ・い・う・え・お
- one Japanese speaker
- source license recorded as **Public Domain (PD-self)**
- voiced token detected automatically from each source recording
- duration adjusted for button usability
- examples of one speaker, not a population norm

### Generic IPA reference

Nine current English-labelled buttons still use vowels extracted from the human “All IPA Vowels” reference recording:

- source license **CC0 1.0**
- active-RMS level-matched for button comparison
- generic human IPA reference, **not** a General American population norm

KIT `/ɪ/` is intentionally excluded from this source set as of v0.4.3.

### US-English KIT reference

- `/ɪ/` extracted from `kid`
- Dvortygirl
- CC BY-SA 2.5
- no time-stretch
- language-specific English word evidence rather than an isolated generic IPA demonstration

## Scientific boundary

A human recording tells us how **that recorded person** sounded. Audio processing such as trimming, time-stretch, fades, and level matching is documented separately. The mouth pose drawn above it is a pedagogical model unless measured articulatory data says otherwise.

Articulation Lab intentionally separates:

- **recorded audio evidence** — human voice sample, with documented preprocessing
- **articulatory teaching target** — modeled tongue/lip posture
- **Mouth Synth acoustics** — continuous pedagogical synthesis model

The vowel quadrilateral is a phonetic teaching map, not literal measured tongue geometry. F1/F2 do not uniquely determine a tongue posture.

## Audio licensing policy

Only recordings with sufficiently explicit permission for redistribution are bundled. “Publicly downloadable” or “usable for research” is **not** treated as redistribution permission.

For that reason, corpora such as JVPD or other research datasets are not copied into the app unless their terms explicitly permit the intended redistribution. Male / female / child language-matched recording sets remain a future addition and should be added only when both recording rights and speaker metadata are explicit.

## Distribution build

`.github/workflows/articulation-v04-preview.yml` validates JavaScript syntax, the processed-audio report, and builds:

- `ArticulationLab_v0.4.3.html` — self-contained single-file preview with CSS, JavaScript, and vetted WAV samples embedded
- `ArticulationLab_v0.4.3_source.zip` — modular source bundle

The self-contained build contains no local external script, stylesheet, or audio-file dependency. Attribution links for the adapted CC BY-SA KIT source remain visible in the UI.

## Non-goals

- 3D rendering
- microphone-based pronunciation scoring
- consonants
- full jaw/tongue-tip control
- claiming a unique inverse mapping from acoustics to anatomy
- claiming current teaching postures are measured anatomy
- claiming the generic English IPA reference voice is a population norm

## Planned educational modes

- **COMPARE** — A/B comparison, especially Japanese vs English vowels
- **LEARN** — move from a familiar Japanese vowel toward an English target zone
- **PHONETICS** — show acoustic values, population, source, and evidence type when source-backed data exists

## Repository status

This folder currently lives in the Formant Canvas repository as a **staging implementation** on branch `design/articulation-lab-v0.1`. The branch name is historical; the staged app itself is now v0.4.3. It remains intentionally isolated from Formant Canvas `main` and should not be merged merely to ship this staging folder.
