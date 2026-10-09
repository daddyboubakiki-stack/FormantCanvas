window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  const SYMBOLS = Object.freeze({
    en_i: 'i', en_I: 'ɪ', en_e: 'ɛ', en_ae: 'æ', en_uh: 'ʌ',
    en_sch: 'ə', en_a: 'ɑ', en_o: 'ɔ', en_U: 'ʊ', en_u: 'u',
    jp_i: 'i', jp_e: 'e', jp_a: 'a', jp_o: 'o', jp_u: 'ɯ'
  });

  function safeLogRatio(a, b) {
    const aa = Math.max(1, Number(a) || 1);
    const bb = Math.max(1, Number(b) || 1);
    return Math.log(aa / bb);
  }

  NS.createApproxIpaEstimator = function createApproxIpaEstimator(engine) {
    const targetTable = (NS.ARTICULATION_TARGETS && NS.ARTICULATION_TARGETS.targets) || {};

    function nearest(state) {
      if (!engine || typeof engine.getAcousticEstimate !== 'function') return null;
      const current = engine.getAcousticEstimate(state);
      let best = null;
      let second = null;

      Object.entries(targetTable).forEach(([id, target]) => {
        if (!SYMBOLS[id]) return;
        const ref = engine.getAcousticEstimate({ ...state, ...target });
        const d1 = safeLogRatio(current.f1Hz, ref.f1Hz);
        const d2 = safeLogRatio(current.f2Hz, ref.f2Hz);
        const d3 = safeLogRatio(current.f3Hz, ref.f3Hz);
        // Vowel identity is dominated here by F1/F2. F3 contributes lightly so
        // lip-rounding changes represented by the current synth are not ignored.
        const score = 1.20 * d1 * d1 + 1.00 * d2 * d2 + 0.16 * d3 * d3;
        const item = { id, symbol: SYMBOLS[id], score, reference: ref };
        if (!best || score < best.score) {
          second = best;
          best = item;
        } else if (!second || score < second.score) {
          second = item;
        }
      });

      if (!best) return null;
      return {
        ...best,
        second,
        current,
        method: 'nearest_modeled_formants',
        evidenceType: 'pedagogical_synth_estimate'
      };
    }

    return { nearest };
  };
})(window.ArticulationLab);
