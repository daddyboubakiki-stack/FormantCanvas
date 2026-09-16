# MVP roadmap

## Phase 0 — contracts first

Goal: freeze meanings before polishing visuals.

- articulation-state schema
- vowel-target schema
- source registry
- scientific contract
- renderer boundary
- audio-engine interface

Success: a second developer/model can read the repository and tell which files are science, which are UI, and which values are allowed to change.

## Phase 1 — playable mouth instrument (implemented in staging v0.1)

Build only what is needed to answer: **is this fun to touch?**

Implemented now:

- one Simple 2D midsagittal renderer
- draggable tongue body
- lip rounding
- F0
- VOICE ON/OFF
- continuous audio during drag
- `/i æ ɑ ə u/` demonstration presets
- F1/F2/F3 engine estimate readout
- mobile/tablet layout
- separated state / constraint / audio / renderer / controller modules

For this phase, presets use a clearly labeled internal `pedagogical_model`. They are not empirical anatomy or language norms.

## Phase 2 — verified acoustic data layer

Port/reconcile acoustic vowel targets from Formant Canvas into a shared versioned format.

Priority:

1. adult English group targets with recoverable numeric source/provenance
2. adult Japanese group/context targets with recoverable numeric source/provenance
3. sex/population switching where sources support it
4. optional F3 only where provenance is explicit

Add automated validation:

- every production acoustic target has a source ID
- every source ID resolves
- Hz values are finite/positive
- population is present
- evidence type is present
- model values cannot masquerade as measured data

## Phase 3 — COMPARE mode

First classroom-ready feature.

Recommended default comparisons:

- Japanese `/a/` ↔ English `/æ/`
- Japanese `/i/` ↔ English `/ɪ/` or `/i/` where dataset labels permit
- Japanese `/e/` ↔ English `/ɛ/`
- Japanese `/ɯ/` ↔ English `/u/` / `/ʊ/` where articulatory modeling is adequate

Features:

- A/B listen
- side-by-side or overlay target zones
- modeled morph
- small F1/F2 panel
- plain-language directional cue
- source/population details in PHONETICS mode

Do not ship a comparison until both displayed acoustic targets identify their data populations and evidence types.

## Phase 4 — LEARN mode

- choose English target
- show nearest/useful Japanese starting point
- show articulatory target zone
- free manipulation to enter zone
- feedback such as `closer`, not numeric pronunciation grades
- no microphone scoring yet

## Phase 5 — skins

Once state/audio are stable:

- Simple
- Cute
- Anatomy

Add a renderer conformance test: switching skin must leave serialized `ArticulationState`, selected data IDs, and acoustic target unchanged.

## Phase 6 — stronger tract synthesis

Evaluate Pink Trombone-compatible backend behind the existing `AcousticEngine` interface.

Requirements:

- isolate third-party code/license
- benchmark touch-to-audio latency
- map high-level state to tract targets reproducibly
- document that synthesizer posture is a model configuration, not human measurement

Pink Trombone-style implementations represent the tract as a diameter array and support continuous target-diameter updates, making them a plausible backend without coupling the UI to the synthesis internals.

## Phase 7 — articulatory evidence upgrade

Add source-backed articulatory targets from appropriate MRI/ultrasound/EMA literature or openly licensed datasets.

The first goal is not exact person-specific anatomy; it is to replace pedagogical postures with better-supported target zones while preserving uncertainty.

## Later, not MVP

- tongue tip/blade/root controls
- jaw as independent control
- velum/nasalization
- consonantal constrictions
- rhotic alternatives
- glottal/voice-quality controls
- user microphone analysis
- 3D
- measured articulatory trajectories
- deep link / shared package integration with Formant Canvas
