#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用「手机版」生成：给桌面 HTML 加 viewport + 响应式样式，输出 <名>-手机版.html。

适用于词根/词缀这类「保留原排版」的页面（与精读页的 build_mobile.py 不同）。
用法:
    python3 build_mobile_generic.py <file1.html> [file2.html ...]
"""
import io, re, sys

MOBILE_CSS = """
  html { -webkit-text-size-adjust: 100%; }
  body { overflow-wrap: break-word; }
  @media (max-width: 640px) {
    body { font-size: 16px !important; line-height: 1.8;
           padding: 14px 12px calc(34px + env(safe-area-inset-bottom)); }
    .header h1 { font-size: 1.5rem; }
    .header .meta { font-size: .82rem; }
    h2.section { font-size: 1.12rem; }
    .card { padding: 11px 13px; border-radius: 10px; }
    .card .root { font-size: 1.18rem; }
    .card li { font-size: 1rem; padding: 3px 0; }
    .card .usage { font-size: .95rem; }
    .card .etym, .card .evo, .card .trick,
    .card .confuse, .card .variant, .card .cognate { font-size: .86rem; }
    table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .flow { font-size: .9rem; }
  }
"""


def process(src):
    h = io.open(src, encoding="utf-8").read()
    if "</style>" not in h:
        print("skip (no style):", src); return
    if "width=device-width" not in h:
        h = h.replace('<meta charset="UTF-8">',
                      '<meta charset="UTF-8">\n'
                      '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">', 1)
    if "/* mobile-generic */" not in h:
        h = h.replace("</style>", "/* mobile-generic */" + MOBILE_CSS + "\n</style>", 1)
    out = src[:-5] + "-手机版.html"
    io.open(out, "w", encoding="utf-8").write(h)
    print("mobile ->", out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 build_mobile_generic.py <file.html> ...")
    for p in sys.argv[1:]:
        process(p)
