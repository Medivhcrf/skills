/* ---------- 单词发音 ---------- */
(function () {
  var synth = ("speechSynthesis" in window) ? window.speechSynthesis : null;
  var audio = new Audio();
  audio.preload = "auto";
  audio.playbackRate = 0.95;
  var curBtn = null;

  function pickVoice() {
    if (!synth) return null;
    var vs = synth.getVoices() || [];
    return vs.filter(function (v) { return /en[-_]US/i.test(v.lang); })[0] ||
           vs.filter(function (v) { return /^en/i.test(v.lang); })[0] || null;
  }
  function tts(text) {
    if (!synth) return;
    var u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US";
    var v = pickVoice(); if (v) u.voice = v;
    try { synth.cancel(); } catch (e) {}
    synth.speak(u);
  }
  function clear() { if (curBtn) { curBtn.classList.remove("playing"); curBtn = null; } }
  function play(el, btn) {
    var src = el.getAttribute("data-say");
    var text = el.textContent.replace(/\s+/g, " ").trim();
    clear();
    if (btn) { btn.classList.add("playing"); curBtn = btn; }
    if (src) {
      audio.src = src;
      audio.onended = function () { if (curBtn === btn) clear(); };
      audio.onerror = function () { if (curBtn === btn) clear(); tts(text); };
      var p = audio.play();
      if (p && p.catch) { p.catch(function () { clear(); tts(text); }); }
    } else {
      tts(text);
      setTimeout(function () { if (curBtn === btn) clear(); }, 1500);
    }
  }

  document.querySelectorAll("[data-say]").forEach(function (el) {
    var prev = el.previousElementSibling;
    if (prev && prev.classList && prev.classList.contains("psay")) return;
    var b = document.createElement("button");
    b.type = "button"; b.className = "psay"; b.textContent = "\uD83D\uDD0A"; b.title = "发音";
    b.setAttribute("aria-label", "发音");
    b.addEventListener("click", function (e) {
      e.stopPropagation(); e.preventDefault();
      if (curBtn === b) {
        try { audio.pause(); } catch (err) {}
        if (synth) { try { synth.cancel(); } catch (err) {} }
        clear(); return;
      }
      play(el, b);
    });
    el.parentNode.insertBefore(b, el);
  });

  /* 点任意英文词发音 */
  var on = false;
  var tg = document.createElement("button");
  tg.id = "pron-toggle"; tg.type = "button"; tg.textContent = "\uD83D\uDD24 点词发音";
  document.body.appendChild(tg);
  tg.addEventListener("click", function () {
    on = !on; tg.classList.toggle("on", on);
    tg.textContent = on ? "\uD83D\uDD24 点词发音：开" : "\uD83D\uDD24 点词发音";
  });
  function wordAt(x, y) {
    var node, offset;
    if (document.caretRangeFromPoint) {
      var r = document.caretRangeFromPoint(x, y);
      if (!r) return null; node = r.startContainer; offset = r.startOffset;
    } else if (document.caretPositionFromPoint) {
      var p = document.caretPositionFromPoint(x, y);
      if (!p) return null; node = p.offsetNode; offset = p.offset;
    } else { return null; }
    if (!node || node.nodeType !== 3) return null;
    var t = node.textContent, re = /[A-Za-z][A-Za-z'\u2019\-]*/g, m;
    while ((m = re.exec(t))) {
      if (offset >= m.index && offset <= m.index + m[0].length) return m[0];
    }
    return null;
  }
  document.addEventListener("click", function (e) {
    if (!on) return;
    if (e.target.closest && (e.target.closest(".psay") || e.target.closest("#pron-toggle"))) return;
    var w = wordAt(e.clientX, e.clientY);
    if (w) tts(w);
  }, true);
})();
