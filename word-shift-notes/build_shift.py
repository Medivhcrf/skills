#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""「词义错位」章节生成器：内容模块 → 桌面 HTML + 手机版 HTML。

用法:
    python3 build_shift.py <内容模块.py> [<内容模块.py> ...]
    python3 build_shift.py <内容模块.py> --out-dir /home/crf/english/shift

产出（默认 --out-dir /home/crf/english/shift）:
    <DATE>-词义错位-<SLUG>.html          桌面版（也是手机版的源）
    <DATE>-词义错位-<SLUG>-手机版.html   手机版（加 viewport + 移动排版）

内容模块字段见 SKILL.md「内容模块格式」一节。所有字段文本按 **HTML** 处理
（可以写 <b> <code>），因为内容由作者核实后手写；日期/标签等结构性文本会自动转义。
"""
import html as html_mod
import importlib.util
import io
import os
import re
import sys
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True  # 别在 examples/ 里拉 __pycache__

DEFAULT_OUT = Path("/home/crf/english/shift")

# ── 站点配色（与 /home/crf/english 其余页面一致） ────────────────────
INK = "#1f2937"
INK_SOFT = "#4b5563"
MUTED = "#9ca3af"
CRIMSON = "#7f1d1d"
CRIMSON_2 = "#b91c1c"
BLUE = "#1e3a8a"
BLUE_SOFT = "#1e40af"
GREEN = "#047857"
VIOLET = "#6d28d9"
AMBER = "#b45309"
LINE = "#e5e7eb"
BG = "#f5f6fa"

CN_NUM = "一二三四五六七八九十"


def esc(s):
    return html_mod.escape(str(s), quote=False)


def _load_module(path):
    spec = importlib.util.spec_from_file_location("shift_content", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _g(mod, name, default=None):
    return getattr(mod, name, default)


def _tup(row, n, default=""):
    """把长度不足的元组补齐到 n 项。"""
    row = tuple(row)
    return row + (default,) * (n - len(row)) if len(row) < n else row[:n]


# ── 各小节渲染 ────────────────────────────────────────────────────────

def render_verdict(verdict, punch):
    if not verdict and not punch:
        return ""
    parts = ['<div class="callout">']
    if verdict:
        parts.append('<div class="label">一句话</div>')
        parts.append(f'<p class="verdict">{verdict}</p>')
    if punch:
        parts.append(f'<p class="punch">{punch}</p>')
    parts.append('</div>')
    return "\n".join(parts)


def render_senses(senses):
    if not senses:
        return ""
    out = []
    for row in senses:
        word, definition, extra, warn, url = _tup(row, 5)
        head = f'<span class="word">{word}</span>'
        if url:
            head = f'<a class="src" href="{esc(url)}" target="_blank" rel="noopener">{head}</a>'
        out.append('<div class="sense">')
        out.append(f'  <div class="sense-head">{head}</div>')
        if definition:
            out.append(f'  <p class="def">{definition}</p>')
        if extra:
            out.append(f'  <p class="syn">{extra}</p>')
        if warn:
            out.append(f'  <p class="warn">{warn}</p>')
        out.append('</div>')
    return "\n".join(out)


def render_etym(etym):
    if not etym:
        return ""
    rows = []
    for row in etym:
        word, form, literal = _tup(row, 3)
        rows.append(f'    <tr><th>{word}</th>'
                    f'<td class="form" data-label="最早形态 / 词根">{form}</td>'
                    f'<td class="lit" data-label="字面本义">{literal}</td></tr>')
    return ('<div class="scroll">\n  <table class="etym">\n'
            '    <thead><tr><th>词</th><th>最早形态 / 词根</th><th>字面本义</th></tr></thead>\n'
            '    <tbody>\n' + "\n".join(rows) + '\n    </tbody>\n  </table>\n</div>')


def render_quote(quote):
    if not quote:
        return ""
    text, source = _tup(quote, 2)
    cite = f'<cite>{source}</cite>' if source else ""
    return f'<blockquote>{text}{cite}</blockquote>'


def render_duty(duty):
    if not duty:
        return ""
    rows = []
    for row in duty:
        word, gloss, cn, limit = _tup(row, 4)
        rows.append(f'    <tr><th>{word}</th>'
                    f'<td data-label="英文原解">{gloss}</td>'
                    f'<td class="cn" data-label="中文">{cn}</td>'
                    f'<td class="limit" data-label="用法限制">{limit}</td></tr>')
    return ('<div class="scroll">\n  <table class="duty">\n'
            '    <thead><tr><th>词</th><th>英文原解</th><th>中文</th><th>用法限制</th></tr></thead>\n'
            '    <tbody>\n' + "\n".join(rows) + '\n    </tbody>\n  </table>\n</div>')


def render_rules(rules):
    if not rules:
        return ""
    items = "\n".join(f'  <li>{r}</li>' for r in rules)
    return f'<ol class="rules">\n{items}\n</ol>'


SECTIONS = [
    ("词典释义（英文原文）", "senses", "只引真实辞书，标记出处；释义原文照抄，不改写"),
    ("词源本义", "etym", "本义看词根，不看现在的常用义"),
    ("错位是怎么产生的", "insight", None),
    ("分工表", "duty", "哪个词管哪种场合，一眼看全"),
    ("可迁移的规律", "rules", None),
]


def render_body(mod):
    blocks = []
    verdict = _g(mod, "VERDICT", "")
    punch = _g(mod, "PUNCH", "")
    v = render_verdict(verdict, punch)
    if v:
        blocks.append(v)

    data = {
        "senses": render_senses(_g(mod, "SENSES", [])),
        "etym": render_etym(_g(mod, "ETYM", [])) + render_quote(_g(mod, "ETYM_QUOTE")),
        "insight": _g(mod, "INSIGHT", ""),
        "duty": render_duty(_g(mod, "DUTY", [])),
        "rules": render_rules(_g(mod, "RULES", [])),
    }
    used = 0
    for title, key, hint in SECTIONS:
        inner = data.get(key) or ""
        if not inner.strip():
            continue
        num = CN_NUM[used] if used < len(CN_NUM) else str(used + 1)
        used += 1
        hint_html = f'<span class="hint">{hint}</span>' if hint else ""
        blocks.append(
            f'<section class="sec">\n'
            f'  <h2><span class="num">{num}</span>{title}{hint_html}</h2>\n'
            f'{inner}\n'
            f'</section>'
        )
    extra = _g(mod, "EXTRA", "")
    if extra:
        blocks.append(extra)
    return "\n\n".join(blocks)


# ── 页面骨架 ──────────────────────────────────────────────────────────

CSS = f"""
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Noto Sans CJK SC', 'Droid Sans Fallback', 'WenQuanYi Zen Hei', sans-serif;
    font-size: 10.5pt; line-height: 1.75; color: {INK}; background: {BG};
    padding: 28px 18px 56px; -webkit-text-size-adjust: 100%;
  }}
  .wrap {{ max-width: 780px; margin: 0 auto; }}

  .hero {{
    background: linear-gradient(135deg, {CRIMSON}, {CRIMSON_2});
    color: #fff; border-radius: 12px; padding: 20px 22px; margin-bottom: 16px;
  }}
  .hero .kicker {{
    font-size: 8.5pt; letter-spacing: 2px; color: #fecaca; margin-bottom: 6px;
  }}
  .hero h1 {{ font-size: 17pt; line-height: 1.35; letter-spacing: .5px; }}
  .hero h1 .en {{ font-family: 'DejaVu Sans', sans-serif; }}
  .hero .sub {{ color: #fee2e2; font-size: 10pt; margin-top: 7px; }}
  .hero .meta {{ color: #fca5a5; font-size: 8.5pt; margin-top: 9px; }}

  .callout {{
    background: #fff; border: 1px solid {LINE}; border-left: 4px solid {CRIMSON_2};
    border-radius: 10px; padding: 13px 16px; margin-bottom: 16px;
  }}
  .callout .label {{
    font-size: 8pt; letter-spacing: 2px; color: {CRIMSON_2};
    font-weight: bold; margin-bottom: 4px;
  }}
  .callout .verdict {{ font-size: 12pt; line-height: 1.6; }}
  .callout .verdict b {{ color: {CRIMSON}; }}
  .callout .punch {{
    margin-top: 8px; padding-top: 8px; border-top: 1px dashed {LINE};
    color: {INK_SOFT}; font-size: 9.8pt;
  }}
  .callout .punch b {{ color: {BLUE}; }}

  .sec {{
    background: #fff; border: 1px solid {LINE}; border-radius: 10px;
    padding: 15px 18px 17px; margin-bottom: 14px;
  }}
  .sec h2 {{
    font-size: 12pt; color: {BLUE}; padding-bottom: 7px; margin-bottom: 10px;
    border-bottom: 1px solid #eef2f7;
  }}
  .sec h2 .num {{
    display: inline-block; width: 19px; height: 19px; margin-right: 7px;
    background: {BLUE}; color: #fff; border-radius: 50%;
    text-align: center; line-height: 19px; font-size: 9pt;
  }}
  .sec h2 .hint {{ float: right; color: {MUTED}; font-size: 8.5pt; font-weight: normal; }}

  /* §1 词典释义 */
  .sense {{ padding: 9px 0; border-bottom: 1px dashed #eef2f7; }}
  .sense:first-child {{ padding-top: 0; }}
  .sense:last-child {{ border-bottom: none; padding-bottom: 0; }}
  .sense-head {{ margin-bottom: 3px; }}
  a.src {{ text-decoration: none; }}
  .sense .word {{
    font-family: 'DejaVu Sans', sans-serif; font-weight: bold;
    font-size: 11.5pt; color: {VIOLET};
  }}
  a.src:hover .word {{ text-decoration: underline; }}
  .sense .def {{
    font-family: 'DejaVu Sans', 'Noto Sans CJK SC', sans-serif;
    background: #f8fafc; border-left: 3px solid #cbd5e1;
    padding: 5px 10px; border-radius: 0 5px 5px 0;
    font-size: 9.8pt; color: {INK};
  }}
  .sense .syn {{ margin-top: 4px; font-size: 9pt; color: {MUTED}; }}
  .sense .warn {{ margin-top: 4px; font-size: 9.3pt; color: {CRIMSON_2}; }}
  .sense .warn::before {{ content: "⚠ "; }}

  /* 表格 */
  .scroll {{ overflow-x: auto; -webkit-overflow-scrolling: touch; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; }}
  th, td {{ border-bottom: 1px solid #eef2f7; padding: 6px 8px; text-align: left; vertical-align: top; }}
  thead th {{
    background: #f8fafc; color: {BLUE}; font-size: 8.8pt; white-space: nowrap;
    border-bottom: 1px solid #e2e8f0;
  }}
  table.etym tbody th, table.duty tbody th {{
    font-family: 'DejaVu Sans', 'Noto Sans CJK SC', sans-serif;
    color: {VIOLET}; font-weight: bold; white-space: nowrap;
  }}
  table.etym .form {{ color: {AMBER}; }}
  table.etym .lit {{ color: {INK}; }}
  table.duty td {{ color: {INK_SOFT}; }}
  table.duty .cn {{ color: {GREEN}; font-weight: bold; white-space: nowrap; }}
  table.duty .limit {{ color: {CRIMSON_2}; }}

  blockquote {{
    margin-top: 10px; background: #f5f3ff; border-left: 3px solid {VIOLET};
    border-radius: 0 6px 6px 0; padding: 8px 12px;
    font-family: 'DejaVu Sans', 'Noto Sans CJK SC', sans-serif;
    font-size: 9.2pt; color: #5b21b6; line-height: 1.65;
  }}
  blockquote cite {{ display: block; margin-top: 5px; font-style: normal; color: #8b5cf6; font-size: 8.5pt; }}

  .sec p {{ margin-bottom: 8px; }}
  .sec p:last-child {{ margin-bottom: 0; }}
  .sec b {{ color: {CRIMSON}; }}
  .sec code {{
    font-family: 'DejaVu Sans Mono', monospace; background: #f1f5f9;
    border-radius: 4px; padding: 1px 5px; font-size: 9.2pt; color: {BLUE_SOFT};
  }}
  .box {{
    background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 7px;
    padding: 9px 12px; margin: 9px 0; font-size: 9.6pt;
  }}
  .box.green {{ background: #ecfdf5; border-color: #a7f3d0; }}
  .box.amber {{ background: #fffbeb; border-color: #fde68a; }}

  ol.rules {{ padding-left: 0; list-style: none; counter-reset: r; }}
  ol.rules li {{
    counter-increment: r; position: relative; padding-left: 26px;
    margin-bottom: 8px; font-size: 9.8pt;
  }}
  ol.rules li:last-child {{ margin-bottom: 0; }}
  ol.rules li::before {{
    content: counter(r); position: absolute; left: 0; top: 1px;
    width: 17px; height: 17px; background: {GREEN}; color: #fff;
    border-radius: 50%; text-align: center; line-height: 17px; font-size: 8.5pt; font-weight: bold;
  }}

  .footer {{
    margin-top: 16px; text-align: center; color: {MUTED};
    font-size: 8.5pt; line-height: 1.7;
  }}
  .footer a {{ color: {BLUE_SOFT}; text-decoration: none; }}
  .footer a:hover {{ text-decoration: underline; }}
"""

MOBILE_CSS = """
  /* mobile-generic: 词义错位手机版 */
  @media (max-width: 640px) {
    body { font-size: 16px; line-height: 1.85; padding: 14px 12px calc(40px + env(safe-area-inset-bottom)); }
    .hero { padding: 16px 15px; border-radius: 10px; }
    .hero h1 { font-size: 1.24rem; }
    .hero .sub { font-size: .92rem; }
    .callout { padding: 12px 13px; }
    .callout .verdict { font-size: 1.04rem; }
    .callout .punch { font-size: .92rem; }
    .sec { padding: 13px 13px 15px; border-radius: 10px; }
    .sec h2 { font-size: 1.06rem; }
    .sec h2 .hint { display: none; }
    .sense .word { font-size: 1.05rem; }
    .sense .def { font-size: .9rem; }
    .sense .syn, .sense .warn { font-size: .85rem; }
    blockquote { font-size: .86rem; }
    .sec code { font-size: .85rem; }
    ol.rules li { font-size: .93rem; }

    /* 表格 → 堆叠卡片：手机上不横向滚，一列一列读 */
    .scroll { overflow-x: visible; }
    table.etym, table.duty { display: block; width: 100%; }
    table.etym thead, table.duty thead { display: none; }
    table.etym tbody, table.duty tbody { display: block; }
    table.etym tr, table.duty tr {
      display: block; border: 1px solid #e5e7eb; border-radius: 8px;
      padding: 8px 11px 9px; margin-bottom: 9px;
    }
    table.etym tr:last-child, table.duty tr:last-child { margin-bottom: 0; }
    table.etym th, table.duty th {
      display: block; border-bottom: 1px solid #eef2f7; white-space: normal;
      padding: 0 0 5px; margin-bottom: 5px; font-size: 1rem;
    }
    table.etym td, table.duty td {
      display: block; border-bottom: none; padding: 2px 0; white-space: normal;
      font-size: .92rem;
    }
    table.etym td::before, table.duty td::before {
      content: attr(data-label) "："; color: #9ca3af; font-size: .78rem;
    }
    table.duty .cn { font-size: .95rem; }
  }
"""


def fmt_date_cn(iso):
    """2026-09-23 → 2026 年 9 月 23 日。"""
    try:
        y, m, d = (int(x) for x in iso.split("-"))
        return f"{y} 年 {m} 月 {d} 日"
    except Exception:
        return iso


def build_html(mod, mobile=False):
    title = _g(mod, "TITLE", "词义错位")
    sub = _g(mod, "SUB", "")
    iso = _g(mod, "DATE") or date.today().isoformat()
    date_cn = _g(mod, "DATE_CN") or fmt_date_cn(iso)
    kicker = _g(mod, "KICKER", "词义错位 · 英文原义 × 汉语对应词")
    meta = _g(mod, "META", "")
    footer = _g(mod, "FOOTER", "")

    head_extra = ""
    if mobile:
        head_extra = ('<meta name="viewport" content="width=device-width, initial-scale=1, '
                      'viewport-fit=cover">\n')

    meta_bits = [b for b in (date_cn, meta) if b]
    meta_html = f'<div class="meta">{" ｜ ".join(meta_bits)}</div>' if meta_bits else ""
    sub_html = f'<p class="sub">{sub}</p>' if sub else ""
    footer_html = footer or '返回 <a href="../index.html">英语学习站</a> · 章节：词义错位'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
{head_extra}<title>{esc(_plain(title))} · 词义错位</title>
<style>
{CSS}{MOBILE_CSS if mobile else ""}
</style>
</head>
<body>
<div class="wrap">

<header class="hero">
  <div class="kicker">{esc(kicker)}</div>
  <h1>{title}</h1>
  {sub_html}
  {meta_html}
</header>

{render_body(mod)}

<div class="footer">{footer_html}</div>

</div>
</body>
</html>
"""


def _plain(s):
    """去掉标签，仅用于 <title>。"""
    return re.sub(r"<[^>]+>", "", str(s))


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    out_dir = DEFAULT_OUT
    if "--out-dir" in argv:
        out_dir = Path(argv[argv.index("--out-dir") + 1])
    if not args:
        sys.exit(__doc__)
    out_dir.mkdir(parents=True, exist_ok=True)

    for src in args:
        mod = _load_module(src)
        d = _g(mod, "DATE") or date.today().isoformat()
        slug = _g(mod, "SLUG")
        if not slug:
            sys.exit(f"{src}: 缺少 SLUG（文件名用，如 at-last）")
        stem = f"{d}-词义错位-{slug}"
        desk = out_dir / f"{stem}.html"
        mob = out_dir / f"{stem}-手机版.html"
        io.open(desk, "w", encoding="utf-8").write(build_html(mod, mobile=False))
        io.open(mob, "w", encoding="utf-8").write(build_html(mod, mobile=True))
        print("desktop ->", desk)
        print("mobile  ->", mob)


if __name__ == "__main__":
    main(sys.argv)
