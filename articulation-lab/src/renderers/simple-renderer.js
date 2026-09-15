window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  NS.createSimpleRenderer = function createSimpleRenderer() {
    let container = null;
    let svg = null;
    let handle = null;
    let handleDot = null;
    let tonguePath = null;
    let cavityPath = null;
    let lipTop = null;
    let lipBottom = null;
    let lowerJawGroup = null;
    let onIntent = null;
    let dragging = false;
    let activePointerId = null;
    let interactive = false;

    const clamp = v => Math.max(0, Math.min(1, Number(v)));

    function tongueGeometry(state) {
      const fb = clamp(state.tongueBodyFrontBack);
      const low = clamp(state.tongueBodyHeight);
      const jaw = clamp(state.jawOpening);
      const root = clamp(state.tongueRootRetraction);
      const x = 184 + fb * 168;
      const y = 145 + low * 88 + jaw * 10;
      const tipY = 210 + low * 17 + jaw * 16;
      const rootX = 340 + root * 24;
      const rootY = 224 + low * 15 + jaw * 10;
      const frontInfluence = (0.5 - fb) * 24;
      const heightLift = (0.5 - low) * 46;
      return { x, y, tipY, rootX, rootY, frontInfluence, heightLift };
    }

    function tonguePoint(state) {
      const g = tongueGeometry(state);
      return { x: g.x, y: g.y };
    }

    function pointerToState(ev) {
      const rect = svg.getBoundingClientRect();
      const x = (ev.clientX - rect.left) * 520 / rect.width;
      const y = (ev.clientY - rect.top) * 350 / rect.height;
      return {
        tongueBodyFrontBack: Math.max(0, Math.min(1, (x - 184) / 168)),
        tongueBodyHeight: Math.max(0, Math.min(1, (y - 150) / 98))
      };
    }

    function mount(target, intentCallback) {
      container = target;
      onIntent = intentCallback;
      container.innerHTML = `
        <div class="mouth-stage sagittal-stage">
          <svg class="mouth-svg sagittal-svg" viewBox="0 0 520 350" role="img" aria-label="Interactive sagittal vocal-tract teaching model">
            <defs>
              <linearGradient id="tongueGlow" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#ff9aae"/><stop offset="1" stop-color="#f36f89"/>
              </linearGradient>
              <linearGradient id="airGlow" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#dff4ff" stop-opacity=".72"/><stop offset="1" stop-color="#d8d4ff" stop-opacity=".45"/>
              </linearGradient>
            </defs>
            <rect x="1" y="1" width="518" height="348" rx="26" class="cavity-bg"/>
            <path id="airCavity" d="" class="cavity-air"/>
            <path d="M92 106 C122 61 194 41 283 50 C360 58 410 101 423 155 C432 194 424 244 399 286" class="face-line"/>
            <path d="M105 128 C159 88 246 82 328 103 C360 112 389 130 408 153" class="palate-line"/>
            <path d="M108 92 C144 59 197 55 234 75" class="nasal-line"/>
            <path d="M105 128 L100 163 M120 123 L115 163" class="teeth-line upper-teeth"/>
            <path id="upperLip" d="M94 166 Q77 176 92 184" class="lip-line"/>
            <path d="M410 156 C400 198 402 244 416 303" class="pharynx-line"/>
            <path d="M350 113 Q375 128 386 150" class="velum-line"/>
            <g id="lowerJawGroup">
              <path id="lowerLip" d="M94 205 Q77 198 92 190" class="lip-line"/>
              <path d="M104 205 L109 178 M119 207 L124 180" class="teeth-line lower-teeth"/>
              <path d="M104 220 C126 287 204 319 309 316 C347 315 376 305 399 289" class="jaw-line"/>
            </g>
            <path id="tongueShape" d="" class="tongue-shape"/>
            <circle id="tongueHandle" cx="272" cy="196" r="22" class="tongue-handle" tabindex="0" aria-label="Tongue body handle. Drag or use arrow keys."/>
            <circle class="tongue-handle-dot" cx="272" cy="196" r="7" pointer-events="none"/>
            <text x="135" y="48" class="anatomy-label">nasal cavity</text>
            <text x="216" y="75" class="anatomy-label">hard palate → soft palate</text>
            <text x="53" y="152" class="anatomy-label">teeth</text>
            <text x="425" y="235" class="anatomy-label">pharynx</text>
            <text x="205" y="334" class="anatomy-label">lower jaw</text>
            <text x="216" y="286" class="anatomy-label">tongue</text>
            <text x="292" y="185" class="air-label">air space</text>
          </svg>
        </div>`;

      svg = container.querySelector('svg');
      handle = container.querySelector('#tongueHandle');
      handleDot = container.querySelector('.tongue-handle-dot');
      tonguePath = container.querySelector('#tongueShape');
      cavityPath = container.querySelector('#airCavity');
      lipTop = container.querySelector('#upperLip');
      lipBottom = container.querySelector('#lowerLip');
      lowerJawGroup = container.querySelector('#lowerJawGroup');

      handle.addEventListener('pointerdown', ev => {
        if (!interactive) return;
        dragging = true;
        activePointerId = ev.pointerId;
        handle.setPointerCapture(ev.pointerId);
        ev.preventDefault();
      });
      handle.addEventListener('pointermove', ev => {
        if (!interactive || !dragging || ev.pointerId !== activePointerId) return;
        onIntent(pointerToState(ev));
      });
      const endDrag = ev => {
        if (ev.pointerId === activePointerId) {
          dragging = false;
          activePointerId = null;
        }
      };
      handle.addEventListener('pointerup', endDrag);
      handle.addEventListener('pointercancel', endDrag);
      handle.addEventListener('keydown', ev => {
        if (!interactive) return;
        const current = handle.dataset.state ? JSON.parse(handle.dataset.state) : { tongueBodyFrontBack:.5, tongueBodyHeight:.5 };
        const step = ev.shiftKey ? 0.08 : 0.025;
        let changed = true;
        if (ev.key === 'ArrowLeft') current.tongueBodyFrontBack -= step;
        else if (ev.key === 'ArrowRight') current.tongueBodyFrontBack += step;
        else if (ev.key === 'ArrowUp') current.tongueBodyHeight -= step;
        else if (ev.key === 'ArrowDown') current.tongueBodyHeight += step;
        else changed = false;
        if (changed) {
          ev.preventDefault();
          onIntent(current);
        }
      });
      setInteractive(false);
    }

    function render(state) {
      if (!svg) return;
      const g = tongueGeometry(state);
      const p = { x:g.x, y:g.y };
      handle.setAttribute('cx', p.x);
      handle.setAttribute('cy', p.y);
      handle.dataset.state = JSON.stringify({ tongueBodyFrontBack: state.tongueBodyFrontBack, tongueBodyHeight: state.tongueBodyHeight });
      handleDot.setAttribute('cx', p.x);
      handleDot.setAttribute('cy', p.y);

      const jaw = clamp(state.jawOpening);
      const root = clamp(state.tongueRootRetraction);
      const spread = clamp(state.lipSpread);
      const rounding = clamp(state.lipRounding);
      const tongueBaseY = 294 + jaw * 11;

      tonguePath.setAttribute('d', [
        `M 113 ${g.tipY}`,
        `Q ${p.x - 74 + g.frontInfluence} ${p.y + 33} ${p.x} ${p.y}`,
        `Q ${p.x + 70} ${p.y - 9 - g.heightLift * 0.20} ${g.rootX} ${g.rootY - g.heightLift * 0.16}`,
        `Q ${376 + root * 6} ${252 + jaw * 5} ${382 + root * 4} ${282 + jaw * 6}`,
        `Q 292 ${tongueBaseY + 12} 200 ${tongueBaseY + 5}`,
        `Q 134 ${tongueBaseY - 5} 113 ${g.tipY}`,
        'Z'
      ].join(' '));

      const jawAngle = -(jaw - 0.18) * 11.5;
      const jawDrop = Math.max(0, jaw - 0.18) * 7;
      lowerJawGroup.setAttribute('transform', `translate(0 ${jawDrop}) rotate(${jawAngle} 405 160)`);

      const protrude = rounding * 14 - spread * 4;
      const flatten = spread * 5;
      lipTop.setAttribute('d', `M94 166 Q ${77-protrude} ${176+rounding*3-flatten*.25} 92 ${183-flatten*.22}`);
      lipBottom.setAttribute('d', `M94 205 Q ${77-protrude} ${198-rounding*2+flatten*.18} 92 ${191+flatten*.18}`);

      // Air-space visualization is intentionally schematic. It helps learners see
      // how changing articulators reshapes the available cavity without claiming
      // a measured area function.
      const mouthTopY = 181 - spread * 2;
      const mouthBottomY = 191 + jaw * 19;
      const posteriorX = 401;
      cavityPath.setAttribute('d', [
        `M 94 ${mouthTopY}`,
        'C 150 125 247 111 329 124',
        `C 365 130 391 143 ${posteriorX} 160`,
        `C 397 202 400 244 405 ${283 + jaw * 7}`,
        `Q ${390 - root * 8} ${278 + jaw * 7} ${g.rootX - 5} ${g.rootY - 7}`,
        `Q ${p.x + 62} ${p.y - 18} ${p.x} ${p.y - 8}`,
        `Q ${p.x - 72} ${p.y + 18} 116 ${g.tipY - 7}`,
        `L 94 ${mouthBottomY}`,
        'Z'
      ].join(' '));
    }

    function setInteractive(enabled) {
      interactive = Boolean(enabled);
      if (!container) return;
      container.classList.toggle('mouth-interactive', interactive);
      handle.setAttribute('aria-disabled', interactive ? 'false' : 'true');
      handle.tabIndex = interactive ? 0 : -1;
    }

    function destroy() {
      if (container) container.innerHTML = '';
      container = svg = handle = handleDot = tonguePath = cavityPath = lipTop = lipBottom = lowerJawGroup = null;
      onIntent = null;
    }

    return { mount, render, destroy, pointerToIntent: pointerToState, setInteractive };
  };
})(window.ArticulationLab);
