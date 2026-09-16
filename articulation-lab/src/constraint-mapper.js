window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  const clamp = (v, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, Number(v)));

  NS.ConstraintMapper = {
    modelVersion: 'constraint-mapper-v0.5-alpha',
    sanitize(partial) {
      const out = { ...partial };
      for (const key of [
        'tongueBodyFrontBack','tongueBodyHeight','tongueRootRetraction',
        'tongueTipFrontBack','tongueTipHeight','lipRounding','lipSpread',
        'lipAperture','jawOpening','velumOpening'
      ]) {
        if (key in out) out[key] = clamp(out[key]);
      }
      if ('f0Hz' in out) out.f0Hz = clamp(out.f0Hz, 70, 320);
      if ('voicing' in out) out.voicing = Boolean(out.voicing);
      return out;
    },
    derive(state) {
      const jawOpening = clamp(state.jawOpening);
      const lipRounding = clamp(state.lipRounding);
      const lipSpread = clamp(state.lipSpread);
      const tongueRootRetraction = clamp(state.tongueRootRetraction);

      // Compatibility value for older audio/rendering code. The new visual model
      // treats jaw opening and lip spread as independent articulation axes.
      const lipAperture = clamp(
        0.16 + jawOpening * 0.58 - lipRounding * 0.20 + lipSpread * 0.06,
        0.10,
        0.90
      );

      return {
        ...state,
        jawOpening,
        lipRounding,
        lipSpread,
        tongueRootRetraction,
        lipAperture,
        modelVersion: this.modelVersion
      };
    }
  };
})(window.ArticulationLab);
