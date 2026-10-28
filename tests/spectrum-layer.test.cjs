// Dependency-free smoke tests for the embedded spectrum X-ray view.
// Run: node tests/spectrum-layer.test.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');

const html = fs.readFileSync(require('node:path').join(__dirname, '..', 'index.html'), 'utf8');
const start = html.indexOf('  // Spectrum X-ray:');
const end = html.indexOf('  function render(){', start);
assert.ok(start > 0 && end > start, 'Spectrum helper stays inside the main application IIFE');
assert.ok(html.includes('class="spectrum-lab learning-plus"'), 'Casual mode remains uncluttered');
assert.ok(html.includes('    drawCursor();\n    renderSpectrumLab();'), 'Existing drawing refreshes spectrum');
assert.ok(html.includes('type="checkbox" aria-controls="spectrumPlot"'), 'Layer toggles are native controls');


assert.ok(html.includes('id="spectrumLearningExplanation"'), 'Learning note is present');
assert.ok(html.includes('class="spectrum-model-details learning-only"'), 'Learning note is mode-specific');
assert.ok(html.includes('id="spectrumResearchSpecification"'), 'Research spec is present');
assert.ok(html.includes('class="spectrum-model-details research-only"'), 'Research spec is mode-specific');
assert.ok(html.includes('どうして「レモン」の谷ができるの？'), 'Learning explains phase interference');
assert.ok(html.includes('過去の入力や出力の影響'), 'Learning uses the system-memory analogy');
assert.ok(html.includes('y[n-1]') && html.includes('x[n-2]'), 'Research includes IIR recurrence');
assert.ok(html.includes('b₀ =  α') && html.includes('a₂ = 1 - α'), 'Research includes normative bandpass coefficients');
assert.ok(html.includes('Q = clamp(f_c / B, 0.2, 80)'), 'Research gives bandwidth-to-Q relation');
assert.ok(html.includes('H_sum(z) = 0.62') && html.includes('0.68H₂(z) + 0.42H₃(z)'), 'Research shows actual gains');
assert.ok(html.includes('220区間') && html.includes('linearRampToValueAtTime'), 'Research shows time automation');
assert.ok(html.includes('https://www.w3.org/TR/webaudio/#BiquadFilterNode'), 'Research points to normative API spec');
assert.ok(html.includes('時間不変伝達関数で完全に記述することはできない'), 'Research explains frozen-time limitation');
assert.ok(html.includes('F_s = 48000 Hz'), 'Research discloses idle graph sample-rate assumption');
// Keep source-filter documentation aligned with the implementation constants.
const synthesis = html.slice(html.indexOf('function scheduleSynthesis('), html.indexOf('function setTransportPlaying(',html.indexOf('function scheduleSynthesis(')));
assert.ok(synthesis.includes("osc.type='sawtooth'") && synthesis.includes('sourceGain.gain.value=0.32'), 'Source model claim matches implementation');
assert.ok(synthesis.includes("['F1',1.00],['F2',0.68],['F3',0.42]"), 'Branch gains match implementation');
assert.ok(synthesis.includes('sum.gain.value=0.62') && synthesis.includes('master.gain.setValueAtTime(0.75'), 'Master and sum gains match implementation');
assert.ok(synthesis.includes('const N=220') && synthesis.includes('filter.type=\'bandpass\''), 'Automation and filter type match implementation');

let strokes = 0;
const stylesDrawn = [];
const ctx = {
  setTransform(){}, clearRect(){}, beginPath(){}, moveTo(){}, lineTo(){},
  stroke(){strokes++;stylesDrawn.push(this.strokeStyle);}, fillText(){}, setLineDash(){}
};
const elements = {
  spectrumLab: {open:true,addEventListener(){}},
  spectrumPlot:{
    width:0,height:0,parentElement:{},
    getBoundingClientRect:()=>({width:370,height:235}),
    getContext:()=>ctx,setAttribute(k,v){this[k]=v;}
  },
  spectrumTime:{value:'50',addEventListener(){}},
  spectrumTimeValue:{textContent:''},
  spectrumValues:{textContent:''},
  spectrumComponentLegend:{hidden:true},
  spectrumBreakdownNote:{hidden:true},
  spectrumLayerSource:{checked:false,addEventListener(){}},
  spectrumLayerFilter:{checked:true,addEventListener(){}},
  spectrumLayerOutput:{checked:true,addEventListener(){}},
  spectrumLayerComponents:{checked:false,addEventListener(){}}
};
const args = ['document','window','requestAnimationFrame','performance','duration',
  'maxHz','clamp','smoothSamples','usingEmpiricalBandwidth','qAt','qEl','f0El',
  'audio','playCursorT','uiMode'];
