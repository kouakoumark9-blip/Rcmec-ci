(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var on = function (el, ev, fn) { if (el) el.addEventListener(ev, fn); };
  var fmt = function (n) { return Math.round(n).toLocaleString('fr-FR').replace(/ /g, ' ') + ' FCFA'; };
  var years = new Date().getFullYear() - 1995;

  function icons() { if (window.lucide) window.lucide.createIcons(); }
  icons();

  /* ---------- Menu mobile ---------- */
  var burger = $('#burger'), menu = $('#menu');
  on(burger, 'click', function () {
    var o = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', o);
  });

  /* ---------- Barre de progression ---------- */
  var bar = $('#progress');
  function prog() {
    var h = document.documentElement;
    if (bar) bar.style.width = (scrollY / Math.max(1, h.scrollHeight - h.clientHeight) * 100) + '%';
  }
  window.addEventListener('scroll', prog, { passive: true }); prog();

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
      if (!matchMedia('(prefers-reduced-motion:reduce)').matches) timer = setInterval(function () { go(cur + 1); }, 6500);
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
      var p = Math.min((t - t0) / 1400, 1), v = Math.round(target * (1 - Math.pow(1 - p, 3)));
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
  }, { threshold: .2 }) : null;
  $$('[data-count]').forEach(function (el) {
    if (io) io.observe(el); else el.textContent = (el.dataset.prefix || '') + (el.dataset.count === 'years' ? years : el.dataset.count);
  });
  $$('.pcard,.profiles article,.tips article,.collage img,.card,.vals article,.arts article,.svc,.ccards article,.cs').forEach(function (el) {
    if (io) { el.classList.add('rv'); io.observe(el); }
  });

  /* ---------- Simulateur ---------- */
  if ($('#c-amount')) {
    var out = function (id, outId, suffix) {
      var el = $(id), o = $(outId);
      var up = function () { o.textContent = suffix === 'm' ? el.value + ' mois' : fmt(el.value); };
      on(el, 'input', up); up();
    };
    var calcCredit = function () {
      var P = +$('#c-amount').value, n = +$('#c-dur').value, r = (+$('#c-rate').value || 0) / 100 / 12;
      var m = r === 0 ? P / n : P * r / (1 - Math.pow(1 + r, -n));
      $('#c-month').textContent = fmt(m); $('#c-cost').textContent = fmt(m * n - P); $('#c-total').textContent = fmt(m * n);
    };
    var calcSave = function () {
      var P = +$('#e-amount').value, n = +$('#e-dur').value, r = (+$('#e-rate').value || 0) / 100;
      var i = P * r * n / 12;
      $('#e-int').textContent = fmt(i); $('#e-total').textContent = fmt(P + i);
    };
    ['#c-amount', '#c-dur', '#c-rate'].forEach(function (s) { on($(s), 'input', calcCredit); });
    ['#e-amount', '#e-dur', '#e-rate'].forEach(function (s) { on($(s), 'input', calcSave); });
    out('#c-amount', '#c-amount-o'); out('#c-dur', '#c-dur-o', 'm'); out('#e-amount', '#e-amount-o'); out('#e-dur', '#e-dur-o', 'm');
    calcCredit(); calcSave();
    $$('.tab').forEach(function (t) {
      on(t, 'click', function () {
        $$('.tab').forEach(function (x) { x.classList.toggle('is-on', x === t); x.setAttribute('aria-selected', x === t); });
        $$('.simform').forEach(function (f) { f.hidden = f.dataset.panel !== t.dataset.tab; });
      });
    });
  }

  /* ---------- Répertoire des caisses (filtre) ---------- */
  if ($('#dir')) {
    var region = 'Toutes', q = $('#q');
    var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    var render = function () {
      var term = norm(q.value.trim()), shown = 0;
      $$('.cs').forEach(function (c) {
        var ok = (region === 'Toutes' || c.dataset.region === region) && (!term || norm(c.dataset.q).indexOf(term) > -1);
        c.hidden = !ok; if (ok) shown++;
      });
      $('#empty').hidden = shown > 0;
    };
    $$('.chip').forEach(function (b) {
      on(b, 'click', function () {
        region = b.dataset.region;
        $$('.chip').forEach(function (c) { c.classList.toggle('on', c === b); });
        render();
      });
    });
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
