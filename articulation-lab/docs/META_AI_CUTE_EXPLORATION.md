# MetaAI design exploration handoff

Branch: `design/metaai-cute-exploration`
Base checkpoint: Articulation Lab `v0.5-alpha.17`
Base commit: `496328777912832ed92918077a009c489db3a195`

This branch exists for **visual / interaction exploration only**. The goal is to let MetaAI experiment freely with the app's exterior without destabilizing the scientific and audio foundation.

## Product intent

Articulation Lab should feel like a strange, delightful educational instrument first and an articulatory-phonetics teaching tool second.

The current app has two coordinated views:

- sagittal / side view
- frontal / front view

Both are driven by one shared articulation state.

Long-term skin ideas include:

- Simple
- Anatomy
- Cute
- animal-like exteriors such as cat / monkey while preserving the same mouth-state semantics

Cute work should make the app more inviting without obscuring how the mouth is changing.

## Safe playground — feel free to change

MetaAI may freely explore:

- `articulation-lab/styles/base.css`
- frontal-face exterior artwork in `src/renderers/frontal-renderer.js`
- non-scientific decorative SVG paths
- eyes, eyebrows, cheeks, face outline, cute exterior skin ideas
- layout, spacing, panel styling, buttons, tabs and microcopy
- animations that do not alter articulation state semantics
- optional blink / idle animations
- transitions between visual states
- skin-selection UI prototypes
- color systems and accessibility improvements
- responsive/mobile polish

It is acceptable to produce bold alternate designs on this branch. Nothing here is automatically promoted back to the staging checkpoint.

## Protected core — do not reinterpret or silently change

Do **not** change the meaning, scale or scientific semantics of these articulation axes:

- `tongueBodyFrontBack`
- `tongueBodyHeight`
- `tongueRootRetraction`
- `jawOpening`
- `lipRounding`
- `lipSpread`

Do not silently alter:

- `data/articulation-targets.js`
- human recording URLs / provenance
- `assets/audio/real/**`
- real-voice preprocessing or build reports
- Vowel Buttons human-recording behavior
- Natural / Independent coordination semantics
- approximate-IPA acoustic estimator semantics
- the distinction between recorded audio evidence, articulatory teaching targets and Mouth Synth synthesis

If a design idea seems to require changing one of these, leave a note rather than changing it.

## Renderer contract

The exterior skin may change, but visual mouth behavior should still communicate the same state.

Examples:

- stronger `jawOpening` should look more open
- stronger `lipRounding` should look more rounded / protruded / narrow
- stronger `lipSpread` should look more laterally spread
- front/back and high/low tongue differences should remain legible in the sagittal teaching view

Cute skins may exaggerate these differences for clarity, but should not reverse them.

## Current frontal Simple-skin decisions from user review

The alpha.17 checkpoint intentionally has:

- neutral gray page background
- smooth, simple lips
- no visible gum layer in Simple skin
- teeth clipped inside the oral aperture
- upper and lower tooth widths kept fairly close, with upper slightly wider
- lower teeth favored for close spread vowels such as `/i/` and `/ɪ/`
- tongue favored for more open front vowels such as `/ɛ/` and `/æ/`
- round eyes
- short soft eyebrows
- simple line nose
- no character-selection tab in the baseline

These are not sacred aesthetics; they are the current stable baseline. Alternate face ideas should be implemented as skin/design experiments rather than overwriting scientific state semantics.

## Useful design experiments

Good things to try:

1. A true `Cute` renderer or skin that wraps the existing mouth state in a friendly character face.
2. Subtle idle blinking that respects `prefers-reduced-motion`.
3. A skin registry that lets Simple remain the stable teaching view while Cute can be playful.
4. Clearer visual distinction between educational controls and decorative controls.
5. Better mobile composition for Side / Front / Both.
6. Small delight moments when a vowel is played, without masking the mouth shape.

## Please avoid

- photorealistic uncanny-valley faces
- large white-eyed / realistic eyeball designs that steal attention from the mouth
- animation that moves the mouth independently of articulation state
- changing a vowel's teaching posture merely to make a character expression prettier
- presenting synthesized output as a natural human recording
- presenting the nearest-modeled IPA hint as automatic phonetic transcription
- copying restricted artwork from Seeing Speech, Dynamic Dialects or other references

## Reverse-import workflow

The intended workflow is:

1. MetaAI experiments on this branch.
2. Keep changes visually scoped where possible.
3. User reviews the result.
4. ChatGPT / the staging branch selectively reverse-imports useful pieces.
5. Scientific/audio/data changes require separate review before import.

This branch is a sandbox, not the source of truth.

## Scientific reference boundary

The project may learn from the interaction / teaching approaches of resources such as Seeing Speech, Sounds of Speech, Dynamic Dialects, Pink Trombone and VocalTractLab. Do not copy restricted artwork or code with incompatible licensing into the app.

Have fun with the exterior. Keep the articulation contract intact.
