/* ═══════════════════════════════════════════════════════════════════
   RONIN · interaction layer
   Dash renders the layout client-side, so everything boots once the
   DOM nodes exist (see boot() at the bottom).
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer  = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };

  /* ── Toast ─────────────────────────────────────────────────────── */
  let toastTimer;
  function toast(msg) {
    const el = $('#toast'); if (!el) return;
    el.textContent = msg; el.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('show'), 2600);
  }

  /* ══════════════════════════════════════════════════════════════
     RAIN + LEAVES (canvas)
     ══════════════════════════════════════════════════════════════ */
  // Japanese maple leaf, 7 pointed lobes, ~20 units across
  const MAPLE = new Path2D('M0,-10 L1.6,-4.6 L5.6,-8.2 L4.4,-2.6 L9.8,-3.6 L6.4,0.6 L9.2,3.4 L3.6,2.8 L4.2,6.8 L0.9,4.2 L0,4.6 L-0.9,4.2 L-4.2,6.8 L-3.6,2.8 L-9.2,3.4 L-6.4,0.6 L-9.8,-3.6 L-4.4,-2.6 L-5.6,-8.2 L-1.6,-4.6 Z');
  const MODES = ['drizzle', 'storm', 'off'];
  const Rain = {
    mode: store.get('ronin-rain', reduceMotion ? 'off' : 'drizzle'),
    drops: [], splashes: [], leaves: [],
    wind: -0.6, windTarget: -0.6, W: 0, H: 0, dpr: 1, ctx: null, canvas: null, running: false,

    init() {
      this.canvas = $('#rain'); if (!this.canvas) return;
      this.ctx = this.canvas.getContext('2d');
      this.resize(); window.addEventListener('resize', () => this.resize());
      window.addEventListener('pointermove', e => {
        const max = this.mode === 'storm' ? 3.2 : 1.4;
        this.windTarget = -0.6 + ((e.clientX / this.W) - 0.5) * 2 * max;
      }, { passive: true });
      window.addEventListener('deviceorientation', e => {
        if (e.gamma == null) return;
        this.windTarget = -0.6 + clamp(e.gamma / 30, -1, 1) * 2.2;
      }, { passive: true });
      document.addEventListener('visibilitychange', () => { if (!document.hidden) this.start(); });
      this.setMode(this.mode, true);
    },

    resize() {
      this.dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      this.W = window.innerWidth; this.H = window.innerHeight;
      this.canvas.width = this.W * this.dpr; this.canvas.height = this.H * this.dpr;
      this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
      this.populate();
    },

    target() {
      const area = clamp((this.W * this.H) / (1440 * 900), 0.35, 1.6);
      return Math.round((this.mode === 'storm' ? 420 : this.mode === 'drizzle' ? 150 : 0) * area);
    },

    newDrop(initial) {
      const z = Math.random() * 0.7 + 0.3;           // depth: far drops are thin, slow, faint
      return {
        x: Math.random() * (this.W + 200) - 100,
        y: initial ? Math.random() * this.H : -Math.random() * 120 - 20,
        z, len: (this.mode === 'storm' ? 22 : 14) * z + Math.random() * 8,
        v: (this.mode === 'storm' ? 15 : 9) * z + Math.random() * 3,
      };
    },

    newLeaf(burst) {
      return {
        x: Math.random() * this.W, y: burst ? -Math.random() * this.H * 0.6 : -30,
        s: Math.random() * 7 + 7, r: Math.random() * Math.PI * 2, vr: (Math.random() - 0.5) * 0.04,
        vy: Math.random() * 0.6 + 0.5, sway: Math.random() * Math.PI * 2, swayV: Math.random() * 0.02 + 0.01,
        hue: Math.random() < 0.8 ? '212,64,47' : '226,120,52',
      };
    },

    populate() {
      const n = this.target();
      while (this.drops.length < n) this.drops.push(this.newDrop(true));
      this.drops.length = n;
      const leaves = this.mode === 'off' ? 0 : (this.W < 760 ? 3 : 6);
      while (this.leaves.length < leaves) this.leaves.push(this.newLeaf(true));
      this.leaves.length = leaves;
    },

    setMode(mode, silent) {
      this.mode = mode; store.set('ronin-rain', mode);
      this.populate();
      const btn = $('#rain-toggle');
      if (btn) {
        btn.classList.toggle('on', mode !== 'off');
        btn.innerHTML = mode === 'storm' ? '<i class="fa-solid fa-cloud-bolt"></i>'
                      : mode === 'drizzle' ? '<i class="fa-solid fa-cloud-rain"></i>'
                      : '<i class="fa-solid fa-cloud"></i>';
      }
      Storm.schedule();
      Sound.update();
      if (!silent) toast(mode === 'storm' ? 'Storm. Good weather for shipping.' : mode === 'drizzle' ? 'Drizzle. Lantern stays lit.' : 'Rain stopped. Rare in these parts.');
      this.start();
    },

    cycle() { this.setMode(MODES[(MODES.indexOf(this.mode) + 1) % MODES.length]); },

    burst(n) { for (let i = 0; i < n; i++) this.leaves.push(this.newLeaf(true)); this.start(); },

    start() { if (!this.running && !document.hidden) { this.running = true; requestAnimationFrame(t => this.frame(t)); } },

    drawLeaf(l) {
      const c = this.ctx, s = l.s;
      c.save(); c.translate(l.x, l.y); c.rotate(l.r); c.scale(1, Math.cos(l.sway * 2) * 0.35 + 0.65);
      c.fillStyle = `rgba(${l.hue},.85)`;
      c.scale(s / 10, s / 10);
      c.fill(MAPLE);
      c.strokeStyle = `rgba(${l.hue},.9)`; c.lineWidth = 1;
      c.lineWidth = 0.8; c.beginPath(); c.moveTo(0, 3); c.lineTo(0, 11); c.stroke();
      c.restore();
    },

    frame() {
      const c = this.ctx;
      if (document.hidden) { this.running = false; return; }
      if (document.body.classList.contains('menu-open')) { requestAnimationFrame(() => this.frame()); return; }
      c.clearRect(0, 0, this.W, this.H);
      this.wind = lerp(this.wind, this.windTarget, 0.03);

      // rain
      c.lineCap = 'round';
      for (const d of this.drops) {
        d.y += d.v; d.x += this.wind * d.z * 1.2;
        if (d.y > this.H) {
          if (d.z > 0.75 && Math.random() < 0.5 && this.splashes.length < 160) {
            for (let k = 0; k < 2; k++) this.splashes.push({ x: d.x, y: this.H - 2, vx: (Math.random() - 0.5) * 2.4, vy: -Math.random() * 2.4 - 1, life: 1 });
          }
          Object.assign(d, this.newDrop(false));
        }
        if (d.x > this.W + 120) d.x = -100; else if (d.x < -120) d.x = this.W + 100;
        c.strokeStyle = `rgba(178,198,228,${0.12 + d.z * 0.32})`;
        c.lineWidth = d.z * 1.15;
        c.beginPath(); c.moveTo(d.x, d.y); c.lineTo(d.x + this.wind * d.len * 0.12, d.y + d.len); c.stroke();
      }

      // splashes
      for (let i = this.splashes.length - 1; i >= 0; i--) {
        const s = this.splashes[i];
        s.x += s.vx; s.y += s.vy; s.vy += 0.18; s.life -= 0.04;
        if (s.life <= 0) { this.splashes.splice(i, 1); continue; }
        c.fillStyle = `rgba(190,208,235,${s.life * 0.5})`;
        c.fillRect(s.x, s.y, 1.4, 1.4);
      }

      // leaves
      for (let i = this.leaves.length - 1; i >= 0; i--) {
        const l = this.leaves[i];
        l.sway += l.swayV; l.r += l.vr;
        l.y += l.vy * (this.mode === 'storm' ? 1.8 : 1);
        l.x += Math.sin(l.sway) * 0.8 + this.wind * 0.35;
        this.drawLeaf(l);
        if (l.y > this.H + 30 || l.x < -60 || l.x > this.W + 60) {
          const base = this.mode === 'off' ? 0 : (this.W < 760 ? 3 : 6);
          if (this.leaves.length > base) this.leaves.splice(i, 1); else Object.assign(l, this.newLeaf(false));
        }
      }

      if (!this.drops.length && !this.leaves.length && !this.splashes.length) { this.running = false; c.clearRect(0, 0, this.W, this.H); return; }
      requestAnimationFrame(() => this.frame());
    },
  };

  /* ── Lightning ─────────────────────────────────────────────────── */
  const Storm = {
    timer: null,
    schedule() {
      clearTimeout(this.timer);
      if (Rain.mode !== 'storm' || reduceMotion) return;
      this.timer = setTimeout(() => { this.strike(); this.schedule(); }, 8000 + Math.random() * 14000);
    },
    strike() {
      const f = $('#flash'); if (!f || document.hidden) return;
      f.classList.remove('strike'); void f.offsetWidth; f.classList.add('strike');
      setTimeout(() => Sound.thunder(), 300 + Math.random() * 900);
    },
  };

  /* ══════════════════════════════════════════════════════════════
     SOUND · layered procedural rain (no audio files)
       wash    : stereo pink noise, the distant "shhh" of rain on a forest
       patter  : pre-rendered buffers of thousands of tiny droplet ticks
       body    : brown-noise low end, heavier in storms
       drops   : real-time Minnaert bubble chirps + leaf splats, panned
       eaves   : a steady drip from the shrine roof, just to your right
       space   : generated stereo reverb so it all sits outdoors
     ══════════════════════════════════════════════════════════════ */
  const Sound = {
    on: false, ctx: null, timer: null, next: {},
    LEVELS: {
      drizzle: { wash: 0.48, light: 0.85, heavy: 0.00, body: 0.16, hp: 700, lp: 6500, bubbles: 2.5, splats: 7, eaves: true },
      storm:   { wash: 0.55, light: 0.25, heavy: 0.75, body: 0.40, hp: 400, lp: 10000, bubbles: 6, splats: 22, eaves: true },
      off:     { wash: 0, light: 0, heavy: 0, body: 0, hp: 700, lp: 6500, bubbles: 0, splats: 0, eaves: false },
    },

    /* ── buffers ── */
    stereo(seconds, fill) {
      const sr = this.ctx.sampleRate, len = Math.floor(sr * seconds), buf = this.ctx.createBuffer(2, len, sr);
      for (let ch = 0; ch < 2; ch++) fill(buf.getChannelData(ch), sr, ch);
      return buf;
    },
    pink(d) {
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
      for (let i = 0; i < d.length; i++) {
        const w = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + w * 0.0555179; b1 = 0.99332 * b1 + w * 0.0750759; b2 = 0.96900 * b2 + w * 0.1538520;
        b3 = 0.86650 * b3 + w * 0.3104856; b4 = 0.55000 * b4 + w * 0.5329522; b5 = -0.7616 * b5 - w * 0.0168980;
        d[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + w * 0.5362) * 0.11; b6 = w * 0.115926;
      }
    },
    brown(d) { let l = 0; for (let i = 0; i < d.length; i++) { l = (l + 0.02 * (Math.random() * 2 - 1)) / 1.02; d[i] = l * 3.5; } },
    // Thousands of 1-5 ms droplet ticks, exponential loudness so a few stand out
    patter(rate) {
      return this.stereo(8, (d, sr, ch) => {
        const n = Math.floor(rate * 8);
        for (let k = 0; k < n; k++) {
          const at = Math.floor(Math.random() * d.length), dur = Math.floor(sr * (0.001 + Math.random() * 0.004));
          const amp = Math.min(1, -Math.log(Math.random()) * 0.12) * (Math.random() < 0.5 ? 1 : 0.35);
          const tone = 0.3 + Math.random() * 0.6;
          let prev = 0;
          for (let j = 0; j < dur && at + j < d.length; j++) {
            const env = Math.exp(-j / (dur * 0.25));
            const w = Math.random() * 2 - 1; prev = prev * tone + w * (1 - tone);   // per-drop timbre
            d[at + j] += (w - prev) * amp * env;
          }
        }
      });
    },
    impulse(seconds) {
      return this.stereo(seconds, (d, sr) => {
        let lp = 0;
        for (let i = 0; i < d.length; i++) {
          const t = i / d.length; lp = lp * 0.6 + (Math.random() * 2 - 1) * 0.4;
          d[i] = lp * Math.pow(1 - t, 3.2) * (i < sr * 0.012 ? i / (sr * 0.012) : 1);
        }
      });
    },

    loop(buf, ...chain) {
      const src = this.ctx.createBufferSource(); src.buffer = buf; src.loop = true;
      src.loopStart = 0; src.start(0, Math.random() * buf.duration);
      chain.reduce((n, m) => (n.connect(m), m), src);
      return src;
    },
    filter(type, f, q) { const b = this.ctx.createBiquadFilter(); b.type = type; b.frequency.value = f; if (q) b.Q.value = q; return b; },
    gain(v) { const g = this.ctx.createGain(); g.gain.value = v; return g; },

    ensure() {
      if (this.ctx) return;
      const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
      const c = this.ctx = new AC();

      const comp = c.createDynamicsCompressor(); comp.threshold.value = -14; comp.ratio.value = 3;
      this.master = this.gain(0); this.master.connect(comp).connect(c.destination);
      this.dry = this.gain(1); this.dry.connect(this.master);
      const verb = c.createConvolver(); verb.buffer = this.impulse(2.6);
      this.send = this.gain(1); this.send.connect(verb).connect(this.gain(0.35)).connect(this.master);

      // wash
      this.washHP = this.filter('highpass', 700); this.washLP = this.filter('lowpass', 6500);
      this.washG = this.gain(0); this.gust = this.gain(1);
      this.loop(this.stereo(7, d => this.pink(d)), this.washHP, this.washLP, this.washG, this.gust, this.dry);
      this.gust.connect(this.send);

      // patter
      const tickHP = this.filter('highpass', 1400), tickPeak = this.filter('peaking', 4200, 0.8); tickPeak.gain.value = 4;
      tickHP.connect(tickPeak).connect(this.dry); tickPeak.connect(this.send);
      this.lightG = this.gain(0); this.heavyG = this.gain(0);
      this.loop(this.patter(260), this.lightG, tickHP);
      this.loop(this.patter(1100), this.heavyG, tickHP);

      // body
      this.bodyG = this.gain(0);
      this.loop(this.stereo(6, d => this.brown(d)), this.filter('lowpass', 380), this.bodyG, this.dry);

      // shared short noise for splats
      this.splatBuf = this.stereo(0.05, d => { for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; });
      this.eavesPitch = 820 + Math.random() * 300;
    },

    /* ── one-shot events ── */
    pan(v) { const p = this.ctx.createStereoPanner ? this.ctx.createStereoPanner() : this.gain(1); if (p.pan) p.pan.value = v; return p; },
    bubble(t, f0, amp, pan, wet) {
      const c = this.ctx, o = c.createOscillator(), g = this.gain(0), p = this.pan(pan), dur = 0.018 + Math.random() * 0.03;
      o.type = 'sine'; o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(f0 * (1.4 + Math.random() * 0.6), t + dur);
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(amp, t + 0.0015); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g).connect(p).connect(this.dry); if (wet) p.connect(this.send);
      o.start(t); o.stop(t + dur + 0.02);
    },
    splat(t, amp, pan) {
      const s = this.ctx.createBufferSource(), bp = this.filter('bandpass', 900 + Math.random() * 2600, 1.2 + Math.random() * 2);
      const g = this.gain(0), p = this.pan(pan), dur = 0.006 + Math.random() * 0.02;
      s.buffer = this.splatBuf; g.gain.setValueAtTime(amp, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      s.connect(bp).connect(g).connect(p).connect(this.dry); p.connect(this.send);
      s.start(t, Math.random() * 0.02, dur + 0.01);
    },
    gustNow(t) {
      const L = this.LEVELS[Rain.mode]; if (!L.wash) return;
      const v = 0.75 + Math.random() * 0.5, len = 1.5 + Math.random() * 4;
      this.gust.gain.setTargetAtTime(v, t, len / 3);
      this.washLP.frequency.setTargetAtTime(L.lp * (0.8 + Math.random() * 0.35), t, len / 3);
    },

    schedule() {
      const c = this.ctx, L = this.LEVELS[Rain.mode], now = c.currentTime, ahead = now + 0.15;
      const exp = r => -Math.log(1 - Math.random()) / r;   // Poisson inter-arrival
      const n = this.next;
      if (L.bubbles) { n.b = Math.max(n.b || 0, now); while (n.b < ahead) { this.bubble(n.b, 1100 + Math.random() * 3200, 0.02 + Math.random() * 0.05, Math.random() * 1.8 - 0.9, true); n.b += exp(L.bubbles); } }
      if (L.splats)  { n.s = Math.max(n.s || 0, now); while (n.s < ahead) { this.splat(n.s, 0.04 + Math.random() * 0.14, Math.random() * 2 - 1); n.s += exp(L.splats); } }
      if (L.eaves)   { n.e = Math.max(n.e || 0, now); while (n.e < ahead) {
        const t = n.e; this.bubble(t, this.eavesPitch * (0.94 + Math.random() * 0.12), 0.09, 0.55, true);
        if (Math.random() < 0.6) this.splat(t + 0.004, 0.08, 0.55);
        n.e += (Rain.mode === 'storm' ? 0.45 : 0.9) + Math.random() * 0.7; } }
      n.g = Math.max(n.g || 0, now); if (n.g < ahead) { this.gustNow(n.g); n.g += 2 + Math.random() * 5; }
    },

    update() {
      const btn = $('#sound-toggle');
      if (btn) { btn.classList.toggle('on', this.on); btn.innerHTML = this.on ? '<i class="fa-solid fa-volume-high"></i>' : '<i class="fa-solid fa-volume-xmark"></i>'; }
      if (!this.ctx) return;
      const L = this.LEVELS[Rain.mode], t = this.ctx.currentTime, k = 1.2;
      this.master.gain.setTargetAtTime(this.on ? 0.9 : 0, t, 0.5);
      this.washG.gain.setTargetAtTime(L.wash, t, k); this.lightG.gain.setTargetAtTime(L.light, t, k);
      this.heavyG.gain.setTargetAtTime(L.heavy, t, k); this.bodyG.gain.setTargetAtTime(L.body, t, k);
      this.washHP.frequency.setTargetAtTime(L.hp, t, k); this.washLP.frequency.setTargetAtTime(L.lp, t, k);
      clearInterval(this.timer); this.timer = null;
      if (this.on && Rain.mode !== 'off') this.timer = setInterval(() => { if (!document.hidden) this.schedule(); }, 40);
    },
    toggle() {
      this.on = !this.on; this.ensure();
      if (this.ctx && this.ctx.state === 'suspended') this.ctx.resume();
      this.update();
      toast(this.on ? (Rain.mode === 'off' ? 'Sound on. Turn the rain back on to hear it.' : 'Sound on. Headphones recommended.') : 'Sound off.');
    },
    thunder() {
      if (!this.on || !this.ctx) return;
      const c = this.ctx, t = c.currentTime + 0.05, near = Math.random() < 0.4;
      // crack: bright, short, only for close strikes
      if (near) {
        const s = c.createBufferSource(); s.buffer = this.stereo(0.4, d => { for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / d.length, 2); });
        const g = this.gain(0.5); s.connect(this.filter('highpass', 1800)).connect(g); g.connect(this.dry); g.connect(this.send); s.start(t);
      }
      // rumble: brown noise with a few rolling swells, mostly reverb
      const dur = 5 + Math.random() * 3, s = c.createBufferSource(); s.buffer = this.stereo(dur, d => this.brown(d));
      const lp = this.filter('lowpass', near ? 260 : 150), g = this.gain(0);
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(near ? 1.1 : 0.7, t + (near ? 0.12 : 0.6));
      let tt = t + 0.8;
      while (tt < t + dur - 1.5) { g.gain.linearRampToValueAtTime(0.25 + Math.random() * 0.6, tt); tt += 0.4 + Math.random() * 0.9; }
      g.gain.exponentialRampToValueAtTime(0.001, t + dur);
      s.connect(lp).connect(g); g.connect(this.dry); g.connect(this.send); s.start(t); s.stop(t + dur);
    },
  };

  /* ══════════════════════════════════════════════════════════════
     HERO: parallax + lantern glow pinned to the painted lantern
     ══════════════════════════════════════════════════════════════ */
  const Hero = {
    px: 0, py: 0, tx: 0, ty: 0,
    init() {
      this.bg = $('#hero-bg'); this.img = $('#hero-img'); this.glow = $('#lantern-glow'); this.hero = $('#hero');
      if (!this.img) return;
      const place = () => this.placeGlow();
      if (this.img.complete) place(); else this.img.addEventListener('load', place);
      window.addEventListener('resize', place);
      if (finePointer && !reduceMotion) {
        this.hero.addEventListener('pointermove', e => {
          this.tx = (e.clientX / window.innerWidth - 0.5); this.ty = (e.clientY / window.innerHeight - 0.5);
        });
      }
      const loop = () => {
        this.px = lerp(this.px, this.tx, 0.06); this.py = lerp(this.py, this.ty, 0.06);
        const sy = window.scrollY;
        if (sy < window.innerHeight * 1.2 && !reduceMotion) {
          this.bg.style.transform = `translate3d(${this.px * -16}px, ${sy * 0.28 + this.py * -10}px, 0) scale(1.02)`;
        }
        requestAnimationFrame(loop);
      };
      loop();
    },
    // Map the lantern's position in the source painting onto the object-fit: cover image.
    placeGlow() {
      const img = this.img, g = this.glow; if (!img.naturalWidth || !g) return;
      const mobile = (img.currentSrc || '').includes('mobile');
      const fx = mobile ? 0.503 : 0.712, fy = 0.31, lanternW = mobile ? 0.134 : 0.078;
      const W = img.clientWidth, H = img.clientHeight, iw = img.naturalWidth, ih = img.naturalHeight;
      const s = Math.max(W / iw, H / ih);
      const pos = getComputedStyle(img).objectPosition.split(' ').map(v => parseFloat(v) / 100);
      const dx = (W - iw * s) * (pos[0] || 0.5), dy = (H - ih * s) * (pos[1] || 0.5);
      const size = clamp(lanternW * iw * s * 3.2, 160, 520);
      Object.assign(g.style, {
        left: `${dx + fx * iw * s}px`, top: `${dy + fy * ih * s}px`,
        width: `${size}px`, height: `${size}px`, marginLeft: `${-size / 2}px`, marginTop: `${-size / 2}px`,
      });
    },
  };

  /* ── Typewriter ────────────────────────────────────────────────── */
  function typewriter() {
    const el = $('#typewriter-text'); if (!el) return;
    const phrases = ['AI Engineer', 'LangGraph Architect', 'RAG Pipeline Smith', 'Multi-Agent Wrangler', 'Production ML Person', 'Hackathon Ronin'];
    if (reduceMotion) { el.textContent = phrases[0]; return; }
    let pi = 0, ci = 0, del = false;
    (function type() {
      const p = phrases[pi];
      el.textContent = p.slice(0, del ? --ci : ++ci);
      let wait = del ? 34 : 64 + Math.random() * 40;
      if (!del && ci === p.length) { del = true; wait = 1900; }
      else if (del && ci === 0) { del = false; pi = (pi + 1) % phrases.length; wait = 350; }
      setTimeout(type, wait);
    })();
  }

  /* ── Count-up ──────────────────────────────────────────────────── */
  function countUp(el) {
    const target = +el.dataset.count, suf = el.dataset.suffix || '', pre = el.dataset.prefix || '';
    if (reduceMotion) return;
    const t0 = performance.now(), dur = 1500;
    (function tick(t) {
      const k = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - k, 3);
      el.textContent = pre + Math.round(target * e) + suf;
      if (k < 1) requestAnimationFrame(tick);
    })(t0);
  }

  /* ── Scroll reveal (with sibling stagger) ──────────────────────── */
  function reveal() {
    const els = $$('.reveal');
    const groups = new Map();
    els.forEach(el => {
      const p = el.parentElement, i = groups.get(p) || 0; groups.set(p, i + 1);
      el.style.setProperty('--d', `${(i % 6) * 0.07}s`);
    });
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target; el.classList.add('visible'); io.unobserve(el);
        $$('[data-count]', el).forEach(countUp);
        if (el.classList.contains('skill-cat')) lightChips(el);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach(el => io.observe(el));
  }

  // Chips flash their brand colour in sequence when a category scrolls in
  function lightChips(cat) {
    if (reduceMotion) return;
    $$('.skill-chip', cat).forEach((chip, i) => {
      setTimeout(() => { chip.classList.add('flash'); setTimeout(() => chip.classList.remove('flash'), 900); }, 300 + i * 90);
    });
  }

  /* ── Nav: scrolled state, active link, progress, mobile menu ──── */
  function nav() {
    const bar = $('#navbar'), prog = $('#progress'), rain = $('#rain');
    const onScroll = () => {
      const y = window.scrollY, max = document.documentElement.scrollHeight - window.innerHeight;
      bar.classList.toggle('scrolled', y > 30);
      prog.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
      if (rain) rain.style.opacity = y > window.innerHeight * 0.8 ? '0.45' : '1';
    };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

    const links = $$('[data-nav]');
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) links.forEach(a => a.classList.toggle('active', a.dataset.nav === e.target.id));
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.forEach(a => { const s = document.getElementById(a.dataset.nav); if (s) io.observe(s); });

    const burger = $('#burger');
    const setMenu = open => {
      document.body.classList.toggle('menu-open', open);
      burger.setAttribute('aria-expanded', String(open));
      document.documentElement.style.overflow = open ? 'hidden' : '';
    };
    burger.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
    $$('#mobile-menu a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
    window.addEventListener('resize', () => { if (window.innerWidth > 860) setMenu(false); });
  }

  /* ── Projects: filter, live toggle, show more ──────────────────── */
  function projects() {
    const cards = $$('.project-card'), btns = $$('.filter-btn'), more = $('#show-more'), live = $('#live-toggle'), empty = $('#projects-empty');
    if (!cards.length) return;
    const LIMIT = () => (window.innerWidth < 760 ? 4 : 6);
    const st = { filter: 'all', live: false, expanded: false };

    function apply(animate) {
      const matches = cards.filter(c => (st.filter === 'all' || c.dataset.tags.split(' ').includes(st.filter)) && (!st.live || c.dataset.live === '1'));
      const capped = st.filter === 'all' && !st.live && !st.expanded;
      cards.forEach(c => {
        const idx = matches.indexOf(c), show = idx !== -1 && (!capped || idx < LIMIT());
        const wasHidden = c.classList.contains('hide');
        c.classList.toggle('hide', !show);
        if (show && wasHidden && animate) {
          c.classList.add('visible'); c.classList.remove('pop'); void c.offsetWidth;
          c.style.animationDelay = `${Math.min(idx, 8) * 0.04}s`; c.classList.add('pop');
        }
      });
      const canMore = st.filter === 'all' && !st.live && matches.length > LIMIT();
      more.classList.toggle('gone', !canMore);
      more.classList.toggle('open', st.expanded);
      $('.more-label', more).textContent = st.expanded ? 'Sheathe' : `Unsheathe all ${matches.length}`;
      empty.classList.toggle('show', matches.length === 0);
    }

    btns.forEach(b => b.addEventListener('click', () => {
      btns.forEach(x => x.classList.toggle('active', x === b));
      st.filter = b.dataset.filter; apply(true);
    }));
    live.addEventListener('click', e => {
      e.preventDefault(); st.live = !st.live; live.dataset.on = st.live ? '1' : '0'; apply(true);
    });
    more.addEventListener('click', () => {
      st.expanded = !st.expanded; apply(true);
      if (!st.expanded) $('#projects').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
    });
    let lastLimit = LIMIT();
    window.addEventListener('resize', () => { if (LIMIT() !== lastLimit) { lastLimit = LIMIT(); apply(false); } });
    apply(false);

    // tilt + lantern spotlight on cards
    if (finePointer && !reduceMotion) {
      cards.forEach(c => {
        c.addEventListener('pointermove', e => {
          const r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
          c.style.setProperty('--mx', `${x * 100}%`); c.style.setProperty('--my', `${y * 100}%`);
          c.style.setProperty('--ry', `${(x - 0.5) * 7}deg`); c.style.setProperty('--rx', `${(0.5 - y) * 7}deg`);
        });
        c.addEventListener('pointerleave', () => { c.style.setProperty('--rx', '0deg'); c.style.setProperty('--ry', '0deg'); });
      });
    }
  }

  /* ── Lantern cursor + ink ripples ──────────────────────────────── */
  function cursor() {
    if (!finePointer || reduceMotion) return;
    const el = $('#lantern-cursor'); let x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y;
    window.addEventListener('pointermove', e => { x = e.clientX; y = e.clientY; document.body.classList.add('has-pointer'); }, { passive: true });
    document.addEventListener('pointerleave', () => document.body.classList.remove('has-pointer'));
    (function loop() { cx = lerp(cx, x, 0.12); cy = lerp(cy, y, 0.12); el.style.transform = `translate3d(${cx}px, ${cy}px, 0)`; requestAnimationFrame(loop); })();
  }
  function ripples() {
    if (reduceMotion) return;
    document.addEventListener('pointerdown', e => {
      if (e.target.closest('a, button, label, input')) return;
      const r = document.createElement('span'); r.className = 'ink-ripple';
      r.style.left = `${e.clientX}px`; r.style.top = `${e.clientY}px`;
      document.body.appendChild(r); setTimeout(() => r.remove(), 1000);
    });
  }

  /* ── Copy email ────────────────────────────────────────────────── */
  function copyEmail() {
    const b = $('#copy-email'); if (!b) return;
    b.addEventListener('click', async () => {
      const v = b.dataset.copy;
      try { await navigator.clipboard.writeText(v); }
      catch (e) { const t = document.createElement('textarea'); t.value = v; document.body.appendChild(t); t.select(); document.execCommand('copy'); t.remove(); }
      toast('Email copied. The crow is on its way.');
    });
  }

  /* ── Architecture graphs: hover a node to trace its upstream + downstream ── */
  function archGraphs() {
    $$('svg.arch').forEach(svg => {
      const edges = $$('.edge', svg), nodes = $$('.node', svg);
      const walk = (start, dir) => {          // dir: 'to' = downstream, 'from' = upstream
        const seen = new Set([start]), lit = new Set(), q = [start];
        while (q.length) {
          const n = q.shift();
          edges.forEach(e => {
            const a = e.dataset.from, b = e.dataset.to, [here, there] = dir === 'to' ? [a, b] : [b, a];
            if (here === n && !e.classList.contains('dashed')) { lit.add(e); if (!seen.has(there)) { seen.add(there); q.push(there); } }
          });
        }
        return [seen, lit];
      };
      const trace = node => {
        const k = node.dataset.node, [d1, e1] = walk(k, 'to'), [d2, e2] = walk(k, 'from');
        svg.classList.add('tracing');
        nodes.forEach(n => n.classList.toggle('lit', d1.has(n.dataset.node) || d2.has(n.dataset.node)));
        edges.forEach(e => e.classList.toggle('lit', e1.has(e) || e2.has(e)));
      };
      const clear = () => { svg.classList.remove('tracing'); $$('.lit', svg).forEach(x => x.classList.remove('lit')); };
      nodes.forEach(n => {
        n.addEventListener('pointerenter', () => trace(n));
        n.addEventListener('focus', () => trace(n));
        n.addEventListener('click', () => (n.classList.contains('lit') && svg.classList.contains('tracing') ? clear() : trace(n)));
        n.addEventListener('blur', clear);
      });
      svg.addEventListener('pointerleave', clear);
    });
  }

  /* ── Case-study terminal: types itself out when scrolled into view, then loops ── */
  function terminals() {
    $$('.tterm').forEach(term => {
      const lines = $$('.tline', term);
      if (reduceMotion) { lines.forEach(l => l.classList.add('typed')); return; }
      let running = false;
      const run = async () => {
        if (running) return; running = true;
        const wait = ms => new Promise(r => setTimeout(r, ms));
        while (true) {
          lines.forEach(l => { l.classList.remove('typed', 'typing'); l.textContent = ''; });
          for (const l of lines) {
            const text = l.dataset.text, isSql = l.classList.contains('t-sql');
            l.classList.add('typing');
            for (let i = 1; i <= text.length; i++) { l.textContent = text.slice(0, i); await wait(isSql ? 14 : 28); }
            l.classList.remove('typing'); l.classList.add('typed');
            await wait(l.classList.contains('t-q') ? 500 : 220);
          }
          await wait(4200);
        }
      };
      new IntersectionObserver((es, io) => { if (es[0].isIntersecting) { run(); io.disconnect(); } }, { threshold: 0.4 }).observe(term);
    });
  }

  /* ── LinkedIn posts: lazy iframes at full height, clipped + "Read more", carousel arrows ── */
  function posts() {
    const track = $('#posts-track'); if (!track) return;
    const frames = $$('.post-frame', track);
    // LinkedIn's height is for a 504px-wide embed; narrower cards reflow taller, so scale up with some slack
    const fullHeight = f => Math.round(+f.dataset.h * (1 + (Math.max(1, 504 / f.clientWidth) - 1) * 0.6) + 60);
    const load = f => {
      if (f.querySelector('iframe')) return;
      const i = document.createElement('iframe');
      i.src = f.dataset.src; i.title = 'LinkedIn post'; i.loading = 'lazy'; i.allowFullscreen = true;
      i.setAttribute('scrolling', 'no');
      i.style.height = `${fullHeight(f)}px`;
      i.addEventListener('load', () => f.classList.add('loaded'));
      f.appendChild(i);
    };
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { load(e.target); io.unobserve(e.target); } }),
      { rootMargin: '400px 600px' });
    frames.forEach(f => io.observe(f));

    $$('.post-card', track).forEach(card => {
      const btn = $('.post-more', card), f = $('.post-frame', card);
      btn.addEventListener('click', () => {
        const open = !card.classList.contains('expanded');
        card.classList.toggle('expanded', open);
        load(f);
        f.style.height = open ? `${(f.querySelector('iframe')?.offsetHeight) || fullHeight(f)}px` : '';
        $('.rm-label', card).textContent = open ? 'Show less' : 'Read more';
        if (!open) card.scrollIntoView({ block: 'nearest', behavior: reduceMotion ? 'auto' : 'smooth' });
      });
    });
    window.addEventListener('resize', () => frames.forEach(f => {
      const i = f.querySelector('iframe'); if (i) i.style.height = `${fullHeight(f)}px`;
      if (f.closest('.post-card').classList.contains('expanded') && i) f.style.height = i.style.height;
    }));

    const prev = $('#posts-prev'), next = $('#posts-next');
    const step = () => (track.querySelector('.post-card')?.getBoundingClientRect().width || 400) + 18;
    const sync = () => {
      const end = track.scrollLeft + track.clientWidth >= track.scrollWidth - 8;
      prev.disabled = track.scrollLeft < 8; next.disabled = end;
      track.classList.toggle('at-end', end);
    };
    prev.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
    next.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
    track.addEventListener('scroll', sync, { passive: true }); window.addEventListener('resize', sync); sync();
  }

  /* ── Keys + easter egg ─────────────────────────────────────────── */
  function keys() {
    let buf = '';
    document.addEventListener('keydown', e => {
      if (e.metaKey || e.ctrlKey || e.altKey || /input|textarea/i.test(e.target.tagName)) return;
      const k = e.key.toLowerCase();
      buf = (buf + k).slice(-7);
      if (buf === 'bushido') {
        Rain.setMode('storm', true); Rain.burst(36); Storm.strike();
        toast('義 勇 仁 礼 誠 名誉 忠義. Storm mode unlocked.'); buf = ''; return;
      }
      if (k === 'r') Rain.cycle();
      if (k === 's') Sound.toggle();
    });
    $('#rain-toggle').addEventListener('click', () => Rain.cycle());
    $('#sound-toggle').addEventListener('click', () => Sound.toggle());
  }

  /* ── Boot once Dash has mounted the layout ─────────────────────── */
  let booted = false;
  function boot() {
    if (booted || !$('#hero-img') || !$('.site-footer')) return false;
    booted = true;
    Rain.init(); Hero.init(); typewriter(); reveal(); nav(); projects(); cursor(); ripples(); copyEmail(); archGraphs(); terminals(); posts(); keys();
    console.log('%c浪人 %cYou opened the console. Respect.\nType "bushido" on the page for weather.',
      'color:#d4402f;font:800 20px serif', 'color:#e9e4d8;font:12px monospace');
    return true;
  }
  if (!boot()) {
    const mo = new MutationObserver(() => { if (boot()) mo.disconnect(); });
    const watch = () => mo.observe(document.body, { childList: true, subtree: true });
    if (document.body) watch(); else document.addEventListener('DOMContentLoaded', () => { if (!boot()) watch(); });
  }
})();
