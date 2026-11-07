// Deck viewer: slide preview (slide list, stage, notes) and present mode.
// Slides live in slides/<id>.html; order and title come from deck.json.
(function () {
  'use strict';

  var SVG_NS = 'http://www.w3.org/2000/svg';
  var state = { deck: null, slides: [], index: 0, presenting: false, signature: '', view: null, versions: {} };
  var $ = function (id) { return document.getElementById(id); };
  var sectionOpen = {};
  var notesPosition = 'bottom', notesCollapsed = false;
  try {
    var savedNotes = JSON.parse(localStorage.getItem('hilegal-notes-layout') || 'null');
    if (savedNotes) {
      notesPosition = savedNotes.position === 'right' ? 'right' : 'bottom';
      notesCollapsed = savedNotes.collapsed === true;
    }
  } catch (e) {}
  // Clear credentials left by the retired browser editor.
  try { localStorage.removeItem('gh-token'); } catch (e) {}

  function fetchText(url) {
    return fetch(url, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error(r.status + ' ' + url);
      return r.text();
    });
  }

  function loadAll() {
    return fetchText('deck.json').then(function (txt) {
      var deck = JSON.parse(txt);
      return Promise.all(deck.order.map(function (id) {
        return fetchText('slides/' + id + '.html').catch(function () { return null; });
      })).then(function (texts) { return { deck: deck, texts: texts, signature: txt + texts.join('\u0000') }; });
    });
  }

  function missingSlide(id) {
    return '<section id="' + id + '" style="background:#ffffff;align-items:center;justify-content:center">' +
      '<p style="font-size:40px;color:#d92605">Missing file: slides/' + id + '.html</p></section>';
  }

  function parseSlide(id, html) {
    if (html == null) html = missingSlide(id);
    var tpl = document.createElement('template');
    tpl.innerHTML = html.trim();
    var sec = tpl.content.querySelector('section');
    var aside = sec && sec.querySelector('aside');
    var heading = sec && sec.querySelector('h1, h2');
    return {
      id: id,
      html: html,
      notes: aside ? aside.textContent.trim() : '',
      hidden: !!(sec && sec.hasAttribute('hidden')),
      chapter: sec ? sec.getAttribute('data-chapter') : null,
      title: heading ? heading.textContent.replace(/\s+/g, ' ').trim() : id
    };
  }

  // Turns the slide markup (incl. x-connector and x-embed) into plain DOM.
  function buildCanvas(slide, opts) {
    opts = opts || {};
    var canvas = document.createElement('div');
    canvas.className = 'canvas';
    var tpl = document.createElement('template');
    tpl.innerHTML = slide.html.trim();
    var sec = tpl.content.querySelector('section');
    if (!sec) return canvas;
    sec.removeAttribute('hidden');
    sec.querySelectorAll('aside').forEach(function (a) { a.remove(); });

    sec.querySelectorAll('img[data-crop]').forEach(function (img) {
      var parts = img.getAttribute('data-crop').trim().split(/\s+/);
      img.style.objectFit = 'cover';
      if (parts.length >= 3) img.style.objectPosition = parts[1] + ' ' + parts[2];
    });

    sec.querySelectorAll('x-embed').forEach(function (el) {
      if (opts.static) { el.remove(); return; }
      var frame = document.createElement('iframe');
      frame.setAttribute('style', (el.getAttribute('style') || '') + ';border:0;background:transparent');
      frame.setAttribute('sandbox', 'allow-scripts');
      frame.setAttribute('title', 'Animation');
      frame.srcdoc = '<!doctype html><html><head><meta charset="utf-8"></head>' +
        '<body style="margin:0;background:transparent;overflow:hidden;font-family:Segoe UI,Arial,sans-serif">' +
        el.innerHTML + '</body></html>';
      el.replaceWith(frame);
    });

    drawConnectors(sec);

    sec.querySelectorAll('a[href]').forEach(function (a) { a.target = '_blank'; a.rel = 'noopener'; });
    canvas.appendChild(sec);
    return canvas;
  }

  function drawConnectors(sec) {
    var items = Array.prototype.slice.call(sec.querySelectorAll('x-connector'));
    if (!items.length) return;
    var svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('width', '1920');
    svg.setAttribute('height', '1080');
    svg.setAttribute('viewBox', '0 0 1920 1080');
    svg.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;overflow:visible';
    items[0].parentNode.insertBefore(svg, items[0]);
    items.forEach(function (c) {
      var st = c.getAttribute('style') || '';
      var col = ((st.match(/(?:^|;)\s*color:\s*([^;]+)/) || [0, '#101010'])[1]).trim();
      var w = parseFloat((st.match(/border-width:\s*([\d.]+)/) || [0, 2])[1]);
      var dash = /dashed/.test(st) ? (w * 3.3) + ' ' + (w * 2.7) : (/dotted/.test(st) ? '2 ' + (w * 2.5) : '');
      var x1 = +c.getAttribute('x1'), y1 = +c.getAttribute('y1'), x2 = +c.getAttribute('x2'), y2 = +c.getAttribute('y2');
      var line = document.createElementNS(SVG_NS, 'line');
      line.setAttribute('x1', x1); line.setAttribute('y1', y1);
      line.setAttribute('x2', x2); line.setAttribute('y2', y2);
      line.setAttribute('stroke', col); line.setAttribute('stroke-width', w);
      if (dash) line.setAttribute('stroke-dasharray', dash);
      svg.appendChild(line);
      var head = c.getAttribute('head') || 'end';
      if (head === 'end' || head === 'both') arrowHead(svg, x1, y1, x2, y2, col, w);
      if (head === 'both') arrowHead(svg, x2, y2, x1, y1, col, w);
      c.remove();
    });
  }

  function arrowHead(svg, xa, ya, xb, yb, col, w) {
    var a = Math.atan2(yb - ya, xb - xa), len = 10 + w * 2;
    var p = document.createElementNS(SVG_NS, 'polygon');
    p.setAttribute('points', xb + ',' + yb + ' ' +
      (xb - len * Math.cos(a - 0.45)) + ',' + (yb - len * Math.sin(a - 0.45)) + ' ' +
      (xb - len * Math.cos(a + 0.45)) + ',' + (yb - len * Math.sin(a + 0.45)));
    p.setAttribute('fill', col);
    svg.appendChild(p);
  }

  function fit(box, canvas) {
    var w = box.clientWidth, h = box.clientHeight;
    if (!w || !h) return;
    var style = getComputedStyle(box);
    var left = parseFloat(style.paddingLeft) || 0, right = parseFloat(style.paddingRight) || 0;
    var top = parseFloat(style.paddingTop) || 0, bottom = parseFloat(style.paddingBottom) || 0;
    var availableWidth = Math.max(1, w - left - right), availableHeight = Math.max(1, h - top - bottom);
    var k = Math.min(availableWidth / 1920, availableHeight / 1080);
    canvas.style.transform = 'translate(' + (left + (availableWidth - 1920 * k) / 2) + 'px,' + (top + (availableHeight - 1080 * k) / 2) + 'px) scale(' + k + ')';
  }

  // Chapter dividers are not numbered, so the page numbers printed on the slides stay correct.
  function isNumbered(s) { return !s.hidden && !s.chapter; }

  function slideNumber(i) {
    if (!isNumbered(state.slides[i])) return null;
    var n = 0;
    for (var j = 0; j <= i; j++) if (isNumbered(state.slides[j])) n++;
    return n;
  }

  function slideLabel(s, n) {
    if (s.chapter) return 'Chapter ' + s.chapter;
    return n === null ? 'hidden' : String(n);
  }

  // Slide preview
  function railSection(key, section, count) {
    var group = document.createElement('details');
    group.className = 'rail-section';
    group.dataset.section = key;
    group.open = sectionOpen[key] !== false;
    var heading = document.createElement('summary');
    var title = document.createElement('span');
    title.className = 'section-title';
    var names = { internal: 'Internal', intro: 'Introduction', appendix: 'Appendix' };
    title.textContent = names[key] || ((/^s[1-9]$/.test(key) ? '0' + key.slice(1) + '  ' : '') + section.description);
    var total = document.createElement('span');
    total.className = 'section-count';
    total.textContent = count;
    total.setAttribute('aria-label', count + (count === 1 ? ' slide' : ' slides'));
    heading.appendChild(title);
    heading.appendChild(total);
    var body = document.createElement('div');
    body.className = 'section-slides';
    group.appendChild(heading);
    group.appendChild(body);
    group.addEventListener('toggle', function () {
      sectionOpen[key] = group.open;
      if (group.open) requestAnimationFrame(function () {
        group.querySelectorAll('.thumb-box').forEach(function (box) { fit(box, box.querySelector('.canvas')); });
      });
    });
    $('rail').appendChild(group);
    return body;
  }

  function renderRail() {
    var rail = $('rail');
    rail.innerHTML = '';
    var starts = {}, sections = state.deck.sections || {};
    Object.keys(sections).forEach(function (key) {
      starts[sections[key].start] = { key: key, section: sections[key] };
    });
    var target = rail;
    state.slides.forEach(function (s, i) {
      if (starts[s.id]) {
        var group = starts[s.id], end = i + 1;
        while (end < state.slides.length && !starts[state.slides[end].id]) end++;
        target = railSection(group.key, group.section, end - i);
      }
      var item = document.createElement('button');
      item.type = 'button';
      item.className = 'thumb' + (i === state.index ? ' active' : '') + (s.hidden ? ' is-hidden' : '');
      var box = document.createElement('div');
      box.className = 'thumb-box';
      var canvas = buildCanvas(s, { static: true });
      box.appendChild(canvas);
      var label = document.createElement('div');
      label.className = 'thumb-label';
      var n = slideNumber(i);
      label.textContent = slideLabel(s, n) + ' | ' + s.id;
      item.title = s.title;
      item.appendChild(box);
      item.appendChild(label);
      item.addEventListener('click', function () { select(i); });
      target.appendChild(item);
      requestAnimationFrame(function () { fit(box, canvas); });
    });
  }

  // Version history: earlier versions of a slide, read from the GitHub commit history (deck.json "history").
  function historyCfg() { return state.deck && state.deck.history; }

  function historyPaths(id) {
    return (historyCfg().paths || ['slides/{id}.html']).map(function (p) { return p.replace('{id}', id); });
  }

  function loadVersions(id) {
    if (state.versions[id]) return state.versions[id];
    var cfg = historyCfg(), key = 'versions:' + cfg.repo + ':' + id;
    try {
      var cached = JSON.parse(sessionStorage.getItem(key) || 'null');
      if (cached && Date.now() - cached.t < 600000) return (state.versions[id] = Promise.resolve(cached.list));
    } catch (e) {}
    var api = 'https://api.github.com/repos/' + cfg.repo + '/commits?per_page=50&sha=' +
      encodeURIComponent(cfg.branch || 'main') + '&path=';
    var p = Promise.all(historyPaths(id).map(function (path) {
      return fetch(api + encodeURIComponent(path)).then(function (r) {
        if (!r.ok) throw new Error(r.status === 403 ? 'GitHub limit reached, try again in an hour' : 'GitHub ' + r.status);
        return r.json();
      });
    })).then(function (lists) {
      var seen = {}, out = [];
      lists.forEach(function (list) {
        list.forEach(function (c) {
          if (seen[c.sha]) return;
          seen[c.sha] = true;
          out.push({ sha: c.sha, date: c.commit.author.date, author: c.commit.author.name, msg: c.commit.message.split('\n')[0] });
        });
      });
      out.sort(function (a, b) { return a.date < b.date ? 1 : -1; });
      try { sessionStorage.setItem(key, JSON.stringify({ t: Date.now(), list: out })); } catch (e) {}
      return out;
    });
    p.catch(function () { delete state.versions[id]; });
    return (state.versions[id] = p);
  }

  // Slides moved folders once, so try every configured path at that commit.
  function fetchVersion(id, sha) {
    var paths = historyPaths(id), base = 'https://raw.githubusercontent.com/' + historyCfg().repo + '/' + sha + '/', i = 0;
    function next() {
      if (i >= paths.length) return Promise.reject(new Error('file not found in ' + sha.slice(0, 7)));
      var path = paths[i++];
      return fetch(base + path).then(function (r) {
        return r.ok ? r.text().then(function (html) { return { html: html, path: path }; }) : next();
      });
    }
    return next();
  }

  function addOption(sel, value, label, disabled) {
    var o = document.createElement('option');
    o.value = value;
    o.textContent = label;
    o.disabled = !!disabled;
    sel.appendChild(o);
  }

  function updateVersionMenu() {
    var sel = $('version'), s = state.slides[state.index];
    sel.parentNode.hidden = !historyCfg();
    if (!s || !historyCfg()) return;
    if (sel.dataset.slide !== s.id) {
      sel.dataset.slide = s.id;
      sel.innerHTML = '';
      addOption(sel, '', 'Current file');
      addOption(sel, '', 'Loading history…', true);
      loadVersions(s.id).then(function (list) {
        if (sel.dataset.slide !== s.id) return;
        sel.innerHTML = '';
        addOption(sel, '', 'Current file');
        if (!list.length) addOption(sel, '', 'No versions on GitHub yet', true);
        list.forEach(function (v) {
          var when = new Date(v.date).toLocaleString('en-GB', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
          addOption(sel, v.sha, when + ' | ' + v.sha.slice(0, 7) + ' | ' + v.author + ' | ' + v.msg);
        });
        sel.value = state.view ? state.view.sha : '';
      }, function (err) {
        if (sel.dataset.slide !== s.id) return;
        sel.innerHTML = '';
        addOption(sel, '', 'Current file');
        addOption(sel, '', 'History unavailable: ' + err.message, true);
      });
    }
    sel.value = state.view ? state.view.sha : '';
  }

  function showVersion(sha) {
    var s = state.slides[state.index];
    if (!sha) { state.view = null; renderStage(); return; }
    setStatus('Loading version ' + sha.slice(0, 7) + '…');
    fetchVersion(s.id, sha).then(function (res) {
      if (state.slides[state.index].id !== s.id) return;
      state.view = parseSlide(s.id, res.html);
      state.view.sha = sha;
      state.view.path = res.path;
      renderStage();
      setStatus('');
    }).catch(function (err) {
      setStatus('Could not load version: ' + err.message);
      $('version').value = state.view ? state.view.sha : '';
    });
  }

  function renderStage() {
    var cur = state.slides[state.index];
    if (!cur) return;
    if (state.view && state.view.id !== cur.id) state.view = null;
    var s = state.view || cur;
    var stage = $('stage');
    stage.innerHTML = '';
    var canvas = buildCanvas(s);
    stage.appendChild(canvas);
    fit(stage, canvas);
    var n = slideNumber(state.index);
    $('slideNo').textContent = (s.chapter ? 'Chapter divider ' + s.chapter : (n === null ? 'Hidden slide' : 'Slide ' + n)) + ' | ' + s.title;
    $('slidePath').textContent = 'slides/' + s.id + '.html';
    $('hiddenBadge').hidden = !s.hidden;
    $('notes').textContent = s.notes || '(no notes)';
    $('notes').scrollTop = 0;
    $('versionBadge').hidden = !state.view;
    if (state.view) $('versionBadge').textContent = 'Old version ' + state.view.sha.slice(0, 7) + ' | view only';
    updateVersionMenu();
    requestAnimationFrame(function () { fit(stage, canvas); });
    document.querySelectorAll('.thumb').forEach(function (t, i) { t.classList.toggle('active', i === state.index); });
    var active = document.querySelectorAll('.thumb')[state.index];
    if (active) {
      var group = active.closest('.rail-section');
      if (group) group.open = true;
      if (active.scrollIntoView) active.scrollIntoView({ block: 'nearest' });
    }
  }

  function select(i) {
    if (i < 0 || i >= state.slides.length) return;
    state.index = i;
    history.replaceState(null, '', '#' + state.slides[i].id);
    renderStage();
  }

  // Present mode
  function visibleIndices() {
    var out = [];
    state.slides.forEach(function (s, i) { if (!s.hidden) out.push(i); });
    return out;
  }

  function renderPresent() {
    var s = state.slides[state.index];
    var stage = $('pstage');
    stage.innerHTML = '';
    var canvas = buildCanvas(s);
    stage.appendChild(canvas);
    fit(stage, canvas);
    $('pnotes').textContent = s.notes || '';
    var total = state.slides.filter(isNumbered).length, n = slideNumber(state.index);
    $('pcount').textContent = n === null ? '' : n + ' / ' + total;
  }

  function startPresent() {
    var vis = visibleIndices();
    if (!vis.length) return;
    if (vis.indexOf(state.index) < 0) state.index = vis.filter(function (i) { return i > state.index; })[0] || vis[0];
    state.presenting = true;
    $('present').hidden = false;
    var el = document.documentElement;
    if (el.requestFullscreen) el.requestFullscreen().catch(function () {});
    renderPresent();
  }

  function stopPresent() {
    if (!state.presenting) return;
    state.presenting = false;
    $('present').hidden = true;
    $('pstage').innerHTML = '';
    if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(function () {});
    select(state.index);
  }

  function step(delta) {
    if (state.presenting) {
      var vis = visibleIndices();
      var pos = vis.indexOf(state.index) + delta;
      if (pos < 0 || pos >= vis.length) return;
      state.index = vis[pos];
      renderPresent();
      syncSend();
    } else {
      select(state.index + delta);
    }
  }

  // Room sync (?room=…): the projector follows the presenter pages and sends its own slide changes.
  function syncSend() {
    if (!state.sync) return;
    var s = state.slides[state.index], r = state.remote;
    state.remote = { slide: s.id, running: !!(r && r.running), elapsed: DeckSync.elapsedOf(r), receivedAt: Date.now() };
    state.sync.send(state.remote);
  }

  function startSync() {
    var room = window.DeckSync && DeckSync.roomFromUrl();
    $('lnkPresenter').href = 'presenter.html' + (room ? '?room=' + room : '');
    if (!room) return;
    state.sync = DeckSync.connect(room, function (st, own) {
      state.remote = st;
      if (own) return;
      var i = state.slides.findIndex(function (s) { return s.id === st.slide; });
      if (i < 0 || i === state.index) return;
      if (state.presenting) { state.index = i; renderPresent(); } else select(i);
    }, function (on) { setStatus(on ? 'Room ' + room + ' connected' : 'Room ' + room + ' reconnecting…'); });
  }

  // Loading and live reload
  function apply(data, keepId) {
    state.deck = data.deck;
    state.signature = data.signature;
    state.slides = data.deck.order.map(function (id, i) {
      return parseSlide(id, data.texts[i]);
    });
    document.title = data.deck.title || 'Deck';
    $('deckTitle').textContent = data.deck.title || 'Deck';
    var idx = keepId ? state.slides.findIndex(function (s) { return s.id === keepId; }) : -1;
    if (idx < 0) idx = Math.min(state.index, state.slides.length - 1);
    state.index = Math.max(0, idx);
    renderRail();
    if (state.presenting) renderPresent(); else renderStage();
  }

  function reload(silent) {
    var keep = state.slides[state.index] && state.slides[state.index].id;
    return loadAll().then(function (data) {
      if (silent && data.signature === state.signature) return;
      apply(data, keep);
      setStatus('Updated ' + new Date().toLocaleTimeString());
    }).catch(function (err) { setStatus('Load error: ' + err.message); });
  }

  function setStatus(msg) { $('status').textContent = msg; }

  function setNotesLayout(position, collapsed) {
    notesPosition = position;
    notesCollapsed = collapsed;
    $('workspace').classList.toggle('notes-right', position === 'right');
    $('workspace').classList.toggle('notes-collapsed', collapsed);
    $('notesPanel').hidden = collapsed;
    $('btnNotesBottom').setAttribute('aria-pressed', String(position === 'bottom' && !collapsed));
    $('btnNotesRight').setAttribute('aria-pressed', String(position === 'right' && !collapsed));
    var toggle = $('btnNotesToggle');
    toggle.setAttribute('aria-expanded', String(!collapsed));
    toggle.setAttribute('aria-label', collapsed ? 'Show speaker notes' : 'Hide speaker notes');
    toggle.title = (collapsed ? 'Show notes' : 'Hide notes') + ' (N)';
    var direction = position === 'right' ? (collapsed ? 'left' : 'right') : (collapsed ? 'up' : 'down');
    $('notesToggleIcon').src = 'assets/icons/chevron-' + direction + '.svg';
    try { localStorage.setItem('hilegal-notes-layout', JSON.stringify({ position: position, collapsed: collapsed })); } catch (e) {}
  }

  function bind() {
    setNotesLayout(notesPosition, notesCollapsed);
    $('btnNotesBottom').addEventListener('click', function () { setNotesLayout('bottom', false); });
    $('btnNotesRight').addEventListener('click', function () { setNotesLayout('right', false); });
    $('btnNotesToggle').addEventListener('click', function () { setNotesLayout(notesPosition, !notesCollapsed); });
    // Handle only vertical wheel gestures over the slide preview. Notes and the rail scroll normally.
    var wheelTotal = 0, wheelLast = 0, wheelChangedAt = -1000;
    $('stage').addEventListener('wheel', function (e) {
      if (state.presenting || !state.slides.length || e.ctrlKey || e.metaKey || Math.abs(e.deltaX) >= Math.abs(e.deltaY)) return;
      if (e.target.closest('a, button, input, textarea, select, iframe')) return;
      e.preventDefault();
      var now = performance.now();
      var delta = e.deltaY * (e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? $('stage').clientHeight : 1);
      if (now - wheelLast > 180 || wheelTotal * delta < 0) wheelTotal = 0;
      wheelLast = now;
      if (now - wheelChangedAt < 320) return;
      wheelTotal += delta;
      if (Math.abs(wheelTotal) >= 40) {
        wheelTotal = 0;
        wheelChangedAt = now;
        step(delta > 0 ? 1 : -1);
      }
    }, { passive: false });
    function setAllSections(open) {
      $('rail').querySelectorAll('.rail-section').forEach(function (group) {
        sectionOpen[group.dataset.section] = open;
        group.open = open;
      });
    }
    $('btnExpandAll').addEventListener('click', function () { setAllSections(true); });
    $('btnCollapseAll').addEventListener('click', function () { setAllSections(false); });
    $('btnPresent').addEventListener('click', startPresent);
    $('btnReload').addEventListener('click', function () { reload(false); });
    $('btnCopy').addEventListener('click', function () {
      var path = $('slidePath').textContent;
      if (navigator.clipboard) navigator.clipboard.writeText(path).then(function () { setStatus('Copied ' + path); });
    });
    $('version').addEventListener('change', function (e) { showVersion(e.target.value); });
    // Present mode: click the left half to go back, the right half to go forward.
    $('present').addEventListener('click', function (e) {
      if (!state.presenting || e.target.closest('a, button, iframe, #pnotes')) return;
      step(e.clientX < window.innerWidth / 2 ? -1 : 1);
    });
    document.addEventListener('keydown', function (e) {
      if (e.target && (/INPUT|TEXTAREA|SELECT|SUMMARY/.test(e.target.tagName) || e.target.isContentEditable)) return;
      var k = e.key;
      if (state.presenting) {
        if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || k === ' ' || k === 'Enter') { e.preventDefault(); step(1); }
        else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp' || k === 'Backspace') { e.preventDefault(); step(-1); }
        else if (k === 'Home') { var v = visibleIndices(); state.index = v[0]; renderPresent(); syncSend(); }
        else if (k === 'End') { var w = visibleIndices(); state.index = w[w.length - 1]; renderPresent(); syncSend(); }
        else if (k === 'n' || k === 'N') { $('pnotes').hidden = !$('pnotes').hidden; }
        else if (k === 'Escape') { stopPresent(); }
        return;
      }
      if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown') { e.preventDefault(); step(1); }
      else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp') { e.preventDefault(); step(-1); }
      else if (k === 'n' || k === 'N') { setNotesLayout(notesPosition, !notesCollapsed); }
      else if (k === 'p' || k === 'P') { startPresent(); }
      else if (k === 'r' || k === 'R') { reload(false); }
    });
    window.addEventListener('hashchange', function () {
      var id = decodeURIComponent(location.hash.replace(/^#/, ''));
      var i = state.slides.findIndex(function (s) { return s.id === id; });
      if (i < 0 || i === state.index) return;
      state.index = i;
      if (state.presenting) renderPresent(); else renderStage();
    });
    document.addEventListener('fullscreenchange', function () {
      if (!document.fullscreenElement && state.presenting) stopPresent();
    });
    var refit = function () {
      ['stage', 'pstage'].forEach(function (id) {
        var box = $(id), canvas = box.querySelector('.canvas');
        if (canvas) fit(box, canvas);
      });
    };
    if (window.ResizeObserver) {
      var ro = new ResizeObserver(refit);
      ro.observe($('stage'));
      ro.observe($('pstage'));
    }
    window.addEventListener('resize', function () {
      refit();
      document.querySelectorAll('.thumb-box').forEach(function (b) { var c = b.querySelector('.canvas'); if (c) fit(b, c); });
    });
    setInterval(function () {
      if (!state.presenting && $('live').checked && document.visibilityState === 'visible') reload(true);
    }, 2500);
  }

  // Browsers block loading slide files from file:// pages, so explain how to start it instead.
  function showFileHint() {
    $('stage').innerHTML =
      '<div style="max-width:720px;margin:48px auto;padding:32px;background:#ffffff;border-top:3px solid #d92605;border-radius:6px;line-height:1.6">' +
      '<h2 style="margin:0 0 12px;font-size:24px">Open the presentation with start.bat</h2>' +
      '<p style="margin:0 0 12px">This page was opened directly from the folder, so the browser blocks loading the slide files.</p>' +
      '<p style="margin:0 0 12px"><b>Windows:</b> close this tab and double-click <code>start.bat</code> in the same folder. It starts a small local server and opens the deck at <code>http://localhost:8000</code>.</p>' +
      '<p style="margin:0"><b>Mac / other:</b> run <code>npx serve .</code> or <code>python3 -m http.server 8000</code> in this folder, then open the address it prints.</p>' +
      '</div>';
    setStatus('Opened from file – use start.bat');
  }

  bind();
  if (location.protocol === 'file:') { showFileHint(); return; }
  loadAll().then(function (data) {
    var hashId = decodeURIComponent(location.hash.replace(/^#/, ''));
    apply(data, hashId || null);
    if (/[?&]present\b/.test(location.search)) startPresent();
    startSync();
  }).catch(function (err) {
    setStatus('Load error: ' + err.message + ' (open via a local web server, see README)');
  });
})();
