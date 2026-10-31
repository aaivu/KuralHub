(function () {
  'use strict';

  // Light/dark switch. The head script applies a saved choice before paint.
  var root = document.documentElement;
  var toggle = document.querySelector('.theme-toggle');
  var dark = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function mode() {
    return root.getAttribute('data-theme') || (dark && dark.matches ? 'dark' : 'light');
  }
  function sync() {
    var m = mode();
    toggle.setAttribute('data-mode', m);
    toggle.setAttribute('aria-label', m === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    toggle.title = toggle.getAttribute('aria-label');
  }
  if (toggle) {
    toggle.hidden = false;
    sync();
    toggle.addEventListener('click', function () {
      var next = mode() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('kh-theme', next); } catch (e) {}
      sync();
    });
    if (dark && dark.addEventListener) dark.addEventListener('change', sync);
  }

  // Live GitHub star count next to the Star button, cached for the session.
  var count = document.querySelector('.star-count');
  if (count && window.fetch) {
    var show = function (n) {
      if (typeof n !== 'number') return;
      count.textContent = n >= 1000 ? (n / 1000).toFixed(1) + 'k' : String(n);
      count.hidden = false;
    };
    var cached = null;
    try { cached = sessionStorage.getItem('kh-stars'); } catch (e) {}
    if (cached) {
      show(Number(cached));
    } else {
      fetch('https://api.github.com/repos/aaivu/KuralHub')
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (!d) return;
          show(d.stargazers_count);
          try { sessionStorage.setItem('kh-stars', d.stargazers_count); } catch (e) {}
        })
        .catch(function () {});
    }
  }

  // Copy buttons: <button class="copy-btn" data-copy="#id">
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var el = document.querySelector(btn.getAttribute('data-copy'));
      if (!el || !navigator.clipboard) return;
      navigator.clipboard.writeText(el.innerText.trim()).then(function () {
        var label = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = label; }, 1500);
      });
    });
  });

  // Figure zoom: <a class="zoom" href="full.png"><img></a>
  var box = document.createElement('div');
  box.className = 'lightbox';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-label', 'Enlarged figure');
  box.innerHTML = '<img alt="">';
  document.body.appendChild(box);
  var boxImg = box.querySelector('img');
  document.querySelectorAll('a.zoom').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var img = a.querySelector('img');
      boxImg.src = a.getAttribute('href');
      boxImg.alt = img ? img.alt : '';
      box.classList.add('open');
    });
  });
  box.addEventListener('click', function () { box.classList.remove('open'); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') box.classList.remove('open');
  });

  // Highlight the current section in the sidebar table of contents.
  var tocLinks = document.querySelectorAll('.toc a[href^="#"]');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        tocLinks.forEach(function (a) { a.classList.remove('active'); });
        var link = byId[en.target.id];
        if (link) link.classList.add('active');
      });
    }, { rootMargin: '-60px 0px -70% 0px' });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }

  // Sortable tables: <th data-sort="num|text">
  document.querySelectorAll('table').forEach(function (table) {
    var heads = table.querySelectorAll('th[data-sort]');
    heads.forEach(function (th) {
      th.setAttribute('tabindex', '0');
      function sort() {
        var idx = Array.prototype.indexOf.call(th.parentNode.children, th);
        var asc = th.getAttribute('aria-sort') !== 'ascending';
        heads.forEach(function (h) { h.removeAttribute('aria-sort'); });
        th.setAttribute('aria-sort', asc ? 'ascending' : 'descending');
        var numeric = th.getAttribute('data-sort') === 'num';
        var body = table.tBodies[0];
        var rows = Array.prototype.slice.call(body.rows);
        rows.sort(function (a, b) {
          var x = a.cells[idx], y = b.cells[idx];
          if (!x || !y) return 0;
          var vx = x.getAttribute('data-v') || x.textContent.trim();
          var vy = y.getAttribute('data-v') || y.textContent.trim();
          if (!numeric) return asc ? vx.localeCompare(vy) : vy.localeCompare(vx);
          var nx = parseFloat(vx.replace(/[^\d.\-]/g, ''));
          var ny = parseFloat(vy.replace(/[^\d.\-]/g, ''));
          if (isNaN(nx) || isNaN(ny)) return isNaN(nx) - isNaN(ny);
          return asc ? nx - ny : ny - nx;
        });
        rows.forEach(function (r) { body.appendChild(r); });
      }
      th.addEventListener('click', sort);
      th.addEventListener('keydown', function (e) { if (e.key === 'Enter') sort(); });
    });
  });

  // Filterable tables: a .filters block with data-table="#id" containing an
  // <input type="search"> and/or <select data-key="attr"> (matches tr[data-attr]).
  document.querySelectorAll('.filters[data-table]').forEach(function (bar) {
    var table = document.querySelector(bar.getAttribute('data-table'));
    if (!table) return;
    var input = bar.querySelector('input[type="search"]');
    var selects = bar.querySelectorAll('select[data-key]');
    var count = bar.querySelector('.count');
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);

    var params = new URLSearchParams(window.location.search);
    if (input && params.get('q')) input.value = params.get('q');
    selects.forEach(function (s) { if (params.get(s.getAttribute('data-key'))) s.value = params.get(s.getAttribute('data-key')); });

    function apply() {
      var q = input ? input.value.trim().toLowerCase() : '';
      var shown = 0;
      rows.forEach(function (row) {
        var ok = !q || row.textContent.toLowerCase().indexOf(q) !== -1;
        selects.forEach(function (s) {
          if (ok && s.value && row.getAttribute('data-' + s.getAttribute('data-key')) !== s.value) ok = false;
        });
        row.hidden = !ok;
        if (ok) shown++;
      });
      if (count) count.textContent = shown + ' of ' + rows.length + ' shown';
    }
    if (input) input.addEventListener('input', apply);
    selects.forEach(function (s) { s.addEventListener('change', apply); });
    apply();
  });
})();
