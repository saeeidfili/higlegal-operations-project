// Deck viewer: edit view (slide list, stage, notes) and present mode.
// Slides live in slides/<id>.html; order and title come from deck.json.
(function () {
  'use strict';

  var SVG_NS = 'http://www.w3.org/2000/svg';
  var state = { deck: null, slides: [], index: 0, presenting: false, signature: '' };
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

  function renderStage() {
    var s = state.slides[state.index];
    if (!s) return;
    var stage = $('stage');
    stage.innerHTML = '';
    var canvas = buildCanvas(s);
    stage.appendChild(canvas);
    fit(stage, canvas);
    var n = slideNumber(state.index);
    $('slideNo').textContent = (n === null ? 'Hidden slide' : 'Slide ' + n) + ' · ' + s.title;
    $('slidePath').textContent = 'slides/' + s.id + '.html';
    $('hiddenBadge').hidden = !s.hidden;
    $('notes').textContent = s.notes || '(no notes)';
    requestAnimationFrame(function () { fit(stage, canvas); });
    document.querySelectorAll('.thumb').forEach(function (t, i) { t.classList.toggle('active', i === state.index); });
    var active = document.querySelectorAll('.thumb')[state.index];
    if (active && active.scrollIntoView) active.scrollIntoView({ block: 'nearest' });
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
    var vis = visibleIndices();
    $('pcount').textContent = (vis.indexOf(state.index) + 1) + ' / ' + vis.length;
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
    } else {
      select(state.index + delta);
    }
  }

  // Loading and live reload
  function apply(data, keepId) {
    state.deck = data.deck;
    state.signature = data.signature;
    state.slides = data.deck.order.map(function (id, i) { return parseSlide(id, data.texts[i]); });
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

  function bind() {
    $('btnPresent').addEventListener('click', startPresent);
    $('btnReload').addEventListener('click', function () { reload(false); });
    $('btnCopy').addEventListener('click', function () {
      var path = $('slidePath').textContent;
      if (navigator.clipboard) navigator.clipboard.writeText(path).then(function () { setStatus('Copied ' + path); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.target && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
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
