/* Motion for the v2 pages.
 *
 * Design rule: nothing here may ever leave content invisible. The CSS
 * hidden states are gated behind the .js class this file sets, so if the
 * script never runs the page renders fully. A 2s timer force-reveals
 * everything regardless of what the observer did. */
(function () {
  'use strict';

  var reduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var root = document.documentElement;
  if (!reduced) root.classList.add('js');

  function revealAll() {
    var els = document.querySelectorAll('.reveal');
    for (var i = 0; i < els.length; i++) els[i].classList.add('in');
  }

  document.addEventListener('DOMContentLoaded', function () {

    /* —— Scroll reveal —— */
    if (reduced || !('IntersectionObserver' in window)) {
      revealAll();
    } else {
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add('in');
            obs.unobserve(e.target);
          }
        });
      }, { rootMargin: '400px 0px 400px 0px', threshold: 0 });

      var targets = document.querySelectorAll('.reveal');
      for (var i = 0; i < targets.length; i++) obs.observe(targets[i]);

      // Backstop. If anything above misbehaves, the page still shows.
      setTimeout(revealAll, 2000);
    }

    /* —— Nav condense —— */
    var nav = document.querySelector('nav');
    if (nav) {
      var onScroll = function () {
        nav.classList.toggle('scrolled', window.scrollY > 24);
      };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
    }

    /* —— Reading progress, blog posts only —— */
    var article = document.querySelector('.post-wrap');
    if (article && !reduced) {
      var bar = document.createElement('div');
      bar.className = 'progress';
      document.body.appendChild(bar);

      var track = function () {
        var top = article.offsetTop;
        var span = article.offsetHeight - window.innerHeight;
        var done = span > 0 ? (window.scrollY - top) / span : 0;
        bar.style.width = Math.max(0, Math.min(1, done)) * 100 + '%';
      };
      track();
      window.addEventListener('scroll', track, { passive: true });
      window.addEventListener('resize', track);
    }

    if (reduced) return;

    /* —— Count up the hero stats ——
       The final value is already in the HTML, so a failure here leaves
       the correct number on screen rather than a zero. */
    var stats = document.querySelectorAll('.hero-stat-num');
    for (var s = 0; s < stats.length; s++) {
      (function (el) {
        var full = el.textContent.trim();
        var digits = full.match(/[\d.]+/);
        if (!digits) return;

        var target = parseFloat(digits[0]);
        var before = full.slice(0, full.indexOf(digits[0]));
        var after = full.slice(full.indexOf(digits[0]) + digits[0].length);
        var decimals = (digits[0].split('.')[1] || '').length;
        var started = false;

        var run = function () {
          if (started) return;
          started = true;
          var t0 = null;
          var step = function (now) {
            if (t0 === null) t0 = now;
            var p = Math.min((now - t0) / 1100, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = before + (target * eased).toFixed(decimals) + after;
            if (p < 1) requestAnimationFrame(step);
            else el.textContent = full;
          };
          requestAnimationFrame(step);
        };

        // Only animate if it is on screen at load; otherwise leave it be.
        if (el.getBoundingClientRect().top < window.innerHeight) {
          setTimeout(run, 320);
        }
      })(stats[s]);
    }

    /* —— Hero results panel ——
       Cycles three real campaigns, animating the metric each time a
       slide becomes active. Slide 1 is already correct in the HTML, so
       a failure here leaves a valid static panel. */
    var stage = document.querySelector('.viz-stage');
    if (stage) {
      var slides = stage.querySelectorAll('.viz-slide');
      var tabs = document.querySelectorAll('.viz-tabs span');
      var at = 0;

      var countUp = function (el) {
        var to = parseFloat(el.dataset.to);
        var from = parseFloat(el.dataset.from || 0);
        var dec = parseInt(el.dataset.dec || 0, 10);
        var pre = el.dataset.pre || '';
        var suf = el.dataset.suf || '';
        var t0 = null;

        var fmt = function (n) {
          return pre + n.toFixed(dec).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suf;
        };
        var step = function (now) {
          if (t0 === null) t0 = now;
          var p = Math.min((now - t0) / 1200, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = fmt(from + (to - from) * eased);
          if (p < 1) requestAnimationFrame(step);
          else el.textContent = fmt(to);
        };
        requestAnimationFrame(step);
      };

      var show = function (i) {
        for (var s = 0; s < slides.length; s++) {
          slides[s].classList.remove('is-on');
          if (tabs[s]) tabs[s].classList.remove('is-on');
        }
        // Reflow so the chart/bar keyframes restart on re-entry
        void slides[i].offsetWidth;
        slides[i].classList.add('is-on');
        if (tabs[i]) tabs[i].classList.add('is-on');

        var num = slides[i].querySelector('.viz-num');
        if (num) countUp(num);
      };

      show(0);
      setInterval(function () {
        at = (at + 1) % slides.length;
        show(at);
      }, 4600);

      /* Tilt the panel toward the cursor */
      var viz = document.querySelector('.viz');
      if (viz && window.matchMedia('(pointer: fine)').matches) {
        window.addEventListener('mousemove', function (e) {
          var x = e.clientX / window.innerWidth - 0.5;
          viz.style.setProperty('--vr', (x * 4).toFixed(2) + 'deg');
        }, { passive: true });
      }
    }

    /* —— Hero glow follows the cursor, gently —— */
    var hero = document.querySelector('.hero');
    if (hero && window.matchMedia('(pointer: fine)').matches) {
      hero.addEventListener('mousemove', function (e) {
        var r = hero.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        hero.style.setProperty('--gx', (x * 36).toFixed(1) + 'px');
        hero.style.setProperty('--gy', (y * 28).toFixed(1) + 'px');
      });
      hero.addEventListener('mouseleave', function () {
        hero.style.setProperty('--gx', '0px');
        hero.style.setProperty('--gy', '0px');
      });
    }
  });
})();
