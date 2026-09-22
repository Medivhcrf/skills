/* ---------- 单词发音：优先预生成的神经语音 MP3，缺失/失败才回退系统语音 ---------- */
(function () {
  var ICON_SPEAKER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>';

  var synth = ("speechSynthesis" in window) ? window.speechSynthesis : null;
  var audio = new Audio();
  audio.preload = "auto";
  audio.playbackRate = 0.95;
  var curBtn = null;
  var token = 0;

  /* ── 为什么是「MP3 优先」而不是「系统语音优先」 ─────────────────────────
     Windows 中文系统上，浏览器里的 speechSynthesis 只有老式 SAPI5 语音
     （Microsoft David / Zira / Huihui），默认英文语音是 David = 生硬男声。
     而 words-audio/ 里是 edge-tts 生成的神经语音（自然女声）。
     所以有 MP3 就必须用 MP3，系统语音只作为「没有 MP3 时的兜底」。
     反面教材：2026-09 曾经改成 hasSystemVoice() 优先，结果一点击发音
     就出机械男声，好几个页面都是这个毛病。不要改回去。 */
  function liveVoices() {
    if (!synth) return [];
    try { return (synth.getVoices() || []); } catch (e) { return []; }
  }
  function hasSystemVoice() {
    if (!synth) return false;
    if (liveVoices().some(function (v) { return /^en/i.test(v.lang); })) return true;
    return /iP(hone|ad|od)|Android/i.test(navigator.userAgent || "");
  }
  function tts(text, onend) {
    if (!synth || !hasSystemVoice()) return false;
    /* 不指定具体 voice，交给系统用「默认英文语音」（即用户在系统里选好的那个） */
    var u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US";
    if (onend) u.onend = onend;
    try { synth.cancel(); } catch (e) {}
    synth.speak(u);
    return true;
  }
  function clear() {
    if (curBtn) { curBtn.classList.remove("playing"); curBtn = null; }
  }
  function speakTTS(text, btn) {
    if (!tts(text, function () { if (curBtn === btn) clear(); })) clear();
  }
  function playAudio(src, text, btn) {
    var my = ++token;
    audio.onended = null; audio.onerror = null;
    audio.src = src;
    audio.onended = function () { if (my === token) clear(); };
    audio.onerror = function () {          /* 音频缺失 / 播放失败 → 回退系统语音 */
      if (my !== token) return;
      audio.onerror = null;
      if (!tts(text, function () { if (curBtn === btn) clear(); })) clear();
    };
    var p = audio.play();
    if (p && p.catch) {
      p.catch(function () {
        if (my !== token) return;
        audio.onerror = null;
        if (!tts(text, function () { if (curBtn === btn) clear(); })) clear();
      });
    }
  }
  function play(el, btn) {
    var src = el.getAttribute("data-say");
    var text = el.textContent.replace(/\s+/g, " ").trim();
    clear();
    if (btn) { btn.classList.add("playing"); curBtn = btn; }
    if (src) {
      playAudio(src, text, btn);            /* 有预生成音频就用它（自然语音） */
    } else if (!tts(text, function () { if (curBtn === btn) clear(); })) {
      clear();                              /* 既没音频也没系统语音 */
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
