#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给已有的桌面版精读 HTML 注入 / 刷新「朗读」功能（CSS + JS）。

用法:
    python3 add_read_aloud.py <file.html>

- 向 <style> 末尾追加 read_aloud.css（用 `/* ra-start */ … /* ra-end */` 标记，
  重跑时先删旧的，所以可重复运行）；
- 把 read_aloud.js 放进**独立的** `<script>` 块（用 `/* ra-js-start */ … /* ra-js-end */`
  标记），重跑时整块替换。

⚠️ 曾经的坑：`build_article.py` 会把朗读 JS 和模板 JS **嵌在同一个 `<script>` 块**里，
而旧版本脚本只会删「以朗读注释开头的整块」，删不掉合并块里的那一份，
于是每跑一次就往页面里**再插一份 read_aloud.js**——同一个页面里朗读逻辑执行两遍，
逐句的 🔊 按钮被加两次（功能看着正常，但按钮数量翻倍）。
现在改为：先删带标记的整块，再把任何块内从朗读标记起的**尾部截断**
（保留块内其它 JS），最后统一插一个新的带标记块。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RA_JS_START = "/* ra-js-start */"
RA_JS_END = "/* ra-js-end */"
# 旧版（无标记）read_aloud.js 的首行注释，用来识别历史注入
LEGACY_MARK = "/* ---------- 朗读"


def strip_read_aloud_js(h):
    """删掉页面里已有的朗读 JS：带标记的整块 + 合并块里的遗留尾部。"""
    # 1) 带标记的独立块
    h = re.sub(r'<script>\s*' + re.escape(RA_JS_START) + r'.*?' + re.escape(RA_JS_END)
               + r'\s*</script>\s*', '', h, flags=re.S)

    # 2) 遗留：块内从朗读标记起截断（可能和模板 JS 同块）
    def cut(m):
        body = m.group(1)
        i = body.find(RA_JS_START)
        if i < 0:
            i = body.find(LEGACY_MARK)
        if i < 0:
            return m.group(0)
        kept = body[:i].rstrip()
        return ('<script>' + kept + '</script>') if kept else ''

    return re.sub(r'<script>(.*?)</script>', cut, h, flags=re.S)


def main(path):
    h = io.open(path, encoding="utf-8").read()
    if "</style>" not in h or "</body>" not in h:
        sys.exit("not a full HTML document: " + path)
    css = io.open(os.path.join(HERE, "read_aloud.css"), encoding="utf-8").read()
    js = io.open(os.path.join(HERE, "read_aloud.js"), encoding="utf-8").read()

    h = re.sub(r'/\* ra-start \*/.*?/\* ra-end \*/', '', h, flags=re.S)
    h = h.replace("</style>", css + "\n</style>", 1)

    h = strip_read_aloud_js(h)
    h = h.replace("</body>",
                  "<script>\n" + RA_JS_START + "\n" + js + "\n" + RA_JS_END + "\n</script>\n</body>", 1)

    io.open(path, "w", encoding="utf-8").write(h)
    print("read-aloud synced into", path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 add_read_aloud.py <file.html>")
    main(sys.argv[1])