const f0 = {value:'100'};
const values = {
  document:{getElementById:id=>elements[id]},
  window:{devicePixelRatio:2},requestAnimationFrame:()=>{},performance:{now:()=>1000},
  duration:()=>0.6,maxHz:()=>4000,clamp:(v,a,b)=>Math.max(a,Math.min(b,v)),
  smoothSamples:name=>Array(221).fill({F1:550,F2:1450,F3:2350}[name]),
  usingEmpiricalBandwidth:()=>false,qAt:()=>8,qEl:{value:'8'},
  f0El:f0,audio:null,playCursorT:null,uiMode:'learning'
};
const api = new Function(...args,
  html.slice(start,end) + '\nreturn {spectrumBandpassResponse,spectrumComponentResponse,spectrumParallelResponse,renderSpectrumLab};'
)(...args.map(k=>values[k]));
const magnitude = h => Math.hypot(h.re,h.im);
assert.ok(Math.abs(magnitude(api.spectrumBandpassResponse(550,550,8,48000))-1)<1e-7,
  'Bandpass response peaks at its center frequency');
assert.ok(magnitude(api.spectrumBandpassResponse(0,550,8,48000))<1e-7,
  'Bandpass rejects DC');
const d=[{hz:550,q:8,gain:1},{hz:1450,q:8,gain:.68},{hz:2350,q:8,gain:.42}];
assert.ok(Number.isFinite(api.spectrumParallelResponse(550,d,48000)), 'Parallel response is finite');
assert.ok(Math.abs(api.spectrumComponentResponse(550,d[0],48000)-0.62)<1e-7,
  'F1 branch response includes its gain and shared summing gain');
assert.ok(Math.abs(api.spectrumComponentResponse(1450,d[1],48000)-0.62*0.68)<1e-7,
  'F2 branch response uses its own gain without re-normalizing');
api.renderSpectrumLab();
assert.match(elements.spectrumValues.textContent,/F0 100 Hz.*F1 550 Hz/);
assert.equal(elements.spectrumTimeValue.textContent,'0.30 s');
assert.ok(strokes>20,'Frequency response and output harmonics are drawn');
assert.match(elements.spectrumPlot['aria-label'],/F1 550 Hz/);
assert.equal(elements.spectrumComponentLegend.hidden,true,'Component curves start hidden');
assert.equal(elements.spectrumBreakdownNote.hidden,true,'Breakdown explanation starts hidden');
const beforeComponents=strokes;
elements.spectrumLayerComponents.checked=true;
api.renderSpectrumLab();
assert.equal(elements.spectrumComponentLegend.hidden,false,'Enabling components reveals F1/F2/F3 legend');
assert.equal(elements.spectrumBreakdownNote.hidden,false,'Breakdown explanation appears only when enabled');
assert.ok(strokes-beforeComponents>3,'Each component adds its own rendered curve');
for(const color of ['rgba(185,78,104,.65)','rgba(65,120,190,.65)','rgba(120,89,173,.65)']){
  assert.ok(stylesDrawn.includes(color),'Component curve '+color+' is drawn');
}
assert.match(elements.spectrumPlot['aria-label'],/各フィルターの内訳/);
const prev=strokes;
f0.value='110';
elements.spectrumLayerSource.checked=true;
api.renderSpectrumLab();
assert.match(elements.spectrumValues.textContent,/F0 110 Hz/);
assert.ok(strokes>prev,'Changing F0 and layer visibility redraws');
elements.spectrumLayerSource.checked=false;
elements.spectrumLayerFilter.checked=false;
elements.spectrumLayerOutput.checked=false;
elements.spectrumLayerComponents.checked=false;
api.renderSpectrumLab();
assert.equal(elements.spectrumComponentLegend.hidden,true,'Disabling components hides their legend');
assert.equal(elements.spectrumBreakdownNote.hidden,true,'Disabling components hides the explanation');
assert.ok(strokes>prev,'Axes remain available when all overlays are disabled');
console.log('Spectrum layer plus per-formant branch math, controls, and rendering smoke checks: PASS');
