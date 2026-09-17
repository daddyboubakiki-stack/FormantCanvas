# Formantasia（フォルマンタジア）

**声をえがくキャンバス · Draw Your Voice**

**Live app:** https://formantasia.netlify.app/

Formantasia（フォルマンタジア）は、F1・F2・F3のフォルマント軌跡を描いて音を聴き、母音・フォルマント・音声学を学べる教育・実験用Webアプリです。

Formantasia is an educational and experimental formant-drawing synthesizer. Draw F1, F2, and F3 trajectories, listen to the resulting sound, explore vowel presets, and inspect the literature sources and modeling assumptions behind the built-in reference data.

The current public build is a **Research Preview**. Presets may combine published empirical values with clearly labeled borrowed or modeled intervals; see the in-app Research mode for provenance details.

## For AI coding agents and contributors

Before making code changes, read:

1. [`GLOBAL_APP_PRINCIPLES.md`](GLOBAL_APP_PRINCIPLES.md) — the entrypoint declaring which rules apply across all current and future app projects.
2. [`DEVELOPMENT_METHOD.md`](DEVELOPMENT_METHOD.md) — the shared AI co-development method and priority rules used across projects.
3. [`APP_KICKOFF.md`](APP_KICKOFF.md) — the shared kickoff routine for aligning target users, age, purpose, context, experience direction, priorities, and assumptions before implementation.
4. [`VISUAL_SENSORY_DESIGN.md`](VISUAL_SENSORY_DESIGN.md) — the shared visual/sensory craft protocol for art direction, hierarchy, spacing, low-stimulation design, motion, typography, and guarded-autonomy sound/font decisions.
5. [`GAMIFICATION_DESIGN.md`](GAMIFICATION_DESIGN.md) — the shared adaptive gamification protocol: use game elements only when they support the purpose, and vary their intensity by age, context, and tool type.
6. [`AGENTS.md`](AGENTS.md) — standing Formantasia-specific development rules and invariants.
7. [`PROJECT_STATE.md`](PROJECT_STATE.md) — current implementation snapshot, known risks, and handoff context.
8. [`DECISIONS.md`](DECISIONS.md) — durable design and research decisions and their rationale.

The first five documents are **cross-project principles**, not Formantasia-only rules. New app projects should carry them forward and add their own project-specific `AGENTS.md`, `PROJECT_STATE.md`, and `DECISIONS.md` as appropriate.

For a new app or a major new product direction, use `APP_KICKOFF.md` before substantial implementation. Start with the short selectable Mini Kickoff, let the AI prefill anything already known from the conversation, and ask only the unresolved questions that materially affect design. The resulting Project Brief is a living shared understanding, not a permanent contract.

These files are the repository's shared project memory. Do not rely on chat history alone for durable implementation assumptions.

**Important:** research values, provenance, evidence classifications, and research-derived parameters are protected data. They must not be silently changed during unrelated implementation work; see `DEVELOPMENT_METHOD.md` and `AGENTS.md` for the required research-data workflow.

**Visual/sensory quality is also part of product quality:** substantial UI, illustration, motion, or sensory changes should follow `VISUAL_SENSORY_DESIGN.md`. Lightweight custom fonts and SE may be added autonomously only when the protocol's licensing, performance, compatibility, fallback, accessibility, and sensory-load checks are satisfied; otherwise propose them first.

**Gamification is adaptive, not mandatory:** when points, badges, collections, progress systems, streaks, rankings, challenges, or other game elements are considered, apply `GAMIFICATION_DESIGN.md`. Child/novice learning experiences may benefit from playful exploration and gentle achievement, while adult research/professional tools should usually keep gamification subtle or omit it unless it clearly helps the task.

*Formantasia · Daddy's little phonetics lab 🧪*
