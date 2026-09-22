/* ---------- 单词发音：优先系统语音，无系统语音时用预生成音频 ---------- */
(function () {
  var ICON_SPEAKER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>';

  var synth = ("speechSynthesis" in window) ? window.speechSynthesis : null;
  var audio = new Audio();
  audio.preload = "auto";
  audio.playbackRate = 0.95;
  var curBtn = null;
  var sysVoices = [];

  function refreshVoices() {
    if (!synth) return;
    try { sysVoices = (synth.getVoices() || []).filter(function (v) { return /^en/i.test(v.lang); }); }
    catch (e) { sysVoices = []; }
  }
  function hasSystemVoice() { return sysVoices.length > 0; }
  if (synth) {
    refreshVoices();
    if (synth.onvoiceschanged !== undefined) { synth.onvoiceschanged = refreshVoices; }
    setTimeout(refreshVoices, 600);
    setTimeout(refreshVoices, 1800);
  }

  function pickVoice() {
    var us = sysVoices.filter(function (v) { return /en[-_]US/i.test(v.lang); });
    return (us[0] || sysVoices[0] || null);
  }
  function tts(text) {
    if (!synth || !hasSystemVoice()) return false;
    var u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US";
    var v = pickVoice(); if (v) u.voice = v;
    try { synth.cancel(); } catch (e) {}
    synth.speak(u);
    return true;
  }
  function clear() { if (curBtn) { curBtn.classList.remove("playing"); curBtn = null; } }
  function playAudio(src, text, btn) {
    if (!src) { if (btn) clear(); return; }
    audio.src = src;
    audio.onended = function () { if (curBtn === btn) clear(); };
    audio.onerror = function () { if (curBtn === btn) clear(); };
    var p = audio.play();
    if (p && p.catch) { p.catch(function () { if (curBtn === btn) clear(); }); }
  }
  function play(el, btn) {
    var src = el.getAttribute("data-say");
    var text = el.textContent.replace(/\s+/g, " ").trim();
    clear();
    if (btn) { btn.classList.add("playing"); curBtn = btn; }
    if (hasSystemVoice()) {
      if (!tts(text)) { playAudio(src, text, btn); }
      else { setTimeout(function () { if (curBtn === btn) clear(); }, Math.max(1200, text.length * 80)); }
    } else {
      playAudio(src, text, btn);
    }
  }

  document.querySelectorAll("[data-say]").forEach(function (el) {
    var prev = el.previousElementSibling;
    if (prev && prev.classList && prev.classList.contains("psay")) return;
    var b = document.createElement("button");
    b.type = "button"; b.className = "psay"; b.innerHTML = ICON_SPEAKER; b.title = "发音";
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
  tg.id = "pron-toggle"; tg.type = "button";
  tg.innerHTML = ICON_SPEAKER + '<span>点词发音</span>';
  document.body.appendChild(tg);
  tg.addEventListener("click", function () {
    on = !on; tg.classList.toggle("on", on);
    tg.querySelector("span").textContent = on ? "点词发音：开" : "点词发音";
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
