(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var on = function (el, ev, fn) { if (el) el.addEventListener(ev, fn); };
  var fmt = function (n) { return Math.round(n).toLocaleString('fr-FR').replace(/ /g, ' ') + ' FCFA'; };
  var years = new Date().getFullYear() - 1995;

  function icons() { if (window.lucide) window.lucide.createIcons(); }
  icons();

  /* ---------- Menu mobile + sous-menu ---------- */
  var burger = $('#burger'), menu = $('#menu');
  on(burger, 'click', function () {
    var o = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', o);
  });
  $$('.sub-toggle').forEach(function (b) {
    on(b, 'click', function () {
      var p = b.closest('.has-sub'), o = p.classList.toggle('open');
      b.setAttribute('aria-expanded', o);
    });
  });

  /* ---------- Sélecteur de profil ---------- */
  var who = $('#who');
  on(who, 'change', function () { if (who.value) location.href = who.value; });

  /* ---------- En-tête + progression ---------- */
  var bar = $('#progress'), nav = $('#nav');
  function onScroll() {
    var h = document.documentElement;
    if (bar) bar.style.width = (scrollY / Math.max(1, h.scrollHeight - h.clientHeight) * 100) + '%';
    if (nav) nav.classList.toggle('scrolled', scrollY > 30);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- Slider (accueil) ---------- */
  var slides = $$('.slide');
  if (slides.length) {
    var dots = $('#dots'), cur = 0, timer;
    var go = function (i) {
      cur = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('is-active', k === cur); });
      $$('button', dots).forEach(function (d, k) { d.classList.toggle('on', k === cur); });
    };
    var start = function () {
      clearInterval(timer);
      if (!matchMedia('(prefers-reduced-motion:reduce)').matches) timer = setInterval(function () { go(cur + 1); }, 7000);
    };
    slides.forEach(function (_, i) {
      var b = document.createElement('button');
      b.setAttribute('aria-label', 'Diapositive ' + (i + 1));
      on(b, 'click', function () { go(i); start(); });
      dots.appendChild(b);
    });
    on($('#prev'), 'click', function () { go(cur - 1); start(); });
    on($('#next'), 'click', function () { go(cur + 1); start(); });
    go(0); start();
  }

  /* ---------- Compteurs + apparition ---------- */
  function count(el) {
    var raw = el.dataset.count, target = raw === 'years' ? years : +raw;
    var pre = el.dataset.prefix || '', plain = el.dataset.plain, t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 1500, 1), v = Math.round(target * (1 - Math.pow(1 - p, 3)));
      el.textContent = pre + (plain ? v : v.toLocaleString('fr-FR'));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      if (e.target.dataset.count) count(e.target); else e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { threshold: .15 }) : null;
  $$('[data-count]').forEach(function (el) {
    if (io) io.observe(el); else el.textContent = (el.dataset.prefix || '') + (el.dataset.count === 'years' ? years : el.dataset.count);
  });
  $$('.item,.row,.statement,.values li,.split__img,.split__txt,.cform,.contact__info,.sim__box').forEach(function (el, i) {
    if (io) { el.classList.add('rv'); el.style.transitionDelay = (i % 3) * 80 + 'ms'; io.observe(el); }
  });

  /* ---------- Simulateur ---------- */
  var out = function (id, outId, suffix) {
    var el = $(id), o = $(outId);
    if (!el || !o) return;
    var up = function () { o.textContent = suffix === 'm' ? el.value + ' mois' : fmt(el.value); };
    on(el, 'input', up); up();
  };
  if ($('#c-amount')) {
    var calcCredit = function () {
      var P = +$('#c-amount').value, n = +$('#c-dur').value, rate = parseFloat($('#c-rate').value);
      if (isNaN(rate) || rate < 0) { ['#c-month', '#c-cost', '#c-total'].forEach(function (k) { $(k).textContent = '-'; }); return; }
      var r = rate / 100 / 12;
      var m = r === 0 ? P / n : P * r / (1 - Math.pow(1 + r, -n));
      $('#c-month').textContent = fmt(m); $('#c-cost').textContent = fmt(m * n - P); $('#c-total').textContent = fmt(m * n);
    };
    ['#c-amount', '#c-dur', '#c-rate'].forEach(function (s) { on($(s), 'input', calcCredit); });
    out('#c-amount', '#c-amount-o'); out('#c-dur', '#c-dur-o', 'm');
    calcCredit();
  }
  if ($('#e-amount')) {
    var calcSave = function () {
      var P = +$('#e-amount').value, n = +$('#e-dur').value, rate = parseFloat($('#e-rate').value);
      if (isNaN(rate) || rate < 0) { $('#e-int').textContent = '-'; $('#e-total').textContent = '-'; return; }
      var i = P * (rate / 100) * n / 12;
      $('#e-int').textContent = fmt(i); $('#e-total').textContent = fmt(P + i);
    };
    ['#e-amount', '#e-dur', '#e-rate'].forEach(function (s) { on($(s), 'input', calcSave); });
    out('#e-amount', '#e-amount-o'); out('#e-dur', '#e-dur-o', 'm');
    calcSave();
  }
  $$('.tab').forEach(function (t) {
    on(t, 'click', function () {
      $$('.tab').forEach(function (x) { x.classList.toggle('is-on', x === t); x.setAttribute('aria-selected', x === t); });
      $$('.simform').forEach(function (f) { f.hidden = f.dataset.panel !== t.dataset.tab; });
    });
  });

  /* ---------- Caisses : filtre (page annuaire et accueil) ---------- */
  if ($('#dir')) {
    var region = 'Toutes', q = $('#q'), sel = $('#region-sel'), empty = $('#empty');
    var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    var render = function () {
      var term = q ? norm(q.value.trim()) : '', shown = 0;
      $$('.cs').forEach(function (c) {
        var ok = (region === 'Toutes' || c.dataset.region === region) && (!term || norm(c.dataset.q).indexOf(term) > -1);
        c.hidden = !ok; if (ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    };
    $$('.chip').forEach(function (b) {
      on(b, 'click', function () {
        region = b.dataset.region;
        $$('.chip').forEach(function (c) { c.classList.toggle('on', c === b); });
        render();
      });
    });
    on(sel, 'change', function () { region = sel.value; render(); });
    on(q, 'input', render);
  }

  /* ---------- Formulaires (mailto, sans backend) ---------- */
  on($('#cform'), 'submit', function (e) {
    e.preventDefault();
    var f = e.target, body = 'Nom : ' + f.nom.value + '\nE-mail : ' + f.email.value + '\nTéléphone : ' + f.tel.value + '\n\n' + f.msg.value;
    location.href = 'mailto:contact@rcmec.ci?subject=' + encodeURIComponent(f.objet.value) + '&body=' + encodeURIComponent(body);
  });
  on($('#nl'), 'submit', function (e) {
    e.preventDefault();
    var v = e.target.querySelector('input').value;
    location.href = 'mailto:contact@rcmec.ci?subject=' + encodeURIComponent('Inscription newsletter') + '&body=' + encodeURIComponent('Merci d\'inscrire cette adresse à la newsletter : ' + v);
  });

  var y = $('#y'); if (y) y.textContent = new Date().getFullYear();
})();
