window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  function estimateFormants(state) {
    const x = state.tongueBodyFrontBack;
    const y = state.tongueBodyHeight;
    const r = state.lipRounding;
    const jaw = state.jawOpening;
    const f1Hz = Math.max(240, Math.min(900, 255 + 540 * y + 100 * jaw + 30 * r));
    const f2Hz = Math.max(650, Math.min(2900, 2750 - 1350 * x - 510 * r - 170 * y));
    const f3Hz = Math.max(2100, Math.min(3550, 3350 - 180 * x - 560 * r - 100 * y));
    return {
      f1Hz, f2Hz, f3Hz,
      method: 'pedagogical_state_mapping_v0.1',
      confidence: 'demo_only'
    };
  }

  NS.createFormantEngine = function createFormantEngine() {
    let ctx = null;
    let osc = null;
    let sourceGain = null;
    let master = null;
    let filters = [];
    let running = false;
    let lastState = null;

    function ensureContext() {
      if (ctx) return true;
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return false;
      ctx = new AC();
      return true;
    }

    function apply(state) {
      lastState = state;
      if (!running || !ctx) return;
      const t = ctx.currentTime;
      const est = estimateFormants(state);
      osc.frequency.setTargetAtTime(state.f0Hz, t, 0.015);
      [est.f1Hz, est.f2Hz, est.f3Hz].forEach((hz, i) => {
        filters[i].frequency.setTargetAtTime(hz, t, 0.018);
      });
    }

    return {
      start(state) {
        if (running) return true;
        if (!ensureContext()) return false;
        if (ctx.state === 'suspended') ctx.resume();

        osc = ctx.createOscillator();
        osc.type = 'sawtooth';
        sourceGain = ctx.createGain();
        master = ctx.createGain();
        sourceGain.gain.value = 0.20;
        master.gain.value = 0.0001;
        osc.connect(sourceGain);
        master.connect(ctx.destination);

        const specs = [
          { q: 9, gain: 0.95 },
          { q: 13, gain: 0.50 },
          { q: 18, gain: 0.22 }
        ];
        filters = specs.map(spec => {
          const filter = ctx.createBiquadFilter();
          filter.type = 'bandpass';
          filter.Q.value = spec.q;
          const gain = ctx.createGain();
          gain.gain.value = spec.gain;
          sourceGain.connect(filter);
          filter.connect(gain);
          gain.connect(master);
          return filter;
        });

        osc.start();
        running = true;
        apply(state || lastState || { tongueBodyFrontBack:0.5,tongueBodyHeight:0.5,lipRounding:0.1,jawOpening:0.5,f0Hz:125 });
        master.gain.setTargetAtTime(0.20, ctx.currentTime, 0.03);
        return true;
      },
      stop() {
        if (!running || !ctx) return;
        running = false;
        const oldCtx = ctx;
        const oldOsc = osc;
        try { master.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.025); } catch (_) {}
        setTimeout(() => {
          try { oldOsc.stop(); } catch (_) {}
          try { oldCtx.close(); } catch (_) {}
        }, 90);
        ctx = osc = sourceGain = master = null;
        filters = [];
      },
      setArticulation(state) { apply(state); },
      setF0(hz) { if (lastState) apply({ ...lastState, f0Hz: hz }); },
      getAcousticEstimate(state) { return estimateFormants(state || lastState); },
      isRunning() { return running; }
    };
  };
})(window.ArticulationLab);
