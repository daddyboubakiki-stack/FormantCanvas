window.ArticulationLab = window.ArticulationLab || {};
window.ArticulationLab.VOWEL_PRESETS = {
  schema: 'articulation-lab.vowel-presets.v0.4.3',
  evidenceNotice: 'Vowel Buttons use redistribution-safe human recordings when available. Mouth posture remains a pedagogical articulation model and is not claimed to be the recorded speaker’s measured anatomy.',
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
        en_i:   { label:'/i/',  name:'FLEECE', articulation:{ tongueBodyFrontBack:.08, tongueBodyHeight:.08, lipRounding:.01 }, realAudio:'assets/audio/real/ipa_reference/i.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_I:   { label:'/ɪ/',  name:'KIT',    articulation:{ tongueBodyFrontBack:.18, tongueBodyHeight:.22, lipRounding:.01 }, realAudio:'assets/audio/real/en_us_word_reference/I.wav', audioEvidence:'human_recording', voiceSetId:'en_us_word_reference_dvortygirl_2006', sourceWord:'kid', durationCue:'naturally short' },
        en_e:   { label:'/ɛ/',  name:'DRESS',  articulation:{ tongueBodyFrontBack:.19, tongueBodyHeight:.48, lipRounding:.01 }, realAudio:'assets/audio/real/ipa_reference/epsilon.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_ae:  { label:'/æ/',  name:'TRAP',   articulation:{ tongueBodyFrontBack:.17, tongueBodyHeight:.79, lipRounding:.01 }, realAudio:'assets/audio/real/ipa_reference/ae.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_uh:  { label:'/ʌ/',  name:'STRUT',  articulation:{ tongueBodyFrontBack:.51, tongueBodyHeight:.57, lipRounding:.02 }, realAudio:'assets/audio/real/ipa_reference/turned_v.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_sch: { label:'/ə/',  name:'schwa',  articulation:{ tongueBodyFrontBack:.50, tongueBodyHeight:.49, lipRounding:.08 }, realAudio:'assets/audio/real/ipa_reference/schwa.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_a:   { label:'/ɑ/',  name:'PALM',   articulation:{ tongueBodyFrontBack:.85, tongueBodyHeight:.86, lipRounding:.03 }, realAudio:'assets/audio/real/ipa_reference/alpha.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_o:   { label:'/ɔ/',  name:'THOUGHT',articulation:{ tongueBodyFrontBack:.82, tongueBodyHeight:.59, lipRounding:.58 }, realAudio:'assets/audio/real/ipa_reference/open_o.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_U:   { label:'/ʊ/',  name:'FOOT',   articulation:{ tongueBodyFrontBack:.75, tongueBodyHeight:.29, lipRounding:.52 }, realAudio:'assets/audio/real/ipa_reference/U.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' },
        en_u:   { label:'/u/',  name:'GOOSE',  articulation:{ tongueBodyFrontBack:.88, tongueBodyHeight:.12, lipRounding:.94 }, realAudio:'assets/audio/real/ipa_reference/u.wav', audioEvidence:'human_recording', voiceSetId:'ipa_reference_cc0_2021' }
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
        jp_i: { label:'/i/', name:'い', articulation:{ tongueBodyFrontBack:.12, tongueBodyHeight:.10, lipRounding:.01 }, realAudio:'assets/audio/real/jp_reference/i.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' },
        jp_e: { label:'/e/', name:'え', articulation:{ tongueBodyFrontBack:.24, tongueBodyHeight:.37, lipRounding:.01 }, realAudio:'assets/audio/real/jp_reference/e.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' },
        jp_a: { label:'/a/', name:'あ', articulation:{ tongueBodyFrontBack:.55, tongueBodyHeight:.72, lipRounding:.02 }, realAudio:'assets/audio/real/jp_reference/a.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' },
        jp_o: { label:'/o/', name:'お', articulation:{ tongueBodyFrontBack:.72, tongueBodyHeight:.40, lipRounding:.58 }, realAudio:'assets/audio/real/jp_reference/o.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' },
        jp_u: { label:'/ɯ/', name:'う ≈ [ɯᵝ]', articulation:{ tongueBodyFrontBack:.79, tongueBodyHeight:.18, lipRounding:.24 }, realAudio:'assets/audio/real/jp_reference/u.wav', audioEvidence:'human_recording', voiceSetId:'jp_reference_pd_2009' }
      }
    }
  }
};
