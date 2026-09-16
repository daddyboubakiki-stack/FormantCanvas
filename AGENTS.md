# AGENTS.md — Formantasia development instructions

This file is the standing **Formantasia-specific** instruction manual for AI coding agents and human contributors.

Before changing code or research data, read:

1. `GLOBAL_APP_PRINCIPLES.md` — the entrypoint for all current and future app projects.
2. `DEVELOPMENT_METHOD.md` — the shared AI co-development method and global priority rules.
3. `VISUAL_SENSORY_DESIGN.md` — the shared visual/sensory craft protocol for UI, art direction, motion, low-stimulation design, typography, and guarded-autonomy sound/font decisions.
4. `PROJECT_STATE.md` — the current snapshot and known risks.
5. `DECISIONS.md` — important design and research decisions and their rationale.
6. `README.md` — the public product description.

`GLOBAL_APP_PRINCIPLES.md`, `DEVELOPMENT_METHOD.md`, and `VISUAL_SENSORY_DESIGN.md` are cross-project rules. This file adds Formantasia-specific invariants and safety rules; it does not silently weaken the shared principles.

---

## Priority rules for Formantasia

### P0 — Protect research data and other protected artifacts

Research values, research-derived parameters, population mappings, duration values, evidence classifications, provenance labels, and source attributions are **protected data**, not ordinary implementation details.

Do **not** alter them as a side effect of UI work, refactoring, bug fixing, cleanup, optimization, visual tuning, or unrelated feature work.

If you suspect a research-data error while working on another task:

1. do not silently correct it;
2. report the suspected issue and evidence;
3. leave the current value unchanged;
4. treat any correction as a separate, explicit research-data task.

A research value may be added, replaced, or corrected only when the current task explicitly concerns research data and the change is supported by an identifiable source or documented derivation.

For any permitted change to existing research values or evidence classification:

1. record the exact source;
2. record old value → new value;
3. state whether the value is empirical, borrowed, modeled, or derived;
4. keep user-visible provenance synchronized with implementation;
5. do not overstate measurement precision;
6. isolate the research-data change from unrelated feature work whenever practical;
7. obtain **explicit user approval before merge**.

### P1 — Preserve the user's actual goal

Implement the intended experience, not merely the literal wording of a requested technique.

If the requested implementation method is not the best way to achieve the goal, proactively propose a safer, simpler, more maintainable, or higher-quality alternative before implementation. Do not silently replace the user's design intent.

### P1-V — Treat visual and sensory craft as product quality, not decoration

When a task materially changes UI, illustration, layout, motion, density, visual hierarchy, typography, sound, or sensory presentation, read and apply `VISUAL_SENSORY_DESIGN.md` before polishing the implementation.

The default Formantasia art direction favors **cute, soothing, gentle, warm, approachable, slightly analog, low-stimulation** presentation while preserving scientific clarity and accessibility.

Do not equate "simple" with "unrefined". Use intentional hierarchy, spacing, typography, shape language, and restraint. Important screens should be evaluated separately for functional correctness and aesthetic/sensory quality.

User feedback such as "なんかダサい", "固い", "ごちゃごちゃする", "目が疲れる", or "耳が疲れる" is a legitimate QA signal and should be decomposed into concrete visual/sensory causes rather than dismissed as subjective noise.

**Custom fonts and lightweight SE use guarded autonomy.** They may be added without a separate request when they materially improve the experience and satisfy `VISUAL_SENSORY_DESIGN.md` requirements for licensing, reasonable loading cost, device/browser compatibility, robust fallback, accessibility, and low sensory burden. If those risks are substantial or uncertain, propose the change first. Never make sound essential to understanding, and never let a missing custom font break readability or core interaction.

### P2 — Inspect before editing

Before making changes, inspect the relevant implementation, data structures, dependencies, protected data, and existing behavior.

Determine:

- whether the request can be implemented as stated;
- whether it conflicts with working behavior or research assumptions;
- whether a better implementation path exists;
- whether the change requires architectural work rather than a local patch.

Surface important constraints early.

### P3 — Keep changes small and protect working behavior

Break large requests into small, testable units. Prefer the dependency order:

**data / architecture → behavior / logic → UI → visual polish**

For each change, identify both what is intentionally changing and what must remain unchanged. Do not bundle unrelated refactors into feature or bug-fix work.

### P4 — Resolve high-impact ambiguity and define completion

