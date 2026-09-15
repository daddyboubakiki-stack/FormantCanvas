# Articulation Lab — v0.4.2 staging build

Articulation Lab is a proposed sister app to Formant Canvas.

- **Formant Canvas:** manipulate acoustic space and hear the result.
- **Articulation Lab:** manipulate vocal-tract articulation and hear the result.

The app deliberately separates two play experiences.

1. **Vowel Buttons** — tap IPA buttons on a simplified vowel quadrilateral. The mouth moves toward a pedagogical posture while a short **human recording** plays.
2. **Mouth Synth** — turn on continuous synthesis and drag the tongue directly like an instrument.

This keeps “hear a real vowel example” and “freely play an articulatory model” from pretending to be the same scientific object.

## v0.4.2 implementation status

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

## v0.4.2 audio optimization

Listening on a real user device exposed three useful defects in the first real-voice bundle:

- Japanese buttons felt much shorter than the English buttons;
- Japanese `/i/` was effectively inaudible;
- English `/ɔ/` was noticeably quieter.

The user report was confirmed by inspecting the bundled WAVs. The old Japanese files could contain a long file window but only a very short audible token, and the old Japanese `/i/` and English `/ɔ/` were substantially below neighboring samples in active RMS level.

v0.4.2 therefore rebuilds the button audio with these rules:

1. **Japanese voiced-token detection** — find an actual voiced kana token rather than using a fixed midpoint crop.
2. **Small onset/offset margin** — retain a little real context around the detected nucleus.
3. **Pitch-preserving duration adjustment** — the unusually short Japanese source tokens are lengthened with chained `atempo`, capped at 4×. The current outputs contain about **0.39–0.41 s of audible vowel material**.
4. **Active-RMS comparison target** — all English reference buttons target roughly **−16.5 dBFS** active RMS; Japanese samples are brought into the same usable comparison window while respecting peak headroom.
5. **Safe gain recovery** — unusually quiet source recordings may receive up to +24 dB gain, but the independent peak-headroom bound remains the clipping guard.
6. **Fail-closed CI** — Japanese output duration must be 0.38–0.62 s, all button samples must fall between −19 and −14 dBFS active RMS, and suspiciously low peaks are rejected.

Current verified examples after processing:

- Japanese `/i/`: about 0.392 s, active RMS about −16.5 dBFS
- English `/ɔ/`: about 0.58 s, active RMS about −16.5 dBFS
- English `/ɪ/`: about 0.38 s, active RMS about −16.9 dBFS

The Japanese duration processing is intentionally disclosed: these remain recordings of a real speaker, but the button duration is **not the speaker’s untouched natural token duration**.

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

Therefore v0.4.2 intentionally separates:

- **recorded audio evidence** — human voice sample, with documented preprocessing
- **articulatory teaching target** — modeled tongue/lip posture
- **Mouth Synth acoustics** — continuous pedagogical synthesis model

The vowel quadrilateral is a phonetic teaching map, not literal measured tongue geometry. F1/F2 do not uniquely determine a tongue posture.

## Audio licensing policy

Only recordings with sufficiently explicit permission for redistribution are bundled. “Publicly downloadable” or “usable for research” is **not** treated as redistribution permission.

For that reason, corpora such as JVPD or other research datasets are not copied into the app unless their terms explicitly permit the intended redistribution. Male / female / child language-matched recording sets remain a future addition and should be added only when both recording rights and speaker metadata are explicit.

## Distribution build

`.github/workflows/articulation-v04-preview.yml` validates JavaScript syntax, the processed-audio report, and builds:

- `ArticulationLab_v0.4.2.html` — self-contained single-file preview with CSS, JavaScript, and vetted WAV samples embedded
- `ArticulationLab_v0.4.2_source.zip` — modular source bundle

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

This folder currently lives in the Formant Canvas repository as a **staging implementation** on branch `design/articulation-lab-v0.1`. The branch name is historical; the staged app itself is now v0.4.2. It remains intentionally isolated from Formant Canvas `main` and should not be merged merely to ship this staging folder.
