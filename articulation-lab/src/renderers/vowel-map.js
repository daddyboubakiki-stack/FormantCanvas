window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  // Internal build compatibility label: Articulation Lab v0.5-alpha.19.
  NS.createVowelMap = function createVowelMap() {
    let container = null;
    let languageMode = 'both';
    let selectedKey = null;
    let onPreset = null;

    function setButtonSelection(layer, key) {
      layer.querySelectorAll('.vowel-map-btn').forEach(btn => {
        const isSelected = btn.dataset.key === key;
        btn.classList.toggle('selected', isSelected);
        btn.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
      });
    }

    function targetForPreset(preset) {
      const id = preset.articulationTargetId;
      return (NS.ARTICULATION_TARGETS && NS.ARTICULATION_TARGETS.targets[id]) || preset.articulation || {
        tongueBodyFrontBack: .5,
        tongueBodyHeight: .5
      };
    }

    function mapPoint(articulation) {
      const yNorm = Math.max(0, Math.min(1, articulation.tongueBodyHeight));
      const xNorm = Math.max(0, Math.min(1, articulation.tongueBodyFrontBack));
      const topLeft = 58, topRight = 404;
      const bottomLeft = 174, bottomRight = 344;
      const left = topLeft + (bottomLeft - topLeft) * yNorm;
      const right = topRight + (bottomRight - topRight) * yNorm;
      return {
        x: left + (right - left) * xNorm,
        y: 42 + yNorm * 218
      };
    }

    function rebuild() {
      if (!container) return;
      container.innerHTML = `
        <div class="vowel-map-wrap">
          <svg class="vowel-map-svg" viewBox="0 0 460 300" role="img" aria-label="Simplified vowel quadrilateral">
            <path d="M58 42 L404 42 L344 260 L174 260 Z" class="quad-outline"/>
            <path d="M87 97 L389 97 M116 151 L374 151 M145 206 L359 206" class="quad-grid"/>
            <text x="55" y="27" class="quad-label">front</text>
            <text x="377" y="27" class="quad-label">back</text>
            <text x="15" y="49" class="quad-label">close</text>
            <text x="18" y="266" class="quad-label">open</text>
          </svg>
          <div class="vowel-button-layer" aria-label="Vowel buttons"></div>
        </div>`;
      const layer = container.querySelector('.vowel-button-layer');
      const langs = NS.VOWEL_PRESETS.languages;
      const use = languageMode === 'both' ? ['english','japanese'] : [languageMode];

      use.forEach(langId => {
        const lang = langs[langId];
        Object.entries(lang.vowels).forEach(([id, preset]) => {
          const p = mapPoint(targetForPreset(preset));
          const key = `${langId}:${id}`;
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = `vowel-map-btn map-${langId}`;
          btn.dataset.key = key;
          btn.setAttribute('aria-label', `${lang.label} ${preset.label} ${preset.name}`);
          btn.setAttribute('aria-pressed', key === selectedKey ? 'true' : 'false');
          const nudge = languageMode === 'both' ? (langId === 'english' ? -8 : 8) : 0;
          btn.style.left = `${((p.x + nudge) / 460) * 100}%`;
          btn.style.top = `${(p.y / 300) * 100}%`;
          btn.innerHTML = `<span>${preset.label}</span><small>${lang.short}</small>`;
          btn.classList.toggle('selected', key === selectedKey);
          btn.addEventListener('click', () => {
            selectedKey = key;
            setButtonSelection(layer, key);
            if (onPreset) onPreset(langId, id, preset, btn);
          });
          layer.appendChild(btn);
        });
      });
    }

    function mount(target, callback) {
      container = target;
      onPreset = callback;
      rebuild();
    }
    function setLanguageMode(mode) {
      languageMode = ['english','japanese','both'].includes(mode) ? mode : 'both';
      rebuild();
    }
    function setSelected(langId, id) {
      selectedKey = langId && id ? `${langId}:${id}` : null;
      if (container) {
        const layer = container.querySelector('.vowel-button-layer');
        if (layer) setButtonSelection(layer, selectedKey);
      }
    }
    function pulse(langId, id) {
      if (!container) return;
      const key = `${langId}:${id}`;
      const btn = Array.from(container.querySelectorAll('.vowel-map-btn')).find(b => b.dataset.key === key);
      if (!btn) return;
      btn.classList.remove('sounding');
      void btn.offsetWidth;
      btn.classList.add('sounding');
      setTimeout(() => btn.classList.remove('sounding'), 520);
    }
    function destroy() {
      if (container) container.innerHTML = '';
      container = null;
      onPreset = null;
    }
    return { mount, setLanguageMode, setSelected, pulse, destroy, mapPoint };
  };
})(window.ArticulationLab);
