window.ArticulationLab = window.ArticulationLab || {};
(function (NS) {
  NS.createSamplePlayer = function createSamplePlayer() {
    let ctx = null;
    let currentSource = null;
    let currentGain = null;
    const arrayBuffers = new Map();
    const decoded = new Map();
    const pending = new Map();

    function getContext() {
      if (!ctx) {
        const AC = window.AudioContext || window.webkitAudioContext;
        if (!AC) return null;
        ctx = new AC();
      }
      return ctx;
    }

    async function fetchBytes(url) {
      if (arrayBuffers.has(url)) return arrayBuffers.get(url).slice(0);
      if (pending.has(url)) return (await pending.get(url)).slice(0);
      const task = fetch(url, { cache: 'force-cache' }).then(async response => {
        if (!response.ok) throw new Error(`Audio asset ${response.status}: ${url}`);
        const data = await response.arrayBuffer();
        arrayBuffers.set(url, data);
        pending.delete(url);
        return data;
      }).catch(err => {
        pending.delete(url);
        throw err;
      });
      pending.set(url, task);
      return (await task).slice(0);
    }

    async function decode(url) {
      if (decoded.has(url)) return decoded.get(url);
      const audioCtx = getContext();
      if (!audioCtx) throw new Error('Web Audio API unavailable');
      const bytes = await fetchBytes(url);
      const buffer = await audioCtx.decodeAudioData(bytes);
      decoded.set(url, buffer);
      return buffer;
    }

    function stop(releaseSeconds = 0.025) {
      if (!ctx || !currentSource) return;
      const source = currentSource;
      const gain = currentGain;
      currentSource = null;
      currentGain = null;
      const now = ctx.currentTime;
      try {
        gain.gain.cancelScheduledValues(now);
        gain.gain.setValueAtTime(Math.max(0.0001, gain.gain.value), now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + releaseSeconds);
        source.stop(now + releaseSeconds + 0.01);
      } catch (_) {
        try { source.stop(); } catch (_) {}
      }
    }

    async function play(url, options = {}) {
      const audioCtx = getContext();
      if (!audioCtx) return false;
      if (audioCtx.state === 'suspended') await audioCtx.resume();
      let buffer;
      try {
        buffer = await decode(url);
      } catch (err) {
        console.warn('Real-voice sample unavailable:', err);
        return false;
      }

      stop(0.018);
      const source = audioCtx.createBufferSource();
      const gain = audioCtx.createGain();
      const now = audioCtx.currentTime + 0.006;
      const level = Math.max(0.03, Math.min(1.0, Number(options.gain) || 0.92));
      const attack = Math.max(0.008, Number(options.attackSeconds) || 0.018);
      const release = Math.max(0.015, Number(options.releaseSeconds) || 0.035);
      source.buffer = buffer;
      source.connect(gain).connect(audioCtx.destination);
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.exponentialRampToValueAtTime(level, now + attack);
      const end = now + buffer.duration;
      const fadeStart = Math.max(now + attack, end - release);
      gain.gain.setValueAtTime(level, fadeStart);
      gain.gain.exponentialRampToValueAtTime(0.0001, end);
      source.start(now);
      source.stop(end + 0.02);
      currentSource = source;
      currentGain = gain;
      source.onended = () => {
        if (currentSource === source) {
          currentSource = null;
          currentGain = null;
        }
      };
      return true;
    }

    async function preload(urls) {
      const unique = [...new Set((urls || []).filter(Boolean))];
      await Promise.allSettled(unique.map(fetchBytes));
      return unique.length;
    }

    return {
      play,
      stop,
      preload,
      hasBuffered(url) { return arrayBuffers.has(url) || decoded.has(url); },
      async decodeAll(urls) {
        const audioCtx = getContext();
        if (!audioCtx) return false;
        if (audioCtx.state === 'suspended') await audioCtx.resume();
        await Promise.allSettled([...new Set(urls || [])].filter(Boolean).map(decode));
        return true;
      }
    };
  };
})(window.ArticulationLab);
