# MetaAI handoff contract

## Goal

You are improving the visual/UI layer of Articulation Lab without silently changing its scientific meaning or interaction semantics.

Before editing, read:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/SCIENTIFIC_CONTRACT.md`
4. `contracts/articulation-state.schema.json`
5. `contracts/vowel-target.schema.json`
6. `data/source-registry.json`

Then run the current staging build at `articulation-lab/index.html` and verify both current play modes before redesigning it.

## Current v0.3 interaction contract

Articulation Lab intentionally separates two experiences.

### 1. Vowel Buttons

Purpose: a quick, child-friendly and classroom-friendly vowel toy.

- the mouth is a result/visualization area, not the main input area
- the tongue handle is visually subdued and non-interactive
- IPA buttons live on a separate simplified vowel quadrilateral below the mouth
- buttons are translucent circular controls
- one tap moves the modeled tongue/lips and triggers about **0.5 seconds** of sound
- no separate VOICE ON step is required
- English / Japanese / Both filtering must remain available
- English and Japanese buttons must remain distinguishable by more than position alone

Do not move the IPA buttons back on top of the tongue unless the interaction design is explicitly reconsidered. The separate map exists to avoid visual overlap between the anatomical display and the selectable vowel inventory.

### 2. Mouth Synth

Purpose: free instrumental play.

- the vowel quadrilateral is hidden
- the tongue handle becomes clearly interactive
- VOICE ON/OFF controls continuous voicing
- dragging the tongue continuously updates the sound
- there should be no competing IPA-button layer over the mouth

A visual redesign must preserve the conceptual difference between **tap-to-trigger short vowel** and **continuous mouth instrument**.

## Current evidence status

The current vowel-map positions, tongue targets, and source-filter formant mapping use an internal `pedagogical_model`. They exist to make interaction testable and fun. They are **not** source-backed English/Japanese normative values and are **not** measured anatomy.

The simplified vowel quadrilateral is a teaching/phonetic map. Do not present its screen coordinates as literal tongue coordinates.

The next scientific-data milestone will port source-verified vowel targets from Formant Canvas into the versioned target schema while preserving population, context, source, units, and evidence type.

## Areas you are encouraged to redesign

- visual style
- responsive layout
- button shape and visual treatment
- animations and transitions
- SVG mouth illustration
- Simple / Anatomy / Cute skins
- appearance of the vowel quadrilateral
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
- the distinction between Vowel Buttons and Mouth Synth
- duration/trigger semantics of Vowel Buttons without explicit product approval

If you believe one of these needs changing, propose the change explicitly rather than altering it as part of a visual cleanup.

## Renderer rule

A mouth skin is a renderer of `ArticulationState`.

Changing from `Simple` to `Cute` must not change:

- articulation state
- selected vowel dataset
- audio target
- F1/F2/F3 target/estimate

The same state should merely be drawn differently.

The vowel quadrilateral is a **separate renderer/selector** (`src/renderers/vowel-map.js`). It may be restyled independently from the mouth skin, but it must keep the same preset IDs and state targets.

Conceptually:

```text
                    ┌── Simple mouth renderer
ArticulationState ──┼── Anatomy mouth renderer (future)
                    └── Cute mouth renderer (future)
          │
          └────────────> AcousticEngine

VowelMap selector ──> preset ID ──> ArticulationState
```

Do not make sound depend directly on SVG pixel coordinates outside the shared renderer → intent → state pathway.

## Desired mouth skins

### Simple
Clear educational vector drawing. Strong landmarks, low visual clutter.

### Anatomy
More anatomically recognizable midsagittal view. Still readable on a classroom projector/tablet. Avoid pretending to model anatomical detail that the state model does not actually control.

### Cute
Friendly stylized mouth/tongue. May be expressive or character-like, but hard palate, tongue front/back, oral opening, and lip rounding must remain spatially interpretable.

## Interaction priority

For Mouth Synth:

1. immediate tongue drag response
2. immediate sound response
3. clear physical constraints
4. polish/decorative animation

For Vowel Buttons:

1. easy-to-hit IPA buttons
2. immediate short sound trigger
3. obvious EN/JP distinction
4. visible tongue/lip response above
5. visual polish

Do not improve appearance at the expense of latency, touch target size, or drag precision.

## Compare mode contract

COMPARE should eventually make it easy to choose two vowel targets, especially Japanese vs English, then:

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

## Voice/audio rule

Current voice profiles (Child / Teen / Adult / Soft-airy) are rendering presets, not demographic acoustic datasets.

If integrating Pink Trombone or another synthesis engine:

- isolate it under an obvious backend/third-party boundary
- preserve required copyright/license notices
- document what was copied, adapted, or wrapped
- do not mix GPL code into the main implementation casually
- preserve the existing engine-facing interaction contract so UI code does not need to know the synthesis internals

## Safe workflow for a graphics pass

1. Run both Vowel Buttons and Mouth Synth before editing.
2. Make renderer/style/UI changes first.
3. Do not replace scientific/data files merely to match the artwork.
4. If new artwork needs an additional state variable, propose it explicitly rather than overloading an existing one.
5. Test the same vowel preset before and after the visual change; the underlying preset/state/sound should remain unchanged.
6. Test short 0.5 s button triggering and continuous synth separately.
7. Keep Pointer Events and touch interaction working on Android/tablet.
8. Verify English / 日本語 / Both filtering after any vowel-map redesign.

## Product tone

The app should feel like a **playable pronunciation toy / mouth instrument**, not a configuration dashboard.

A child or first-time learner should be able to tap a translucent IPA circle and immediately get a sound without understanding the settings first. A curious user should then be able to switch to Mouth Synth and physically explore the sound space by dragging the tongue.

Education is layered on after play: Vowel Buttons / Mouth Synth → COMPARE → LEARN → PHONETICS.

## Definition of done for a visual pass

A visual/UI change is successful only if:

- Vowel Buttons still trigger short sounds without VOICE ON
- Mouth Synth still supports continuous sound while dragging
- tongue drag still works on touch and pointer devices in Mouth Synth
- the vowel map does not obscure the mouth
- language filtering still works
- state values remain unchanged by skin switching
- English/Japanese data IDs remain unchanged
- source/evidence badges still refer to the same records
- no scientific values were replaced with guessed values
