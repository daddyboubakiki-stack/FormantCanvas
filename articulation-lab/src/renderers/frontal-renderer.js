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
    let tongue = null;
    let jawGuide = null;

    const clamp = v => Math.max(0, Math.min(1, Number(v)));

    function mouthGeometry(state) {
      const jaw = clamp(state.jawOpening);
      const rounding = clamp(state.lipRounding);
      const spread = clamp(state.lipSpread);
      const low = clamp(state.tongueBodyHeight);
      const fb = clamp(state.tongueBodyFrontBack);

      const width = 90 + spread * 72 - rounding * 42;
      const height = 18 + jaw * 72 + rounding * 8;
      const outerWidth = width + 20 + rounding * 15;
      const outerHeight = height + 16 + rounding * 10;
      const tongueVisibility = clamp((jaw - .32) * 1.8 + (low - .55) * .8);
      const tongueWidth = Math.max(42, width * (.54 + (1 - fb) * .08));
      return { jaw, rounding, spread, low, fb, width, height, outerWidth, outerHeight, tongueVisibility, tongueWidth };
    }

    function ellipsePath(cx, cy, rx, ry) {
      return `M ${cx-rx} ${cy} A ${rx} ${ry} 0 1 0 ${cx+rx} ${cy} A ${rx} ${ry} 0 1 0 ${cx-rx} ${cy} Z`;
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
            <path id="outerLip" d="" class="frontal-lip"/>
            <path id="innerMouth" d="" class="frontal-mouth-opening"/>
            <path id="frontalTongue" d="" class="frontal-tongue"/>
            <path id="upperTeeth" d="" class="frontal-teeth"/>
            <path id="lowerTeeth" d="" class="frontal-teeth lower"/>
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
      outerLip.setAttribute('d', ellipsePath(cx, cy, outerRx, outerRy));
      innerMouth.setAttribute('d', ellipsePath(cx, cy, innerRx, innerRy));

      const tongueAlpha = g.tongueVisibility;
      if (tongueAlpha > .05) {
        const tongueY = cy + innerRy * (.22 + (1-g.low) * .12);
        const tr = g.tongueWidth / 2;
        tongue.setAttribute('d', `M ${cx-tr} ${tongueY+11} Q ${cx} ${tongueY-9} ${cx+tr} ${tongueY+11} Q ${cx} ${tongueY+28} ${cx-tr} ${tongueY+11} Z`);
        tongue.style.opacity = String(.18 + tongueAlpha * .65);
      } else {
        tongue.setAttribute('d', '');
      }

      // Teeth are drawn after the tongue because, from the front, the incisors
      // are physically in front of the tongue. The lower teeth are deliberately
      // shallow and fade out as the jaw opens/rounds so they do not float across
      // a low/back tongue posture.
      const toothInset = Math.max(7, innerRx * .15);
      const upperY = cy - innerRy + 4;
      const upperDepth = Math.max(0, Math.min(18, innerRy * .42 - g.rounding * 8));
      upperTeeth.setAttribute('d', upperDepth > 2
        ? `M ${cx-innerRx+toothInset} ${upperY} Q ${cx} ${upperY+upperDepth} ${cx+innerRx-toothInset} ${upperY} L ${cx+innerRx-toothInset-3} ${upperY+upperDepth*.76} Q ${cx} ${upperY+upperDepth+3} ${cx-innerRx+toothInset+3} ${upperY+upperDepth*.76} Z`
        : '');

      const lowerVisibility = clamp((0.64 - g.jaw) * 2.35) * (1 - g.rounding * .58);
      const lowerY = cy + innerRy - 2;
      const lowerHalfWidth = innerRx * (.34 + (1 - g.spread) * .05);
      const lowerDepth = Math.max(0, Math.min(7, innerRy * .13)) * lowerVisibility;
      lowerTeeth.setAttribute('d', lowerVisibility > .12 && lowerDepth > 1.2
        ? `M ${cx-lowerHalfWidth} ${lowerY} Q ${cx} ${lowerY-lowerDepth} ${cx+lowerHalfWidth} ${lowerY} L ${cx+lowerHalfWidth*.88} ${lowerY-lowerDepth*.45} Q ${cx} ${lowerY-lowerDepth-2} ${cx-lowerHalfWidth*.88} ${lowerY-lowerDepth*.45} Z`
        : '');
      lowerTeeth.style.opacity = String(.35 + lowerVisibility * .65);

      const jawY = 273 + g.jaw * 23;
      const jawWidth = 92 - g.rounding * 10;
      jawGuide.setAttribute('d', `M ${cx-jawWidth} ${jawY} Q ${cx} ${jawY+38} ${cx+jawWidth} ${jawY}`);

      stage.dataset.rounded = g.rounding > .55 ? 'true' : 'false';
      stage.dataset.spread = g.spread > .48 ? 'true' : 'false';
    }

    function setInteractive() {}
    function destroy() {
      if (container) container.innerHTML = '';
      container = stage = svg = facePath = outerLip = innerMouth = upperTeeth = lowerTeeth = tongue = jawGuide = null;
    }

    return { mount, render, setInteractive, destroy, mouthGeometry };
  };
})(window.ArticulationLab);
