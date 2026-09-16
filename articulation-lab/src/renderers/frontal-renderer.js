window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  NS.createFrontalRenderer = function createFrontalRenderer() {
    let container = null;
    let stage = null;
    let svg = null;
    let facePath = null;
    let outerLip = null;
    let innerMouth = null;
    let innerLipRim = null;
    let mouthClipPath = null;
    let upperTeeth = null;
    let lowerTeeth = null;
    let toothSeparators = null;
    let tongue = null;
    let jawGuide = null;
    let leftBrow = null;
    let rightBrow = null;
    let leftEye = null;
    let rightEye = null;
    let nose = null;
    let skin = 'simple';
    let lastState = null;

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
      const spreadSmile = spread * (1 - rounding);
      const width = Math.max(28, 86 + spread * 84 - rounding * 60);
      const height = Math.max(4, 12 + jaw * 64 - rounding * 13 - spreadSmile * 24);
      const lipSide = 11 + rounding * 7 - spread * 1.5;
      const lipVertical = 9 + rounding * 5 + jaw * 1.5;
      const outerWidth = width + lipSide * 2;
      const outerHeight = height + lipVertical * 2;
      const tongueVisibility = clamp((jaw - .30) * 1.85 + (low - .54) * .82 - rounding * .16 - spreadSmile * .42);
      const tongueWidth = Math.max(38, width * (.56 + (1 - fb) * .08));
      return {
        jaw, rounding, spread, low, fb,
        width, height, outerWidth, outerHeight,
        tongueVisibility, tongueWidth
      };
    }

    function lipContourPath(cx, cy, rx, ry, rounding) {
      const lowerFullness = ry * (.15 + (1 - rounding) * .04);
      const topCenterY = cy - ry * .78;
      return [
        `M ${cx-rx} ${cy}`,
        `C ${cx-rx*.82} ${cy-ry*.48} ${cx-rx*.44} ${cy-ry*.92} ${cx} ${topCenterY}`,
        `C ${cx+rx*.44} ${cy-ry*.92} ${cx+rx*.82} ${cy-ry*.48} ${cx+rx} ${cy}`,
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
            <defs>
              <clipPath id="frontalMouthClip">
                <path id="mouthClipPath" d=""/>
              </clipPath>
            </defs>
            <rect x="1" y="1" width="358" height="348" rx="26" class="cavity-bg"/>
            <g class="tutor-hair" aria-hidden="true">
              <path class="tutor-hair-back" d="M88 167 C85 76 125 30 180 30 C237 30 277 76 272 167 L258 214 L102 214 Z"/>
            </g>
            <path id="frontalFace" d="M180 40 C105 40 62 92 65 176 C68 267 117 315 180 318 C243 315 292 267 295 176 C298 92 255 40 180 40 Z" class="frontal-face"/>
            <g class="tutor-face-details" aria-hidden="true">
              <path class="tutor-fringe" d="M104 94 C114 50 147 39 181 39 C217 39 246 55 257 94 C243 83 231 78 218 77 C207 87 194 91 180 91 C162 91 146 86 135 77 C124 78 114 84 104 94 Z"/>
              <path class="tutor-fringe-strand left" d="M129 70 Q119 98 124 116"/>
              <path class="tutor-fringe-strand right" d="M226 70 Q237 98 232 116"/>
              <ellipse class="tutor-cheek left" cx="118" cy="190" rx="19" ry="12"/>
              <ellipse class="tutor-cheek right" cx="242" cy="190" rx="19" ry="12"/>
              <path class="tutor-smile-eye left" d="M118 148 Q139 163 161 147"/>
              <path class="tutor-smile-eye right" d="M199 147 Q221 163 242 148"/>
            </g>
            <path id="leftBrow" d="M124 118 Q145 114 166 118" class="frontal-brow"/>
            <path id="rightBrow" d="M194 118 Q215 114 236 118" class="frontal-brow"/>
            <ellipse id="leftEye" cx="145" cy="144" rx="6.4" ry="6.4" class="frontal-eye"/>
            <ellipse id="rightEye" cx="215" cy="144" rx="6.4" ry="6.4" class="frontal-eye"/>
            <path id="frontalNose" d="M180 136 Q171 165 180 176 Q189 165 180 136" class="frontal-nose"/>
            <path id="outerLip" d="" class="frontal-lip"/>
            <path id="innerMouth" d="" class="frontal-mouth-opening"/>
            <path id="upperTeeth" d="" class="frontal-teeth" clip-path="url(#frontalMouthClip)"/>
            <path id="toothSeparators" d="" class="frontal-tooth-separators" clip-path="url(#frontalMouthClip)"/>
            <path id="frontalTongue" d="" class="frontal-tongue" clip-path="url(#frontalMouthClip)"/>
            <path id="lowerTeeth" d="" class="frontal-teeth lower" clip-path="url(#frontalMouthClip)"/>
            <path id="innerLipRim" d="" class="frontal-inner-lip"/>
            <path id="jawGuide" d="" class="frontal-jaw-guide"/>
            <text x="180" y="336" text-anchor="middle" class="anatomy-label">front view · same articulation state</text>
          </svg>
        </div>`;
      stage = container.querySelector('.frontal-stage');
      svg = container.querySelector('svg');
      facePath = container.querySelector('#frontalFace');
      outerLip = container.querySelector('#outerLip');
      innerMouth = container.querySelector('#innerMouth');
      innerLipRim = container.querySelector('#innerLipRim');
      mouthClipPath = container.querySelector('#mouthClipPath');
      upperTeeth = container.querySelector('#upperTeeth');
      lowerTeeth = container.querySelector('#lowerTeeth');
      toothSeparators = container.querySelector('#toothSeparators');
      tongue = container.querySelector('#frontalTongue');
      jawGuide = container.querySelector('#jawGuide');
      leftBrow = container.querySelector('#leftBrow');
      rightBrow = container.querySelector('#rightBrow');
      leftEye = container.querySelector('#leftEye');
      rightEye = container.querySelector('#rightEye');
      nose = container.querySelector('#frontalNose');
      stage.dataset.skin = skin;
    }

    function render(state) {
      if (!svg) return;
      lastState = state;
      const g = mouthGeometry(state);
      const cx = 180;
      const cy = 216 + g.jaw * 8;
      const innerRx = g.width / 2;
      const innerRy = g.height / 2;
      const baseOuterRx = g.outerWidth / 2;
      const baseOuterRy = g.outerHeight / 2;
      const outerRx = baseOuterRx;
      const outerRy = baseOuterRy;
      const chinDrop = g.jaw * 14;

      facePath.setAttribute('d', skin === 'cute'
        ? `M180 42 C118 35 78 77 76 157 C73 238 115 ${295+chinDrop*.40} 180 ${304+chinDrop*.62} C245 ${295+chinDrop*.40} 287 238 284 157 C282 77 242 35 180 42 Z`
        : `M180 40 C105 40 62 92 65 176 C68 267 117 ${309+chinDrop*.55} 180 ${318+chinDrop} C243 ${309+chinDrop*.55} 292 267 295 176 C298 92 255 40 180 40 Z`);
      leftBrow.setAttribute('d', skin === 'cute'
        ? 'M 112 122 Q 140 114 168 117'
        : 'M 124 118 Q 145 114 166 118');
      rightBrow.setAttribute('d', skin === 'cute'
        ? 'M 192 117 Q 220 114 248 122'
        : 'M 194 118 Q 215 114 236 118');
      leftEye.setAttribute('cx', '145');
      leftEye.setAttribute('cy', '144');
      leftEye.setAttribute('rx', '6.4');
      leftEye.setAttribute('ry', '6.4');
      rightEye.setAttribute('cx', '215');
      rightEye.setAttribute('cy', '144');
      rightEye.setAttribute('rx', '6.4');
      rightEye.setAttribute('ry', '6.4');
      outerLip.setAttribute('d', lipContourPath(cx, cy, outerRx, outerRy, g.rounding));
      const innerPath = openingPath(cx, cy, innerRx, innerRy, g.rounding);
      innerMouth.setAttribute('d', innerPath);
      innerLipRim.setAttribute('d', innerPath);
      mouthClipPath.setAttribute('d', innerPath);

      const tongueAlpha = g.tongueVisibility;

      // Decide whether the lower oral slot should show the tongue surface or
      // the lower teeth. A front vowel does not automatically mean visible
      // lower teeth: spread-close vowels like /i/ and /ɪ/ favor a "grinning"
      // lower-teeth view, whereas more open front vowels like /ɛ/ and /æ/
      // favor the tongue.
      const smileClosure = clamp(g.spread * 1.10 - g.jaw * .20 - g.rounding * .48);
      const closeSmile = clamp(1 - g.jaw * 1.55 - g.low * .55 + g.spread * .95 - g.rounding * .55);
      const tongueScore = clamp(tongueAlpha * .95 + g.jaw * .55 + g.low * .45 + (1 - Math.abs(g.fb - .32) * 1.7) * .22 - g.spread * .34);
      const lowerTeethScore = clamp(closeSmile * .95 + g.spread * .52 - tongueAlpha * .72);
      const showLowerTeeth = lowerTeethScore > tongueScore + .04;
      const showTongue = !showLowerTeeth && tongueAlpha > .05;

      if (showTongue) {
        const tongueY = cy + innerRy * (.32 + (1-g.low) * .10);
        const tr = Math.min(g.tongueWidth / 2, innerRx * .80);
        tongue.setAttribute('d', `M ${cx-tr} ${tongueY+8} Q ${cx} ${tongueY-9} ${cx+tr} ${tongueY+8} Q ${cx} ${tongueY+23} ${cx-tr} ${tongueY+8} Z`);
        tongue.style.opacity = String(.18 + tongueAlpha * .66);
      } else {
        tongue.setAttribute('d', '');
        tongue.style.opacity = '0';
      }

      // Teeth are clipped to the oral opening so they never spill outside the lips.
      // The frontal teaching model intentionally omits gums for visual stability
      // across very narrow and very open vowel postures.
      const toothInset = Math.max(8, innerRx * .22);
      const upperHalfWidth = innerRx - toothInset;
      const upperY = cy - innerRy + 1.2;
      const upperVisibility = clamp(1 - g.rounding * .60 + g.spread * .16);
      const upperDepth = Math.max(0, Math.min(13, innerRy * .31 + smileClosure * 1.1)) * upperVisibility;
      const gumHeight = 0;
      upperTeeth.setAttribute('d', upperDepth > 2
        ? `M ${cx-upperHalfWidth} ${upperY+gumHeight*.70} Q ${cx} ${upperY+gumHeight*.98} ${cx+upperHalfWidth} ${upperY+gumHeight*.70} L ${cx+upperHalfWidth-3} ${upperY+gumHeight+upperDepth*.84} Q ${cx} ${upperY+gumHeight+upperDepth+1.1} ${cx-upperHalfWidth+3} ${upperY+gumHeight+upperDepth*.84} Z`
        : '');

      const lowerVisibility = showLowerTeeth
        ? clamp((0.44 - g.jaw) * 2.7 + smileClosure * 1.70 + g.spread * .22) * (1 - g.rounding * .86)
        : 0;
      // Anchor the lower incisors a bit closer to the lower lip so that close
      // spread vowels like /ɪ/ do not leave a floating-tooth look.
      let lowerY = cy + innerRy - 1.1 - smileClosure * 2.2;
      const lowerHalfWidth = upperHalfWidth * (.90 - g.rounding * .04 + g.spread * .02);
      const lowerDepth = Math.max(0, Math.min(14.2, innerRy * .28 + smileClosure * 3.5)) * lowerVisibility;
      const upperTeethBottom = upperY + gumHeight + upperDepth + 1.1;
      const minInterdentalGap = showLowerTeeth ? (1.6 + (1 - g.jaw) * 1.8 + g.spread * .8) : 0;
      const lowerTeethTop = lowerY - lowerDepth - 1.0;
      const minAllowedLowerTop = upperTeethBottom + minInterdentalGap;
      if (lowerTeethTop < minAllowedLowerTop) {
        lowerY += (minAllowedLowerTop - lowerTeethTop);
      }
      const lowerTopY = lowerY - lowerDepth;
      lowerTeeth.setAttribute('d', lowerVisibility > .15 && lowerDepth > 1.2
        ? `M ${cx-lowerHalfWidth} ${lowerTopY} Q ${cx} ${lowerTopY-0.7} ${cx+lowerHalfWidth} ${lowerTopY} L ${cx+lowerHalfWidth*.94} ${lowerY} Q ${cx} ${lowerY+0.3} ${cx-lowerHalfWidth*.94} ${lowerY} Z`
        : '');
      upperTeeth.style.opacity = String(.42 + upperVisibility * .50);
      lowerTeeth.style.opacity = String(showLowerTeeth ? (.38 + lowerVisibility * .58) : 0);

      const separatorParts = [];
      if (upperDepth > 4 && innerRx > 20) {
        const sepTop = upperY + gumHeight + 1.5;
        const sepBottom = upperY + gumHeight + upperDepth * .72;
        const dx = Math.min(12, upperHalfWidth * .32);
        separatorParts.push(`M ${cx-dx} ${sepTop} L ${cx-dx*.85} ${sepBottom}`);
        separatorParts.push(`M ${cx} ${sepTop-0.4} L ${cx} ${sepBottom+0.8}`);
        separatorParts.push(`M ${cx+dx} ${sepTop} L ${cx+dx*.85} ${sepBottom}`);
      }
      if (showLowerTeeth && lowerDepth > 3.2 && lowerHalfWidth > 18) {
        const lowerSepTop = lowerTopY + 0.4;
        const lowerSepBottom = lowerY - 0.2;
        const ldx = Math.min(11, lowerHalfWidth * .34);
        separatorParts.push(`M ${cx-ldx} ${lowerSepTop} L ${cx-ldx*.88} ${lowerSepBottom}`);
        separatorParts.push(`M ${cx} ${lowerSepTop-0.2} L ${cx} ${lowerSepBottom}`);
        separatorParts.push(`M ${cx+ldx} ${lowerSepTop} L ${cx+ldx*.88} ${lowerSepBottom}`);
      }
      toothSeparators.setAttribute('d', separatorParts.join(' '));
      toothSeparators.style.opacity = separatorParts.length ? String(.22 + upperVisibility * .26 + (showLowerTeeth ? .08 : 0)) : '0';

      const jawY = 273 + g.jaw * 23;
      const jawWidth = 92 - g.rounding * 14;
      jawGuide.setAttribute('d', `M ${cx-jawWidth} ${jawY} Q ${cx} ${jawY+38} ${cx+jawWidth} ${jawY}`);

      stage.dataset.rounded = g.rounding > .55 ? 'true' : 'false';
      stage.dataset.strongRounded = g.rounding > .82 ? 'true' : 'false';
      stage.dataset.spread = g.spread > .48 ? 'true' : 'false';
    }

    function setInteractive() {}
    function setSkin(nextSkin) {
      skin = nextSkin === 'cute' ? 'cute' : 'simple';
      if (stage) stage.dataset.skin = skin;
      if (lastState) render(lastState);
    }
    function destroy() {
      if (container) container.innerHTML = '';
      container = stage = svg = facePath = outerLip = innerMouth = innerLipRim = mouthClipPath = upperTeeth = lowerTeeth = toothSeparators = tongue = jawGuide = leftBrow = rightBrow = leftEye = rightEye = nose = null;
      lastState = null;
    }

    return { mount, render, setInteractive, setSkin, destroy, mouthGeometry };
  };
})(window.ArticulationLab);
