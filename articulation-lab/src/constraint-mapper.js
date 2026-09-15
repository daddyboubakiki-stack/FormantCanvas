window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  const clamp = (v, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, Number(v)));

  NS.ConstraintMapper = {
    modelVersion: 'constraint-mapper-v0.1',
    sanitize(partial) {
      const out = { ...partial };
      for (const key of ['tongueBodyFrontBack','tongueBodyHeight','tongueTipFrontBack','tongueTipHeight','lipRounding','lipAperture','jawOpening','velumOpening']) {
        if (key in out) out[key] = clamp(out[key]);
      }
      if ('f0Hz' in out) out.f0Hz = clamp(out.f0Hz, 70, 320);
      if ('voicing' in out) out.voicing = Boolean(out.voicing);
      return out;
    },
    derive(state) {
      const jawOpening = clamp(0.18 + state.tongueBodyHeight * 0.72);
      const lipAperture = clamp((0.52 - state.lipRounding * 0.25) + jawOpening * 0.18, 0.16, 0.82);
      return { ...state, jawOpening, lipAperture, modelVersion: this.modelVersion };
    }
  };
})(window.ArticulationLab);
