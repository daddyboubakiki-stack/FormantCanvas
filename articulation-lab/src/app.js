window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  function $(sel) { return document.querySelector(sel); }
  const store = NS.createStateStore({ f0Hz: NS.VOICE_PROFILES.child.defaultF0 });
  const engine = NS.createFormantEngine();
  const approxIpa = NS.createApproxIpaEstimator(engine);
  const samplePlayer = NS.createSamplePlayer();
  const mouthRenderer = NS.createSimpleRenderer();
  const frontalRenderer = NS.createFrontalRenderer();
  const vowelMap = NS.createVowelMap();
  const langs = NS.VOWEL_PRESETS.languages;
  let playMode = 'buttons';
  let languageMode = 'both';
  let viewMode = 'both';
  let coordinationMode = 'natural';
  let voiceProfileId = 'child';
  let skinMode = 'simple';
  let morphFrame = null;

  function articulationForPreset(preset) {
    const id = preset && preset.articulationTargetId;
    return (id && NS.ARTICULATION_TARGETS && NS.ARTICULATION_TARGETS.targets[id]) || preset.articulation || {};
  }

  function updateState(partial) {
    const clean = NS.ConstraintMapper.sanitize(partial);
    const next = NS.ConstraintMapper.derive({ ...store.getState(), ...clean });
    store.setState(next);
  }

  function allRealAudioUrls() {
    const urls = [];
    Object.values(langs).forEach(lang => {
      Object.values(lang.vowels).forEach(vowel => {
        if (vowel.realAudio) urls.push(vowel.realAudio);
      });
    });
    return urls;
  }

  function animateTo(articulation, duration = 230) {
    if (morphFrame) cancelAnimationFrame(morphFrame);
    const from = store.getState();
    const target = NS.ConstraintMapper.derive({ ...from, ...NS.ConstraintMapper.sanitize(articulation) });
    const keys = [
      'tongueBodyFrontBack','tongueBodyHeight','tongueRootRetraction',
      'lipRounding','lipSpread','jawOpening'
    ];
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

  async function playPreset(langId, id, preset) {
    if (playMode !== 'buttons') return;
    const articulation = articulationForPreset(preset);
    const current = store.getState();
    const target = NS.ConstraintMapper.derive({ ...current, ...NS.ConstraintMapper.sanitize(articulation) });
    const lang = langs[langId];
    vowelMap.setSelected(langId, id);
    vowelMap.pulse(langId, id);
    $('#selectedVowel').textContent = `${lang.label} ${preset.label} · ${preset.name}`;
    animateTo(articulation, 240);
    engine.stop();

    if (preset.realAudio) {
      const ok = await samplePlayer.play(preset.realAudio, { gain: 0.92, attackSeconds: 0.014, releaseSeconds: 0.035 });
      if (playMode !== 'buttons') return;
      if (ok) {
        const audioSet = lang.audioSet;
        $('#recordingHint').textContent = `${audioSet.label} · ${audioSet.license}`;
        $('#status').textContent = `${lang.label} ${preset.label} — human recording · visual posture = pedagogical model.`;
        return;
      }
    }

    engine.setVoiceProfile(voiceProfileId);
    const ok = engine.playBurst(target, 500);
    if (!ok) $('#status').textContent = 'Audio playback is unavailable here; the articulation animation still works.';
    else $('#status').textContent = `${lang.label} ${preset.label} — synth fallback (recording unavailable).`;
  }

  function applyView(mode) {
    viewMode = ['sagittal','frontal','both'].includes(mode) ? mode : 'both';
    document.body.dataset.viewMode = viewMode;
    document.querySelectorAll('[data-view-mode]').forEach(b => b.classList.toggle('selected', b.dataset.viewMode === viewMode));
  }

  function applySkin(mode) {
    skinMode = mode === 'cute' ? 'cute' : 'simple';
    document.body.dataset.skin = skinMode;
    frontalRenderer.setSkin(skinMode);
    document.querySelectorAll('[data-skin-mode]').forEach(button => {
      const selected = button.dataset.skinMode === skinMode;
      button.classList.toggle('selected', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
    const description = $('#skinDescription');
    if (description) {
      description.textContent = skinMode === 'cute'
        ? 'Mogu the monkey · same shared articulation state'
        : 'Simple skin · shared articulation state';
    }
    try { localStorage.setItem('articulationLabSkin', skinMode); } catch (_) {}
  }

  function coordinationHint() {
    if (coordinationMode === 'natural') {
      return 'Natural: dragging the tongue also follows a smooth pedagogical jaw/lip/root coordination field built from the vowel targets. You can still tweak sliders; the next tongue drag re-couples them.';
    }
    return 'Independent: tongue, jaw, lip spread and lip rounding can be manipulated separately, including deliberately unusual combinations.';
  }

  function applyCoordination(mode, recouple = true) {
    coordinationMode = mode === 'independent' ? 'independent' : 'natural';
    document.body.dataset.coordinationMode = coordinationMode;
    document.querySelectorAll('[data-coordination-mode]').forEach(b => b.classList.toggle('selected', b.dataset.coordinationMode === coordinationMode));
    const hint = $('#coordinationHint');
    if (hint) hint.textContent = coordinationHint();
    if (playMode === 'synth' && coordinationMode === 'natural' && recouple && NS.NaturalCoordination) {
      const current = store.getState();
      updateState(NS.NaturalCoordination.fromTongue({}, current));
    }
  }

  function applyMode(mode) {
    playMode = mode === 'synth' ? 'synth' : 'buttons';
    samplePlayer.stop();
    engine.stop();
    updateState({ voicing: false });
    if (playMode === 'buttons') {
      mouthRenderer.setInteractive(false);
      frontalRenderer.setInteractive(false);
      $('#modeTitle').textContent = 'Vowel Buttons';
      $('#modeDescription').textContent = 'Tap an IPA button: hear a human recording while sagittal and frontal teaching models move together.';
      $('#dragHint').textContent = 'Both views share one articulation state; the drawing is a teaching model, while the button sound is a human recording.';
      $('#status').textContent = 'Tap a vowel button to hear a human recording.';
      if ($('#selectedVowel').textContent === 'Free articulation') $('#selectedVowel').textContent = 'Choose a vowel below';
    } else {
      mouthRenderer.setInteractive(true);
      frontalRenderer.setInteractive(false);
      vowelMap.setSelected(null, null);
      $('#selectedVowel').textContent = 'Free articulation';
      $('#modeTitle').textContent = 'Mouth Synth';
      $('#modeDescription').textContent = 'Turn the synthetic voice on and manipulate tongue, jaw and lips like an instrument.';
      $('#dragHint').textContent = coordinationMode === 'natural'
        ? 'VOICE ON → drag the tongue; jaw, lip spread, rounding and tongue root follow the pedagogical coordination field.'
        : 'VOICE ON → drag the tongue; jaw and lips stay independent until you move their controls.';
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
      $('#voiceHint').textContent = `${p.label}: ${p.defaultF0} Hz base · synth rendering preset`;
    });
  }

  function initControls() {
    document.querySelectorAll('[data-skin-mode]').forEach(btn => btn.addEventListener('click', () => applySkin(btn.dataset.skinMode)));
    document.querySelectorAll('[data-play-mode]').forEach(btn => btn.addEventListener('click', () => applyMode(btn.dataset.playMode)));
    document.querySelectorAll('[data-view-mode]').forEach(btn => btn.addEventListener('click', () => applyView(btn.dataset.viewMode)));
    document.querySelectorAll('[data-coordination-mode]').forEach(btn => btn.addEventListener('click', () => {
      applyCoordination(btn.dataset.coordinationMode, true);
      if (playMode === 'synth') {
        $('#dragHint').textContent = coordinationMode === 'natural'
          ? 'VOICE ON → drag the tongue; jaw, lip spread, rounding and tongue root follow the pedagogical coordination field.'
          : 'VOICE ON → drag the tongue; jaw and lips stay independent until you move their controls.';
      }
    }));
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
    $('#lipSpread').addEventListener('input', ev => {
      if (playMode !== 'synth') return;
      updateState({ lipSpread: Number(ev.target.value) });
    });
    $('#jawOpening').addEventListener('input', ev => {
      if (playMode !== 'synth') return;
      updateState({ jawOpening: Number(ev.target.value) });
    });
    $('#f0').addEventListener('input', ev => {
      if (playMode !== 'synth') return;
      updateState({ f0Hz: Number(ev.target.value) });
    });
  }

  function init() {
    mouthRenderer.mount($('#mouthMount'), partial => {
      if (playMode !== 'synth') return;
      const intended = coordinationMode === 'natural' && NS.NaturalCoordination
        ? NS.NaturalCoordination.fromTongue(partial, store.getState())
        : partial;
      updateState(intended);
      $('#selectedVowel').textContent = 'Free articulation';
    });
    frontalRenderer.mount($('#frontalMount'));
    vowelMap.mount($('#vowelMapMount'), playPreset);
    vowelMap.setLanguageMode(languageMode);
    initVoiceOptions();
    initControls();

    store.subscribe(state => {
      mouthRenderer.render(state);
      frontalRenderer.render(state);
      if (playMode === 'synth') engine.setArticulation(state);
      const est = engine.getAcousticEstimate(state);
      $('#f1Value').textContent = `${Math.round(est.f1Hz)} Hz`;
      $('#f2Value').textContent = `${Math.round(est.f2Hz)} Hz`;
      $('#f3Value').textContent = `${Math.round(est.f3Hz)} Hz`;
      $('#f0Value').textContent = `${Math.round(state.f0Hz)} Hz`;
      $('#lipRounding').value = state.lipRounding;
      $('#lipSpread').value = state.lipSpread;
      $('#jawOpening').value = state.jawOpening;
      $('#f0').value = state.f0Hz;
      $('#voiceButton').textContent = state.voicing ? 'VOICE OFF' : 'VOICE ON';
      $('#voiceButton').classList.toggle('active', state.voicing);

      const approxEl = $('#approxIpaValue');
      const approxNote = $('#approxIpaNote');
      if (state.voicing) {
        const nearest = approxIpa.nearest(state);
        approxEl.textContent = nearest ? `≈ [${nearest.symbol}]` : '≈ —';
        approxEl.classList.add('sounding');
        approxNote.textContent = 'Nearest IPA anchor in the current synth F1/F2/F3 model.';
      } else {
        approxEl.textContent = '—';
        approxEl.classList.remove('sounding');
        approxNote.textContent = 'VOICE ON to show the nearest modeled IPA vowel.';
      }

      if (playMode === 'synth') {
        $('#status').textContent = state.voicing
          ? `${NS.VOICE_PROFILES[voiceProfileId].label} synth voice on — ${coordinationMode === 'natural' ? 'Natural coordination' : 'Independent articulation'}.`
          : 'Press VOICE ON, then play the mouth.';
      }
    });

    $('#voiceHint').textContent = `Child: ${NS.VOICE_PROFILES.child.defaultF0} Hz base · synth rendering preset`;
    $('#recordingHint').textContent = 'Japanese: language-specific PD recording · English buttons: redistribution-safe human references';
    samplePlayer.preload(allRealAudioUrls());
    let savedSkin = 'simple';
    try { savedSkin = localStorage.getItem('articulationLabSkin') || 'simple'; } catch (_) {}
    applySkin(savedSkin);
    applyView('both');
    applyCoordination('natural', false);
    applyMode('buttons');
    window.addEventListener('pagehide', () => {
      samplePlayer.stop();
      engine.stop();
    }, { once: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})(window.ArticulationLab);
