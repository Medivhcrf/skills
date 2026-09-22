#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""english-article-reading 技能：把桌面 / A4 精读页转换成手机版。

用法:
    python3 build_mobile.py <输入.html> [输出.html]

- 输入：由 template.html 填好的桌面版精读页；
- 输出：默认与输入同目录，文件名加后缀 `-手机版.html`；
- 转换内容：加 viewport、移动端 CSS、表格转卡片（补 data-label）、
  ①② 词源提示改为「轻点」弹出、加返回顶部按钮。CSS 与 JS 内置在本脚本中。
"""
import io, os, re, sys

if len(sys.argv) < 2:
    sys.exit("用法: python3 build_mobile.py <输入.html> [输出.html]")
SRC = sys.argv[1]
DST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    os.path.dirname(os.path.abspath(SRC)),
    os.path.splitext(os.path.basename(SRC))[0] + "-手机版.html")

src = io.open(SRC, encoding="utf-8").read()
_src_title = re.search(r"<title>(.*?)</title>", src, re.S)
_src_title = _src_title.group(1).strip() if _src_title else "英语文章精读"
MOBILE_TITLE = _src_title + "（手机版）"

# ---- extract body ----
m = re.search(r"<body>(.*)</body>", src, re.S)
assert m, "body not found"
body = m.group(1).strip("\n")
body = re.sub(r"<script\b.*?</script>", "", body, flags=re.S)

MOBILE_CSS = r"""
  :root{
    --bg:#f3f4f8; --card:#ffffff; --ink:#1f2937; --line:#e5e7eb;
    --red:#b91c1c; --red-d:#7f1d1d; --blue:#1e3a8a;
    --pad:14px;
  }
  *{ box-sizing:border-box; margin:0; padding:0;
     -webkit-print-color-adjust:exact; print-color-adjust:exact;
     -webkit-tap-highlight-color:transparent; }
  html{ -webkit-text-size-adjust:100%; scroll-behavior:smooth; }
  body{
    font-family:'Noto Sans CJK SC','Droid Sans Fallback','WenQuanYi Zen Hei',
      -apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;
    font-size:16px; line-height:1.78; color:var(--ink); background:var(--bg);
    max-width:760px; margin:0 auto;
    padding:var(--pad) calc(var(--pad) - 2px) calc(28px + env(safe-area-inset-bottom));
    overflow-wrap:break-word; word-break:break-word;
  }

  /* ---------- header ---------- */
  .header{
    background:linear-gradient(135deg,#7f1d1d,#b91c1c);
    color:#fff; border-radius:14px; padding:16px 16px 14px;
    margin-bottom:14px; box-shadow:0 4px 14px rgba(127,29,29,.18);
  }
  .header h1{ font-size:1.5rem; line-height:1.25; letter-spacing:.5px; }
  .header .sub{ font-size:.86rem; color:#fee2e2; margin-top:4px;
    font-family:'DejaVu Sans',sans-serif; }
  .header .meta{ font-size:.78rem; color:#fecaca; margin-top:6px;
    padding-top:6px; border-top:1px solid rgba(255,255,255,.22); }
  .header .meta b{ color:#fff; }

  /* ---------- section titles ---------- */
  h2.section{
    font-size:1.08rem; color:var(--blue); margin:20px 0 10px;
    padding:2px 0 2px 10px; border-left:5px solid var(--blue);
    line-height:1.4;
  }

  .intro{
    background:#fef2f2; border:1px solid #fecaca; border-radius:12px;
    padding:12px 13px; margin-bottom:12px; font-size:.9rem; color:#7f1d1d;
  }
  .intro b{ color:var(--red); }

  /* ---------- speech ---------- */
  .speech{
    background:var(--card); border:1px solid var(--line); border-radius:14px;
    padding:12px 13px 6px; margin-bottom:14px;
    box-shadow:0 1px 3px rgba(0,0,0,.04);
  }
  .speech .para{ margin:0 0 14px; padding-bottom:12px; border-bottom:1px dashed #eef0f4; }
  .speech .para:last-child{ border-bottom:none; padding-bottom:0; }
  .speech .sent{ margin:8px 0; font-family:'DejaVu Sans','Noto Sans CJK SC',sans-serif; }
  .speech .pnum{
    display:inline-block; background:var(--blue); color:#fff; font-size:.68rem;
    font-weight:bold; border-radius:5px; padding:1px 6px; margin-right:6px;
    vertical-align:1px; letter-spacing:.5px;
  }
  .speech .ck{
    border-radius:3px; padding:1px 2px;
    -webkit-box-decoration-break:clone; box-decoration-break:clone;
  }
  .speech .sup{
    color:var(--red); font-size:.7em; font-weight:bold; vertical-align:super;
    padding:0 2px; cursor:pointer; touch-action:manipulation;
    border-bottom:1px dotted #fca5a5;
  }
  .speech .kw{ color:var(--red); font-weight:bold; border-bottom:1px dotted #fca5a5; }

  /* structure breakdown box */
  .speech .brk{
    margin:8px 0 4px; padding:8px 10px 4px;
    border-left:3px solid #93c5fd; background:#f8fafc;
    border-radius:0 10px 10px 0; font-size:.82rem;
  }
  .speech .brk .bhead{
    font-weight:bold; color:#1d4ed8; font-size:.76rem; margin-bottom:4px;
  }
  .speech .brk .ly{ padding:7px 0; border-top:1px dashed #e2e8f0; }
  .speech .brk .ly:first-of-type{ border-top:none; }
  .speech .brk .ly.d1{ padding-left:14px; }
  .speech .brk .ly.d2{ padding-left:28px; }
  .speech .brk .ly.d3{ padding-left:42px; }
  .speech .brk .ly.d4{ padding-left:56px; }
  .speech .brk .tbranch{ color:#cbd5e1; white-space:pre; margin-right:1px; }
  .speech .brk .role{ margin-right:5px; font-size:.76rem; }
  .speech .brk .chip{
    display:inline-block; min-width:17px; height:17px; line-height:17px;
    text-align:center; color:#fff; font-size:.68rem; font-weight:bold;
    border-radius:5px; margin-right:6px; padding:0 3px;
    font-family:'DejaVu Sans',sans-serif; vertical-align:1px;
  }
  .speech .brk .mod{ display:block; margin:5px 0 0; color:#1e293b; font-weight:bold;
    font-size:.82rem; line-height:1.55; }
  .speech .brk .tg{ display:inline-block; margin-top:4px; color:#94a3b8; font-size:.68rem;
    font-weight:normal; }
  .speech .brk .sg{ display:block; margin:4px 0 0; font-size:.9rem; line-height:1.6;
    font-family:'DejaVu Sans','Noto Sans CJK SC',sans-serif; }
  .speech .brk .note{ display:block; margin-top:3px; color:#64748b; font-size:.8rem; line-height:1.6; }
  .speech .brk .sg u{ text-decoration-color:#f87171; }

  .refrain{ font-weight:bold; border-radius:4px; padding:0 3px;
    -webkit-box-decoration-break:clone; box-decoration-break:clone; }
  .refrain.dream{ background:#fde68a; color:#78350f; }
  .refrain.hundred{ background:#bae6fd; color:#075985; }
  .refrain.now{ background:#bbf7d0; color:#14532d; }
  .refrain.satisfied{ background:#fbcfe8; color:#831843; }
  .refrain.goback{ background:#fed7aa; color:#7c2d12; }
  .refrain.ring{ background:#ddd6fe; color:#4c1d95; }
  .refrain.free{ background:#fecaca; color:#7f1d1d; }

  .legend{
    display:flex; flex-wrap:wrap; gap:6px 10px; background:#fff7ed;
    border:1px solid #fed7aa; border-radius:12px; padding:10px 12px;
    margin-bottom:10px; font-size:.82rem; color:#7c2d12;
  }
  .legend .item{ padding:1px 8px; border-radius:4px; font-weight:bold; }

  /* ---------- tables ---------- */
  table{ width:100%; border-collapse:collapse; font-size:.86rem; margin:8px 0 14px; }
  th{ background:var(--blue); color:#fff; border:1px solid var(--blue);
      padding:7px 8px; text-align:left; font-size:.82rem; }
  td{ border:1px solid var(--line); padding:7px 8px; vertical-align:top; }
  tr:nth-child(even) td{ background:#f0f4ff; }
  td b{ color:#1e40af; }
  td .e{ color:#6b7280; font-size:.8rem; }
  td .n{ color:var(--red); font-weight:bold; }
  table#vocab td .ipa{ color:#6b7280; font-size:.78rem; font-family:'DejaVu Sans',sans-serif; }

  /* narrow: turn every table into stacked cards */
  @media (max-width:600px){
    table thead{ display:none; }
    table tr{
      display:block; background:var(--card); border:1px solid var(--line);
      border-radius:12px; margin-bottom:10px; padding:9px 11px;
      box-shadow:0 1px 2px rgba(0,0,0,.03);
    }
    table tr:nth-child(even) td{ background:transparent; }
    table td{
      display:block; border:none; padding:3px 0; background:transparent !important;
    }
    table td:first-child{
      font-size:.98rem; font-weight:bold; color:#1e3a8a;
      padding-bottom:6px; margin-bottom:5px; border-bottom:1px solid #f1f5f9;
    }
    table td + td::before{
      content:attr(data-label); display:block; font-size:.7rem; color:#94a3b8;
      letter-spacing:.5px; margin-bottom:1px;
    }
    .quiz table.match td:nth-child(1){ width:auto; }
  }

  /* ---------- cards ---------- */
  .card{
    background:var(--card); border:1px solid var(--line); border-left:4px solid var(--red);
    border-radius:12px; padding:11px 13px 12px; margin-bottom:11px;
    box-shadow:0 1px 3px rgba(0,0,0,.04);
  }
  .card .head{ margin-bottom:6px; display:flex; align-items:baseline; gap:7px; }
  .card .num{
    flex:0 0 auto; display:inline-block; width:20px; height:20px;
    background:var(--red); color:#fff; border-radius:50%; text-align:center;
    line-height:20px; font-size:.8rem; font-weight:bold;
  }
  .card .t{ font-size:.98rem; font-weight:bold; color:var(--red-d);
    font-family:'DejaVu Sans','Noto Sans CJK SC',sans-serif; line-height:1.5; }
  .card .why{
    display:block; margin-top:6px; font-size:.86rem; color:#5b21b6;
    background:#f5f3ff; border-left:3px solid #a78bfa; border-radius:0 8px 8px 0;
    padding:8px 10px; line-height:1.7;
  }
  .card .why b{ color:#5b21b6; }
  .card .usage{
    display:block; margin-top:8px; background:#eff6ff; border-radius:8px;
    padding:8px 10px; font-size:.86rem; color:#1e3a8a; line-height:1.7;
  }
  .card .usage b{ color:#1e40af; }

  /* ---------- quiz ---------- */
  .quiz .qhead{
    background:#e0e7ff; border-radius:10px; padding:8px 12px;
    font-size:.92rem; font-weight:bold; color:var(--blue); margin-bottom:8px;
  }
  .quiz .qhead .hint{ display:block; font-weight:normal; color:#6b7280;
    font-size:.76rem; margin-top:2px; }
  .quiz ol.fill{ list-style:decimal; padding-left:22px; }
  .quiz ol.fill li{ margin:8px 0; font-size:.9rem; line-height:1.7; }
  .quiz ol.fill li b{ color:var(--red); }
  .quiz .bank{
    background:#f0fdf4; border:1px dashed #86efac; border-radius:10px;
    padding:8px 12px; font-size:.84rem; color:#065f46; margin-bottom:8px;
  }
  .quiz .bank b{ color:#047857; }

  .answers{
    margin-top:8px; background:#ecfdf5; border:1px dashed #34d399;
    border-radius:12px; padding:12px 13px; font-size:.88rem; color:#065f46;
    line-height:2;
  }
  .answers .atitle{ font-weight:bold; color:#047857; }
  .answers b{ color:#047857; }

  .footer{
    margin-top:22px; text-align:center; color:#9ca3af; font-size:.78rem;
    border-top:1px solid var(--line); padding-top:12px; line-height:1.8;
  }

  /* ---------- word tip: bottom sheet on touch ---------- */
  #tips{
    position:fixed; display:none; z-index:999; max-width:360px;
    background:#fff; border:1px solid #e2e8f0; border-left:4px solid var(--red);
    border-radius:10px; box-shadow:0 8px 24px rgba(0,0,0,.2);
    padding:9px 12px; font-size:.85rem; line-height:1.6; color:var(--ink);
    pointer-events:none;
  }
  #tips .tw{ font-weight:bold; color:var(--red-d); font-size:.98rem; }
  #tips .tipa{ color:#475569; font-family:'DejaVu Sans',sans-serif; font-weight:normal; margin-left:4px; }
  #tips .te{ color:#6d28d9; display:block; margin-top:4px; }
  #tips .tm{ color:var(--blue); display:block; margin-top:4px; }

  @media (max-width:600px){
    #tips{
      left:0; right:0; bottom:0; top:auto; max-width:none;
      border-left:none; border-top:4px solid var(--red);
      border-radius:16px 16px 0 0;
      padding:14px 16px calc(16px + env(safe-area-inset-bottom));
      box-shadow:0 -8px 28px rgba(0,0,0,.22);
    }
    #tips::after{
      content:"轻点空白处关闭"; display:block; margin-top:8px;
      font-size:.72rem; color:#9ca3af; text-align:center;
    }
  }

  /* ---------- back to top ---------- */
  #top-btn{
    position:fixed; right:14px; bottom:calc(16px + env(safe-area-inset-bottom));
    z-index:900; width:44px; height:44px; border:none; border-radius:50%;
    background:rgba(30,58,138,.9); color:#fff; font-size:1.2rem; line-height:44px;
    text-align:center; box-shadow:0 4px 14px rgba(0,0,0,.25); display:none;
    cursor:pointer; touch-action:manipulation;
  }
  #top-btn.show{ display:block; }

  @media (min-width:601px){
    body{ font-size:17px; }
    .header h1{ font-size:1.8rem; }
  }
"""

MOBILE_JS = r"""
(function () {
  var esc = function (s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  };
  var tip = document.createElement("div");
  tip.id = "tips";
  document.body.appendChild(tip);

  var map = {};
  var rows = document.querySelectorAll("#vocab tbody tr");
  for (var i = 0; i < rows.length; i++) {
    var n = rows[i].querySelector(".n");
    var w = rows[i].querySelector("b");
    var tds = rows[i].querySelectorAll("td");
    if (!n || !w || tds.length < 3) continue;
    map[n.textContent.trim()] = {
      word: w.textContent.trim(),
      ipa: rows[i].querySelector(".ipa") ? rows[i].querySelector(".ipa").textContent.trim() : "",
      etym: tds[1].textContent.trim(),
      mean: tds[2].textContent.trim()
    };
  }

  var isTouch = window.matchMedia && window.matchMedia("(hover: none)").matches;
  var current = null;

  function closestSup(el) {
    while (el && el !== document.body) {
      if (el.classList && el.classList.contains("sup")) return el;
      el = el.parentNode;
    }
    return null;
  }
  function render(sup) {
    var key = sup.textContent.trim();
    var d = map[key];
    if (!d) return false;
    tip.innerHTML = '<span class="tw">' + esc(key) + " " + esc(d.word) +
      '</span><span class="tipa">' + esc(d.ipa) + '</span>' +
      '<span class="te">词源：' + esc(d.etym) +
      '</span><span class="tm">在演讲中：' + esc(d.mean) + '</span>';
    return true;
  }
  function show(sup) {
    if (!render(sup)) return;
    tip.style.display = "block";
    current = sup;
  }
  function hide() { tip.style.display = "none"; current = null; }

  /* tap / click: toggle bottom sheet (touch) or anchored tip (desktop) */
  document.addEventListener("click", function (e) {
    var sup = closestSup(e.target);
    if (sup) {
      e.preventDefault();
      if (current === sup) { hide(); } else { show(sup); }
      return;
    }
    if (!tip.contains(e.target)) hide();
  }, true);

  if (!isTouch) {
    document.addEventListener("mouseover", function (e) {
      var sup = closestSup(e.target);
      if (sup) show(sup);
    });
    document.addEventListener("mouseout", function (e) {
      if (!closestSup(e.target)) hide();
    });
    document.addEventListener("mousemove", function (e) {
      if (tip.style.display === "none" || current) {
        if (tip.style.display === "none") return;
      }
      var x = e.clientX + 14, y = e.clientY + 16;
      var r = tip.getBoundingClientRect();
      if (x + r.width > window.innerWidth - 6) x = e.clientX - r.width - 12;
      if (y + r.height > window.innerHeight - 6) y = e.clientY - r.height - 12;
      tip.style.left = x + "px";
      tip.style.top = y + "px";
    });
  }

  /* back to top */
  var btn = document.createElement("button");
  btn.id = "top-btn";
  btn.setAttribute("aria-label", "回到顶部");
  btn.textContent = "\u2191";
  document.body.appendChild(btn);
  window.addEventListener("scroll", function () {
    if (window.scrollY > 600) btn.classList.add("show");
    else btn.classList.remove("show");
  }, { passive: true });
  btn.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
})();
"""

def add_data_labels(h):
    """Copy each table's <th> text onto the matching <td> as data-label,
    so the stacked mobile card view still shows column context."""
    def repl_table(tm):
        table = tm.group(0)
        ths = re.findall(r"<th\b[^>]*>(.*?)</th>", table, re.S)
        if not ths:
            return table
        labels = [re.sub(r"<[^>]+>", "", t).strip() for t in ths]

        def repl_row(rm):
            row = rm.group(0)
            cells = list(re.finditer(r"<td\b([^>]*)>(.*?)</td>", row, re.S))
            if not cells:
                return row
            parts, last = [], 0
            for idx, cm in enumerate(cells):
                parts.append(row[last:cm.start()])
                attrs, inner = cm.group(1), cm.group(2)
                if idx >= 1 and idx < len(labels) and "data-label" not in attrs:
                    attrs += ' data-label="%s"' % labels[idx]
                parts.append("<td%s>%s</td>" % (attrs, inner))
                last = cm.end()
            parts.append(row[last:])
            return "".join(parts)

        return re.sub(r"<tr\b[^>]*>.*?</tr>", repl_row, table, flags=re.S)

    return re.sub(r"<table\b.*?</table>", repl_table, h, flags=re.S)


body = add_data_labels(body)
body = body.replace(u"鼠标悬停正文的", u"轻点正文的")

_HERE = os.path.dirname(os.path.abspath(__file__))
MOBILE_CSS += io.open(os.path.join(_HERE, "read_aloud.css"), encoding="utf-8").read()
MOBILE_JS += io.open(os.path.join(_HERE, "read_aloud.js"), encoding="utf-8").read()

html = u"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#b91c1c">
<title>@@MOBILE_TITLE@@</title>
<style>
""" + MOBILE_CSS + u"""
</style>
</head>
<body>
""" + body + u"""
</body>
<script>
""" + MOBILE_JS + u"""
</script>
</html>
"""

html = html.replace("@@MOBILE_TITLE@@", MOBILE_TITLE)
io.open(DST, "w", encoding="utf-8").write(html)
print("wrote", DST, len(html), "bytes")
