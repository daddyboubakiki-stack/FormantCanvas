window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  NS.createFrontalRenderer = function createFrontalRenderer() {
    let container = null;
    let stage = null;
    let svg = null;
    let facePath = null;
    let outerLip = null;
    let innerMouth = null;
    let upperTeeth = null;
    let lowerTeeth = null;
    let toothSeparators = null;
    let tongue = null;
    let jawGuide = null;

    const clamp = v => Math.max(0, Math.min(1, Number(v)));

    function mouthGeometry(state) {
      const jaw = clamp(state.jawOpening);
      const rounding = clamp(state.lipRounding);
      const spread = clamp(state.lipSpread);
      const low = clamp(state.tongueBodyHeight);
      const fb = clamp(state.tongueBodyFrontBack);

      // Rounded vowels should visibly narrow the aperture. In v0.5-alpha.1 the
      // rounding term mostly changed lip thickness, leaving /u/ too open. Here
      // both width and height narrow strongly as rounding rises.
      const width = Math.max(28, 88 + spread * 78 - rounding * 60);
      const height = Math.max(12, 14 + jaw * 70 - rounding * 12);
      const lipSide = 11 + rounding * 7 - spread * 1.5;
      const lipVertical = 9 + rounding * 5 + jaw * 1.5;
      const outerWidth = width + lipSide * 2;
      const outerHeight = height + lipVertical * 2;
      const tongueVisibility = clamp((jaw - .30) * 1.85 + (low - .54) * .82 - rounding * .16);
      const tongueWidth = Math.max(38, width * (.56 + (1 - fb) * .08));
      return {
        jaw, rounding, spread, low, fb,
        width, height, outerWidth, outerHeight,
        tongueVisibility, tongueWidth
      };
    }

    function lipContourPath(cx, cy, rx, ry, rounding) {
      const bow = 3.7 * (1 - rounding * .72);
      const lowerFullness = ry * (.16 + (1 - rounding) * .05);
      return [
        `M ${cx-rx} ${cy}`,
        `C ${cx-rx*.82} ${cy-ry*.48} ${cx-rx*.43} ${cy-ry*.95} ${cx-rx*.10} ${cy-ry*.78}`,
        `C ${cx-rx*.04} ${cy-ry*.72} ${cx-bow} ${cy-ry*.91} ${cx} ${cy-ry*.76}`,
        `C ${cx+bow} ${cy-ry*.91} ${cx+rx*.04} ${cy-ry*.72} ${cx+rx*.10} ${cy-ry*.78}`,
        `C ${cx+rx*.43} ${cy-ry*.95} ${cx+rx*.82} ${cy-ry*.48} ${cx+rx} ${cy}`,
        `C ${cx+rx*.80} ${cy+ry*.42} ${cx+rx*.42} ${cy+ry*.88+lowerFullness} ${cx} ${cy+ry}`,
        `C ${cx-rx*.42} ${cy+ry*.88+lowerFullness} ${cx-rx*.80} ${cy+ry*.42} ${cx-rx} ${cy}`,
        'Z'
      ].join(' ');
    }

    function openingPath(cx, cy, rx, ry, rounding) {
      const topFlatten = 1 - rounding * .42;
      return [
        `M ${cx-rx} ${cy}`,
        `C ${cx-rx*.72} ${cy-ry*.62*topFlatten} ${cx-rx*.31} ${cy-ry} ${cx} ${cy-ry*.92}`,
        `C ${cx+rx*.31} ${cy-ry} ${cx+rx*.72} ${cy-ry*.62*topFlatten} ${cx+rx} ${cy}`,
        `C ${cx+rx*.68} ${cy+ry*.78} ${cx+rx*.30} ${cy+ry} ${cx} ${cy+ry}`,
        `C ${cx-rx*.30} ${cy+ry} ${cx-rx*.68} ${cy+ry*.78} ${cx-rx} ${cy}`,
        'Z'
      ].join(' ');
    }

    function mount(target) {
      container = target;
      container.innerHTML = `
        <div class="mouth-stage frontal-stage">
          <svg class="mouth-svg frontal-svg" viewBox="0 0 360 350" role="img" aria-label="Frontal mouth opening teaching model">
            <rect x="1" y="1" width="358" height="348" rx="26" class="cavity-bg"/>
            <path id="frontalFace" d="M180 40 C105 40 62 92 65 176 C68 267 117 315 180 318 C243 315 292 267 295 176 C298 92 255 40 180 40 Z" class="frontal-face"/>
            <path d="M124 129 Q145 115 164 127" class="frontal-eye"/>
            <path d="M196 127 Q215 115 236 129" class="frontal-eye"/>
            <path d="M180 132 Q168 169 180 179 Q192 169 180 132" class="frontal-nose"/>
            <path d="M166 183 Q172 187 178 184 M182 184 Q188 187 194 183" class="frontal-nostril"/>
            <path id="outerLip" d="" class="frontal-lip"/>
            <path id="innerMouth" d="" class="frontal-mouth-opening"/>
            <path id="frontalTongue" d="" class="frontal-tongue"/>
            <path id="upperTeeth" d="" class="frontal-teeth"/>
            <path id="lowerTeeth" d="" class="frontal-teeth lower"/>
            <path id="toothSeparators" d="" class="frontal-tooth-separators"/>
            <path id="jawGuide" d="" class="frontal-jaw-guide"/>
            <text x="180" y="336" text-anchor="middle" class="anatomy-label">front view · same articulation state</text>
          </svg>
        </div>`;
      stage = container.querySelector('.frontal-stage');
      svg = container.querySelector('svg');
      facePath = container.querySelector('#frontalFace');
      outerLip = container.querySelector('#outerLip');
      innerMouth = container.querySelector('#innerMouth');
      upperTeeth = container.querySelector('#upperTeeth');
      lowerTeeth = container.querySelector('#lowerTeeth');
      toothSeparators = container.querySelector('#toothSeparators');
      tongue = container.querySelector('#frontalTongue');
      jawGuide = container.querySelector('#jawGuide');
    }

    function render(state) {
      if (!svg) return;
      const g = mouthGeometry(state);
      const cx = 180;
      const cy = 224 + g.jaw * 8;
      const outerRx = g.outerWidth / 2;
      const outerRy = g.outerHeight / 2;
      const innerRx = g.width / 2;
      const innerRy = g.height / 2;
      const chinDrop = g.jaw * 14;

      facePath.setAttribute('d', `M180 40 C105 40 62 92 65 176 C68 267 117 ${309+chinDrop*.55} 180 ${318+chinDrop} C243 ${309+chinDrop*.55} 292 267 295 176 C298 92 255 40 180 40 Z`);
      outerLip.setAttribute('d', lipContourPath(cx, cy, outerRx, outerRy, g.rounding));
      innerMouth.setAttribute('d', openingPath(cx, cy, innerRx, innerRy, g.rounding));

      const tongueAlpha = g.tongueVisibility;
      if (tongueAlpha > .05) {
        const tongueY = cy + innerRy * (.30 + (1-g.low) * .10);
        const tr = Math.min(g.tongueWidth / 2, innerRx * .78);
        tongue.setAttribute('d', `M ${cx-tr} ${tongueY+8} Q ${cx} ${tongueY-9} ${cx+tr} ${tongueY+8} Q ${cx} ${tongueY+23} ${cx-tr} ${tongueY+8} Z`);
        tongue.style.opacity = String(.16 + tongueAlpha * .68);
      } else {
        tongue.setAttribute('d', '');
      }

      // Teeth stay anatomically in front of the tongue but are intentionally
      // modest: the upper incisors dominate, while lower incisors only peek over
      // the lower lip in relatively unrounded, not-too-open postures.
      const toothInset = Math.max(5, innerRx * .12);
      const upperY = cy - innerRy + 3;
      const upperVisibility = clamp(1 - g.rounding * .52);
      const upperDepth = Math.max(0, Math.min(16, innerRy * .42)) * upperVisibility;
      upperTeeth.setAttribute('d', upperDepth > 2
        ? `M ${cx-innerRx+toothInset} ${upperY} Q ${cx} ${upperY+upperDepth*.34} ${cx+innerRx-toothInset} ${upperY} L ${cx+innerRx-toothInset-3} ${upperY+upperDepth*.78} Q ${cx} ${upperY+upperDepth+2} ${cx-innerRx+toothInset+3} ${upperY+upperDepth*.78} Z`
        : '');

      const lowerVisibility = clamp((0.58 - g.jaw) * 2.55) * (1 - g.rounding * .76);
      const lowerY = cy + innerRy - 2;
      const lowerHalfWidth = innerRx * (.28 + (1 - g.spread) * .05);
      const lowerDepth = Math.max(0, Math.min(5.5, innerRy * .11)) * lowerVisibility;
      lowerTeeth.setAttribute('d', lowerVisibility > .15 && lowerDepth > 1.0
        ? `M ${cx-lowerHalfWidth} ${lowerY} Q ${cx} ${lowerY-lowerDepth} ${cx+lowerHalfWidth} ${lowerY} L ${cx+lowerHalfWidth*.86} ${lowerY-lowerDepth*.42} Q ${cx} ${lowerY-lowerDepth-1.2} ${cx-lowerHalfWidth*.86} ${lowerY-lowerDepth*.42} Z`
        : '');
      lowerTeeth.style.opacity = String(.25 + lowerVisibility * .62);

      if (upperDepth > 4 && innerRx > 20) {
        const sepTop = upperY + 2;
        const sepBottom = upperY + upperDepth * .72;
        const dx = Math.min(15, innerRx * .28);
        toothSeparators.setAttribute('d', `M ${cx-dx} ${sepTop+1} L ${cx-dx*.85} ${sepBottom} M ${cx} ${sepTop} L ${cx} ${sepBottom+1} M ${cx+dx} ${sepTop+1} L ${cx+dx*.85} ${sepBottom}`);
        toothSeparators.style.opacity = String(.28 + upperVisibility * .35);
      } else {
        toothSeparators.setAttribute('d', '');
      }

      const jawY = 273 + g.jaw * 23;
      const jawWidth = 92 - g.rounding * 14;
      jawGuide.setAttribute('d', `M ${cx-jawWidth} ${jawY} Q ${cx} ${jawY+38} ${cx+jawWidth} ${jawY}`);

      stage.dataset.rounded = g.rounding > .55 ? 'true' : 'false';
      stage.dataset.strongRounded = g.rounding > .82 ? 'true' : 'false';
      stage.dataset.spread = g.spread > .48 ? 'true' : 'false';
    }

    function setInteractive() {}
    function destroy() {
      if (container) container.innerHTML = '';
      container = stage = svg = facePath = outerLip = innerMouth = upperTeeth = lowerTeeth = toothSeparators = tongue = jawGuide = null;
    }

    return { mount, render, setInteractive, destroy, mouthGeometry };
  };
})(window.ArticulationLab);
