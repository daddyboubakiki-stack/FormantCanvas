# Articulation Lab — v0.4.1 staging build

Articulation Lab is a proposed sister app to Formant Canvas.

- **Formant Canvas:** manipulate acoustic space and hear the result.
- **Articulation Lab:** manipulate vocal-tract articulation and hear the result.

The app deliberately separates two play experiences.

1. **Vowel Buttons** — tap IPA buttons on a simplified vowel quadrilateral. The mouth moves toward a pedagogical posture while a short **human recording** plays.
2. **Mouth Synth** — turn on continuous synthesis and drag the tongue directly like an instrument.

This keeps “hear a real vowel example” and “freely play an articulatory model” from pretending to be the same scientific object.

## v0.4.1 implementation status

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

## v0.4.1 audio correction

User listening exposed two problems in the first v0.4 bundle: Japanese samples sounded abnormally short, Japanese `/i/` was effectively silent, and English `/ɔ/` was a little quieter than the other buttons.

The cause was preprocessing, not the language data itself:

- the Japanese source files contain several very short kana repetitions separated by long silence;
- v0.4 cropped a fixed window around the file midpoint, which could capture mostly silence;
- sample levels were not sufficiently matched for direct A/B button comparison.

v0.4.1 therefore:

1. detects an actual voiced Japanese token rather than cropping the file midpoint;
2. adds a small onset/offset margin;
3. uses pitch-preserving `atempo` processing to lengthen the unusually short Japanese source token for clearer button playback, capped at 3×;
4. active-RMS level-matches all bundled button samples to approximately **-17 dBFS**, subject to peak headroom.

The resulting Japanese WAV durations are roughly **0.34–0.40 s**. This processing is intentionally disclosed: they remain recordings of a real speaker, but their playback duration is **not the speaker’s untouched natural token duration**.

English `/ɔ/` is now level-matched using the same active-RMS target as the other button samples.

## Real-voice sets currently bundled

### Japanese reference voice

- five language-specific Japanese vowel recordings: あ・い・う・え・お
- one Japanese speaker
- source license recorded as **Public Domain (PD-self)**
- voiced token detected automatically from each source recording
- duration adjusted for button usability as described above
- examples of one speaker, not a population norm

### English-labelled IPA reference

- ten vowels extracted from a human “All IPA Vowels” reference recording
- source license recorded as **CC0 1.0**
- active-RMS level-matched for button comparison
- generic human IPA reference, **not** a General American population norm

`assets/audio/real/real-voice-sources.json` and `build-report.json` preserve provenance and processing metadata.

## Scientific boundary

A human recording tells us how **that recorded person** sounded. Audio processing such as trimming, time-stretch, fades, and level matching is documented separately. The mouth pose drawn above it is a pedagogical model unless measured articulatory data says otherwise.

Therefore v0.4.1 intentionally separates:

- **recorded audio evidence** — human voice sample, with documented preprocessing
- **articulatory teaching target** — modeled tongue/lip posture
- **Mouth Synth acoustics** — continuous pedagogical synthesis model

The vowel quadrilateral is a phonetic teaching map, not literal measured tongue geometry. F1/F2 do not uniquely determine a tongue posture.

## Audio licensing policy

Only recordings with sufficiently explicit permission for redistribution are bundled. “Publicly downloadable” or “usable for research” is **not** treated as redistribution permission.

For that reason, corpora such as JVPD or other research datasets are not copied into the app unless their terms explicitly permit the intended redistribution. Male / female / child language-matched recording sets remain a future addition and should be added only when both recording rights and speaker metadata are explicit.

## Distribution build

`.github/workflows/articulation-v04-preview.yml` validates JavaScript syntax and builds:

- `ArticulationLab_v0.4.1.html` — self-contained single-file preview with CSS, JavaScript, and vetted WAV samples embedded
- `ArticulationLab_v0.4.1_source.zip` — modular source bundle

The self-contained build contains no local external script, stylesheet, or audio-file dependency.

## Non-goals

- 3D rendering
- microphone-based pronunciation scoring
- consonants
- full jaw/tongue-tip control
- claiming a unique inverse mapping from acoustics to anatomy
- claiming current teaching postures are measured anatomy
- claiming the English IPA reference voice is a population norm

## Planned educational modes

- **COMPARE** — A/B comparison, especially Japanese vs English vowels
- **LEARN** — move from a familiar Japanese vowel toward an English target zone
- **PHONETICS** — show acoustic values, population, source, and evidence type when source-backed data exists

## Repository status

This folder currently lives in the Formant Canvas repository as a **staging implementation** on branch `design/articulation-lab-v0.1`. The branch name is historical; the staged app itself is now v0.4.1. It remains intentionally isolated from Formant Canvas `main` and should not be merged merely to ship this staging folder.
