# PROJECT_STATE.md — Formantasia

Snapshot date: 2026-09-16

This file records the current repository state so that a new human or AI collaborator can understand the project without relying on chat history.

## Product

**Formantasia（フォルマンタジア） — 声をえがくキャンバス · Draw Your Voice**

Public app: `https://formantasia.netlify.app/`

Purpose: an educational and experimental Web app for drawing F1/F2/F3 formant trajectories, listening to the resulting sound, exploring vowel presets, and inspecting the literature sources and modeling assumptions behind reference data.

The public build is currently described as a **Research Preview**.

## Repository shape

Current root files:
- `index.html` — main application; currently a large single-file implementation containing styling, UI, data, and behavior.
- `README.md` — public project description.
- `robots.txt`
- `sitemap.xml`
- `AGENTS.md` — standing development rules.
- `PROJECT_STATE.md` — this snapshot.
- `DECISIONS.md` — durable design/research decisions.

There is currently no root-level package manifest or multi-module application structure. Treat the monolithic `index.html` as a regression risk: inspect surrounding code before making local changes.

## Confirmed current UI / behavior

The current `index.html` contains:
- Casual, Learning, and Research UI modes.
- F1, F2, and F3 drawing/visualization controls.
- Voice/preset selection UI.
- Playback controls.
- WAV download support in the interface.
- Research tools and evidence display.
- Evidence categories visually distinguishing empirical, borrowed, and modeled information.
- Mobile-specific presentation rules.
- SEO/canonical metadata for the Formantasia public site.

## Research-data policy currently represented in the app

The app explicitly distinguishes confidence/provenance levels rather than presenting every preset as equally empirical.

Current research-note principles include:
- published numerical averages and public materials are preferred;
- non-public or researcher-provided raw audio should not be bundled casually;
- derived statistics may be used when clearly documented as derived;
- empirical, borrowed, and app-modeled information should remain visibly distinguishable;
- display-only straight lines for monophthongs are not to be misrepresented as measured time-series trajectories.

The current app text identifies Hillenbrand et al. (1995) public 10% trajectories as a future integration candidate rather than as already integrated trajectory data.

## Recent repository-level decisions / changes

Recent merged work includes:
- public-facing rebrand from FormantCanvas to Formantasia while preserving selected internal/legacy identifiers;
- mobile display fixes for mode-specific content;
- search-discovery / SEO improvements;
- canonical site declaration and sitemap support.

See `DECISIONS.md` for durable rationale rather than relying only on commit history.

## Known engineering risks

1. **Monolithic implementation** — unrelated concerns live close together in `index.html`, so broad edits can create regressions.
2. **Multiple UI modes** — a change that looks correct in one mode can hide or alter content in another.
3. **Research provenance** — changing a value without updating its source/evidence classification can make the UI scientifically misleading.
4. **Legacy identifiers** — public branding is Formantasia, but internal names or persisted keys may intentionally retain older naming.
5. **Visual / interaction acceptance** — some important correctness criteria are perceptual and require manual UI review, not only code inspection.

## Working method

For all new work:
1. Read `AGENTS.md` first.
2. Inspect the relevant code before proposing a patch.
3. Define acceptance criteria and protected behavior.
4. Prefer small, reviewable changes.
5. Update this file when the current implementation state materially changes.

## Near-term documentation TODO

- Add concrete manual regression checks as recurring behavior stabilizes.
- Add project-specific test commands if/when a test/build system is introduced.
- Keep this snapshot focused on what is actually merged into the repository; exploratory ideas should not be described as implemented features.
