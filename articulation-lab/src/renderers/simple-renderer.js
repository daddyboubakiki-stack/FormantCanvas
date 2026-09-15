window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  NS.createSimpleRenderer = function createSimpleRenderer() {
    let container = null;
    let svg = null;
    let handle = null;
    let handleDot = null;
    let tonguePath = null;
    let lipTop = null;
    let lipBottom = null;
    let onIntent = null;
    let dragging = false;
    let activePointerId = null;
    let interactive = false;

    function tonguePoint(state) {
      return {
        x: 188 + state.tongueBodyFrontBack * 168,
        y: 150 + state.tongueBodyHeight * 92
      };
    }

    function pointerToState(ev) {
      const rect = svg.getBoundingClientRect();
      const x = (ev.clientX - rect.left) * 520 / rect.width;
      const y = (ev.clientY - rect.top) * 350 / rect.height;
      return {
        tongueBodyFrontBack: Math.max(0, Math.min(1, (x - 188) / 168)),
        tongueBodyHeight: Math.max(0, Math.min(1, (y - 150) / 92))
      };
    }

    function mount(target, intentCallback) {
      container = target;
      onIntent = intentCallback;
      container.innerHTML = `
        <div class="mouth-stage">
          <svg class="mouth-svg" viewBox="0 0 520 350" role="img" aria-label="Interactive sagittal vocal-tract diagram">
            <defs>
              <linearGradient id="tongueGlow" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#ff9aae"/><stop offset="1" stop-color="#f36f89"/>
              </linearGradient>
            </defs>
            <rect x="1" y="1" width="518" height="348" rx="26" class="cavity-bg"/>
            <path d="M92 106 C122 61 194 41 283 50 C360 58 410 101 423 155 C432 194 424 244 399 286" class="face-line"/>
            <path d="M105 128 C159 88 246 82 328 103 C360 112 389 130 408 153" class="palate-line"/>
            <path d="M108 92 C144 59 197 55 234 75" class="nasal-line"/>
            <path d="M105 128 L100 163 M120 123 L115 163" class="teeth-line"/>
            <path id="upperLip" d="M94 166 Q77 176 92 184" class="lip-line"/>
            <path id="lowerLip" d="M94 209 Q77 198 92 190" class="lip-line"/>
            <path d="M410 156 C400 198 402 244 416 303" class="pharynx-line"/>
            <path d="M104 220 C126 287 204 319 309 316 C347 315 376 305 399 289" class="jaw-line"/>
            <path d="M350 113 Q375 128 386 150" class="velum-line"/>
            <path id="tongueShape" d="" class="tongue-shape"/>
            <circle id="tongueHandle" cx="272" cy="196" r="22" class="tongue-handle" tabindex="0" aria-label="Tongue body handle. Drag or use arrow keys."/>
            <circle class="tongue-handle-dot" cx="272" cy="196" r="7" pointer-events="none"/>
            <text x="135" y="48" class="anatomy-label">nasal cavity</text>
            <text x="216" y="75" class="anatomy-label">hard palate → soft palate</text>
            <text x="53" y="152" class="anatomy-label">teeth</text>
            <text x="425" y="235" class="anatomy-label">pharynx</text>
            <text x="205" y="334" class="anatomy-label">lower jaw</text>
            <text x="216" y="286" class="anatomy-label">tongue</text>
          </svg>
        </div>`;

      svg = container.querySelector('svg');
      handle = container.querySelector('#tongueHandle');
      handleDot = container.querySelector('.tongue-handle-dot');
      tonguePath = container.querySelector('#tongueShape');
      lipTop = container.querySelector('#upperLip');
      lipBottom = container.querySelector('#lowerLip');

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
      const p = tonguePoint(state);
      handle.setAttribute('cx', p.x);
      handle.setAttribute('cy', p.y);
      handle.dataset.state = JSON.stringify({ tongueBodyFrontBack: state.tongueBodyFrontBack, tongueBodyHeight: state.tongueBodyHeight });
      handleDot.setAttribute('cx', p.x);
      handleDot.setAttribute('cy', p.y);

      const tipY = 224 + state.tongueBodyHeight * 17;
      const rootY = 235 + state.tongueBodyHeight * 17;
      const frontInfluence = (0.5 - state.tongueBodyFrontBack) * 22;
      const heightLift = (0.5 - state.tongueBodyHeight) * 44;
      tonguePath.setAttribute('d', [
        `M 113 ${tipY}`,
        `Q ${p.x - 72 + frontInfluence} ${p.y + 31} ${p.x} ${p.y}`,
        `Q ${p.x + 71} ${p.y - 8 - heightLift * 0.20} 354 ${rootY - heightLift * 0.18}`,
        `Q 375 252 381 285`,
        `Q 292 307 200 300`,
        `Q 134 290 113 ${tipY}`,
        'Z'
      ].join(' '));

      const r = state.lipRounding;
      const protrude = r * 13;
      const aperture = 18 - r * 7 + state.jawOpening * 5;
      lipTop.setAttribute('d', `M94 166 Q ${77-protrude} ${174+aperture*0.25} 92 ${184-aperture*0.10}`);
      lipBottom.setAttribute('d', `M94 209 Q ${77-protrude} ${200-aperture*0.25} 92 ${190+aperture*0.10}`);
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
      container = svg = handle = handleDot = tonguePath = lipTop = lipBottom = null;
      onIntent = null;
    }

    return { mount, render, destroy, pointerToIntent: pointerToState, setInteractive };
  };
})(window.ArticulationLab);
