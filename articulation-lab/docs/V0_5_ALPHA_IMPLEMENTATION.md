# Articulation Lab v0.5-alpha — visual articulation foundation

## Goal

Move the app from a tongue-point toy toward a reusable visual model of the whole vocal tract while preserving the v0.4.3 split:

- Vowel Buttons = recorded human evidence
- Mouth Synth = continuous pedagogical synthesis
- articulation drawings = pedagogical targets, not measured anatomy of the recorded speaker

The first visual acceptance pair is English /æ/ versus /ɑ/.

## Implementation order

1. Separate articulation targets from recording metadata.
2. Make jaw opening an independent articulation parameter rather than deriving it unconditionally from tongue height.
3. Add `lipSpread` and `tongueRootRetraction` to shared state and constraints.
4. Upgrade the sagittal Simple renderer:
   - jaw rotation/translation
   - lower teeth/lip follow the jaw
   - tongue root responds independently
   - lip spread and rounding are separate
   - schematic cavity fill makes available air space visible
5. Add a frontal Simple renderer driven by the same state:
   - vertical opening
   - horizontal opening
   - rounding/protrusion cue
   - teeth/tongue visibility
6. Add Sagittal / Frontal / Both view switching without changing audio behavior.
7. Add synth sliders for jaw opening and lip spread so Mouth Synth can explore the new axes.
8. Validate /æ/ versus /ɑ/ visually before adding Anatomy/Cute skins.
9. Keep renderer contracts ready for future `Simple`, `Anatomy`, and `Cute` skins.

## Scientific / educational precedents

The visual architecture is intentionally inspired by established articulatory teaching/modeling approaches without copying their artwork or code.

- **Seeing Speech / STAR** documents a 2-D head rig based on midsagittal imaging. Its animation workflow gives the jaw both translation and rotation and controls the tongue with multiple regions/control points (including root, dorsum, front, blade and tip). This supports the v0.5 decision to stop treating the tongue as one point and the jaw as a value derived from tongue height.
  - https://seeingspeech.ac.uk/creating-the-animations/
  - https://seeingspeech.ac.uk/ipa-charts/
- **VocalTractLab** separates higher-level phonetic controls such as tongue height, tongue frontness and lip rounding while its full articulatory model uses a much richer parameter set and derives an acoustic area function from vocal-tract geometry. Articulation Lab uses the higher-level-control idea for education, but does not copy VTL's implementation or claim VTL-level physical accuracy.
  - https://www.vocaltractlab.de/

For the current alpha, the cavity shading is only a visual hint of available airway space. It is **not** a computed cross-sectional area function.

## Shared state axes (v0.5)

All normalized 0..1 unless noted:

- `tongueBodyFrontBack`: front → back
- `tongueBodyHeight`: high → low
- `tongueRootRetraction`: advanced/neutral → retracted
- `jawOpening`: closed → wide open
- `lipRounding`: unrounded → rounded/protruded
- `lipSpread`: neutral → laterally spread
- existing tongue-tip, velum, F0 and voicing parameters remain available for future consonant work

`lipAperture` remains a derived compatibility value, but it no longer controls the visual model by itself.

## Initial pedagogical targets

These are visual teaching targets, not measured anatomy.

### English /æ/ TRAP

- tongue body front-back: 0.20
- tongue body height: 0.82
- tongue root retraction: 0.20
- jaw opening: 0.78
- lip rounding: 0.02
- lip spread: 0.62

Expected appearance: low/front tongue, strongly open jaw, laterally spread mouth; the front oral cavity looks broad and shallow relative to /ɑ/.

### English /ɑ/ PALM

- tongue body front-back: 0.82
- tongue body height: 0.88
- tongue root retraction: 0.62
- jaw opening: 0.88
- lip rounding: 0.04
- lip spread: 0.15

Expected appearance: low/back tongue, slightly larger vertical jaw opening, less lateral spreading, and a more posterior tongue/root configuration. Tongue-root retraction may narrow/reshape parts of the pharyngeal airway, so the model must **not** equate “back vowel” with “uniformly larger pharyngeal space.”

## Renderer contract

A skin should eventually be able to expose:

```js
renderer.mount(target, intentCallback)
renderer.render(state)
renderer.setInteractive(enabled)
renderer.destroy()
```

The sagittal and frontal views must use the same articulation state. Switching skin must never change audio, preset data, or scientific metadata.

## v0.5-alpha acceptance criteria

- Selecting /æ/ and /ɑ/ produces visibly different jaw, tongue-root and lip-spread states.
- In frontal view /æ/ appears wider; /ɑ/ appears relatively taller/deeper.
- In sagittal view /ɑ/ has a more posterior tongue/root configuration than /æ/.
- Existing v0.4.3 real-vowel playback remains unchanged.
- Existing Mouth Synth still works, with new jaw and lip-spread controls.
- JavaScript syntax validation and standalone packaging pass.
- No merge to Formant Canvas `main`; this remains staging work.

## Acoustic boundary for new visual axes

The existing Mouth Synth already includes `jawOpening` in its pedagogical F1 estimate. The newly exposed `lipSpread` and `tongueRootRetraction` axes are currently primarily visual/model-state axes. The alpha deliberately does not invent strong acoustic coefficients for them without a better tract model. A later acoustics upgrade should prefer a geometry/area-function approach rather than pretending every articulatory parameter maps independently to one formant.

## Future-compatible hooks

Do not implement yet, but preserve room for:

- `tongueTipRaise` / tongue-tip constriction
- `constrictionLocation` and `constrictionDegree`
- velum opening / nasal coupling
- voicing and glottal-state visualization
- airflow overlays
- consonants
- Anatomy skin
- Cute skins (monkey, cat, etc.) that change the exterior shell only while keeping articulation geometry driven by the same state
