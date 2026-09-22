/* ---------- 朗读：优先播放预生成音频(data-audio)，否则用系统语音 ---------- */
(function () {
  var sents = Array.prototype.slice.call(document.querySelectorAll(".speech .sent"));
  if (!sents.length) return;

  var synth = ("speechSynthesis" in window) ? window.speechSynthesis : null;
  var audio = new Audio();
  audio.preload = "auto";

  var rate = 0.95, playing = false, paused = false, idx = 0;
  var currentBtn = null, mode = null;

  function strip(sent) {
    var c = sent.cloneNode(true);
    c.querySelectorAll(".brk,.sup,.pnum,.say").forEach(function (n) {
      n.parentNode.removeChild(n);
    });
    return c.textContent.replace(/\s+/g, " ").replace(/\s+([.,!?;:])/g, "$1").trim();
  }
  function pickVoice() {
    if (!synth) return null;
    var vs = synth.getVoices() || [];
    var en = vs.filter(function (v) { return /^en/i.test(v.lang); });
    var us = en.filter(function (v) { return /en[-_]US/i.test(v.lang); });
    return (us[0] || en[0] || null);
  }
  function utter(text) {
    var u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US"; u.rate = rate;
    var v = pickVoice(); if (v) u.voice = v;
    return u;
  }
  function mark(btn) { clearMark(); if (btn) { btn.classList.add("speaking"); currentBtn = btn; } }
  function clearMark() { if (currentBtn) currentBtn.classList.remove("speaking"); currentBtn = null; }

  function stopAll() {
    playing = false; paused = false;
    try { audio.pause(); } catch (e) {}
    if (synth) { try { synth.cancel(); } catch (e) {} }
    clearMark(); updateBar();
  }
  function speakTTS(sent, done) {
    if (!synth) { done(); return; }
    mode = "tts";
    var u = utter(strip(sent));
    u.onend = done; u.onerror = done;
    synth.speak(u);
  }
  function speakSentence(sent, btn, done) {
    mark(btn);
    try { sent.scrollIntoView({ behavior: "smooth", block: "center" }); } catch (e) {}
    var src = sent.getAttribute("data-audio");
    if (src) {
      mode = "audio";
      audio.src = src;
      audio.playbackRate = rate;
      audio.onended = function () { audio.onended = null; audio.onerror = null; done(); };
      audio.onerror = function () { audio.onerror = null; speakTTS(sent, done); };
      var p = audio.play();
      if (p && p.catch) { p.catch(function () { audio.onerror = null; speakTTS(sent, done); }); }
    } else {
      speakTTS(sent, done);
    }
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
    var b = document.createElement("button");
    b.type = "button"; b.className = "say";
    b.textContent = "\uD83D\uDD0A";
    b.title = "朗读这句"; b.setAttribute("aria-label", "朗读这句");
    b.addEventListener("click", function (e) {
      e.stopPropagation(); e.preventDefault();
      if (b.classList.contains("speaking")) { stopAll(); return; }
      stopAll();
      speakSentence(sent, b, function () { if (currentBtn === b) clearMark(); });
    });
    var p = sent.querySelector(".pnum");
    if (p) p.parentNode.insertBefore(b, p.nextSibling);
    else sent.insertBefore(b, sent.firstChild);
  });

  var bar = document.createElement("div");
  bar.id = "tts-bar";
  bar.innerHTML = '<button data-act="play">\u25B6 朗读全文</button>' +
                  '<button data-act="stop">\u25A0 停止</button>' +
                  '<button data-act="rate" class="rate">0.95\u00D7</button>';
  document.body.appendChild(bar);
  function updateBar() {
    var pb = bar.querySelector('[data-act="play"]');
    pb.textContent = (playing && !paused) ? "\u23F8 暂停" : (paused ? "\u25B6 继续" : "\u25B6 朗读全文");
  }
  bar.addEventListener("click", function (e) {
    var t = e.target, act = t.getAttribute && t.getAttribute("data-act");
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
      t.textContent = rate.toFixed(2) + "\u00D7";
      audio.playbackRate = rate;
    }
  });

  if (synth && synth.onvoiceschanged !== undefined) { synth.onvoiceschanged = function () {}; }
})();
