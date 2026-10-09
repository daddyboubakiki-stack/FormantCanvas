window.ArticulationLab = window.ArticulationLab || {};
window.ArticulationLab.VOWEL_PRESETS = {
  schema: 'articulation-lab.vowel-presets.v0.5-alpha',
  evidenceNotice: 'Vowel Buttons use redistribution-safe human recordings when available. Articulation targets are stored separately as pedagogical models and are not claimed to be the recorded speaker’s measured anatomy.',
  languages: {
    english: {
      id: 'english', label: 'English', short: 'EN',
      audioSet: {
        id: 'english_mixed_human_reference_v043',
        label: 'Human English/IPA references',
        evidenceType: 'human_recording',
        scope: 'mixed_source_reference_not_population_norm',
        license: 'Mixed: CC0 1.0 + CC BY-SA 2.5'
      },
      vowels: {
        en_i:   { label:'/i/',  name:'FLEECE',  articulationTargetId:'en_i',   realAudio:'assets/audio/real/ipa_reference/i.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_I:   { label:'/ɪ/',  name:'KIT',     articulationTargetId:'en_I',   realAudio:'assets/audio/real/en_us_word_reference/I.wav', audioEvidence:'human_recording', voiceSetId:'en_us_word_reference_dvortygirl_2006', sourceWord:'kid', durationCue:'naturally short' },
        en_e:   { label:'/ɛ/',  name:'DRESS',   articulationTargetId:'en_e',   realAudio:'assets/audio/real/ipa_reference/epsilon.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_ae:  { label:'/æ/',  name:'TRAP',    articulationTargetId:'en_ae',  realAudio:'assets/audio/real/ipa_reference/ae.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_uh:  { label:'/ʌ/',  name:'STRUT',   articulationTargetId:'en_uh',  realAudio:'assets/audio/real/ipa_reference/turned_v.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_sch: { label:'/ə/',  name:'schwa',   articulationTargetId:'en_sch', realAudio:'assets/audio/real/ipa_reference/schwa.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_a:   { label:'/ɑ/',  name:'PALM',    articulationTargetId:'en_a',   realAudio:'assets/audio/real/ipa_reference/alpha.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_o:   { label:'/ɔ/',  name:'THOUGHT', articulationTargetId:'en_o',   realAudio:'assets/audio/real/ipa_reference/open_o.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_U:   { label:'/ʊ/',  name:'FOOT',    articulationTargetId:'en_U',   realAudio:'assets/audio/real/ipa_reference/U.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_u:   { label:'/u/',  name:'GOOSE',   articulationTargetId:'en_u',   realAudio:'assets/audio/real/ipa_reference/u.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' }
      }
    },
    japanese: {
      id: 'japanese', label: 'Japanese', short: 'JP',
      audioSet: {
        id: 'jp_reference_pd_2009',
        label: 'Japanese reference voice',
        evidenceType: 'human_recording',
        scope: 'language_specific_japanese_reference',
        license: 'Public Domain (PD-self)'
      },
      vowels: {
        jp_i: { label:'/i/', name:'い', articulationTargetId:'jp_i', realAudio:'assets/audio/real/jp_reference/i.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' },
        jp_e: { label:'/e/', name:'え', articulationTargetId:'jp_e', realAudio:'assets/audio/real/jp_reference/e.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' },
        jp_a: { label:'/a/', name:'あ', articulationTargetId:'jp_a', realAudio:'assets/audio/real/jp_reference/a.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' },
        jp_o: { label:'/o/', name:'お', articulationTargetId:'jp_o', realAudio:'assets/audio/real/jp_reference/o.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' },
        jp_u: { label:'/ɯ/', name:'う ≈ [ɯᵝ]', articulationTargetId:'jp_u', realAudio:'assets/audio/real/jp_reference/u.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' }
      }
    }
  }
};
