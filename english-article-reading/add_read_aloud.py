#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给已有的桌面版精读 HTML 注入 / 刷新「朗读」功能（CSS + JS）。

用法:
    python3 add_read_aloud.py <file.html>

- 向 <style> 末尾追加 read_aloud.css（已存在则跳过）；
- 移除旧的朗读 <script> 块，并在 </body> 后插入最新的 read_aloud.js；
- 可重复运行：用于在 read_aloud.js 更新后刷新页面。
之后可用 build_mobile.py 重生成手机版。
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main(path):
    h = io.open(path, encoding="utf-8").read()
    if "</style>" not in h or "</body>" not in h:
        sys.exit("not a full HTML document: " + path)
    css = io.open(os.path.join(HERE, "read_aloud.css"), encoding="utf-8").read()
    js = io.open(os.path.join(HERE, "read_aloud.js"), encoding="utf-8").read()

    if ".say{" not in h and ".say {" not in h:
        h = h.replace("</style>", css + "\n</style>", 1)

    h = re.sub(r'<script>\s*/\* -+ 朗读.*?</script>', '', h, flags=re.S)
    h = h.replace("</body>", "</body>\n<script>\n" + js + "\n</script>", 1)

    io.open(path, "w", encoding="utf-8").write(h)
    print("read-aloud synced into", path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 add_read_aloud.py <file.html>")
    main(sys.argv[1])
