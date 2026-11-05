// Deck viewer: edit view (slide list, stage, notes) and present mode.
// Slides live in slides/<id>.html; order and title come from deck.json.
(function () {
  'use strict';

  var SVG_NS = 'http://www.w3.org/2000/svg';
  var state = { deck: null, slides: [], index: 0, presenting: false, signature: '', view: null, versions: {}, editing: null, saved: {} };
  var $ = function (id) { return document.getElementById(id); };

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
    if (opts.editable) markEditable(sec);
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
    var k = Math.min(w / 1920, h / 1080);
    canvas.style.transform = 'translate(' + ((w - 1920 * k) / 2) + 'px,' + ((h - 1080 * k) / 2) + 'px) scale(' + k + ')';
  }

  function slideNumber(i) {
    if (state.slides[i].hidden) return null;
    var n = 0;
    for (var j = 0; j <= i; j++) if (!state.slides[j].hidden) n++;
    return n;
  }

  // Edit view
  function renderRail() {
    var rail = $('rail');
    rail.innerHTML = '';
    state.slides.forEach(function (s, i) {
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
      label.textContent = (n === null ? 'hidden' : n) + ' · ' + s.id;
      item.title = s.title;
      item.appendChild(box);
      item.appendChild(label);
      item.addEventListener('click', function () { select(i); });
      rail.appendChild(item);
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
          addOption(sel, v.sha, when + ' · ' + v.sha.slice(0, 7) + ' · ' + v.author + ' · ' + v.msg);
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

  // Online editing: text on the slide and the notes, saved as a commit through the GitHub API.
  var INLINE = /^(B|STRONG|I|EM|U|S|BR|SPAN|A|SUP|SUB|CODE|SMALL|MARK)$/;
  var EDIT_SKIP = 'aside, x-embed, x-connector, svg, script, style';

  function canEditOnline() {
    return !!historyCfg() && (/\.github\.io$/.test(location.hostname) || /[?&]edit\b/.test(location.search));
  }

  function isTextBlock(el) {
    if (!el.textContent.trim()) return false;
    for (var n = el.firstElementChild; n; n = n.nextElementSibling) if (!INLINE.test(n.tagName)) return false;
    return true;
  }

  // Runs on the source and on the rendered slide in the same order, so the ids match.
  function markEditable(sec) {
    var n = 0;
    (function walk(el) {
      for (var c = el.firstElementChild; c; c = c.nextElementSibling) {
        if (c.matches(EDIT_SKIP)) continue;
        if (isTextBlock(c)) c.setAttribute('data-eid', n++);
        else walk(c);
      }
    })(sec);
  }

  function norm(s) { return String(s).replace(/\r\n/g, '\n').trim(); }

  function ghToken() { try { return localStorage.getItem('gh-token') || ''; } catch (e) { return ''; } }

  function gh(path, opts) {
    opts = opts || {};
    opts.headers = { Authorization: 'Bearer ' + ghToken(), Accept: 'application/vnd.github+json' };
    return fetch('https://api.github.com/repos/' + historyCfg().repo + path, opts).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (r.ok) return j;
        if (r.status === 401) throw new Error('token not accepted, set it again');
        if (r.status === 403 || r.status === 404) throw new Error('no write access with this token (' + r.status + ')');
        throw new Error(j.message || 'GitHub ' + r.status);
      });
    });
  }

  function b64decode(s) {
    var bin = atob(s.replace(/\s/g, '')), bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder().decode(bytes);
  }

  function b64encode(str) {
    var bytes = new TextEncoder().encode(str), bin = '';
    for (var i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
    return btoa(bin);
  }

  // Refuses to save when the file on GitHub is no longer the one this edit started from.
  function saveHtml(id, base, html, message) {
    var cfg = historyCfg(), path = 'slides/' + id + '.html', branch = cfg.branch || 'main';
    return gh('/contents/' + path + '?ref=' + encodeURIComponent(branch)).then(function (cur) {
      if (norm(b64decode(cur.content)) !== norm(base)) {
        throw new Error('someone changed this slide on GitHub in the meantime. Copy your text, press Cancel, wait a minute and Reload');
      }
      return gh('/contents/' + path, {
        method: 'PUT',
        body: JSON.stringify({ message: message, content: b64encode(html), sha: cur.sha, branch: branch })
      });
    }).then(function (res) {
      state.saved[id] = html;
      var i = state.slides.findIndex(function (s) { return s.id === id; });
      if (i >= 0) state.slides[i] = parseSlide(id, html);
      delete state.versions[id];
      try { sessionStorage.removeItem('versions:' + cfg.repo + ':' + id); } catch (e) {}
      $('version').dataset.slide = '';
      return res.commit.sha.slice(0, 7);
    });
  }

  function escapeHtml(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  // Patches only the changed text in the original file, so the rest of the HTML stays byte-identical.
  // Falls back to re-serialising the slide when a changed text cannot be found in the file.
  function collectEdits() {
    var ed = state.editing, raw = ed.base.replace(/\r\n/g, '\n');
    var tpl = document.createElement('template');
    tpl.innerHTML = raw.trim();
    var sec = tpl.content.querySelector('section');
    markEditable(sec);
    var patches = [], pos = 0, located = true;
    sec.querySelectorAll('[data-eid]').forEach(function (src) {
      var el = $('stage').querySelector('[data-eid="' + src.dataset.eid + '"]');
      var changed = el && el.innerHTML !== ed.orig[src.dataset.eid];
      var at = raw.indexOf('>' + src.innerHTML + '</' + src.tagName.toLowerCase(), pos);
      if (at < 0) { if (changed) located = false; return; }
      pos = at + 1 + src.innerHTML.length;
      if (changed) patches.push([at + 1, pos, el.innerHTML]);
      src.innerHTML = el ? el.innerHTML : src.innerHTML;
    });
    var out;
    if (located) {
      out = raw;
      for (var i = patches.length - 1; i >= 0; i--) out = out.slice(0, patches[i][0]) + patches[i][2] + out.slice(patches[i][1]);
    } else {
      sec.querySelectorAll('[data-eid]').forEach(function (el) { el.removeAttribute('data-eid'); });
      out = tpl.innerHTML + '\n';
    }
    var notes = norm($('notes').innerText), notesChanged = notes !== norm(ed.notes);
    if (notesChanged) {
      var m = /<aside\b[^>]*>([\s\S]*?)(?=<\/aside>|<\/section>)/i.exec(out);
      if (m) {
        var from = m.index + m[0].length - m[1].length;
        out = out.slice(0, from) + escapeHtml(notes) + out.slice(from + m[1].length);
      } else {
        var end = out.lastIndexOf('</section>');
        out = out.slice(0, end) + '  <aside>' + escapeHtml(notes) + '</aside>\n' + out.slice(end);
      }
    }
    return (patches.length || !located || notesChanged) ? out : null;
  }

  function setEditUi() {
    var on = !!state.editing;
    $('btnEdit').hidden = !canEditOnline() || on;
    $('btnSave').hidden = !on;
    $('btnCancel').hidden = !on;
    $('btnPresent').disabled = on;
    $('btnReload').disabled = on;
    $('version').disabled = on;
    $('btnRestore').textContent = canEditOnline() ? 'Restore this version' : 'Copy restore request';
  }

  function startEdit() {
    var s = state.slides[state.index];
    if (!s) return;
    if (state.view) { setStatus('Switch the Version menu to "Current file" to edit'); return; }
    state.editing = { id: s.id, base: s.html, notes: s.notes, orig: {} };
    renderStage();
    setStatus('Editing: click a text on the slide or the notes');
  }

  function stopEdit() {
    state.editing = null;
    renderStage();
  }

  // Returns false when the user wants to keep unsaved edits.
  function leaveEdit() {
    if (!state.editing) return true;
    if (collectEdits() && !confirm('Discard your unsaved edits on this slide?')) return false;
    state.editing = null;
    return true;
  }

  function saveEdit() {
    var ed = state.editing, html = collectEdits();
    if (!html) { stopEdit(); setStatus('No changes'); return; }
    if (!ghToken()) { openTokenDialog(saveEdit); return; }
    setStatus('Saving…');
    $('btnSave').disabled = true;
    saveHtml(ed.id, ed.base, html, 'Edit slide ' + ed.id + ' in viewer').then(function (sha) {
      $('btnSave').disabled = false;
      state.editing = null;
      renderRail();
      renderStage();
      setStatus('Saved as commit ' + sha + ' · live for everyone in about 1 min');
    }).catch(function (err) {
      $('btnSave').disabled = false;
      setStatus('Not saved: ' + err.message);
    });
  }

  function restoreVersion() {
    var v = state.view, cur = state.slides[state.index];
    if (!v) return;
    if (!canEditOnline()) {
      var text = 'Restore slides/' + v.id + '.html to the version in commit ' + v.sha.slice(0, 7) +
        ' (file ' + v.path + ' at that commit). Follow STYLE.md.';
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { setStatus('Copied restore request'); });
      return;
    }
    if (!ghToken()) { openTokenDialog(restoreVersion); return; }
    if (!confirm('Replace the current slide with version ' + v.sha.slice(0, 7) + '? This creates a new commit; nothing is lost.')) return;
    setStatus('Restoring…');
    saveHtml(cur.id, cur.html, v.html, 'Restore slide ' + cur.id + ' to ' + v.sha.slice(0, 7) + ' in viewer').then(function (sha) {
      state.view = null;
      renderRail();
      renderStage();
      setStatus('Restored as commit ' + sha + ' · live for everyone in about 1 min');
    }).catch(function (err) { setStatus('Not restored: ' + err.message); });
  }

  function openTokenDialog(then) {
    var dlg = $('tokenDlg');
    $('tokenInput').value = '';
    $('tokenForget').hidden = !ghToken();
    dlg.onclose = function () {
      if (dlg.returnValue === 'forget') { try { localStorage.removeItem('gh-token'); } catch (e) {} setStatus('Token removed from this browser'); return; }
      var t = $('tokenInput').value.trim();
      if (dlg.returnValue !== 'ok' || !t) return;
      try { localStorage.setItem('gh-token', t); } catch (e) { setStatus('This browser blocks saving the token'); return; }
      if (then) then();
    };
    dlg.showModal();
  }

  function renderStage() {
    var cur = state.slides[state.index];
    if (!cur) return;
    if (state.view && state.view.id !== cur.id) state.view = null;
    if (state.editing && state.editing.id !== cur.id) state.editing = null;
    var s = state.view || cur;
    var stage = $('stage');
    stage.innerHTML = '';
    var canvas = buildCanvas(s, { editable: !!state.editing });
    if (state.editing) {
      canvas.classList.add('editing');
      canvas.querySelectorAll('[data-eid]').forEach(function (el) {
        state.editing.orig[el.dataset.eid] = el.innerHTML;
        el.contentEditable = 'true';
      });
    }
    stage.appendChild(canvas);
    fit(stage, canvas);
    var n = slideNumber(state.index);
    $('slideNo').textContent = (n === null ? 'Hidden slide' : 'Slide ' + n) + ' · ' + s.title;
    $('slidePath').textContent = 'slides/' + s.id + '.html';
    $('hiddenBadge').hidden = !s.hidden;
    $('notes').textContent = state.editing ? s.notes : (s.notes || '(no notes)');
    try { $('notes').contentEditable = state.editing ? 'plaintext-only' : 'false'; }
    catch (e) { $('notes').contentEditable = state.editing ? 'true' : 'false'; }
    setEditUi();
    $('versionBadge').hidden = !state.view;
    $('btnRestore').hidden = !state.view;
    if (state.view) $('versionBadge').textContent = 'Old version ' + state.view.sha.slice(0, 7) + ' · view only';
    updateVersionMenu();
    requestAnimationFrame(function () { fit(stage, canvas); });
    document.querySelectorAll('.thumb').forEach(function (t, i) { t.classList.toggle('active', i === state.index); });
    var active = document.querySelectorAll('.thumb')[state.index];
    if (active && active.scrollIntoView) active.scrollIntoView({ block: 'nearest' });
  }

  function select(i) {
    if (i < 0 || i >= state.slides.length) return;
    if (i !== state.index && !leaveEdit()) return;
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
    var vis = visibleIndices();
    $('pcount').textContent = (vis.indexOf(state.index) + 1) + ' / ' + vis.length;
  }

  function startPresent() {
    if (state.editing) return;
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
    } else {
      select(state.index + delta);
    }
  }

  // Loading and live reload
  function apply(data, keepId) {
    state.deck = data.deck;
    state.signature = data.signature;
    // GitHub Pages needs about a minute after a save; until then keep showing the saved text.
    state.slides = data.deck.order.map(function (id, i) {
      var saved = state.saved[id];
      if (saved != null && data.texts[i] != null && norm(data.texts[i]) === norm(saved)) delete state.saved[id];
      return parseSlide(id, state.saved[id] != null ? state.saved[id] : data.texts[i]);
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
    if (state.editing) return Promise.resolve();
    var keep = state.slides[state.index] && state.slides[state.index].id;
    return loadAll().then(function (data) {
      if (silent && data.signature === state.signature) return;
      apply(data, keep);
      setStatus('Updated ' + new Date().toLocaleTimeString());
    }).catch(function (err) { setStatus('Load error: ' + err.message); });
  }

  function setStatus(msg) { $('status').textContent = msg; }

  function bind() {
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
    $('btnRestore').addEventListener('click', restoreVersion);
    $('btnEdit').addEventListener('click', startEdit);
    $('btnSave').addEventListener('click', saveEdit);
    $('btnCancel').addEventListener('click', function () { if (leaveEdit()) { renderStage(); setStatus(''); } });
    // Plain text only, and Enter makes a line break instead of a new block.
    $('stage').addEventListener('paste', function (e) {
      if (!state.editing) return;
      e.preventDefault();
      document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain'));
    });
    $('stage').addEventListener('keydown', function (e) {
      if (state.editing && e.key === 'Enter') { e.preventDefault(); document.execCommand('insertLineBreak'); }
    });
    window.addEventListener('beforeunload', function (e) {
      if (state.editing && collectEdits()) { e.preventDefault(); e.returnValue = ''; }
    });
    document.addEventListener('keydown', function (e) {
      if (e.target && (/INPUT|TEXTAREA|SELECT/.test(e.target.tagName) || e.target.isContentEditable)) return;
      var k = e.key;
      if (state.presenting) {
        if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || k === ' ' || k === 'Enter') { e.preventDefault(); step(1); }
        else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp' || k === 'Backspace') { e.preventDefault(); step(-1); }
        else if (k === 'Home') { var v = visibleIndices(); state.index = v[0]; renderPresent(); }
        else if (k === 'End') { var w = visibleIndices(); state.index = w[w.length - 1]; renderPresent(); }
        else if (k === 'n' || k === 'N') { $('pnotes').hidden = !$('pnotes').hidden; }
        else if (k === 'Escape') { stopPresent(); }
        return;
      }
      if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown') { e.preventDefault(); step(1); }
      else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp') { e.preventDefault(); step(-1); }
      else if (k === 'p' || k === 'P') { startPresent(); }
      else if (k === 'r' || k === 'R') { reload(false); }
    });
    window.addEventListener('hashchange', function () {
      var id = decodeURIComponent(location.hash.replace(/^#/, ''));
      var i = state.slides.findIndex(function (s) { return s.id === id; });
      if (i < 0 || i === state.index) return;
      if (!leaveEdit()) { history.replaceState(null, '', '#' + state.slides[state.index].id); return; }
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
  }).catch(function (err) {
    setStatus('Load error: ' + err.message + ' (open via a local web server, see README)');
  });
})();
