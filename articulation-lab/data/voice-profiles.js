window.ArticulationLab = window.ArticulationLab || {};
window.ArticulationLab.VOICE_PROFILES = {
  child: {
    id: 'child', label: 'Child', emoji: '🧒', defaultF0: 245,
    spectralTilt: 1.12, breathiness: 0.022, vibratoCents: 7,
    formantScale: 1.08, sourceBrightnessHz: 6200, outputGain: 0.11
  },
  teen: {
    id: 'teen', label: 'Teen', emoji: '🌱', defaultF0: 190,
    spectralTilt: 1.22, breathiness: 0.020, vibratoCents: 5,
    formantScale: 1.035, sourceBrightnessHz: 5700, outputGain: 0.12
  },
  adult: {
    id: 'adult', label: 'Adult', emoji: '🧑', defaultF0: 135,
    spectralTilt: 1.38, breathiness: 0.014, vibratoCents: 3,
    formantScale: 1.0, sourceBrightnessHz: 5000, outputGain: 0.13
  },
  soft: {
    id: 'soft', label: 'Soft / airy', emoji: '☁️', defaultF0: 175,
    spectralTilt: 1.55, breathiness: 0.052, vibratoCents: 4,
    formantScale: 1.0, sourceBrightnessHz: 4300, outputGain: 0.12
  }
};
