(function () {
  var gridEl = document.getElementById('langGrid');
  var panel = document.getElementById('mdPanel');
  var body = document.getElementById('mdBody');
  var emptyHint = document.getElementById('emptyHint');
  var searchEl = document.getElementById('search');
  var famSel = document.getElementById('famFilter');
  var countEl = document.getElementById('langCount');

  var LANGS = [];
  var activeFolder = null;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }

  fetch('data/languages.json').then(function (r) { return r.json(); }).then(function (data) {
    LANGS = data;
    // family filter options
    var fams = {};
    LANGS.forEach(function (l) { if (l.family) fams[l.family] = true; });
    Object.keys(fams).sort().forEach(function (f) {
      famSel.insertAdjacentHTML('beforeend', '<option value="' + esc(f) + '">' + esc(f) + '</option>');
    });
    // Deep links: ?q=search and ?lang=Folder
    var params = new URLSearchParams(window.location.search);
    var q = params.get('q'); var lang = params.get('lang');
    if (q) searchEl.value = q;
    if (lang && params.get('fam')) famSel.value = params.get('fam');
    render();
    if (lang && LANGS.some(function (l) { return l.folder === lang; })) selectLang(lang);
  }).catch(function (err) {
    gridEl.innerHTML = '<div class="note-banner">Could not load the language list. ' + esc(err.message) + '</div>';
  });

  function render() {
    var q = (searchEl.value || '').trim().toLowerCase();
    var fam = famSel.value;
    var list = LANGS.filter(function (l) {
      if (fam !== 'all' && l.family !== fam) return false;
      if (q && l.name.toLowerCase().indexOf(q) === -1) return false;
      return true;
    });
    countEl.textContent = list.length + ' of ' + LANGS.length + ' languages';

    if (!list.length) {
      gridEl.innerHTML = '<div class="empty-state" style="grid-column:1/-1;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg><p>No languages match “' + esc(searchEl.value) + '”.</p></div>';
      return;
    }

    gridEl.innerHTML = list.map(function (l) {
      return '<button class="lang-tile' + (l.folder === activeFolder ? ' active' : '') + '" data-folder="' + esc(l.folder) + '">' +
        '<div class="name">' + esc(l.name) + '</div>' +
        '<div class="meta">' + l.count + ' dataset' + (l.count === 1 ? '' : 's') + '</div>' +
        (l.family ? '<div class="fam">' + esc(l.family) + '</div>' : '') +
        '</button>';
    }).join('');

    gridEl.querySelectorAll('.lang-tile').forEach(function (btn) {
      btn.addEventListener('click', function () { selectLang(btn.getAttribute('data-folder')); });
    });
  }

  function selectLang(folder) {
    var lang = LANGS.find(function (l) { return l.folder === folder; });
    if (!lang) return;
    activeFolder = folder;
    render();
    emptyHint.style.display = 'none';
    panel.style.display = 'block';
    body.innerHTML = '<div class="spinner"></div>';
    panel.scrollIntoView({ behavior: 'smooth', block: 'start' });

    var rel = 'datasets/' + folder + '/' + lang.readme;
    KH.fetchDoc(rel).then(function (md) {
      body.innerHTML = marked.parse(md);
      rewriteLinks(folder);
    }).catch(function () {
      body.innerHTML = '<div class="note-banner"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>' +
        'Could not load the documentation for ' + esc(lang.name) + '. View it on ' +
        '<a href="' + KH.repoUrl + '/tree/main/datasets/' + encodeURIComponent(folder) + '" target="_blank" rel="noopener">GitHub</a>.</div>';
    });
  }

  // Rewrite relative links/images inside rendered markdown to work off the repo
  function rewriteLinks(folder) {
    var base = 'datasets/' + folder + '/';
    body.querySelectorAll('a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (/^(https?:|mailto:|#)/i.test(href)) { a.target = '_blank'; a.rel = 'noopener'; return; }
      // strip leading ./
      href = href.replace(/^\.\//, '');
      if (/\.md$/i.test(href) && href.indexOf('/') === -1) {
        // sibling dataset file -> load inline
        a.addEventListener('click', function (e) {
          e.preventDefault();
          body.innerHTML = '<div class="spinner"></div>';
          panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
          KH.fetchDoc(base + href).then(function (md) {
            body.innerHTML = '<p style="margin-bottom:18px;"><a href="#" id="backLink">&larr; Back to ' + esc(folder) + '</a></p>' + marked.parse(md);
            rewriteLinks(folder);
            var bl = document.getElementById('backLink');
            if (bl) bl.addEventListener('click', function (ev) { ev.preventDefault(); selectLang(folder); });
          }).catch(function () {
            window.open(KH.repoUrl + '/blob/main/' + base + href, '_blank');
          });
        });
      } else {
        // other relative path -> point at GitHub
        a.href = KH.repoUrl + '/blob/main/' + base + href.replace(/^\.\.\//, '');
        a.target = '_blank'; a.rel = 'noopener';
      }
    });
    body.querySelectorAll('img[src]').forEach(function (img) {
      var src = img.getAttribute('src');
      if (!/^https?:/i.test(src)) img.src = base + src.replace(/^\.\//, '').replace(/^\.\.\//, '');
    });
  }

  searchEl.addEventListener('input', render);
  famSel.addEventListener('change', render);
})();
