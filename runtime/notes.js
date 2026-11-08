// Turns plain speaker notes into readable HTML: one block per "LABEL:" section,
// numbered and dash lines as lists, quoted sentences as the spoken text, the rest of SAY lines as italic directions.
window.DeckNotes = (function () {
  'use strict';

  var LABEL = /^([A-Z][A-Z \/&\-]{1,30}):\s*(.*)$/;

  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  // Labels inside a running line, e.g. "TIME:" after the speaker name or labels in older one-line notes.
  function inlineLabels(s) {
    return s.replace(/(^|[\s.])((?:[A-Z][A-Z\/&\-]+ ){0,3}[A-Z][A-Z\/&\-]{2,}):/g, '$1<b class="n-inline">$2:</b>');
  }

  // Quoted parts are what the speaker says; text outside quotes is a stage direction.
  function sayLine(s) {
    var parts = esc(s).split('"');
    if (parts.length < 3) return '<em class="n-dir">' + parts.join('"') + '</em>';
    return parts.map(function (p, i) {
      if (i % 2) return '<span class="n-quote">“' + p + '”</span>';
      return p.trim() ? '<em class="n-dir">' + p + '</em>' : p;
    }).join('');
  }

  function html(text) {
    var lines = String(text || '').replace(/\r/g, '').split('\n');
    var out = [], key = null, list = null;
    function closeList() { if (list) { out.push('</' + list + '>'); list = null; } }
    function closeSec() { closeList(); if (key) { out.push('</div>'); key = null; } }
    function item(kind, content) {
      if (list !== kind) { closeList(); out.push('<' + kind + '>'); list = kind; }
      out.push('<li>' + content + '</li>');
    }
    lines.forEach(function (raw) {
      var line = raw.trim();
      if (!line) return;
      var m = LABEL.exec(line);
      if (m) {
        closeSec();
        key = m[1].toLowerCase().replace(/[^a-z]+/g, '-');
        out.push('<div class="n-sec n-' + key + '"><span class="n-label">' + esc(m[1]) + '</span>');
        if (m[2]) out.push('<p>' + (key === 'say' ? sayLine(m[2]) : inlineLabels(esc(m[2]))) + '</p>');
        return;
      }
      var num = /^\((\d+)\)\s*(.*)$/.exec(line), dash = /^-\s+(.*)$/.exec(line);
      if (num) return item('ol', key === 'say' ? sayLine(num[2]) : inlineLabels(esc(num[2])));
      if (dash) return item('ul', inlineLabels(esc(dash[1])));
      closeList();
      out.push('<p>' + (key === 'say' ? sayLine(line) : inlineLabels(esc(line))) + '</p>');
    });
    closeSec();
    return out.join('');
  }

  return { html: html };
})();
