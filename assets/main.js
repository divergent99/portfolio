/* ── Particle canvas ──────────────────────────────────────────── */
(function initParticles() {
  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];

  const resize = () => {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  };
  resize();
  window.addEventListener('resize', resize);

  const COLORS = ['#6366f155','#818cf833','#00ffa322','#3b82f622'];
  class Particle {
    constructor() { this.reset(true); }
    reset(initial) {
      this.x  = Math.random() * W;
      this.y  = initial ? Math.random() * H : H + 4;
      this.r  = Math.random() * 1.5 + .3;
      this.vy = -(Math.random() * .4 + .1);
      this.vx = (Math.random() - .5) * .15;
      this.alpha = Math.random() * .5 + .2;
      this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      if (this.y < -4) this.reset(false);
    }
    draw() {
      ctx.save();
      ctx.globalAlpha = this.alpha;
      ctx.fillStyle   = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  const COUNT = 80;
  for (let i = 0; i < COUNT; i++) particles.push(new Particle());

  (function loop() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach(p => { p.update(); p.draw(); });
    requestAnimationFrame(loop);
  })();
})();

(function initTypewriter() {
  function start() {
    const el = document.getElementById('typewriter-text');
    if (!el) { setTimeout(start, 100); return; }  // ← keep retrying until element exists
    const phrases = [
      'AI Engineer',
      'LangGraph Architect',
      'RAG Pipeline Builder',
      'Multi-Agent Systems',
      'GenAI for Enterprise',
    ];
    let pi = 0, ci = 0, deleting = false;
    const type = () => {
      const phrase = phrases[pi];
      if (!deleting) {
        el.textContent = phrase.slice(0, ci + 1);
        ci++;
        if (ci === phrase.length) { deleting = true; setTimeout(type, 1800); return; }
      } else {
        el.textContent = phrase.slice(0, ci - 1);
        ci--;
        if (ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; }
      }
      setTimeout(type, deleting ? 40 : 70);
    };
    type();
  }
  start();
})();

/* ── Scroll reveal ────────────────────────────────────────────── */
(function initReveal() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);   // reveal once, then stop watching
      }
    });
  }, { threshold: .12 });

  const revealAll = () => {
    document.querySelectorAll('.reveal:not(.visible)').forEach(el => {
      const rect = el.getBoundingClientRect();
      // already in (or above) the viewport → reveal immediately
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        el.classList.add('visible');
      } else {
        observer.observe(el);
      }
    });
  };

  // Keep retrying until Dash has actually rendered the .reveal nodes
  function boot(attempts = 0) {
    const found = document.querySelectorAll('.reveal').length;
    if (found > 0) {
      revealAll();
      // re-scan a couple times in case sections mount slightly later
      setTimeout(revealAll, 400);
      setTimeout(revealAll, 1200);
    } else if (attempts < 60) {       // retry up to ~6s
      setTimeout(() => boot(attempts + 1), 100);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => boot());
  } else {
    boot();
  }
})();
