window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  function $(sel) { return document.querySelector(sel); }
  const store = NS.createStateStore();
  const engine = NS.createFormantEngine();
  const renderer = NS.createSimpleRenderer();
  const presets = NS.VOWEL_PRESETS.presets;

  function nearestPreset(state) {
    let best = null;
    for (const [id, p] of Object.entries(presets)) {
      const a = p.articulation;
      const d = Math.hypot(
        (state.tongueBodyFrontBack - a.tongueBodyFrontBack) * 1.05,
        state.tongueBodyHeight - a.tongueBodyHeight,
        (state.lipRounding - a.lipRounding) * 0.55
      );
      if (!best || d < best.distance) best = { id, distance: d, preset: p };
    }
    return best;
  }

  function updateState(partial) {
    const clean = NS.ConstraintMapper.sanitize(partial);
    const next = NS.ConstraintMapper.derive({ ...store.getState(), ...clean });
    store.setState(next);
  }

  function activatePreset(id) {
    const preset = presets[id];
    if (!preset) return;
    updateState(preset.articulation);
  }

  function init() {
    renderer.mount($('#mouthMount'), updateState);

    const presetArea = $('#presetButtons');
    Object.entries(presets).forEach(([id, p]) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'vowel-btn';
      btn.dataset.preset = id;
      btn.innerHTML = `<span>${p.label}</span><small>${p.name}</small>`;
      btn.addEventListener('click', () => activatePreset(id));
      presetArea.appendChild(btn);
    });

    $('#voiceButton').addEventListener('click', () => {
      const state = store.getState();
      if (engine.isRunning()) {
        engine.stop();
        updateState({ voicing: false });
      } else {
        const ok = engine.start(state);
        if (ok) updateState({ voicing: true });
        else $('#status').textContent = 'Web Audio API is unavailable here; visual controls still work.';
      }
    });

    $('#lipRounding').addEventListener('input', ev => updateState({ lipRounding: Number(ev.target.value) }));
    $('#f0').addEventListener('input', ev => updateState({ f0Hz: Number(ev.target.value) }));

    store.subscribe(state => {
      renderer.render(state);
      engine.setArticulation(state);
      const est = engine.getAcousticEstimate(state);
      $('#f1Value').textContent = `${Math.round(est.f1Hz)} Hz`;
      $('#f2Value').textContent = `${Math.round(est.f2Hz)} Hz`;
      $('#f3Value').textContent = `${Math.round(est.f3Hz)} Hz`;
      $('#f0Value').textContent = `${Math.round(state.f0Hz)} Hz`;
      $('#lipRounding').value = state.lipRounding;
      $('#f0').value = state.f0Hz;
      $('#voiceButton').textContent = state.voicing ? 'VOICE OFF' : 'VOICE ON';
      $('#voiceButton').classList.toggle('active', state.voicing);
      const near = nearestPreset(state);
      $('#nearest').textContent = `closest ${near.preset.label}`;
      $('#status').textContent = state.voicing
        ? 'Voicing on — drag the tongue and listen to the vowel color change.'
        : 'Press VOICE ON, then drag the tongue.';
      document.querySelectorAll('.vowel-btn').forEach(btn => btn.classList.toggle('selected', btn.dataset.preset === near.id && near.distance < 0.13));
    });

    window.addEventListener('pagehide', () => engine.stop(), { once: true });
    activatePreset('schwa');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})(window.ArticulationLab);
