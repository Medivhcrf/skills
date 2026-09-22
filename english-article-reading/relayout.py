#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把旧的「精读」页面就地升级到新的分层拆解格式。

用途
----
早期生成的精读页（`english-article-reading` 的旧版产出）里，句子拆解是**平铺列表**、
颜色是旧色盘，也没有角色色点与 mod。本工具只重写两处：

  1) `<style>` 块 —— 换成当前 `template.html` 的 CSS（并保留该页原有的
     `EXTRA_CSS`，如自定义 `.refrain.*` 配色）+ `read_aloud.css`；
  2) 每个 `.sent` / `.brk` 块 —— 按当前渲染逻辑重排（新色盘、层级、色点、mod）。

**其它一律不动**：背景、词源表、修辞、跟读、金句、自测、答案，
以及 `data-audio` / `data-say` 等音频属性都原样保留。因此对有音频的页面是安全的。

用法
----
    python3 relayout.py <页面.html> [更多页面...]
    python3 relayout.py <页面.html> --fix <逐块覆盖.json>

`--fix` 用于**旧页面里拆解行与色块不是 1:1** 的句子（早期作者会把多个色块合并成
一行，`.sg` 用「…」缩写）。JSON 形如：

    {"8": [["排比时间", "排比第三击：一百年后"], ["谓语", "依然在憔悴"], ...]}

键是句中序号（从 1 开始，按页面出现顺序），值是该句**每个色块**的 [语法标签, 汉语解释]。
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import importlib.util
_spec = importlib.util.spec_from_file_location("build_article", os.path.join(HERE, "build_article.py"))
ba = importlib.util.module_from_spec(_spec)
sys.modules["build_article"] = ba
_spec.loader.exec_module(ba)

REFRain = re.compile(r"\.refrain\.[a-z]+\s*\{[^}]*\}")


def new_css(old_css):
    """当前模板 CSS + 该页原有但模板没有的 .refrain 规则 + read_aloud.css。"""
    tpl = io.open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    css = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1).strip("\n")
    extra = [r for r in REFRain.findall(old_css) if r not in css]
    if extra:
        css += "\n  /* ---- 该页原有的 refrain 配色（迁移时保留）---- */\n"
        css += "\n".join("  " + r for r in extra)
    css += "\n" + io.open(os.path.join(HERE, "read_aloud.css"), encoding="utf-8").read()
    return css


def parse_sentence(block):
    """从旧 .sent 块里取出 (data-audio, pnum, [色块 HTML], 句末标点, [(tag, note)])。"""
    m = re.match(r'<div class="sent"([^>]*)>', block)
    attrs = m.group(1) if m else ""
    audio = re.search(r'data-audio="([^"]*)"', attrs)
    pnum = re.search(r'<span class="pnum">P(\d+)</span>', block)
    cks = re.findall(r'<span class="ck"[^>]*>(.*?)</span>', block, re.S)
    # 句末标点：最后一个色块之后、拆解框之前
    tail = block.split("</span>")[-1]
    punct = tail.split('<div class="brk">')[0]
    punct = re.sub(r"\s+", "", punct) or "."
    rows = []
    for r in re.findall(r'<div class="ly[^"]*">(.*?)</div>', block, re.S):
        tg = re.search(r'<span class="tg">(.*?)</span>', r, re.S)
        nt = re.search(r'<span class="note">(.*?)</span>', r, re.S)
        rows.append(((tg.group(1).strip() if tg else ""), (nt.group(1).strip() if nt else "")))
    return (audio.group(1) if audio else None,
            (int(pnum.group(1)) if pnum else 0), cks, punct, rows)


def relayout(path, fixes):
    src = io.open(path, encoding="utf-8").read()
    old_css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)

    blocks = re.findall(r'<div class="sent"[^>]*>.*?</div></div>', src, re.S)
    warns, out_blocks = [], []
    for idx, block in enumerate(blocks, 1):
        audio, pnum, cks, punct, rows = parse_sentence(block)
        if idx in fixes:
            pairs = [tuple(x) for x in fixes[idx]]
            if len(pairs) != len(cks):
                warns.append("第 %d 句：--fix 给了 %d 组，色块 %d 个" % (idx, len(pairs), len(cks)))
        elif len(rows) == len(cks):
            pairs = rows
        else:
            # 非 1:1 且没给覆盖：按序尽力配对，多出的色块留空并告警
            pairs = rows + [("", "")] * (len(cks) - len(rows))
            warns.append("第 %d 句：拆解行 %d ≠ 色块 %d（未提供 --fix，多出的色块无解释）"
                         % (idx, len(rows), len(cks)))
        chunks = [(ck, pairs[i][0], pairs[i][1]) for i, ck in enumerate(cks)]
        new_block = ba.render_sentence(pnum, punct, chunks)
        if audio:   # 把逐句音频引用挂回去
            new_block = new_block.replace('<div class="sent">',
                                          '<div class="sent" data-audio="%s">' % audio, 1)
        out_blocks.append((block, new_block))

    for old, new in out_blocks:
        src = src.replace(old, new, 1)
    src = re.sub(r"<style>.*?</style>", "<style>\n" + new_css(old_css) + "\n</style>", src, flags=re.S)
    src = re.sub(r'<div class="legend">.*?</div>', ba.role_legend(), src, count=1, flags=re.S)
    io.open(path, "w", encoding="utf-8").write(src)
    print("已重排 %s（%d 句）" % (path, len(blocks)))
    for w in warns:
        print("   ⚠️ ", w)
    return warns


def main():
    args = [a for a in sys.argv[1:]]
    fixes = {}
    if "--fix" in args:
        i = args.index("--fix")
        fixes = {int(k): v for k, v in json.load(io.open(args[i + 1], encoding="utf-8")).items()}
        del args[i:i + 2]
    if not args:
        sys.exit(__doc__)
    for p in args:
        relayout(p, fixes)


if __name__ == "__main__":
    main()
