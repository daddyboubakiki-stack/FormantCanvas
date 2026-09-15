window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  function estimateBaseFormants(state) {
    const x = state.tongueBodyFrontBack;
    const y = state.tongueBodyHeight;
    const r = state.lipRounding;
    const jaw = state.jawOpening;
    return {
      f1Hz: Math.max(240, Math.min(900, 255 + 540 * y + 100 * jaw + 30 * r)),
      f2Hz: Math.max(650, Math.min(2900, 2750 - 1350 * x - 510 * r - 170 * y)),
      f3Hz: Math.max(2100, Math.min(3550, 3350 - 180 * x - 560 * r - 100 * y))
    };
  }

  function makePeriodicWave(ctx, profile) {
    const count = 64;
    const real = new Float32Array(count);
    const imag = new Float32Array(count);
    for (let n = 1; n < count; n++) {
      const oddLift = n % 2 ? 1.0 : 0.82;
      imag[n] = oddLift / Math.pow(n, profile.spectralTilt);
    }
    return ctx.createPeriodicWave(real, imag, { disableNormalization: false });
  }

  function makeNoise(ctx) {
    const length = ctx.sampleRate * 2;
    const buffer = ctx.createBuffer(1, length, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    let last = 0;
    for (let i = 0; i < length; i++) {
      const white = Math.random() * 2 - 1;
      last = last * 0.78 + white * 0.22;
      data[i] = last;
    }
    const src = ctx.createBufferSource();
    src.buffer = buffer;
    src.loop = true;
    return src;
  }

  NS.createFormantEngine = function createFormantEngine() {
    let ctx = null;
    let osc = null;
    let noise = null;
    let noiseGain = null;
    let sourceGain = null;
    let sourceLP = null;
    let sourceHP = null;
    let master = null;
    let formants = [];
    let lfo = null;
    let lfoGain = null;
    let running = false;
    let burstTimer = null;
    let lastState = null;
    let profileId = 'child';
    let profile = NS.VOICE_PROFILES.child;

    function ensureContext() {
      if (ctx) return true;
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return false;
      ctx = new AC();
      return true;
    }

    function acousticEstimate(state) {
      const base = estimateBaseFormants(state || lastState || { tongueBodyFrontBack:.5,tongueBodyHeight:.5,lipRounding:.1,jawOpening:.5 });
      const s = profile.formantScale || 1;
      return {
        f1Hz: base.f1Hz * s,
        f2Hz: base.f2Hz * s,
        f3Hz: base.f3Hz * s,
        method: 'pedagogical_state_mapping_v0.3_plus_voice_rendering',
        confidence: 'demo_only',
        voiceProfileId: profileId,
        formantScale: s
      };
    }

    function applyProfile() {
      if (!ctx || !running) return;
      const t = ctx.currentTime;
      try { osc.setPeriodicWave(makePeriodicWave(ctx, profile)); } catch (_) {}
      sourceLP.frequency.setTargetAtTime(profile.sourceBrightnessHz, t, .03);
      noiseGain.gain.setTargetAtTime(profile.breathiness, t, .03);
      lfoGain.gain.setTargetAtTime(profile.vibratoCents, t, .05);
      master.gain.setTargetAtTime(profile.outputGain, t, .04);
    }

    function apply(state) {
      lastState = state;
      if (!running || !ctx) return;
      const t = ctx.currentTime;
      const est = acousticEstimate(state);
      osc.frequency.setTargetAtTime(state.f0Hz, t, 0.012);
      const targets = [est.f1Hz, est.f2Hz, est.f3Hz];
      formants.forEach((filter, i) => filter.frequency.setTargetAtTime(targets[i], t, 0.018));
    }

    function tearDown() {
      if (burstTimer) { clearTimeout(burstTimer); burstTimer = null; }
      const old = { ctx, osc, noise, lfo };
      try { master && master.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.02); } catch (_) {}
      setTimeout(() => {
        try { old.osc && old.osc.stop(); } catch (_) {}
        try { old.noise && old.noise.stop(); } catch (_) {}
        try { old.lfo && old.lfo.stop(); } catch (_) {}
        try { old.ctx && old.ctx.close(); } catch (_) {}
      }, 90);
      ctx = osc = noise = noiseGain = sourceGain = sourceLP = sourceHP = master = lfo = lfoGain = null;
      formants = [];
    }

    return {
      start(state) {
        if (running) return true;
        if (!ensureContext()) return false;
        if (ctx.state === 'suspended') ctx.resume();

        osc = ctx.createOscillator();
        osc.setPeriodicWave(makePeriodicWave(ctx, profile));
        sourceGain = ctx.createGain();
        sourceGain.gain.value = 0.55;
        sourceHP = ctx.createBiquadFilter();
        sourceHP.type = 'highpass';
        sourceHP.frequency.value = 55;
        sourceLP = ctx.createBiquadFilter();
        sourceLP.type = 'lowpass';
        sourceLP.frequency.value = profile.sourceBrightnessHz;

        noise = makeNoise(ctx);
        noiseGain = ctx.createGain();
        noiseGain.gain.value = profile.breathiness;
        const noiseLP = ctx.createBiquadFilter();
        noiseLP.type = 'lowpass';
        noiseLP.frequency.value = 3800;

        const mix = ctx.createGain();
        mix.gain.value = 0.8;
        osc.connect(sourceGain).connect(sourceHP).connect(sourceLP).connect(mix);
        noise.connect(noiseLP).connect(noiseGain).connect(mix);

        const specs = [
          { q: 5.2, gain: 17 },
          { q: 7.5, gain: 14 },
          { q: 10.0, gain: 9 }
        ];
        let chain = mix;
        formants = specs.map(spec => {
          const f = ctx.createBiquadFilter();
          f.type = 'peaking';
          f.Q.value = spec.q;
          f.gain.value = spec.gain;
          chain.connect(f);
          chain = f;
          return f;
        });

        const warmth = ctx.createBiquadFilter();
        warmth.type = 'lowshelf';
        warmth.frequency.value = 450;
        warmth.gain.value = -2;
        chain.connect(warmth);

        const limiter = ctx.createDynamicsCompressor();
        limiter.threshold.value = -13;
        limiter.knee.value = 9;
        limiter.ratio.value = 5;
        limiter.attack.value = 0.005;
        limiter.release.value = 0.09;
        warmth.connect(limiter);

        master = ctx.createGain();
        master.gain.value = 0.0001;
        limiter.connect(master).connect(ctx.destination);

        lfo = ctx.createOscillator();
        lfo.type = 'sine';
        lfo.frequency.value = 5.2;
        lfoGain = ctx.createGain();
        lfoGain.gain.value = profile.vibratoCents;
        lfo.connect(lfoGain).connect(osc.detune);

        osc.start(); noise.start(); lfo.start();
        running = true;
        applyProfile();
        apply(state || lastState || { tongueBodyFrontBack:.5,tongueBodyHeight:.5,lipRounding:.1,jawOpening:.5,f0Hz:profile.defaultF0 });
        return true;
      },
      stop() {
        if (!running) return;
        running = false;
        tearDown();
      },
      playBurst(state, durationMs = 500) {
        const ms = Math.max(120, Math.min(2000, Number(durationMs) || 500));
        if (burstTimer) { clearTimeout(burstTimer); burstTimer = null; }
        if (!running) {
          const ok = this.start(state);
          if (!ok) return false;
        } else {
          apply(state);
        }
        if (ctx && master) {
          const t = ctx.currentTime;
          const g = Math.max(0.02, profile.outputGain);
          try {
            master.gain.cancelScheduledValues(t);
            master.gain.setValueAtTime(0.0001, t);
            master.gain.exponentialRampToValueAtTime(g, t + 0.022);
            master.gain.setValueAtTime(g, t + Math.max(0.04, ms / 1000 - 0.08));
            master.gain.exponentialRampToValueAtTime(0.0001, t + ms / 1000);
          } catch (_) {}
        }
        burstTimer = setTimeout(() => {
          burstTimer = null;
          if (running) { running = false; tearDown(); }
        }, ms + 70);
        return true;
      },
      setArticulation(state) { apply(state); },
      setF0(hz) { if (lastState) apply({ ...lastState, f0Hz: hz }); },
      setVoiceProfile(id) {
        if (!NS.VOICE_PROFILES[id]) return false;
        profileId = id;
        profile = NS.VOICE_PROFILES[id];
        applyProfile();
        if (lastState) apply(lastState);
        return true;
      },
      getVoiceProfile() { return { ...profile }; },
      getAcousticEstimate(state) { return acousticEstimate(state || lastState); },
      isRunning() { return running; }
    };
  };
})(window.ArticulationLab);
