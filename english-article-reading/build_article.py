#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""english-article-reading 技能：数据 → 桌面 HTML 生成器。

适合长文 / 批量：把文章内容写成「内容模块」(Python)，本脚本自动生成
带色块拆解的桌面版 HTML，保证 `.ck` 色块、`.chip` 编号、`.sg` 文本三者严格对齐。

用法:
    python3 build_article.py <内容模块.py> <输出.html>

内容模块需定义（没有的段可省略，会跳过对应章节）:
    TITLE, SUB, DATE
    PARAS   = [ 段落, ... ]     段落 = [ 句子, ... ]
              句子 = (句末标点, [ (色块英文, 语法标签, 汉语解释), ... ])
    VOCAB   = [ (编号①, 单词, 音标, 词源本义, 文中含义), ... ]
    RHET    = [ (编号, 标题, why_html, usage_html_or_None), ... ]
    TIPS    = [ (要点, 建议), ... ]
    QUOTES  = [ (序号A, 英文, why_html), ... ]
    QUIZ_MATCH = [ (左, 右), ... ]
    QUIZ_RHET  = [ "题干", ... ]
    QUIZ_FILL  = [ "题干", ... ]
    ANSWERS = "答案 HTML"
    EXTRA_CSS = ""              # 可选，追加到模板 CSS 之后
    VOCAB_END = "㉔"            # 可选，词汇表标题末位编号；缺省取 VOCAB 最后一个
"""
import io, os, re, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "template.html")

PALETTE = [
    ("#dbeafe", "#1e3a8a"), ("#bbf7d0", "#14532d"), ("#fde68a", "#78350f"),
    ("#fbcfe8", "#831843"), ("#ddd6fe", "#4c1d95"), ("#fed7aa", "#7c2d12"),
]
CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚"


def supify(t):
    for ch in CIRC:
        if ch in t:
            t = t.replace(ch, '<span class="sup">%s</span>' % ch)
    return t


def render_sentence(pnum, punct, chunks):
    cks, lys = [], []
    for i, (text, tag, note) in enumerate(chunks):
        bg, fg = PALETTE[i % len(PALETTE)]
        t = supify(text)
        cks.append('<span class="ck" style="background:%s;color:%s">%s</span>' % (bg, fg, t))
        lys.append('<div class="ly"><span class="chip" style="background:%s">%d</span>'
                   '<span class="tg">%s</span><span class="sg" style="color:%s">%s</span>'
                   '<span class="note">%s</span></div>' % (bg, i + 1, tag, fg, t, note))
    head = '<span class="pnum">P%d</span>' % pnum if pnum else ''
    return ('<div class="sent">%s%s%s\n<div class="brk">%s</div></div>'
            % (head, " ".join(cks), punct, "".join(lys)))


def render_speech(paras):
    out = []
    for pi, para in enumerate(paras, 1):
        sents = [render_sentence(pi if si == 0 else 0, punct, chunks)
                 for si, (punct, chunks) in enumerate(para)]
        out.append('<div class="para">' + "\n".join(sents) + '</div>')
    return '<div class="speech">\n' + "\n".join(out) + '\n</div>'


def load_module(path):
    spec = importlib.util.spec_from_file_location("content_mod", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["content_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def build(content_path, out_path):
    # 内容模块可能 import 同目录的数据文件
    sys.path.insert(0, os.path.dirname(os.path.abspath(content_path)))
    c = load_module(content_path)

    tpl = io.open(TPL, encoding="utf-8").read()
    css = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1).strip("\n")
    js = re.search(r"<script>(.*?)</script>", tpl, re.S).group(1).strip("\n")
    css += getattr(c, "EXTRA_CSS", "") or ""
    css += "\n" + io.open(os.path.join(HERE, "read_aloud.css"), encoding="utf-8").read()
    js += "\n" + io.open(os.path.join(HERE, "read_aloud.js"), encoding="utf-8").read()

    def g(name, default=None):
        return getattr(c, name, default)

    TITLE, SUB, DATE = g("TITLE"), g("SUB"), g("DATE")
    PARAS = g("PARAS", [])
    VOCAB = g("VOCAB", [])
    RHET = g("RHET", [])
    TIPS = g("TIPS", [])
    QUOTES = g("QUOTES", [])
    QUIZ_MATCH = g("QUIZ_MATCH", [])
    QUIZ_RHET = g("QUIZ_RHET", [])
    QUIZ_FILL = g("QUIZ_FILL", [])
    ANSWERS = g("ANSWERS", "")

    last = g("VOCAB_END") or (VOCAB[-1][0] if VOCAB else "①")

    vocab_rows = "\n".join(
        '<tr><td><span class="n">%s</span><b>%s</b> <span class="ipa">%s</span></td>'
        '<td class="e">%s</td><td>%s</td></tr>' % row for row in VOCAB)

    rhet_cards = "\n".join(
        '<div class="card">\n  <div class="head"><span class="num">%s</span><span class="t">%s</span></div>\n'
        '  <div class="why">%s</div>\n  %s\n</div>' % (
            n, t, why, ('<span class="usage">%s</span>' % u) if u else '')
        for n, t, why, u in RHET)

    tips_rows = "\n".join('<tr><td><b>%s</b></td><td>%s</td></tr>' % (p, a) for p, a in TIPS)

    quote_cards = "\n".join(
        '<div class="card">\n  <div class="head"><span class="num">%s</span><span class="t">%s</span></div>\n'
        '  <div class="why">%s</div>\n</div>' % q for q in QUOTES)

    match_rows = "\n".join('<tr><td>%s</td><td>%s</td></tr>' % r for r in QUIZ_MATCH)
    rhet_items = "\n".join('<li>%s</li>' % x for x in QUIZ_RHET)
    fill_items = "\n".join('<li>%s</li>' % x for x in QUIZ_FILL)

    parts = []
    parts.append("""<div class="header">
  <h1>%s</h1>
  <div class="sub">%s</div>
  <div class="meta">%s ｜ 全文精读 · 重点词源 · 修辞分析 · 跟读要点 · 自测</div>
