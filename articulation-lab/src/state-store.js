window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  const defaults = Object.freeze({
    tongueBodyFrontBack: 0.50,
    tongueBodyHeight: 0.50,
    tongueTipFrontBack: 0.34,
    tongueTipHeight: 0.58,
    lipRounding: 0.10,
    lipAperture: 0.52,
    jawOpening: 0.48,
    velumOpening: 0,
    f0Hz: 125,
    voicing: false,
    modelVersion: 'articulation-state-v0.1'
  });

  NS.createStateStore = function createStateStore(initial = {}) {
    let state = { ...defaults, ...initial };
    const listeners = new Set();
    return {
      getState() { return { ...state }; },
      setState(next) {
        state = { ...state, ...next };
        listeners.forEach(fn => fn({ ...state }));
      },
      replaceState(next) {
        state = { ...defaults, ...next };
        listeners.forEach(fn => fn({ ...state }));
      },
      subscribe(fn) {
        listeners.add(fn);
        fn({ ...state });
        return () => listeners.delete(fn);
      }
    };
  };
})(window.ArticulationLab);
