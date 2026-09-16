#!/usr/bin/env python3
from pathlib import Path

path=Path('index.html')
s=path.read_text(encoding='utf-8')

if 'GLOSSARY_SOURCE_DETAILS' in s:
    print('Two-level glossary citation formatting already present; no changes.')
    raise SystemExit(0)

def replace_once(old,new,label):
    global s
    count=s.count(old)
    if count!=1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    s=s.replace(old,new,1)

# Make the lower learning card look like a proper reference list while keeping popovers compact.
replace_once(
"  .learning-source { margin-top:8px; padding-top:8px; border-top:1px solid #e1e6ef; color:#788194; font-size:10.5px; line-height:1.55; }\n  .learning-source a, .learning-popover-source a { color:#315fc4; text-decoration:none; font-weight:750; }\n  .learning-source a:hover, .learning-popover-source a:hover { text-decoration:underline; }\n  .learning-source-sep { margin:0 4px; color:#a0a7b4; }",
"  .learning-source { margin-top:10px; padding-top:9px; border-top:1px solid #e1e6ef; color:#667085; font-size:10.5px; line-height:1.58; }\n  .learning-source-heading { display:block; margin-bottom:5px; color:#4d576b; font-size:10.5px; font-weight:900; }\n  .learning-source-list { margin:0; padding-left:18px; }\n  .learning-source-list li { margin:4px 0; padding-left:1px; }\n  .learning-source a, .learning-popover-source a { color:#315fc4; text-decoration:none; font-weight:700; }\n  .learning-source a:hover, .learning-popover-source a:hover { text-decoration:underline; }\n  .learning-source-sep { margin:0 4px; color:#a0a7b4; }",
'learning reference list css')

# Authoritative full bibliography strings are centralized here so the topic prose stays readable.
marker="""  function learningEvidenceLabel(){"""
details="""  const GLOSSARY_SOURCE_DETAILS = {
    'https://www.fon.hum.uva.nl/praat/manual/frequency.html': {
      short:'Praat Manual',
      citation:'Praat Manual. (n.d.). “frequency.” Praat: doing phonetics by computer. Retrieved 16 September 2026.'
    },
    'https://doi.org/10.1093/acrefore/9780199384655.013.894': {
      short:'Tokuda (2021)',
      citation:'Tokuda, I. (2021). The source–filter theory of speech. Oxford Research Encyclopedia of Linguistics. https://doi.org/10.1093/acrefore/9780199384655.013.894'
    },
    'https://ocw.mit.edu/courses/24-901-language-and-its-structure-i-phonology-fall-2010/resources/mit24_901f10_lec08/': {
      short:'Kenstowicz (2010)',
      citation:'Kenstowicz, M. (2010). Phonetics I: Acoustics of vowels, using Praat [Lecture 8 notes]. 24.901 Language and Its Structure I: Phonology. MIT OpenCourseWare, Massachusetts Institute of Technology.'
    },
    'https://www.mq.edu.au/faculty-of-medicine-health-and-human-sciences/departments-and-schools/department-of-linguistics/our-research/phonetics-and-phonology/speech/acoustics/acoustic-theory-of-speech-production/vocal-tract-resonance': {
      short:'Macquarie Linguistics (2026)',
      citation:'Macquarie University, Department of Linguistics. (2026, June 23). Vocal tract resonance.'
    },
    'https://www.fon.hum.uva.nl/praat/manual/Formant.html': {
      short:'Praat Manual',
      citation:'Praat Manual. (n.d.). “Formant.” Praat: doing phonetics by computer. Retrieved 16 September 2026.'
    },
    'https://www.phon.ox.ac.uk/jcoleman/source_filter': {
      short:'Oxford Phonetics',
      citation:'University of Oxford, Phonetics Laboratory. (n.d.). The source-filter model of speech production. Retrieved 16 September 2026.'
    },
    'https://www.nist.gov/pml/owm/si-units-time': {
      short:'NIST',
      citation:'National Institute of Standards and Technology. (n.d.). SI units—Time. Retrieved 16 September 2026.'
    },
    'https://www.fon.hum.uva.nl/praat/manual/Spectrogram.html': {
      short:'Praat Manual',
      citation:'Praat Manual. (n.d.). “Spectrogram.” Praat: doing phonetics by computer. Retrieved 16 September 2026.'
    },
    'https://www.fon.hum.uva.nl/praat/manual/Intro_3_1__Viewing_a_spectrogram.html': {
      short:'Praat Tutorial',
      citation:'Praat Manual. (n.d.). “Intro 3.1. Viewing a spectrogram.” Praat: doing phonetics by computer. Retrieved 16 September 2026.'
    },
    'https://www.fon.hum.uva.nl/praat/manual/Source-filter_synthesis.html': {
      short:'Praat Manual',
      citation:'Praat Manual. (n.d.). “Source-filter synthesis.” Praat: doing phonetics by computer. Retrieved 16 September 2026.'
    },
    'https://praat.org/': {
      short:'Boersma et al. (2026)',
      citation:'Boersma, P., Weenink, D., & Shchupak, A. (2026). Praat: doing phonetics by computer [Computer program]. Praat.org.'
    },
    'https://www.fon.hum.uva.nl/praat/manual/Intro.html': {
      short:'Praat Manual',
      citation:'Praat Manual. (n.d.). “Intro.” Praat: doing phonetics by computer. Retrieved 16 September 2026.'
    },
    'https://www.fon.hum.uva.nl/praat/manual/Formants__Extract_smoothest_part___.html': {
      short:'Praat Manual',
      citation:'Praat Manual. (n.d.). “Formants: Extract smoothest part...” Praat: doing phonetics by computer. Retrieved 16 September 2026.'
    },
    'https://openstax.org/books/university-physics-volume-2/pages/15-5-resonance-in-an-ac-circuit': {
      short:'Ling et al. (2016)',
      citation:'Ling, S. J., Moebs, W., & Sanny, J. (2016). University Physics Volume 2, §15.5 “Resonance in an AC Circuit.” OpenStax, Rice University.'
    },
    'https://webaudio.github.io/web-audio-api/#BiquadFilterNode': {
      short:'Web Audio API',
      citation:'Adenot, P., & Choi, H. (Eds.). (2024). Web Audio API 1.1, § BiquadFilterNode (First Public Working Draft, 5 November 2024). World Wide Web Consortium.'
    }
  };

  function learningSourceInfo(source){
    const detail=source && source.url ? GLOSSARY_SOURCE_DETAILS[source.url] : null;
    return {
      short:(detail && detail.short) || (source && source.label) || '出典',
      citation:(detail && detail.citation) || (source && source.label) || '出典情報なし',
      url:source && source.url ? source.url : ''
    };
  }

"""
replace_once(marker,details+marker,'source details registry')