Ask a focused question when different interpretations would materially change architecture, interaction, data meaning, protected data, or animation relationships.

Otherwise, state the adopted interpretation briefly and proceed.

Translate the request into observable acceptance criteria before implementation. After implementation, verify those criteria and nearby regression risks. User-visible or interaction-level dissatisfaction counts as a failed acceptance criterion even if automated checks pass.

### P5 — Preserve project knowledge

Keep durable knowledge in the repository rather than relying on chat history.

Update as appropriate:

- `GLOBAL_APP_PRINCIPLES.md` — scope and portability of rules across all app projects;
- `DEVELOPMENT_METHOD.md` — cross-project AI co-development principles;
- `VISUAL_SENSORY_DESIGN.md` — cross-project visual/sensory craft principles;
- `AGENTS.md` — Formantasia-specific rules and invariants;
- `PROJECT_STATE.md` — current implementation state and known issues;
- `DECISIONS.md` — durable design/research decisions and rationale.

After implementation, report what changed, what was verified, remaining uncertainty, and the recommended next step.

---

## Formantasia-specific invariants

### Product identity

- Public product name: **Formantasia（フォルマンタジア）**.
- Tagline: **声をえがくキャンバス · Draw Your Voice**.
- The repository may still contain legacy/internal identifiers based on `FormantCanvas`.
- Do not rename internal identifiers or persisted keys casually; treat migration as a separate, explicit task.

### Research integrity

Formantasia is an educational and experimental phonetics application and the public build is a **Research Preview**.

Research data must retain provenance. Do not silently convert borrowed or modeled values into empirical values.

Current evidence categories are:

- **A / empirical** — directly transcribed published numerical averages or otherwise explicitly empirical values;
- **B / borrowed or combined model** — empirical anchors with interpolation or an explicitly combined model;
- **C / approximation** — values borrowed from another population/source or otherwise approximate.

The UI currently distinguishes evidence visually. Preserve that distinction unless a deliberate redesign is requested.

Do not add non-public/raw research audio or restricted datasets merely because a paper refers to them. Prefer published numerical values, public author/repository data, and clearly documented derived statistics.

### Current architecture caution

The application is currently concentrated in a large root-level `index.html`. UI, data, audio, and behavior can therefore be close together.

Make narrow changes and inspect surrounding code before editing.

Do not perform a broad component/framework migration as a side effect of an unrelated feature request. If modularization would materially reduce risk for a requested feature, propose it first as an architectural task.

### UI modes

The current application includes separate casual, learning, and research presentation modes. A change intended for one mode must be checked for accidental effects on the others.

### Public site

Canonical public URL: `https://formantasia.netlify.app/`.

---

## Standard workflow

### Before coding

1. Identify the actual user goal.
2. Read `GLOBAL_APP_PRINCIPLES.md`, `DEVELOPMENT_METHOD.md`, `PROJECT_STATE.md`, and relevant `DECISIONS.md` entries.
3. For material UI / illustration / motion / sensory changes, read `VISUAL_SENSORY_DESIGN.md` and define the intended visual/sensory direction before polishing.
4. Classify what is editable and what is protected.
5. Inspect relevant code, data, dependencies, and current behavior.
6. Define acceptance criteria and protected behavior.
7. Propose a better method before implementation if one materially improves the result.
8. If research values would be modified, stop and confirm that this is explicitly a research-data task and that source evidence is available.

### During coding

1. Make the smallest coherent change first.
2. Avoid unrelated cleanup.
3. Do not modify protected research values during unrelated work.
4. Keep research provenance and UI labels synchronized with implementation.
5. Preserve existing behavior outside the intended scope.
6. If adding a custom font or SE autonomously, keep it lightweight, licensed, accessible, nonessential to core understanding, and safe under fallback/failure conditions.

### After coding

1. Verify the requested behavior against acceptance criteria.
2. Check nearby regression risks, especially other UI modes and mobile presentation when relevant.
3. For material visual changes, perform a separate visual/sensory QA pass according to `VISUAL_SENSORY_DESIGN.md` rather than treating functional success as aesthetic completion.
4. If custom fonts or SE were added, verify loading cost, fallback/non-audio behavior, device/browser compatibility, and readability/sensory comfort.
5. Update repository memory when durable knowledge changed.
6. For research-data changes, show the source and before/after values and obtain explicit user approval before merge.
7. Report changes, verification, remaining uncertainty, and the next recommendation.
