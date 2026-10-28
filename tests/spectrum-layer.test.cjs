// Dependency-free smoke tests for the embedded spectrum X-ray view.
// Run: node tests/spectrum-layer.test.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');

const html = fs.readFileSync(require('node:path').join(__dirname, '..', 'index.html'), 'utf8');
const start = html.indexOf('  // Spectrum X-ray:');
const end = html.indexOf('  function render(){', start);
assert.ok(start > 0 && end > start, 'Spectrum helper stays inside the main application IIFE');
assert.ok(html.includes('class="spectrum-lab learning-plus"'), 'Casual mode remains uncluttered');
const modeButtons = html.match(/<div class="mode-switch"[^>]*>([\s\S]*?)<\/div>/);
assert.ok(modeButtons, 'Mode switch markup is present');
assert.deepEqual(
  [...modeButtons[1].matchAll(/id="([^"]+ModeBtn)"/g)].map(match => match[1]),
  ['learningModeBtn', 'researchModeBtn', 'casualModeBtn'],
  'Visual, keyboard, and screen reader mode order has Casual on the right'
);
assert.ok(html.includes('    drawCursor();\n    renderSpectrumLab();'), 'Existing drawing refreshes spectrum');
assert.ok(html.includes('type="checkbox" aria-controls="spectrumPlot"'), 'Layer toggles are native controls');


assert.ok(html.includes('id="spectrumLearningExplanation"'), 'Learning note is present');
assert.ok(html.includes('class="spectrum-model-details learning-only"'), 'Learning note is mode-specific');
assert.ok(html.includes('id="spectrumResearchSpecification"'), 'Research spec is present');
assert.ok(html.includes('class="spectrum-model-details research-only"'), 'Research spec is mode-specific');
assert.ok(html.includes('「レモン形の谷」）はどうしてできるの？'), 'Learning explains phase interference');
assert.ok(html.includes('とがった先がレモンのはしに似ている'), 'Learning defines what the lemon-shaped valley refers to');
assert.ok(html.includes('中心より<strong>低い</strong>音と<strong>高い</strong>音とでは'), 'Learning analogy predicts the phase flip across a centre frequency');
assert.ok(html.includes('鼻にかかった母音（鼻音化）') && html.includes('一般的な声道の性質と同じものだと考えないでね'),
  'Learning does not claim real voices lack anti-resonances, but separates the model valley from vocal-tract properties');
assert.ok(!html.includes('>共鳴特性</label>') && html.includes('合成フィルター特性</label>'), 'Filter layer is labelled as the synthesis filter, not the vocal tract');
assert.ok(html.includes('緑の棒の高さ ＝ 青の棒の高さ ＋ 橙の線の高さ') && html.includes('<strong>相対値</strong>'),
  'Learning states the dB relation and its normalisation');
assert.ok(html.includes('id="spectrumPrediction"') && html.includes('深くなる？ 浅くなる？') && html.includes('答え合わせ'),
  'Learning asks for a prediction before revealing the answer');
assert.ok(html.includes('L_out(k) = L_src(k)\n         + 20 log10|H_sum(e^(jω_k))|') && html.includes('≈ −12.4 dB'),
  'Research gives the plotted harmonic levels and the omitted constant gain');
assert.ok(html.includes('z = 0 以外に零点をもたない') && html.includes('実音声でも鼻腔との結合などにより反共鳴'),
  'Research distinguishes the parallel-model valley from anti-resonances in speech');
assert.ok(html.includes('blob/main/index.html') && !html.includes('blob/feat/spectrum-layer-xray'), 'Implementation link survives branch deletion');
assert.ok(!html.includes('aria-label="スペクトルを観察する時間位置"'), 'Time slider is named by its visible label');
assert.ok(!/spectrum-toggle:has\(input:not\(:checked\)\)\s*\{\s*opacity/.test(html), 'Unchecked layer labels are not faded below text contrast');
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
  spectrumTime:{value:'50',addEventListener(){},setAttribute(k,v){this[k]=v;}},
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
assert.equal(elements.spectrumTime['aria-valuetext'],'0.30秒','Slider announces seconds, not a bare percentage');
assert.match(elements.spectrumPlot['aria-label'],/深い谷：F1とF2のあいだ 約\d+ Hz（-\d+ dB）、F2とF3のあいだ/,'Text alternative reports the valleys');
assert.match(elements.spectrumPlot['aria-label'],/いちばん強い倍音：第\d+倍音/,'Text alternative reports the strongest output harmonic');
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
for(const color of ['#b94e68','#4178be','#7859ad']){
  assert.ok(stylesDrawn.includes(color),'Component curve '+color+' is drawn');
}
assert.match(elements.spectrumPlot['aria-label'],/表示中：.*F1・F2・F3の内訳/);
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
// Valleys predicted in the Learning question: /i/-like spacing gives a deeper F1–F2 valley than /a/-like spacing.
const valleyDepth=defs=>{let min=Infinity;for(let f=defs[0].hz;f<=defs[1].hz;f++)min=Math.min(min,20*Math.log10(api.spectrumParallelResponse(f,defs,48000)));
  return 20*Math.log10(api.spectrumParallelResponse(defs[0].hz,defs,48000))-min;};
assert.ok(valleyDepth([{hz:280,q:10,gain:1},{hz:2250,q:10,gain:.68},{hz:3000,q:10,gain:.42}])
  > valleyDepth([{hz:750,q:10,gain:1},{hz:1200,q:10,gain:.68},{hz:2600,q:10,gain:.42}])+15,
  'Prediction answer: wide F1–F2 spacing yields the deeper valley');
const noData=elements.spectrumValues;
values.smoothSamples=()=>Array(221).fill(null);
const emptyApi=new Function(...args, html.slice(start,end)+'\nreturn {renderSpectrumLab};')(...args.map(k=>values[k]));
emptyApi.renderSpectrumLab();
assert.match(elements.spectrumPlot['aria-label'],/グラフは空です/,'Text alternative does not go stale when trajectories are missing');
// Every inline script must still parse.
const vm=require('node:vm');
const scripts=[...html.matchAll(/<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/g)]
  .filter(m=>!/type="application\/ld\+json"/.test(m[1])).map(m=>m[2]);
assert.ok(scripts.length>=1,'Inline scripts found');
scripts.forEach((code,i)=>{ new vm.Script(code,{filename:'inline-'+i+'.js'}); });
console.log('Spectrum layer plus per-formant branch math, controls, and rendering smoke checks: PASS');
