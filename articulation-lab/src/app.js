window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  function $(sel) { return document.querySelector(sel); }
  const store = NS.createStateStore({ f0Hz: NS.VOICE_PROFILES.child.defaultF0 });
  const engine = NS.createFormantEngine();
  const mouthRenderer = NS.createSimpleRenderer();
  const vowelMap = NS.createVowelMap();
  const langs = NS.VOWEL_PRESETS.languages;
  let playMode = 'buttons';
  let languageMode = 'both';
  let voiceProfileId = 'child';
  let morphFrame = null;

  function updateState(partial) {
    const clean = NS.ConstraintMapper.sanitize(partial);
    const next = NS.ConstraintMapper.derive({ ...store.getState(), ...clean });
    store.setState(next);
  }

  function animateTo(articulation, duration = 230) {
    if (morphFrame) cancelAnimationFrame(morphFrame);
    const from = store.getState();
    const target = NS.ConstraintMapper.derive({ ...from, ...NS.ConstraintMapper.sanitize(articulation) });
    const keys = ['tongueBodyFrontBack','tongueBodyHeight','lipRounding','jawOpening'];
    const start = performance.now();
    function tick(now) {
      const raw = Math.min(1, (now - start) / duration);
      const t = 1 - Math.pow(1 - raw, 3);
      const patch = {};
      keys.forEach(k => patch[k] = from[k] + (target[k] - from[k]) * t);
      updateState(patch);
      if (raw < 1) morphFrame = requestAnimationFrame(tick);
      else morphFrame = null;
    }
    morphFrame = requestAnimationFrame(tick);
  }

  function playPreset(langId, id, preset) {
    if (playMode !== 'buttons') return;
    const current = store.getState();
    const target = NS.ConstraintMapper.derive({ ...current, ...NS.ConstraintMapper.sanitize(preset.articulation) });
    vowelMap.setSelected(langId, id);
    vowelMap.pulse(langId, id);
    $('#selectedVowel').textContent = `${langs[langId].label} ${preset.label} · ${preset.name}`;
    animateTo(preset.articulation, 220);
    engine.setVoiceProfile(voiceProfileId);
    const ok = engine.playBurst(target, 500);
    if (!ok) $('#status').textContent = 'Web Audio API is unavailable here; the tongue animation still works.';
    else $('#status').textContent = `${langs[langId].label} ${preset.label} — short vowel burst.`;
  }

  function applyMode(mode) {
    playMode = mode === 'synth' ? 'synth' : 'buttons';
    if (playMode === 'buttons') {
      engine.stop();
      updateState({ voicing: false });
      mouthRenderer.setInteractive(false);
      $('#modeTitle').textContent = 'Vowel Buttons';
      $('#modeDescription').textContent = 'Tap an IPA button: the tongue moves and the vowel sounds for about 0.5 seconds.';
      $('#dragHint').textContent = 'The tongue will move when you tap a vowel button.';
      $('#status').textContent = 'Tap a vowel button to hear it.';
      if ($('#selectedVowel').textContent === 'Free articulation') $('#selectedVowel').textContent = 'Choose a vowel below';
    } else {
      engine.stop();
      updateState({ voicing: false });
      mouthRenderer.setInteractive(true);
      vowelMap.setSelected(null, null);
      $('#selectedVowel').textContent = 'Free articulation';
      $('#modeTitle').textContent = 'Mouth Synth';
      $('#modeDescription').textContent = 'Turn the voice on and drag the tongue continuously like an instrument.';
      $('#dragHint').textContent = 'VOICE ON → drag the purple tongue handle continuously.';
      $('#status').textContent = 'Press VOICE ON, then play the mouth.';
    }
    document.body.dataset.playMode = playMode;
    document.querySelectorAll('[data-play-mode]').forEach(b => b.classList.toggle('selected', b.dataset.playMode === playMode));
  }

  function initVoiceOptions() {
    const select = $('#voiceProfile');
    Object.values(NS.VOICE_PROFILES).forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = `${p.emoji} ${p.label}`;
      select.appendChild(opt);
    });
    select.value = voiceProfileId;
    select.addEventListener('change', () => {
      voiceProfileId = select.value;
      const p = NS.VOICE_PROFILES[voiceProfileId];
      engine.setVoiceProfile(voiceProfileId);
      updateState({ f0Hz: p.defaultF0 });
      $('#voiceHint').textContent = `${p.label}: ${p.defaultF0} Hz base · voice-rendering preset`;
    });
  }

  function initControls() {
    document.querySelectorAll('[data-play-mode]').forEach(btn => btn.addEventListener('click', () => applyMode(btn.dataset.playMode)));
    document.querySelectorAll('[data-language-mode]').forEach(btn => btn.addEventListener('click', () => {
      languageMode = btn.dataset.languageMode;
      vowelMap.setLanguageMode(languageMode);
      document.querySelectorAll('[data-language-mode]').forEach(b => b.classList.toggle('selected', b === btn));
    }));

    $('#voiceButton').addEventListener('click', () => {
      if (playMode !== 'synth') return;
      const state = store.getState();
      if (engine.isRunning()) {
        engine.stop();
        updateState({ voicing: false });
      } else {
        engine.setVoiceProfile(voiceProfileId);
        const ok = engine.start(state);
        if (ok) updateState({ voicing: true });
        else $('#status').textContent = 'Web Audio API is unavailable here; visual controls still work.';
      }
    });

    $('#lipRounding').addEventListener('input', ev => {
      if (playMode !== 'synth') return;
      updateState({ lipRounding: Number(ev.target.value) });
    });
    $('#f0').addEventListener('input', ev => updateState({ f0Hz: Number(ev.target.value) }));
  }

  function init() {
    mouthRenderer.mount($('#mouthMount'), partial => {
      if (playMode !== 'synth') return;
      updateState(partial);
      $('#selectedVowel').textContent = 'Free articulation';
    });
    vowelMap.mount($('#vowelMapMount'), playPreset);
    vowelMap.setLanguageMode(languageMode);
    initVoiceOptions();
    initControls();

    store.subscribe(state => {
      mouthRenderer.render(state);
      if (playMode === 'synth') engine.setArticulation(state);
      const est = engine.getAcousticEstimate(state);
      $('#f1Value').textContent = `${Math.round(est.f1Hz)} Hz`;
      $('#f2Value').textContent = `${Math.round(est.f2Hz)} Hz`;
      $('#f3Value').textContent = `${Math.round(est.f3Hz)} Hz`;
      $('#f0Value').textContent = `${Math.round(state.f0Hz)} Hz`;
      $('#lipRounding').value = state.lipRounding;
      $('#f0').value = state.f0Hz;
      $('#voiceButton').textContent = state.voicing ? 'VOICE OFF' : 'VOICE ON';
      $('#voiceButton').classList.toggle('active', state.voicing);
      if (playMode === 'synth') {
        $('#status').textContent = state.voicing
          ? `${NS.VOICE_PROFILES[voiceProfileId].label} voice on — drag the tongue continuously.`
          : 'Press VOICE ON, then play the mouth.';
      }
    });

    $('#voiceHint').textContent = `Child: ${NS.VOICE_PROFILES.child.defaultF0} Hz base · voice-rendering preset`;
    applyMode('buttons');
    window.addEventListener('pagehide', () => engine.stop(), { once: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})(window.ArticulationLab);
