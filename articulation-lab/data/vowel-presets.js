window.ArticulationLab = window.ArticulationLab || {};
window.ArticulationLab.VOWEL_PRESETS = {
  schema: 'articulation-lab.vowel-presets.v0.3',
  evidenceNotice: 'Articulatory locations in this prototype are pedagogical model positions, not measured anatomy. Source-backed English/Japanese acoustic targets will be layered in separately.',
  languages: {
    english: {
      id: 'english', label: 'English', short: 'EN',
      vowels: {
        en_i:   { label:'/i/',  name:'FLEECE', articulation:{ tongueBodyFrontBack:.08, tongueBodyHeight:.08, lipRounding:.01 } },
        en_I:   { label:'/ɪ/',  name:'KIT',    articulation:{ tongueBodyFrontBack:.18, tongueBodyHeight:.22, lipRounding:.01 } },
        en_e:   { label:'/ɛ/',  name:'DRESS',  articulation:{ tongueBodyFrontBack:.19, tongueBodyHeight:.48, lipRounding:.01 } },
        en_ae:  { label:'/æ/',  name:'TRAP',   articulation:{ tongueBodyFrontBack:.17, tongueBodyHeight:.79, lipRounding:.01 } },
        en_uh:  { label:'/ʌ/',  name:'STRUT',  articulation:{ tongueBodyFrontBack:.51, tongueBodyHeight:.57, lipRounding:.02 } },
        en_sch: { label:'/ə/',  name:'schwa',  articulation:{ tongueBodyFrontBack:.50, tongueBodyHeight:.49, lipRounding:.08 } },
        en_a:   { label:'/ɑ/',  name:'PALM',   articulation:{ tongueBodyFrontBack:.85, tongueBodyHeight:.86, lipRounding:.03 } },
        en_o:   { label:'/ɔ/',  name:'THOUGHT',articulation:{ tongueBodyFrontBack:.82, tongueBodyHeight:.59, lipRounding:.58 } },
        en_U:   { label:'/ʊ/',  name:'FOOT',   articulation:{ tongueBodyFrontBack:.75, tongueBodyHeight:.29, lipRounding:.52 } },
        en_u:   { label:'/u/',  name:'GOOSE',  articulation:{ tongueBodyFrontBack:.88, tongueBodyHeight:.12, lipRounding:.94 } }
      }
    },
    japanese: {
      id: 'japanese', label: 'Japanese', short: 'JP',
      vowels: {
        jp_i: { label:'/i/', name:'い', articulation:{ tongueBodyFrontBack:.12, tongueBodyHeight:.10, lipRounding:.01 } },
        jp_e: { label:'/e/', name:'え', articulation:{ tongueBodyFrontBack:.24, tongueBodyHeight:.37, lipRounding:.01 } },
        jp_a: { label:'/a/', name:'あ', articulation:{ tongueBodyFrontBack:.55, tongueBodyHeight:.72, lipRounding:.02 } },
        jp_o: { label:'/o/', name:'お', articulation:{ tongueBodyFrontBack:.72, tongueBodyHeight:.40, lipRounding:.58 } },
        jp_u: { label:'/ɯ/', name:'う ≈ [ɯᵝ]', articulation:{ tongueBodyFrontBack:.79, tongueBodyHeight:.18, lipRounding:.24 } }
      }
    }
  }
};
