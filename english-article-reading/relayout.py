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
DIV_TOK = re.compile(r"<div\b|</div>")


def div_end(src, start):
    """返回从 start（一个 <div> 的起点）开始的**配平**结束位置。

    旧页面的 `.sent` 结尾是 `</div></div></div>`（关 ly、关 brk、关 sent）。
    若用非贪婪 `.*?</div></div>` 切块，只会吃掉前两个，把关 `.sent` 的那个
    留在替换范围外——**每句多出一个 `</div>`**，逐句累积会把 `.para`、`.speech`
    提前闭合，后面的拆解行掉出 `.sent`，编号底色与间距全部失效。
    """
    depth = 0
    for m in DIV_TOK.finditer(src, start):
        if m.group(0) == "</div>":
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            depth += 1
    return len(src)


def sent_blocks(src):
    """按配平切出所有 `.sent` 块（含其内部的 `.brk`）。"""
    spans = []
    for m in re.finditer(r'<div class="sent"[^>]*>', src):
        spans.append(src[m.start():div_end(src, m.start())])
    return spans


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


def ck_contents(block):
    """取出块内所有 `.ck` 色块的内容，**按嵌套配平**。

    不能用非贪婪正则 `(.*?)</span>`：色块里常嵌 `<span class="sup">①</span>`，
    非贪婪会在内层 sup 的闭合处提前停下，取出一段**未闭合的 span**，
    渲染后 `.sg` 就会吞掉后面的元素、在某个 </div> 处把结构截断
    （症状：从某一页/某一句起，编号徽标底色和所有间距突然消失）。
    """
    out = []
    for m in re.finditer(r'<span class="ck"[^>]*>', block):
        i, depth, start = m.end(), 1, m.end()
        while depth > 0:
            nxt_open = block.find("<span", i)
            nxt_close = block.find("</span>", i)
            if nxt_close < 0:
                break
            if 0 <= nxt_open < nxt_close:
                depth += 1
                i = nxt_open + len("<span")
            else:
                depth -= 1
                if depth == 0:
                    out.append(block[start:nxt_close])
                    break
                i = nxt_close + len("</span>")
    return out


def parse_sentence(block):
    """从旧 .sent 块里取出 (data-audio, pnum, [色块 HTML], 句末标点, [(tag, note)])。"""
    m = re.match(r'<div class="sent"([^>]*)>', block)
    attrs = m.group(1) if m else ""
    audio = re.search(r'data-audio="([^"]*)"', attrs)
    pnum = re.search(r'<span class="pnum">P(\d+)</span>', block)
    cks = ck_contents(block)
    # 句末标点：最后一个色块闭合 与 <div class="brk"> 之间。
    # 注意必须先在 brk 处切开——否则 rfind("</span>") 会命中拆解框里最后一个
    # .note 的闭合标签，把 </div></div> 当成标点写进正文（曾因此弄坏页面结构）。
    sent_part = block.split('<div class="brk">')[0]
    cut = sent_part.rfind("</span>")
    punct = sent_part[cut + len("</span>"):] if cut >= 0 else ""
    punct = re.sub(r"\s+", "", punct)
    if not punct or "<" in punct:      # 兜底：解析异常时退回句号，绝不写入标签
        punct = "."
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

    blocks = sent_blocks(src)
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
