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

# 「与上级的关系」→ 角色标记（emoji）。颜色随语义，不再随序号循环。
REL_EMOJI = {
    "骨架": "🔵", "主语": "🔵", "主句": "🔵", "主谓": "🔵", "分句": "🔵",
    "分句一": "🔵", "分句二": "🔵", "分句三": "🔵", "倒装": "🔵", "形式主语": "🔵",
    "谓语": "🟢", "动作": "🟢", "做什么": "🟢", "系表": "🟢",
    "祈使": "🟢", "被动": "🟢",
    "宾语": "🟠", "表语": "🟠", "双宾": "🟠", "补语": "🟠", "宾补": "🟠",
    "引语": "🟠", "对象": "🟠",
    "定语": "🟡", "同位": "🟡", "同位语": "🟡", "修饰": "🟡", "补充": "🟡",
    "状语": "🟣", "时间": "🟣", "地点": "🟣", "目的": "🟣", "事由": "🟣",
    "条件": "🟣", "原因": "🟣", "方式": "🟣", "范围": "🟣", "时长": "🟣",
    "方向": "🟣", "起点": "🟣", "终点": "🟣", "工具": "🟣", "比较": "🟣",
    "插入": "🟣", "插入语": "🟣", "独立": "🟣", "不定式": "🟣",
    "分词": "🟣", "动名词": "🟣",
    "从句": "🩵", "状语从句": "🩵", "定语从句": "🩵", "名词性从句": "🩵",
    "宾语从句": "🩵", "表语从句": "🩵", "主语从句": "🩵", "同位语从句": "🩵",
    "存在句": "🩵", "疑问": "🩵",
    "并列": "🟤", "转折": "🔴", "让步": "🔴", "对比": "🔴", "收束": "🔴",
    "过渡": "🔴", "结果": "🔴", "判断": "🔴", "结论": "🔴",
    # 短句类同义标签统一归为骨架
    "短句": "🔵", "强调": "🔵", "祝词": "🔵", "致谢": "🔵", "语气": "🔵", "虚拟": "🔵",
    # 实测存在的复合标签，直接钉死其唯一归属
    "从句主句": "🩵",
}
# 兜底：按长度从长到短取第一个「被包含」的键，避免「定语」抢走「定语从句」、
# 也兼容「非限定定语从句」这类前后缀变体。注意「引语」需排在「直接引语」之后
# （长度排序已保证），「从句主句」在表中直接钉死。
REL_KEYS = sorted(REL_EMOJI.items(), key=lambda kv: (-len(kv[0]), kv[0]))
# 复合标签的分隔符：「定语/施事」只取「定语」
REL_SEP = re.compile(r"[/／|｜、,，;；]")
TREE = ("├─", "└─", "│", "　")  # ├─ └─ │ 全角空格


def supify(t):
    for ch in CIRC:
        if ch in t:
            t = t.replace(ch, '<span class="sup">%s</span>' % ch)
    return t


def infer_emoji(tag, rel):
    """按「与上级的关系名」推断角色标记；不确定的返回 ⬜（提示作者补映射）。"""
    for cand in (rel, tag):
        if not cand:
            continue
        c = REL_SEP.split(cand)[0].strip()
        if not c:
            continue
        if c in REL_EMOJI:
            return REL_EMOJI[c]
        for key, e in REL_KEYS:
            if key in c:
                return e
    return "⬜"


def norm_chunk(c):
    """把 3/4/5/6 元组统一成 (text, tag, note, depth, emoji, rel)。

    向后兼容：3 元组 → depth=0、emoji/rel 自动推断，输出与旧版完全一致。
    """
    c = list(c) + [None] * (6 - len(c))
    text, tag, note, depth, emoji, rel = c[:6]
    tag = tag or ""
    if not rel:
        rel = REL_SEP.split(tag)[0].split("+")[0].strip() or tag
    if not emoji:
        emoji = infer_emoji(tag, rel)
    return (text, tag, note or "", int(depth or 0), emoji, rel)


def build_branches(metas):
    """(序号, 层级, 是否本层末行) 列表 → 行首树形前缀（用竖线画承接线）。"""
    out = [""] * len(metas)
    for i, (num, depth, last) in enumerate(metas):
        if depth <= 0:
            continue
        parts = []
        for d in range(1, depth):
            anc = None
            for j in range(i - 1, -1, -1):
                if metas[j][1] == d:
                    anc = j
                    break
            parts.append(TREE[3] if (anc is None or metas[anc][2]) else TREE[2])
        parts.append(TREE[1] if last else TREE[0])
        out[i] = "".join(parts)
    return out


def render_sentence(pnum, punct, chunks):
    metas, cks = [], []
    for i, raw in enumerate(chunks):
        text, tag, note, depth, emoji, rel = norm_chunk(raw)
        bg, fg = PALETTE[i % len(PALETTE)]
        t = supify(text)
        cks.append('<span class="ck" style="background:%s;color:%s">%s</span>' % (bg, fg, t))
        metas.append({"num": i + 1, "tag": tag, "note": note, "depth": depth,
                      "emoji": emoji, "rel": rel, "bg": bg, "fg": fg, "html": t})

    # 本层末行标记：看后面还有没有同层或更深层的行
    for i, m in enumerate(metas):
        m["last"] = not any(x["depth"] >= m["depth"] for x in metas[i + 1:])
    prefixes = build_branches([(m["num"], m["depth"], m["last"]) for m in metas])

    lys = []
    for m, prefix in zip(metas, prefixes):
        branch = ('<span class="tbranch">%s</span>' % prefix) if prefix else ''
        lys.append('<div class="ly d%d">%s'
                   '<span class="chip" style="background:%s">%d</span>'
                   '<span class="role" title="%s">%s</span>'
                   '<span class="tg">%s</span><span class="sg" style="color:%s">%s</span>'
                   '<span class="note">%s</span></div>'
                   % (m["depth"], branch, m["bg"], m["num"], m["rel"], m["emoji"],
                      m["tag"], m["fg"], m["html"], m["note"]))
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

<div class="legend"><span class="item" style="background:#dbeafe;color:#1e3a8a">🧱 色块拆解</span>正文按句子成分分色；句下拆解框里<b>编号 ↔ 色块 ↔ 汉语解释</b>一一对应。第二列是<b>与上级的关系标记</b>：🔵骨架/主语　🟢谓语/祈使　🟠宾语/表语/引语　🟡定语/同位语　🟣非谓语状语（不定式·分词·介词短语）　🩵限定从句（含时间/条件/定语从句）　🟤并列　🔴转折/过渡。读法：<b>缩进就是挂接层级</b>——往右缩进的成分挂在上一行下面；先抓最左边不缩进的那一两个词（骨架），其余都是往右挂的补充。</div>

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
