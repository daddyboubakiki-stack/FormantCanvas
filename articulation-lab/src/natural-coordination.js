window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  const clamp = v => Math.max(0, Math.min(1, Number(v)));
  const COUPLED_KEYS = ['jawOpening', 'lipSpread', 'lipRounding', 'tongueRootRetraction'];

  function targets() {
    return Object.values((NS.ARTICULATION_TARGETS && NS.ARTICULATION_TARGETS.targets) || {});
  }

  function weightedCoordination(x, y) {
    const anchors = targets();
    if (!anchors.length) return {};

    const sums = Object.fromEntries(COUPLED_KEYS.map(k => [k, 0]));
    let total = 0;

    anchors.forEach(anchor => {
      const dx = x - clamp(anchor.tongueBodyFrontBack);
      const dy = y - clamp(anchor.tongueBodyHeight);
      const d2 = dx * dx + dy * dy;
      // Smooth inverse-distance field over the pedagogical vowel targets.
      // The small floor keeps the field finite while still strongly respecting
      // a nearby vowel anchor. This is a teaching coordination model, not an
      // anatomical inverse solution.
      const w = 1 / Math.pow(d2 + 0.0025, 1.7);
      total += w;
      COUPLED_KEYS.forEach(key => { sums[key] += clamp(anchor[key]) * w; });
    });

    const out = {};
    COUPLED_KEYS.forEach(key => { out[key] = clamp(sums[key] / total); });
    return out;
  }

  NS.NaturalCoordination = {
    modelVersion: 'pedagogical-natural-coordination-v0.1',
    evidenceType: 'pedagogical_interpolation',
    description: 'Smoothly interpolates jaw/lip/root teaching targets from tongue-body position. It is not a claim that human articulators are uniquely determined by tongue position.',

    fromTongue(partial = {}, current = {}) {
      const x = clamp(partial.tongueBodyFrontBack ?? current.tongueBodyFrontBack ?? 0.5);
      const y = clamp(partial.tongueBodyHeight ?? current.tongueBodyHeight ?? 0.5);
      return {
        ...partial,
        ...weightedCoordination(x, y)
      };
    },

    estimate(tongueBodyFrontBack, tongueBodyHeight) {
      return weightedCoordination(clamp(tongueBodyFrontBack), clamp(tongueBodyHeight));
    }
  };
})(window.ArticulationLab);
