window.ArticulationLab = window.ArticulationLab || {};
window.ArticulationLab.VOWEL_PRESETS = {
  schema: 'articulation-lab.vowel-presets.v0.1',
  evidenceNotice: 'MVP pedagogical model values. These are not yet source-backed empirical language norms.',
  presets: {
    i: {
      label: '/i/', name: 'high front unrounded',
      articulation: { tongueBodyFrontBack: 0.10, tongueBodyHeight: 0.08, lipRounding: 0.02, jawOpening: 0.18 },
      acousticTarget: { f1Hz: 300, f2Hz: 2450, f3Hz: 3150, evidenceType: 'pedagogical_model', sourceId: 'mvp-model-v0.1' }
    },
    ae: {
      label: '/æ/', name: 'low front unrounded',
      articulation: { tongueBodyFrontBack: 0.18, tongueBodyHeight: 0.82, lipRounding: 0.02, jawOpening: 0.82 },
      acousticTarget: { f1Hz: 720, f2Hz: 1800, f3Hz: 2800, evidenceType: 'pedagogical_model', sourceId: 'mvp-model-v0.1' }
    },
    aa: {
      label: '/ɑ/', name: 'low back unrounded',
      articulation: { tongueBodyFrontBack: 0.86, tongueBodyHeight: 0.88, lipRounding: 0.06, jawOpening: 0.90 },
      acousticTarget: { f1Hz: 760, f2Hz: 1150, f3Hz: 2550, evidenceType: 'pedagogical_model', sourceId: 'mvp-model-v0.1' }
    },
    schwa: {
      label: '/ə/', name: 'mid central',
      articulation: { tongueBodyFrontBack: 0.50, tongueBodyHeight: 0.50, lipRounding: 0.10, jawOpening: 0.48 },
      acousticTarget: { f1Hz: 500, f2Hz: 1500, f3Hz: 2700, evidenceType: 'pedagogical_model', sourceId: 'mvp-model-v0.1' }
    },
    u: {
      label: '/u/', name: 'high back rounded',
      articulation: { tongueBodyFrontBack: 0.86, tongueBodyHeight: 0.12, lipRounding: 0.95, jawOpening: 0.22 },
      acousticTarget: { f1Hz: 330, f2Hz: 850, f3Hz: 2350, evidenceType: 'pedagogical_model', sourceId: 'mvp-model-v0.1' }
    }
  }
};
