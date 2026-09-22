#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给词根/词缀页注入「单词发音」功能（CSS + JS），可重复运行。

用法:
    python3 add_pronounce.py <file1.html> [file2.html ...]
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def process(path):
    h = io.open(path, encoding="utf-8").read()
    if "</style>" not in h or "</body>" not in h:
        print("skip (not full html):", path); return
    css = io.open(os.path.join(HERE, "pronounce.css"), encoding="utf-8").read()
    js = io.open(os.path.join(HERE, "pronounce.js"), encoding="utf-8").read()
    if ".psay{" not in h and ".psay {" not in h:
        h = h.replace("</style>", css + "\n</style>", 1)
    h = re.sub(r'<script>\s*/\* -+ 单词发音.*?</script>', '', h, flags=re.S)
    h = h.replace("</body>", "</body>\n<script>\n" + js + "\n</script>", 1)
    io.open(path, "w", encoding="utf-8").write(h)
    print("pronounce ->", path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 add_pronounce.py <file.html> ...")
    for p in sys.argv[1:]:
        process(p)
