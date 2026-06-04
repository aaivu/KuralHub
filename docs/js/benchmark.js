(function () {
  var resultsEl = document.getElementById('results');

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }

  Promise.all([KH.loadBenchmark(), KH.loadFamilies()])
    .then(function (res) { init(res[0], res[1]); })
    .catch(function (err) {
      resultsEl.innerHTML = '<div class="note-banner">Failed to load benchmark data. ' + esc(err.message) + '</div>';
    });

  function init(bench, families) {
    // Collect models
    var models = {};
    Object.keys(bench).forEach(function (lang) {
      Object.keys(bench[lang]).forEach(function (ds) {
        bench[lang][ds].forEach(function (b) { models[b.model] = true; });
      });
    });

    // Group languages by family / subfamily (fallback to "Other" if unmapped)
    var byFamily = {};
    Object.keys(bench).forEach(function (lang) {
      var fam = (families[lang] && families[lang].family) || 'Other';
      var sub = (families[lang] && families[lang].subfamily) || '_none';
      (byFamily[fam] = byFamily[fam] || {});
      (byFamily[fam][sub] = byFamily[fam][sub] || []).push(lang);
    });

    // Populate filters
    var famSel = document.getElementById('familyFilter');
    Object.keys(byFamily).sort().forEach(function (f) {
      famSel.insertAdjacentHTML('beforeend', '<option value="' + esc(f) + '">' + esc(f) + '</option>');
    });
    var modSel = document.getElementById('modelFilter');
    Object.keys(models).sort().forEach(function (m) {
      modSel.insertAdjacentHTML('beforeend', '<option value="' + esc(m) + '">' + esc(m) + '</option>');
    });

    function render(famFilter, modFilter) {
      var html = '';
      var fams = Object.keys(byFamily).sort();
      var shown = 0;

      fams.forEach(function (fam) {
        if (famFilter !== 'all' && famFilter !== fam) return;

        var famLangs = [];
        Object.keys(byFamily[fam]).forEach(function (sub) { famLangs = famLangs.concat(byFamily[fam][sub]); });

        var block = '<div class="family-block"><h2 class="family-title">' + esc(fam) +
          ' <span class="count">' + famLangs.length + ' language' + (famLangs.length > 1 ? 's' : '') + '</span></h2>';

        Object.keys(byFamily[fam]).sort().forEach(function (sub) {
          if (sub !== '_none') block += '<h3 class="subfamily-title">' + esc(sub) + '</h3>';

          byFamily[fam][sub].slice().sort().forEach(function (lang) {
            if (!bench[lang]) return;
            var info = KH.parseLang(lang);
            var card = '<div class="lang-card"><h4>' + esc(info.name) +
              ' <span style="color:var(--faint);font-weight:500;font-size:.85rem;">' + esc(info.code) + '</span></h4>';
            var hasRows = false;

            Object.keys(bench[lang]).forEach(function (ds) {
              var rows = bench[lang][ds].filter(function (b) { return modFilter === 'all' || b.model === modFilter; });
              if (!rows.length) return;

              // best by test accuracy
              var best = rows.reduce(function (a, b) { return b.test_accuracy > a.test_accuracy ? b : a; }, rows[0]);

              card += '<div class="ds-name">' + esc(ds) + '</div><div class="table-scroll"><table class="bench">' +
                '<thead><tr><th>Model</th><th>Validation</th><th>Test</th><th>Status</th></tr></thead><tbody>';
              rows.forEach(function (b) {
                card += '<tr><td class="model">' + esc(b.model) + (b === best ? '<span class="best-tag">BEST</span>' : '') + '</td>' +
                  '<td><span class="acc ' + KH.accClass(b.val_accuracy) + '">' + KH.pct(b.val_accuracy) + '</span></td>' +
                  '<td><span class="acc ' + KH.accClass(b.test_accuracy) + '">' + KH.pct(b.test_accuracy) + '</span></td>' +
                  '<td>' + (b.completed || '') + '</td></tr>';
              });
              card += '</tbody></table></div>';
              hasRows = true;
            });

            card += '</div>';
            if (hasRows) { block += card; shown++; }
          });
        });

        block += '</div>';
        if (block.indexOf('lang-card') !== -1) html += block;
      });

      resultsEl.innerHTML = html || '<div class="empty-state"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg><p>No results match these filters.</p></div>';
    }

    function current() { render(famSel.value, modSel.value); }
    famSel.addEventListener('change', current);
    modSel.addEventListener('change', current);
    document.getElementById('resetFilters').addEventListener('click', function () {
      famSel.value = 'all'; modSel.value = 'all'; current();
    });
    render('all', 'all');
  }
})();
