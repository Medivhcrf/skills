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
    h = re.sub(r'/\* pron-start \*/.*?/\* pron-end \*/', '', h, flags=re.S)
    h = h.replace("</style>", css + "\n</style>", 1)
    # 历史版本的首行注释有好几种写法（"单词发音"、"单词发音（神经网络…"），
    # 只按 "/* -+ 单词发音" 匹配才能把旧块整块删掉，否则页面里会同时跑新旧两份。
    h = re.sub(r'<script>\s*/\* -+ 单词发音.*?</script>', '', h, flags=re.S)
    h = h.replace("</body>", "</body>\n<script>\n" + js + "\n</script>", 1)
    io.open(path, "w", encoding="utf-8").write(h)
    print("pronounce ->", path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 add_pronounce.py <file.html> ...")
    for p in sys.argv[1:]:
        process(p)