</div>

<h2 class="section">一、背景（为什么要学这篇）</h2>

<div class="intro">%s</div>

<h2 class="section">二、全文精读（重点词已标注①，见词汇表）</h2>

<div class="legend"><span class="item" style="background:#dbeafe;color:#1e3a8a">🧱 色块拆解</span>正文按句子成分分色上色；每句下方拆解框里，<b>色块编号 ↔ 拆解行 ↔ 汉语解释</b>一一对应。</div>

%s""" % (TITLE, SUB, DATE, g("BACKGROUND", ""), render_speech(PARAS)))

    if VOCAB:
        parts.append("""<h2 class="section">三、重点词汇词源（①—%s 对应正文上标，鼠标悬停正文的 ①②… 即可看词源与释义）</h2>

<table id="vocab">
  <thead>
    <tr><th style="width:16%%">单词</th><th style="width:44%%">词源本义</th><th>在演讲中的含义</th></tr>
  </thead>
  <tbody>
%s
  </tbody>
</table>""" % (last, vocab_rows))

    if RHET:
        parts.append('<h2 class="section">四、修辞分析（这篇为什么这么动人）</h2>\n\n%s' % rhet_cards)

    if TIPS:
        parts.append("""<h2 class="section">五、跟读要点（模仿原声）</h2>

<div class="intro">%s</div>

<table>
  <thead>
    <tr><th style="width:24%%">要点</th><th>操作建议</th></tr>
  </thead>
  <tbody>
%s
  </tbody>
</table>""" % (g("TIPS_INTRO", ""), tips_rows))

    if QUOTES:
        parts.append('<h2 class="section">六、名言金句（建议背诵）</h2>\n\n%s' % quote_cards)

    if QUIZ_MATCH or QUIZ_RHET or QUIZ_FILL:
        quiz = ['<h2 class="section">七、自测</h2>']
        if QUIZ_MATCH:
            quiz.append('<div class="quiz">\n  <div class="qhead">练习一 · 词源连线<span class="hint">单词 → 词源本义</span></div>\n'
                        '  <table class="match">\n%s\n  </table>\n</div>' % match_rows)
        if QUIZ_RHET:
            quiz.append('<div class="quiz">\n  <div class="qhead">练习二 · 修辞辨识<span class="hint">指出下列句子用了哪种修辞（可多选）</span></div>\n'
                        '  <div class="bank"><b>选项</b>：%s</div>\n  <ol class="fill">\n%s\n  </ol>\n</div>'
                        % (g("QUIZ_BANK", "A. 排比 anaphora ｜ B. 对偶 antithesis ｜ C. 隐喻 metaphor ｜ D. 引喻 allusion"), rhet_items))
        if QUIZ_FILL:
            quiz.append('<div class="quiz">\n  <div class="qhead">练习三 · 名句填空<span class="hint">凭记忆补全（先背再看答案）</span></div>\n'
                        '  <ol class="fill">\n%s\n  </ol>\n</div>' % fill_items)
        parts.append("\n\n".join(quiz))

    if ANSWERS:
        parts.append('<h2 class="section">八、答案</h2>\n\n<div class="answers">\n%s\n</div>' % ANSWERS)

    footer_text = g("FOOTER")
    if not footer_text:
        footer_text = "%s ｜ 全文精读 + 词源 + 修辞 + 跟读 ｜ 👋" % TITLE
    parts.append('<div class="footer">%s</div>' % footer_text)

    html = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
            '<title>%s · 精读</title>\n<style>\n%s\n</style>\n</head>\n'
            '<body>\n%s\n</body>\n<script>\n%s\n</script>\n</html>\n'
            % (TITLE, css, "\n\n".join(parts), js))

    io.open(out_path, "w", encoding="utf-8").write(html)
    print("wrote", out_path, len(html), "chars")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("用法: python3 build_article.py <内容模块.py> <输出.html>")
    build(sys.argv[1], sys.argv[2])
