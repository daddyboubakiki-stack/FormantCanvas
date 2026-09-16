# AGENTS.md — Formantasia development instructions

This file is the standing instruction manual for AI coding agents and human contributors working on Formantasia. Read it before changing code.

Also read:
- `PROJECT_STATE.md` for the current snapshot and known risks.
- `DECISIONS.md` for important design and research decisions and their rationale.
- `README.md` for the public product description.

## Priority rules

### P0 — Preserve the user's goal
Implement the intended user experience, not merely the literal wording of a requested technique.

If the requested implementation method is not the best way to achieve the goal, propose a safer, simpler, more maintainable, or higher-quality alternative before implementation. Do not silently replace the user's design intent.

### P1 — Inspect before editing
Before changing code, inspect the relevant implementation, data structures, dependencies, and existing behavior.

Determine:
- whether the request can be implemented as stated;
- whether it conflicts with existing behavior or research assumptions;
- whether a better implementation path exists;
- whether the change requires architectural work rather than a local patch.

If there is an important technical constraint, explain it before making the change whenever practical.

### P2 — Do not stop at “cannot”
When the direct request is difficult or unsafe for the current architecture, identify the blocking cause and consider, in order:
1. removing or correcting the cause;
2. an alternative implementation that preserves the same experience;
3. a clearly labeled approximation only when necessary.

State the recommended option and why.

### P3 — Keep changes small and testable
Break large requests into small implementation units. Prefer the dependency order:

**data / architecture → behavior / logic → UI → visual polish**

Do not bundle unrelated refactors into a feature or bug-fix patch.

### P4 — Protect working behavior
For each change, identify both:
- what is intentionally changing;
- what must remain unchanged.

Avoid regressions in unrelated modes, presets, drawing behavior, audio behavior, research displays, and mobile layout.

### P5 — Resolve high-impact ambiguity
Ask a focused question when different interpretations would materially change architecture, interaction, data meaning, or animation relationships.

If clarification is unnecessary, state the adopted interpretation briefly and proceed.

### P6 — Define and verify completion
Before implementation, translate the request into observable acceptance criteria.

After implementation, verify those criteria and relevant regression behavior. Visual or interaction-level user dissatisfaction counts as a failed acceptance criterion even if automated checks pass.

### P7 — Preserve project knowledge
Keep important durable knowledge in the repository instead of relying on chat history.

Update as appropriate:
- `AGENTS.md` — durable rules and invariants;
- `PROJECT_STATE.md` — current implementation state, known issues, and near-term work;
- `DECISIONS.md` — durable design/research decisions and rationale.

### P8 — Report after implementation
Summarize:
- what changed;
- what was verified;
- remaining uncertainty or known issues;
- the recommended next step, if any.

### P9 — Be a co-designer, not an instruction repeater
Proactively surface better UX, architecture, research handling, maintainability, or implementation ideas when they directly support the current goal.

The user owns product direction and experience. The agent owns careful technical reasoning and should not withhold a materially better approach merely because it was not explicitly requested.

---

## Formantasia-specific invariants

### Product identity
- Public product name: **Formantasia（フォルマンタジア）**.
- Tagline: **声をえがくキャンバス · Draw Your Voice**.
- The repository may still contain legacy/internal identifiers based on `FormantCanvas`. Do not rename internal identifiers or persisted keys casually; treat migration as a separate, explicit task.

### Research integrity
Formantasia is an educational and experimental phonetics application and the public build is a **Research Preview**.

Research data must retain provenance. Do not silently convert borrowed or modeled values into “empirical” values.

Current evidence categories are:
- **A / empirical** — directly transcribed published numerical averages or otherwise explicitly empirical values;
- **B / borrowed or combined model** — empirical anchors with interpolation or an explicitly combined model;
- **C / approximation** — values borrowed from another population/source or otherwise approximate.

The UI currently distinguishes evidence visually. Preserve that distinction unless a deliberate redesign is requested.

Do not add non-public/raw research audio or restricted datasets merely because a paper refers to them. Prefer published numerical values, public author/repository data, and clearly documented derived statistics.

When adding or replacing a research value:
1. record the source;
2. record whether the value is empirical, borrowed, modeled, or derived;
3. keep the user-visible provenance consistent with the actual implementation;
4. do not overstate measurement precision.

### Current architecture caution
The application is currently concentrated in a large root-level `index.html`. Because UI, data, audio, and behavior can be close together, make narrow changes and inspect surrounding code before editing.

Do not perform a broad component/framework migration as a side effect of an unrelated feature request. If modularization would materially reduce risk for a requested feature, propose it first as an architectural task.

### UI modes
The current application includes separate casual, learning, and research presentation modes. A change intended for one mode must be checked for accidental effects on the others.

### Public site
Canonical public URL: `https://formantasia.netlify.app/`.

---

## Standard workflow

### Before coding
1. Read the relevant request and identify the actual goal.
2. Read `PROJECT_STATE.md` and relevant entries in `DECISIONS.md`.
3. Inspect the relevant code and research data.
4. State or infer acceptance criteria.
5. Identify protected behavior that must not change.
6. If a better method exists, propose it before implementation.

### During coding
1. Make the smallest coherent change first.
2. Avoid unrelated cleanup.
3. Keep research provenance and UI labels synchronized with implementation.
4. Preserve existing behavior outside the intended scope.

### After coding
1. Verify the requested behavior.
2. Check nearby regression risks, especially the other UI modes and mobile presentation when relevant.
3. Update project documentation when the change alters durable knowledge.
4. Report changes, verification, remaining uncertainty, and next recommendation.
