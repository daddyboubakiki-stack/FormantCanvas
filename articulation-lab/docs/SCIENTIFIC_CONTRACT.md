# Scientific contract

This file defines claims the app is allowed to make.

## 1. Acoustics and articulation are not one-to-one

The app must not tell users that one F1/F2 pair uniquely determines one tongue shape. Acoustic-to-articulatory inversion is underdetermined: multiple vocal-tract configurations may yield similar acoustic outputs.

UI wording should prefer:

- `one possible articulation`
- `target zone`
- `common configuration`
- `candidate posture`

Avoid:

- `the tongue position for this sound`
- `the only correct shape`

## 2. Data types must remain explicit

Every acoustic or articulatory target must carry an evidence type.

Recommended acoustic values:

- `measured_token`
- `measured_single_speaker_mean`
- `measured_group_mean`
- `measured_trajectory`
- `model_prediction`
- `pedagogical_model`

Recommended articulatory values:

- `mri_based`
- `ultrasound_based`
- `ema_based`
- `published_articulatory_description`
- `synthesizer_configuration`
- `pedagogical_model`

A renderer must never change evidence labels.

## 3. Population is part of the datum

Do not store a vowel simply as `/i/ = F1 X, F2 Y`.

A target must identify, when known:

- language
- dialect/region
- age group
- sex/gender grouping as reported by the source
- speaking context
- word/prosodic condition
- measurement method
- normalization

Do not silently mix child and adult values or incompatible speaker groups.

## 4. Language comparison is comparative, not normative

English/Japanese comparisons should say what the selected datasets show. Do not claim that every English or Japanese speaker uses exactly the displayed target.

Prefer ranges/zones or multiple datasets when evidence supports them.

## 5. Modeled motion must be labeled

Animating Japanese `/a/` into English `/æ/` is useful pedagogically, but interpolation between two endpoint configurations is not automatically a measured human articulatory trajectory.

Label such animations as `modeled morph` unless the path itself comes from measured articulatory time-series data.

## 6. Source hierarchy

Preferred order for production presets:

1. recoverable numeric values from original study/data release
2. author/institutional repository with documented provenance
3. numeric tables in publication
4. published model predictions with reproducible parameters
5. pedagogical model clearly labeled as such

Do not digitize a figure and relabel the points as original measured source data.

## 7. Existing Formant Canvas evidence rules to preserve

The Japanese VV evidence audit already enforces useful principles:

- an empirical trajectory requires a reusable numeric series
- figure digitization is not source measurement data
- incompatible age/population groups must not be mixed without explicit labeling

Articulation Lab should follow the same standard.

## 8. Audio engine claims

If v0.1 uses a formant-filter synthesizer, label F1/F2/F3 as the engine's target/estimate, not a direct measurement of a real vocal tract.

If a tract model such as Pink Trombone is later integrated, preserve the distinction between:

- tract-control parameters
- synthesized acoustic result
- published human acoustic targets

Matching a published F1/F2 target does not prove anatomical equivalence.

## 9. Educational wording

The app is allowed to give directional coaching such as:

- `try moving the tongue a little forward`
- `try lowering the tongue body`
- `increase lip rounding`

provided the cue is derived from the selected ArticulatoryTarget/model and is not presented as universal anatomy.

## 10. Uncertainty is a feature

Where multiple articulations are documented (for example, rhotic variants), the app should eventually show alternatives rather than collapsing them into one fake canonical posture.