# MetaAI handoff contract

## Goal

You are improving the visual/UI layer of Articulation Lab without silently changing its scientific meaning.

Before editing, read:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/SCIENTIFIC_CONTRACT.md`
4. `contracts/articulation-state.schema.json`
5. `contracts/vowel-target.schema.json`
6. `data/source-registry.json`

## Areas you are encouraged to redesign

- visual style
- responsive layout
- button shape/placement
- animations and transitions
- SVG mouth illustration
- Simple / Anatomy / Cute skins
- visual affordances for draggable tongue/lips
- educational callouts and friendly microcopy
- accessibility improvements

## Areas you must not silently redefine

- meaning/direction of articulation-state variables
- acoustic target numbers
- provenance/evidence labels
- speaker population metadata
- empirical vs modeled status
- English/Japanese comparison semantics
- audio-engine scientific claims

If you believe one of these needs changing, propose the change explicitly rather than altering it as part of a visual cleanup.

## Renderer rule

A skin is a renderer of `ArticulationState`.

Changing from `Simple` to `Cute` must not change:

- articulation state
- selected vowel dataset
- audio target
- F1/F2/F3 target/estimate

The same state should merely be drawn differently.

## Desired skins

### Simple
Clear educational vector drawing. Strong landmarks, low visual clutter.

### Anatomy
More anatomically recognizable midsagittal view. Still readable on a classroom projector/tablet. Avoid pretending to model anatomical detail that the state model does not actually control.

### Cute
Friendly stylized mouth/tongue. May be expressive or character-like, but hard palate, tongue front/back, oral opening, and lip rounding must remain spatially interpretable.

## Interaction priority

The primary control is direct manipulation of the tongue, not a dashboard of sliders.

Priority order:

1. immediate tongue drag response
2. immediate sound response
3. clear physical constraints
4. readable target zones
5. polish/decorative animation

Do not improve appearance at the expense of latency or drag precision.

## Compare mode contract

COMPARE should make it easy to choose two vowel targets, especially Japanese vs English, then:

- hear A
- hear B
- morph A → B
- see both articulatory targets/zones
- see both F1/F2 targets in phonetics view
- read a simple directional cue

A morph between endpoints is a modeled pedagogical path unless measured articulatory trajectory data exists. Keep that label visible in phonetics/source details.

## Data editing rule

Do not invent or substitute F1/F2/F3 values for visual convenience.

If a required target is missing, either:

- leave the control disabled with a clear reason, or
- add a clearly labeled `pedagogical_model` record after explicit approval.

Never convert a placeholder/model value to `measured_group_mean` or `measured_trajectory` without source evidence.

## Third-party code

If integrating Pink Trombone or another engine:

- isolate it under an obvious backend/third-party boundary
- preserve required copyright/license notices
- document what was copied, adapted, or wrapped
- do not mix GPL code into the main implementation casually

## Definition of done for a visual pass

A visual/UI change is successful only if:

- drag still works on touch and pointer devices
- sound continues while dragging
- state values remain unchanged by skin switching
- English/Japanese data IDs remain unchanged
- source/evidence badges still refer to the same records
- no scientific values were replaced with guessed values
