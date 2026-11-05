// Room sync for Present mode and the presenter page. Uses the public relay ntfy.sh;
// only the current slide id and the timer state are sent.
window.DeckSync = (function () {
  'use strict';

  var BASE = 'https://ntfy.sh/';
  var me = Math.random().toString(36).slice(2, 10);

  function topic(room) { return 'hilegal-deck-' + room; }

  function newRoom() {
    var abc = 'abcdefghjkmnpqrstuvwxyz23456789', bytes = crypto.getRandomValues(new Uint8Array(8)), s = '';
    for (var i = 0; i < bytes.length; i++) s += abc[bytes[i] % abc.length];
    return s;
  }

  function roomFromUrl() {
    var m = /[?&]room=([a-z0-9]{4,32})/i.exec(location.search);
    return m ? m[1].toLowerCase() : '';
  }

  // Elapsed timer time in ms for a received state.
  function elapsedOf(st) {
    if (!st) return 0;
    return st.elapsed + (st.running ? Date.now() - st.receivedAt : 0);
  }

  // onState(state, isOwnEcho), onStatus(connected)
  function connect(room, onState, onStatus) {
    var t = topic(room), lastTime = 0, seen = {}, seq = 0, es = null, pollTimer = null;

    function handle(m) {
      if (!m || m.event !== 'message' || seen[m.id] || m.time < lastTime) return;
      seen[m.id] = true;
      lastTime = m.time;
      var st;
      try { st = JSON.parse(m.message); } catch (e) { return; }
      if (!st || st.v !== 1) return;
      // ntfy time has 1 s resolution: treat fresh messages as instant, add the age of older ones.
      var age = Date.now() - m.time * 1000;
      if (st.running && age > 2000) st.elapsed += age;
      st.receivedAt = Date.now();
      onState(st, st.by === me);
    }

    function poll() {
      return fetch(BASE + t + '/json?poll=1&since=12h').then(function (r) { return r.text(); }).then(function (txt) {
        var lines = txt.trim().split('\n').filter(Boolean);
        if (lines.length) handle(JSON.parse(lines[lines.length - 1]));
      }).catch(function () {});
    }

    function open() {
      es = new EventSource(BASE + t + '/sse');
      es.onopen = function () { onStatus(true); poll(); };
      es.onmessage = function (e) { try { handle(JSON.parse(e.data)); } catch (x) {} };
      es.onerror = function () { onStatus(false); };
    }

    poll();
    open();
    // Safety net if the live connection silently stalls.
    pollTimer = setInterval(poll, 15000);

    return {
      send: function (st) {
        var body = JSON.stringify({ v: 1, by: me, seq: ++seq, slide: st.slide, running: !!st.running, elapsed: Math.round(st.elapsed || 0) });
        return fetch(BASE + t, { method: 'POST', body: body }).catch(function () { onStatus(false); });
      },
      close: function () { if (es) es.close(); clearInterval(pollTimer); }
    };
  }

  return { connect: connect, newRoom: newRoom, roomFromUrl: roomFromUrl, elapsedOf: elapsedOf };
})();
