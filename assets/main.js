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
     SOUND (procedural, no audio files)
     ══════════════════════════════════════════════════════════════ */
  const Sound = {
    on: false, ctx: null, gain: null, filter: null,
    noise(seconds, brown) {
      const len = this.ctx.sampleRate * seconds, buf = this.ctx.createBuffer(1, len, this.ctx.sampleRate), d = buf.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0, last = 0;
      for (let i = 0; i < len; i++) {
        const w = Math.random() * 2 - 1;
        if (brown) { last = (last + 0.02 * w) / 1.02; d[i] = last * 3.5; }
        else { b0 = 0.99765 * b0 + w * 0.0990460; b1 = 0.96300 * b1 + w * 0.2965164; b2 = 0.57000 * b2 + w * 1.0526913; d[i] = (b0 + b1 + b2 + w * 0.1848) * 0.11; }
      }
      return buf;
    },
    ensure() {
      if (this.ctx) return;
      const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
      this.ctx = new AC();
      const src = this.ctx.createBufferSource(); src.buffer = this.noise(4); src.loop = true;
      const hp = this.ctx.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 380;
      this.filter = this.ctx.createBiquadFilter(); this.filter.type = 'lowpass'; this.filter.frequency.value = 6000;
      this.gain = this.ctx.createGain(); this.gain.gain.value = 0;
      src.connect(hp).connect(this.filter).connect(this.gain).connect(this.ctx.destination); src.start();
    },
    update() {
      const btn = $('#sound-toggle');
      if (btn) { btn.classList.toggle('on', this.on); btn.innerHTML = this.on ? '<i class="fa-solid fa-volume-high"></i>' : '<i class="fa-solid fa-volume-xmark"></i>'; }
      if (!this.ctx) return;
      const vol = !this.on ? 0 : Rain.mode === 'storm' ? 0.55 : Rain.mode === 'drizzle' ? 0.28 : 0;
      const t = this.ctx.currentTime;
      this.gain.gain.cancelScheduledValues(t); this.gain.gain.setTargetAtTime(vol, t, 0.6);
      this.filter.frequency.setTargetAtTime(Rain.mode === 'storm' ? 9000 : 5200, t, 0.6);
    },
    toggle() {
      this.on = !this.on; this.ensure();
      if (this.ctx && this.ctx.state === 'suspended') this.ctx.resume();
      this.update();
      toast(this.on ? (Rain.mode === 'off' ? 'Sound on. Turn the rain back on to hear it.' : 'Sound on. Headphones recommended.') : 'Sound off.');
    },
    thunder() {
      if (!this.on || !this.ctx) return;
      const t = this.ctx.currentTime, src = this.ctx.createBufferSource(); src.buffer = this.noise(4, true);
      const lp = this.ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 160;
      const g = this.ctx.createGain(); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.9, t + 0.15); g.gain.exponentialRampToValueAtTime(0.001, t + 3.8);
      src.connect(lp).connect(g).connect(this.ctx.destination); src.start(); src.stop(t + 4);
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
      document.body.style.overflow = open ? 'hidden' : '';
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
    Rain.init(); Hero.init(); typewriter(); reveal(); nav(); projects(); cursor(); ripples(); copyEmail(); keys();
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
