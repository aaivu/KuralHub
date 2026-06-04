/* Shared data access for benchmark + language family data.
   Dataset markdown is mirrored into docs/datasets/ (see scripts/sync-datasets.sh)
   so the site is fully self-contained and served same-origin by GitHub Pages. */
window.KH = (function () {
  var GH_USER = 'aaivu';
  var GH_REPO = 'KuralHub';
  var GH_BRANCH = 'main';
  // Same-origin mirror of the repo's dataset docs (served by Pages from /docs).
  var DOCS_BASE = '';

  function loadJSON(path) {
    return fetch(path).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status + ' for ' + path);
      return r.json();
    });
  }

  return {
    DOCS_BASE: DOCS_BASE,
    repoUrl: 'https://github.com/' + GH_USER + '/' + GH_REPO,
    loadBenchmark: function () { return loadJSON('data/benchmark.json'); },
    loadFamilies: function () { return loadJSON('data/language_families.json'); },
    // language string looks like "English (en)" -> { name: "English", code: "en" }
    parseLang: function (lang) {
      var m = lang.match(/^(.*?)\s*\(([^)]+)\)\s*$/);
      return m ? { name: m[1].trim(), code: m[2].trim() } : { name: lang, code: '' };
    },
    accClass: function (a) { return a >= 0.7 ? 'good' : (a >= 0.5 ? 'mid' : 'low'); },
    pct: function (a) { return (a * 100).toFixed(1) + '%'; },
    // Fetch a mirrored dataset markdown file (same-origin)
    fetchDoc: function (relPath) {
      return fetch(DOCS_BASE + relPath).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.text();
      });
    }
  };
})();
