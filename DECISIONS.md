# DECISIONS.md — Formantasia

This is a lightweight decision log for durable product, architecture, and research decisions. Add an entry when future collaborators would otherwise ask, “Why is it built this way?”

---

## D-001 — Public product name is Formantasia

**Status:** Accepted  
**Date:** 2026-09-15

### Decision
Use **Formantasia（フォルマンタジア）** as the public-facing product name.

### Rationale
The project needs a distinctive, approachable name suited to an educational phonetics tool. The public app and README now use Formantasia.

### Consequence
Older/internal identifiers may still contain `FormantCanvas`. Do not perform broad internal renames merely for cosmetic consistency. Rename persisted keys or internal identifiers only as an explicit migration task with regression checks.

---

## D-002 — Treat the public build as a Research Preview

**Status:** Accepted

### Decision
The app may combine published empirical values with borrowed, derived, interpolated, or modeled values, but their provenance must remain explicit.

### Rationale
Formantasia is both an educational tool and an experimental synthesizer. Hiding differences in evidence quality would make the interface look more scientifically certain than the underlying data supports.

### Consequence
Research displays must preserve evidence labels/categories. New values must not be presented as empirical unless the underlying source supports that claim.

---

## D-003 — Prefer public/published research material and document derivation

**Status:** Accepted

### Decision
Prefer published numerical tables, open/public author materials, and clearly documented derived statistics. Do not bundle restricted or non-public raw research audio merely because it is referenced in a publication.

### Rationale
This keeps the project reproducible, shareable, and safer with respect to dataset permissions while preserving scientific traceability.

### Consequence
If a desirable dataset cannot be redistributed or its numerical values cannot be recovered reliably, keep it as a research lead rather than silently fabricating or substituting values.

---

## D-004 — Preserve the distinction between measured trajectories and display models

**Status:** Accepted

### Decision
A display-only horizontal line or interpolated curve must not be described as a measured time-series trajectory.

### Rationale
A visually plausible trajectory is not the same thing as observed longitudinal formant measurements.

### Consequence
UI copy, evidence markers, and documentation must remain synchronized with whether data are empirical, borrowed, modeled, or display-only.

---

## D-005 — AI collaborators use a co-designer workflow

**Status:** Accepted  
**Date:** 2026-09-16

### Decision
AI agents should not behave as literal instruction repeaters. Before implementation they inspect the current code, identify constraints, define acceptance criteria, protect working behavior, and proactively suggest materially better implementation approaches.

### Rationale
The product owner knows the intended experience, while the AI collaborator can contribute technical alternatives, architecture reasoning, UX suggestions, and implementation risk analysis. Combining those roles reduces expensive rework.

### Consequence
`AGENTS.md` is the standing execution guide. Important project knowledge must be stored in the repository rather than depending on one chat session.

---

## D-006 — Keep current changes narrow; modularization is a separate architectural decision

**Status:** Accepted  
**Date:** 2026-09-16

### Decision
While the application remains concentrated in `index.html`, ordinary feature and bug-fix work should use narrow patches. A broad split into modules/frameworks must be proposed and reviewed as its own architectural task.

### Rationale
Large incidental refactors make it difficult to distinguish intended product changes from regression-causing structural changes.

### Consequence
If a requested feature becomes unsafe or unnecessarily difficult because of the monolithic file, propose modularization with a concrete benefit and migration plan rather than quietly refactoring the whole application.

---

## Entry template

```md
## D-XXX — Short decision title

**Status:** Proposed | Accepted | Superseded  
**Date:** YYYY-MM-DD

### Decision
What was decided?

### Rationale
Why was this chosen?

### Consequence
What must future work preserve or account for?
```