# Replace one renderer with a full lower-card reference renderer and a compact popover renderer.
old_renderer="""  function renderLearningSources(container,item){
    if(!container) return;
    container.textContent='';
    const sources=(item && item.sources) || [];
    if(!sources.length){ container.hidden=true; return; }
    container.hidden=false;
    const prefix=document.createElement('span');
    prefix.textContent='出典：';
    container.appendChild(prefix);
    sources.forEach((source,index)=>{
      if(index){ const sep=document.createElement('span'); sep.className='learning-source-sep'; sep.textContent='·'; container.appendChild(sep); }
      if(source.url){
        const a=document.createElement('a'); a.href=source.url; a.target='_blank'; a.rel='noreferrer'; a.textContent=source.label; container.appendChild(a);
      }else{
        const span=document.createElement('span'); span.textContent=source.label; container.appendChild(span);
      }
    });
  }
"""
new_renderer="""  function appendLearningSourceLink(parent,source,text){
    if(source.url){
      const a=document.createElement('a');
      a.href=source.url; a.target='_blank'; a.rel='noreferrer'; a.textContent=text;
      parent.appendChild(a);
    }else{
      const span=document.createElement('span'); span.textContent=text; parent.appendChild(span);
    }
  }

  function renderLearningReferences(container,item){
    if(!container) return;
    container.textContent='';
    const sources=(item && item.sources) || [];
    if(!sources.length){ container.hidden=true; return; }
    container.hidden=false;
    const heading=document.createElement('strong');
    heading.className='learning-source-heading';
    heading.textContent='出典・参考文献';
    container.appendChild(heading);
    const list=document.createElement('ol');
    list.className='learning-source-list';
    sources.forEach(source=>{
      const li=document.createElement('li');
      const info=learningSourceInfo(source);
      appendLearningSourceLink(li,info,info.citation);
      list.appendChild(li);
    });
    container.appendChild(list);
  }

  function renderLearningSourceShort(container,item){
    if(!container) return;
    container.textContent='';
    const sources=(item && item.sources) || [];
    if(!sources.length){ container.hidden=true; return; }
    container.hidden=false;
    const prefix=document.createElement('span'); prefix.textContent='出典：'; container.appendChild(prefix);
    sources.forEach((source,index)=>{
      if(index){ const sep=document.createElement('span'); sep.className='learning-source-sep'; sep.textContent='·'; container.appendChild(sep); }
      const info=learningSourceInfo(source);
      appendLearningSourceLink(container,info,info.short);
    });
  }
"""
replace_once(old_renderer,new_renderer,'split source renderers')
replace_once('    renderLearningSources(learningExplainSources,item);','    renderLearningReferences(learningExplainSources,item);','lower full references call')
replace_once('    renderLearningSources(learningPopoverSources,item);','    renderLearningSourceShort(learningPopoverSources,item);','popover compact sources call')

path.write_text(s,encoding='utf-8')
print('Separated compact popover sources from full lower-card references.')
