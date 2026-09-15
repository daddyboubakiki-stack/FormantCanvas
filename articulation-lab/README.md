# Articulation Lab — design staging area

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

## v0.1 scope

- 2D midsagittal mouth view
- pointer/touch dragging of tongue body
- lip rounding control
- F0 control
- continuous voiced synthesis
- vowel presets: `/i æ ɑ ə u/`
- current F1/F2/F3 readout
- English/Japanese dataset architecture prepared, but only source-verified values may be populated
- responsive tablet/mobile layout

## Non-goals for v0.1

- 3D rendering
- microphone-based pronunciation scoring
- consonants
- nasal coupling
- full jaw/tongue-tip control
- claiming a unique inverse mapping from acoustics to anatomy

## Planned modes

- **PLAY** — free mouth instrument
- **COMPARE** — A/B and morph comparison, especially Japanese vs English vowels
- **LEARN** — move from a familiar Japanese vowel toward an English target zone
- **PHONETICS** — show acoustic values, population, source, and evidence type

## Handoff rule

A graphics/UI contributor should normally edit renderer/style/UI files, not scientific data or acoustic mappings. See `docs/META_AI_HANDOFF.md` and `docs/SCIENTIFIC_CONTRACT.md`.

## Repository status

This folder currently lives on the Formant Canvas repository only as a **design staging area** on branch `design/articulation-lab-v0.1`. The intended end state is a separate Articulation Lab repository, with shared data contracts between the two apps.