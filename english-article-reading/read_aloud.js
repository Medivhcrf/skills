/* ra-js-start */
/* ---------- 朗读：优先系统语音（电脑/手机自带），无系统语音时才用预生成音频 ---------- */
(function () {
  var ICON_SPEAKER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>';
  var ICON_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><path d="M7 5v14l12-7z"/></svg>';
  var ICON_PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><rect x="6.5" y="5" width="3.5" height="14" rx="1"/><rect x="14" y="5" width="3.5" height="14" rx="1"/></svg>';
  var ICON_STOP = '<svg viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>';

  var sents = Array.prototype.slice.call(document.querySelectorAll(".speech .sent"));
  /* 注意：**不要**在没有 .sent 时直接 return —— 词源表单词与名言金句也要挂 🔊，
     一旦早退，只有词表/金句的片段页（或节选页）就会整个失效。
     只有底部「朗读全文」才真正依赖句子，见下面的 sents.length 判断。 */

  var synth = ("speechSynthesis" in window) ? window.speechSynthesis : null;
  var audio = new Audio();
  audio.preload = "auto";

  var rate = 0.95, playing = false, paused = false, idx = 0;
  var currentBtn = null, mode = null;

  function liveVoices() {
    if (!synth) return [];
    try { return (synth.getVoices() || []); } catch (e) { return []; }
  }
  function hasSystemVoice() {
    if (!synth) return false;
    if (liveVoices().some(function (v) { return /^en/i.test(v.lang); })) return true;
    /* iOS / Android 的系统语音常不列在 getVoices() 里，但确实可用 */
    return /iP(hone|ad|od)|Android/i.test(navigator.userAgent || "");
  }
  function utter(text) {
    /* 不指定具体 voice，交给系统用「默认英文语音」（即用户在系统里选好的那个） */
    var u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US"; u.rate = rate;
    return u;
  }
  function strip(sent) {
    var c = sent.cloneNode(true);
    c.querySelectorAll(".brk,.sup,.pnum,.say").forEach(function (n) { n.parentNode.removeChild(n); });
    return c.textContent.replace(/\s+/g, " ").replace(/\s+([.,!?;:])/g, "$1").trim();
  }
  function mark(btn) { clearMark(); if (btn) { btn.classList.add("speaking"); currentBtn = btn; } }
  function clearMark() { if (currentBtn) currentBtn.classList.remove("speaking"); currentBtn = null; }

  function stopAll() {
    playing = false; paused = false;
    try { audio.pause(); } catch (e) {}
    if (synth) { try { synth.cancel(); } catch (e) {} }
    clearMark(); updateBar();
  }
  function playAudio(sent, done) {
    var src = sent.getAttribute("data-audio");
    if (!src) { done(); return; }
    mode = "audio";
    audio.src = src;
    audio.playbackRate = rate;
    audio.onended = function () { audio.onended = null; audio.onerror = null; done(); };
    audio.onerror = function () { audio.onerror = null; done(); };
    var p = audio.play();
    if (p && p.catch) { p.catch(function () { done(); }); }
  }
  function speakTTS(sent, done) {
    if (!synth) { playAudio(sent, done); return; }
    mode = "tts";
    var u = utter(strip(sent));
    u.onend = done;
    u.onerror = function () { playAudio(sent, done); };
    synth.speak(u);
  }
  function speakSentence(sent, btn, done) {
    mark(btn);
    try { sent.scrollIntoView({ behavior: "smooth", block: "center" }); } catch (e) {}
    if (hasSystemVoice()) { speakTTS(sent, done); }
    else { playAudio(sent, done); }
  }

  function playAll() {
    stopAll();
    playing = true; paused = false; idx = 0;
    updateBar(); next();
  }
  function next() {
    if (!playing) return;
    if (idx >= sents.length) { stopAll(); return; }
    var sent = sents[idx], btn = sent.querySelector(".say");
    speakSentence(sent, btn, function () {
      if (!playing) return;
      clearMark(); idx++; next();
    });
  }

  sents.forEach(function (sent) {
    var b = makeSayBtn(sent);
    var p = sent.querySelector(".pnum");
    if (p) p.parentNode.insertBefore(b, p.nextSibling);
    else sent.insertBefore(b, sent.firstChild);
  });

  /* 词源表的单词、名言金句也挂 🔊：优先系统语音，缺失时回放预生成的 MP3。
     与逐句朗读同一套逻辑，只是按钮更小、跟在词/句后面。 */
  function inlineSay(el) {
    var b = makeSayBtn(el);
    el.parentNode.insertBefore(b, el.nextSibling);
  }
  Array.prototype.forEach.call(document.querySelectorAll("b.w"), inlineSay);
  Array.prototype.forEach.call(document.querySelectorAll(".card .head .t.quote"), inlineSay);

  function makeSayBtn(target) {
    var b = document.createElement("button");
    b.type = "button"; b.className = "say";
    b.innerHTML = ICON_SPEAKER;
    b.title = "朗读"; b.setAttribute("aria-label", "朗读");
    b.addEventListener("click", function (e) {
      e.stopPropagation(); e.preventDefault();
      if (b.classList.contains("speaking")) { stopAll(); return; }
      stopAll();
      speakSentence(target, b, function () { if (currentBtn === b) clearMark(); });
    });
    return b;
  }

  /* 底部「朗读全文」控制条只在有逐句内容时出现；没有句子时 updateBar 安全返回 */
  var bar = null;
  function updateBar() {
    if (!bar) return;
    var pb = bar.querySelector('[data-act="play"]');
    pb.innerHTML = (playing && !paused) ? (ICON_PAUSE + " 暂停")
                 : (paused ? (ICON_PLAY + " 继续") : (ICON_PLAY + " 朗读全文"));
  }
  if (sents.length) {
    bar = document.createElement("div");
    bar.id = "tts-bar";
    bar.innerHTML = '<button data-act="play">' + ICON_PLAY + ' 朗读全文</button>' +
                    '<button data-act="stop">' + ICON_STOP + ' 停止</button>' +
                    '<button data-act="rate" class="rate">0.95\u00D7</button>';
    document.body.appendChild(bar);
    bar.addEventListener("click", function (e) {
      var btn = e.target.closest ? e.target.closest("button") : null;
      if (!btn) return;
      var act = btn.getAttribute("data-act");
      if (act === "play") {
        if (playing && !paused) {
          paused = true;
          if (mode === "audio") { try { audio.pause(); } catch (err) {} }
          if (synth && synth.speaking) { try { synth.pause(); } catch (err) {} }
          updateBar();
        } else if (playing && paused) {
          paused = false;
          if (mode === "audio") { try { audio.play(); } catch (err) {} }
          if (synth && synth.paused) { try { synth.resume(); } catch (err) {} }
          updateBar();
        } else { playAll(); }
      } else if (act === "stop") {
        stopAll();
      } else if (act === "rate") {
        rate = rate >= 1.3 ? 0.8 : Math.round((rate + 0.1) * 100) / 100;
        btn.textContent = rate.toFixed(2) + "\u00D7";
        audio.playbackRate = rate;
      }
    });
  }
})();
/* ra-js-end */
