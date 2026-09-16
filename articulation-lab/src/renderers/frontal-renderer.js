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
    let monkeyLeftEar = null;
    let monkeyRightEar = null;
    let monkeyFacePatch = null;
    let monkeyLeftCheek = null;
    let monkeyRightCheek = null;
    let monkeyMuzzle = null;
    let monkeyNose = null;
    let monkeyNostrils = null;
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
            <g class="monkey-exterior" aria-hidden="true">
              <path class="monkey-tuft" d="M151 48 Q159 27 174 44 Q181 20 190 44 Q204 28 211 51"/>
              <g id="monkeyLeftEar" class="monkey-ear">
                <ellipse cx="62" cy="157" rx="34" ry="43"/>
                <path d="M65 132 C44 132 42 178 65 181 C78 180 83 165 76 153 C69 143 56 149 57 163"/>
              </g>
              <g id="monkeyRightEar" class="monkey-ear">
                <ellipse cx="298" cy="157" rx="34" ry="43"/>
                <path d="M295 132 C316 132 318 178 295 181 C282 180 277 165 284 153 C291 143 304 149 303 163"/>
              </g>
            </g>
            <path id="frontalFace" d="M180 40 C105 40 62 92 65 176 C68 267 117 315 180 318 C243 315 292 267 295 176 C298 92 255 40 180 40 Z" class="frontal-face"/>
            <g class="monkey-face-details" aria-hidden="true">
              <path id="monkeyFacePatch" class="monkey-face-patch" d="M180 79 C157 58 111 67 95 102 C75 145 96 191 119 205 C129 212 137 221 140 235 C151 224 165 218 180 218 C195 218 209 224 220 235 C223 221 231 212 241 205 C264 191 285 145 265 102 C249 67 203 58 180 79 Z"/>
              <ellipse class="monkey-eye-mask left" cx="139" cy="141" rx="31" ry="37"/>
              <ellipse class="monkey-eye-mask right" cx="221" cy="141" rx="31" ry="37"/>
              <ellipse id="monkeyLeftCheek" class="monkey-cheek" cx="112" cy="190" rx="15" ry="10"/>
              <ellipse id="monkeyRightCheek" class="monkey-cheek" cx="248" cy="190" rx="15" ry="10"/>
              <ellipse id="monkeyMuzzle" class="monkey-muzzle" cx="180" cy="183" rx="32" ry="27"/>
              <path id="monkeyNose" class="monkey-nose" d="M164 168 Q180 158 196 168 Q193 181 180 183 Q167 181 164 168 Z"/>
              <path id="monkeyNostrils" class="monkey-nostrils" d="M171 171 Q175 168 178 172 M182 172 Q185 168 189 171"/>
            </g>
            <path id="leftBrow" d="M124 118 Q145 114 166 118" class="frontal-brow"/>
            <path id="rightBrow" d="M194 118 Q215 114 236 118" class="frontal-brow"/>
            <ellipse id="leftEye" cx="145" cy="144" rx="6.4" ry="6.4" class="frontal-eye"/>
            <ellipse id="rightEye" cx="215" cy="144" rx="6.4" ry="6.4" class="frontal-eye"/>
            <g class="monkey-eye-highlights" aria-hidden="true">
              <circle class="monkey-eye-shine left" cx="133" cy="134" r="4.6"/>
              <circle class="monkey-eye-shine right" cx="215" cy="134" r="4.6"/>
            </g>
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
      monkeyLeftEar = container.querySelector('#monkeyLeftEar');
      monkeyRightEar = container.querySelector('#monkeyRightEar');
      monkeyFacePatch = container.querySelector('#monkeyFacePatch');
      monkeyLeftCheek = container.querySelector('#monkeyLeftCheek');
      monkeyRightCheek = container.querySelector('#monkeyRightCheek');
      monkeyMuzzle = container.querySelector('#monkeyMuzzle');
      monkeyNose = container.querySelector('#monkeyNose');
      monkeyNostrils = container.querySelector('#monkeyNostrils');
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
      const outerRx = skin === 'cute' ? innerRx + (baseOuterRx - innerRx) * .56 : baseOuterRx;
      const outerRy = skin === 'cute' ? innerRy + (baseOuterRy - innerRy) * .56 : baseOuterRy;
      const chinDrop = g.jaw * 14;

      facePath.setAttribute('d', skin === 'cute'
        ? `M180 43 C116 30 72 72 70 151 C67 239 112 ${291+chinDrop*.42} 180 ${301+chinDrop*.70} C248 ${291+chinDrop*.42} 293 239 290 151 C288 72 244 30 180 43 Z`
        : `M180 40 C105 40 62 92 65 176 C68 267 117 ${309+chinDrop*.55} 180 ${318+chinDrop} C243 ${309+chinDrop*.55} 292 267 295 176 C298 92 255 40 180 40 Z`);
      leftBrow.setAttribute('d', 'M 124 118 Q 145 114 166 118');
      rightBrow.setAttribute('d', 'M 194 118 Q 215 114 236 118');
      leftEye.setAttribute('cx', '145');
      leftEye.setAttribute('cy', '144');
      leftEye.setAttribute('rx', '6.4');
      leftEye.setAttribute('ry', '6.4');
      rightEye.setAttribute('cx', '215');
      rightEye.setAttribute('cy', '144');
      rightEye.setAttribute('rx', '6.4');
      rightEye.setAttribute('ry', '6.4');
      if (skin === 'cute') {
        leftEye.setAttribute('cx', '139');
        leftEye.setAttribute('cy', '141');
        leftEye.setAttribute('rx', '14');
        leftEye.setAttribute('ry', '16');
        rightEye.setAttribute('cx', '221');
        rightEye.setAttribute('cy', '141');
        rightEye.setAttribute('rx', '14');
        rightEye.setAttribute('ry', '16');
      }
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

      if (monkeyMuzzle) {
        const muzzleY = 181 + g.jaw * 2.5;
        monkeyMuzzle.setAttribute('cy', String(muzzleY));
        monkeyNose.setAttribute('transform', `translate(0 ${g.jaw * 1.2})`);
        monkeyNostrils.setAttribute('transform', `translate(0 ${g.jaw * 1.2})`);
        monkeyLeftCheek.setAttribute('cy', String(188 + g.jaw * 2));
        monkeyRightCheek.setAttribute('cy', String(188 + g.jaw * 2));
      }

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
      container = stage = svg = facePath = outerLip = innerMouth = innerLipRim = mouthClipPath = upperTeeth = lowerTeeth = toothSeparators = tongue = jawGuide = leftBrow = rightBrow = leftEye = rightEye = nose = monkeyLeftEar = monkeyRightEar = monkeyFacePatch = monkeyLeftCheek = monkeyRightCheek = monkeyMuzzle = monkeyNose = monkeyNostrils = null;
      lastState = null;
    }

    return { mount, render, setInteractive, setSkin, destroy, mouthGeometry };
  };
})(window.ArticulationLab);
