# Formantasia（フォルマンタジア）

**声をえがくキャンバス · Draw Your Voice**

**Live app:** https://formantasia.netlify.app/

Formantasia（フォルマンタジア）は、F1・F2・F3のフォルマント軌跡を描いて音を聴き、母音・フォルマント・音声学を学べる教育・実験用Webアプリです。

Formantasia is an educational and experimental formant-drawing synthesizer. Draw F1, F2, and F3 trajectories, listen to the resulting sound, explore vowel presets, and inspect the literature sources and modeling assumptions behind the built-in reference data.

The current public build is a **Research Preview**. Presets may combine published empirical values with clearly labeled borrowed or modeled intervals; see the in-app Research mode for provenance details.

## For AI coding agents and contributors

Before making code changes, read:

1. [`DEVELOPMENT_METHOD.md`](DEVELOPMENT_METHOD.md) — the shared AI co-development method and priority rules used across projects.
2. [`VISUAL_SENSORY_DESIGN.md`](VISUAL_SENSORY_DESIGN.md) — the shared visual/sensory craft protocol for art direction, hierarchy, spacing, low-stimulation design, motion, and opt-in sound/font decisions.
3. [`AGENTS.md`](AGENTS.md) — standing Formantasia-specific development rules and invariants.
4. [`PROJECT_STATE.md`](PROJECT_STATE.md) — current implementation snapshot, known risks, and handoff context.
5. [`DECISIONS.md`](DECISIONS.md) — durable design and research decisions and their rationale.

These files are the repository's shared project memory. Do not rely on chat history alone for durable implementation assumptions.

**Important:** research values, provenance, evidence classifications, and research-derived parameters are protected data. They must not be silently changed during unrelated implementation work; see `DEVELOPMENT_METHOD.md` and `AGENTS.md` for the required research-data workflow.

**Visual/sensory quality is also part of product quality:** substantial UI, illustration, motion, or sensory changes should follow `VISUAL_SENSORY_DESIGN.md`. Sound effects and custom web fonts are opt-in and must not be added merely as automatic polish without explicit user request or approval.

*Formantasia · Daddy's little phonetics lab 🧪*
