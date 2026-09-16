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

## D-007 — Treat research values as protected data

**Status:** Accepted  
**Date:** 2026-09-16

### Decision
Existing research values and their evidence classifications are protected data. They must not be changed incidentally during UI work, refactoring, bug fixes, cleanup, optimization, or visual tuning.

Research values may be changed only in an explicit research-data task with identifiable source evidence or a documented derivation. Changes to existing values or evidence classes require a recorded before/after comparison and explicit user approval before merge.

### Rationale
Formantasia's educational and research credibility depends on numerical values remaining traceable to sources rather than being silently adjusted for implementation convenience or visual plausibility.

### Consequence
If an agent suspects a data error during unrelated work, it should report the suspected problem and evidence but leave the value unchanged. Research-data changes should be isolated from unrelated feature work whenever practical.

---

## D-008 — Use DEVELOPMENT_METHOD.md as the canonical AI co-development method

**Status:** Accepted  
**Date:** 2026-09-16

### Decision
Keep the cross-project AI development method in `DEVELOPMENT_METHOD.md`. `AGENTS.md` applies that method to Formantasia and adds project-specific invariants.

The priority order explicitly places protected artifacts—especially research values and evidence classifications—above ordinary implementation freedom.

### Rationale
A single canonical method reduces drift between chats and AI agents, while separating universal workflow rules from project-specific constraints. Promoting protected research data to the highest priority prevents well-intentioned implementation agents from silently changing evidence-backed values for convenience or visual fit.

### Consequence
New AI agents should read `DEVELOPMENT_METHOD.md` before `AGENTS.md`, then consult `PROJECT_STATE.md` and `DECISIONS.md`. Changes to the development method should be deliberate, documented, and motivated by real workflow experience rather than ad-hoc preference.

---

## D-009 — Treat visual and sensory craft as a standing design protocol

**Status:** Accepted  
**Date:** 2026-09-17

### Decision
Use `VISUAL_SENSORY_DESIGN.md` as the canonical cross-project visual/sensory craft protocol alongside `DEVELOPMENT_METHOD.md`.

For material UI, illustration, motion, density, art-direction, or sensory changes, agents should apply this protocol rather than treating visual polish as an implementation afterthought.

The default aesthetic direction is **cute, soothing, gentle, warm, approachable, slightly analog, and low-stimulation**, while preserving accessibility, clarity, and scientific/educational integrity.

Sound effects and custom web fonts are **opt-in**: agents may research or propose them, but must not add or replace them without explicit user request or approval.

### Rationale
Functional correctness alone does not guarantee a pleasant or coherent experience. AI-generated interfaces tend to fall back to generic card layouts, arbitrary rounded corners, default blue actions, excessive information density, or other implementation-convenient patterns unless aesthetic intent, references, hierarchy, sensory load, and review are explicitly designed.

The protocol turns visual quality from an assumed talent into a repeatable process: visual intent, reference study, concept variation, hierarchy, design tokens, accessibility review, visual QA, sensory QA, and user review.

### Consequence
New agents should read `VISUAL_SENSORY_DESIGN.md` for material visual/sensory work. User feedback such as “なんかダサい”, “固い”, “ごちゃごちゃする”, “目が疲れる”, or “耳が疲れる” is a valid QA signal to investigate rather than dismiss as purely subjective preference.

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
