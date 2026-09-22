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
    ("#c3d9f7", "#16306b"),   # 蓝
    ("#c2e6ce", "#0f4023"),   # 绿
    ("#f8dd9e", "#6b3f02"),   # 琥珀
    ("#f6c2db", "#8a1244"),   # 玫红
    ("#d7cbf5", "#4a1a9e"),   # 紫
    ("#bde3d7", "#0a4f4d"),   # 青
]
CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚"

# 「与上级的关系」→ 角色标记（emoji）。颜色随语义，不再随序号循环。
REL_EMOJI = {
    "骨架": "🔵", "主语": "🔵", "主句": "🔵", "主谓": "🔵", "分句": "🔵",
    "分句一": "🔵", "分句二": "🔵", "分句三": "🔵", "倒装": "🔵", "形式主语": "🔵",
    "谓语": "🟢", "动作": "🟢", "做什么": "🟢", "系表": "🟢",
    "祈使": "🟢", "被动": "🟢",
    "宾语": "🟠", "表语": "🟠", "双宾": "🟠", "补语": "🟠", "宾补": "🟠",
    "引语": "🟠", "对象": "🟠", "施事": "🟠", "受事": "🟠", "与事": "🟠",
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
    # 修辞/语义类自由标签（老页面常用，非语法术语）
    "核心": "🔵", "占位": "🔵",
    "指代": "🟡",
    "内容": "🟠", "给谁": "🟠", "转述": "🟠", "引文": "🟠", "引歌": "🟠", "引语续": "🟠",
    "副歌": "🟠",
    "排比": "🟤", "对仗": "🟤",
    "劝告": "🟢", "揭示": "🟢", "揭晓": "🟢", "回应": "🟢", "回答": "🟢",
    "路径": "🟣", "位置": "🟣", "软化": "🟣", "目标": "🟣", "双重否定": "🟣", "伴随": "🟣",
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

# 角色类别 → (中文名, 色值)。**唯一色源**：色点、图例都由它生成，
# 避免图例里硬编码的色值和实际渲染脱节。
ROLE_TABLE = [
    ("skeleton", "骨架 / 主语", "#334155"),
    ("pred",     "谓语 / 动作", "#0f766e"),
    ("obj",      "宾语 / 施事", "#b45309"),
    ("attr",     "定语 / 同位语", "#6d28d9"),
    ("adv",      "非谓语状语", "#1d4ed8"),
    ("clause",   "限定从句", "#0e7490"),
    ("coord",    "并列", "#4d7c0f"),
    ("contrast", "转折 / 过渡", "#be123c"),
]
ROLE_NAME = dict((k, n) for k, n, _ in ROLE_TABLE)
ROLE_COLOR = dict((k, c) for k, _, c in ROLE_TABLE)


def role_legend():
    """图例 HTML：用色点 + 中文名，顺序与 ROLE_TABLE 一致。"""
    items = "".join(
        '<span class="lg"><i style="background:%s"></i>%s</span>' % (c, n)
        for _, n, c in ROLE_TABLE)
    return ('<div class="legend"><span class="item">🧱 分层拆解</span>'
            '句下拆解框里 <b>编号 ↔ 色块 ↔ 汉语解释</b> 一一对应；'
            '<b>缩进 = 挂接层级</b>（往右缩进的成分挂在上一行下面）。'
            '每行深色粗体那部分是<b>这块在给谁补充什么</b>，'
            '前面色点是它与上级的关系：%s。'
            '读法：先把最左边不缩进的骨架立起来，其余全是在它上面加细节。</div>' % items)

# 角色 → 色点类别。**颜色不用 emoji 实现**：emoji 在缺字体的环境里会退化成
# 单色方块（整个标记列变成一片灰），也不受 CSS 控制、无法精确调色与打印。
# 这里把 emoji 当「角色键」，实际渲染成 CSS 画的色点，跨平台一致。
CAT_BY_EMOJI = {
    "🔵": "skeleton", "🟢": "pred", "🟠": "obj", "🟡": "attr",
    "🟣": "adv", "🩵": "clause", "🟤": "coord", "🔴": "contrast",
}
ROLE_EMOJI_SET = frozenset(CAT_BY_EMOJI)
CAT_BY_REL = {
    "骨架": "skeleton", "主语": "skeleton", "主句": "skeleton", "主谓": "skeleton",
    "分句": "skeleton", "分句一": "skeleton", "分句二": "skeleton", "分句三": "skeleton",
    "倒装": "skeleton", "形式主语": "skeleton", "短句": "skeleton",
    "谓语": "pred", "动作": "pred", "做什么": "pred", "系表": "pred",
    "祈使": "pred", "被动": "pred",
    "宾语": "obj", "表语": "obj", "双宾": "obj", "补语": "obj", "宾补": "obj",
    "引语": "obj", "对象": "obj", "施事": "obj", "受事": "obj", "与事": "obj",
    "定语": "attr", "同位": "attr", "同位语": "attr", "修饰": "attr", "补充": "attr",
    "并列": "coord",
    "转折": "contrast", "让步": "contrast", "对比": "contrast", "收束": "contrast",
    "过渡": "contrast", "结果": "contrast", "判断": "contrast", "结论": "contrast",
}


def role_cat(emoji, rel, tag):
    """决定色点颜色类别：优先看 emoji（角色键），再退回关系名 / 语法标签。"""
    if emoji in CAT_BY_EMOJI:
        return CAT_BY_EMOJI[emoji]
    for cand in (rel, tag):
        if not cand:
            continue
        c = REL_SEP.split(cand)[0].strip()
        if c in CAT_BY_REL:
            return CAT_BY_REL[c]
        for key, cat in CAT_BY_REL.items():
            if key in c:
                return cat
    return "adv"

warnings = []  # 内容模块的写法告警（如把语法术语写进了 mod）


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


# 这些字样属于语法术语；`mod` 里出现它们说明写成了语法标签而非「作用于谁」
GRAMMAR_WORDS = ("从句", "状语", "定语", "谓语", "主语", "宾语", "表语",
                 "同位语", "分词", "不定式", "动名词", "补语", "插入语")

# 兜底：把「与上级的关系」翻译成「在给谁补充什么」的人话
MOD_BY_REL = {
    "🟣": ("补充", "前面的动作"),
    "🩵": ("补充", "前面整句的信息"),
    "🟡": ("限定", "前面的名词"),
    "🟠": ("交代", "动作落到谁身上"),
    "🟢": ("说明", "主语做了什么"),
    "🟤": ("并列", "另起一条主干"),
    "🔴": ("转折", "把前面的话拐个弯"),
    "🔵": ("骨架", "全句的主干"),
}
# 作者已在 mod 里写过的「关系称呼」；命中则直接原样用，不再加前缀
MOD_LEAD = ("补充", "限定", "交代", "说明", "并列", "转折", "骨架", "修饰",
            "解释", "回指", "另起", "追加", "强调", "收束")


def _is_grammar_only(mod):
    """判断 mod 是否「只是语法术语」而非「在给谁补充什么」。

    只拦真正的术语堆砌（短、且以术语收尾、又不含任何关系词），
    像「拐弯之后的真正主语和谓语」这种完整描述不算违规。
    """
    if not mod or any(mod.startswith(x) for x in MOD_LEAD):
        return False
    has_term = any(w in mod for w in GRAMMAR_WORDS)
    if not has_term:
        return False
    # 含「关系/作用」类词的，是合格描述
    if any(k in mod for k in ("谁", "什么", "哪", "时候", "怎么", "为", "给", "对")):
        return False
    return len(mod) <= 8


def _usable(*cands):
    """挑一个可以写进人话的候选：非空、且不是语法术语。"""
    for c in cands:
        if c and not any(w in c for w in GRAMMAR_WORDS):
            return c
    return ""


# 关系名去掉这些语法后缀后，往往剩一个可读的语义词（时间状语 → 时间）
GRAMMAR_SUFFIXES = ("从句", "状语", "定语", "短语", "结构", "成分")
# 语义词 → 人话（用于兜底 mod；比「补充前面的动作」具体得多）
NATURAL = {
    "时间": "发生的时间", "地点": "发生的地点", "目的": "目的",
    "原因": "原因", "条件": "条件", "方式": "方式", "范围": "范围",
    "事由": "事由", "时长": "持续多久", "方向": "方向", "起点": "起点",
    "终点": "终点", "工具": "用什么", "比较": "比较的对象", "对象": "对象",
    "补充": "补充说明", "修饰": "修饰的对象",
    "宾语": "动词的宾语内容", "表语": "主语是什么", "补语": "补充说明",
    "定语": "是哪一个 / 什么样的", "同位": "同位说明", "插入": "插入的说明",
    "分词": "伴随的动作", "不定式": "要做的动作", "动名词": "动作本身",
    "引语": "引述的原话", "疑问": "疑问的内容", "施事": "由谁来做",
    "受事": "承受动作的一方",
}


def _natural(rel, tag):
    """把「时间状语」这类关系名剥成「时间」，再映射成「发生的时间」。"""
    c = (rel or tag or "").strip()
    for suf in GRAMMAR_SUFFIXES:
        if c.endswith(suf) and len(c) > len(suf):
            c = c[: -len(suf)]
    c = REL_SEP.split(c)[0].strip()
    return NATURAL.get(c, "")


def infer_mod(rel, tag, depth, emoji, author_mod):
    """`mod` 缺省时的兜底描述——**只有作者没写 mod 时才走到这里**。

    口吻统一为「在给谁补充什么」，不含语法术语。
    作者写了 mod 就原样使用，绝不加前缀（否则会出现「补充：补充：…」）。
    """
    if author_mod:
        return author_mod
    if depth == 0 and emoji in ("🔵", "🟢"):
        return "全句骨架的一部分"
    act, tgt = MOD_BY_REL.get(emoji, ("补充", "前面的信息"))
    who = _natural(rel, tag) or _usable(rel, tag)
    if not who:
        return "%s：%s" % (act, tgt)      # 统一用冒号，避免「骨架全句的主干」这类粘连
    if who == act:
        return who          # 避免「并列：并列」「转折：转折」这类重复
    return "%s：%s" % (act, who)


def strip_role_emoji(s):
    """去掉语法标签/关系名尾部的角色 emoji。

    颜色已由 CSS 色点负责，标签里再带 emoji 是冗余（且缺字体的环境会变方块）。
    只清角色 emoji，不动标签正文。
    """
    if not s:
        return s
    s = "".join(ch for ch in s if ch not in ROLE_EMOJI_SET)
    return s.strip()


# note 里引用角色 emoji 时（如「是从句（🩵）不是短语（🟣）」），
# 换成不依赖 emoji 字体的文字说法，否则在无 emoji 环境下会变成方块。
NOTE_EMOJI_WORD = {
    "🔵": "骨架色", "🟢": "谓语色", "🟠": "宾语色", "🟡": "定语色",
    "🟣": "状语色", "🩵": "从句色", "🟤": "并列色", "🔴": "转折色",
}


def normalize_note(s):
    """把 note 里的角色 emoji 换成文字说法（其余照原样）。"""
    if not s:
        return s
    for e, w in NOTE_EMOJI_WORD.items():
        s = s.replace(e, w)
    return s


def norm_chunk(c):
    """把 3/4/5/6 元组统一成 (text, tag, note, depth, rel, mod, emoji)。

    字段顺序（前 3 个是旧格式，永远不变）：
        0 text  英文原文
        1 tag   语法标签（小字参考）
        2 note  汉语解释
        3 depth 挂接层级（0 = 骨架）
        4 rel   与上级的关系名（决定 emoji 与兜底措辞）
        5 mod   **在给谁补充什么**（主视觉，自然语言）
        6 emoji 覆盖自动推断的角色标记

    向后兼容：3 元组 → depth=0、rel/mod/emoji 全部自动推断，旧模块无需改动。
    """
    c = list(c) + [None] * (7 - len(c))
    text, tag, note, depth, rel, mod, emoji = c[:7]
    tag = strip_role_emoji(tag or "")
    depth = int(depth or 0)
    if not rel:
        rel = REL_SEP.split(tag)[0].split("+")[0].strip() or tag
    rel = strip_role_emoji(rel)
    mod = strip_role_emoji(mod) if mod else mod
    if _is_grammar_only(mod):
        # 提醒：mod 要写「在给谁补充什么」，不是语法术语
        warnings.append("mod 写成了语法术语：%r（应写「在给谁补充什么」，如「补充：被收养的时间」）" % mod)
    if not emoji:
        emoji = infer_emoji(tag, rel)
    mod = infer_mod(rel, tag, depth, emoji, mod)
    return (text, tag, normalize_note(note or ""), depth, rel, mod, emoji)


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


# 未显式给「层级」的句子，是否按规则自动推断（骨架 d0 / 修饰语逐层右挂）。
# 老模块只有 3 元组，开启后也能得到树形；设 False 则保持全平铺。
INFER_LAYOUT = True

# 这些标签算「骨架」：它们作为主干并列展开，不往右缩进
SPINE_WORDS = ("主句", "分句", "主谓", "主语", "谓语", "祈使", "并列", "短句",
               "开场", "插入语", "倒装", "形式主语", "被动谓语", "从句主句",
               "祝词", "语气词", "强调")


def is_spine(tag):
    return any(k in (tag or "") for k in SPINE_WORDS)


def infer_depths(tags):
    """按「骨架 d0、修饰语挂到前一个骨架下、连续修饰语逐层加深」推断层级。

    规则是可预期的近似，不是句法分析：
    - 骨架类标签 → d0；
    - 句首的修饰语（前面还没有骨架）→ d0，避免句子以缩进行开头；
    - 其余修饰语 → 紧跟骨架时 d1，连续出现则逐层 +1，上限 d3。
    个别判断（如并列分句被当作修饰语）仍需人工校正，改模块里的第 4 个元素即可。
    """
    out, depth, seen_spine = [], 0, False
    for i, tag in enumerate(tags):
        if is_spine(tag):
            depth, seen_spine = 0, True
        elif not seen_spine:
            depth = 0
        elif i == 0 or is_spine(tags[i - 1]):
            depth = 1
        else:
            depth = min(depth + 1, 3)
        out.append(depth)
    return out


def render_sentence(pnum, punct, chunks):
    # 老模块只写 3 元组：先按规则补出层级，再走统一渲染
    if INFER_LAYOUT and not any(len(c) >= 4 for c in chunks):
        ds = infer_depths([(c[1] if len(c) > 1 else "") for c in chunks])
        chunks = [tuple(c) + (d,) for c, d in zip(chunks, ds)]

    metas, cks = [], []
    for i, raw in enumerate(chunks):
        text, tag, note, depth, rel, mod, emoji = norm_chunk(raw)
        bg, fg = PALETTE[i % len(PALETTE)]
        t = supify(text)
        cks.append('<span class="ck" style="background:%s;color:%s">%s</span>' % (bg, fg, t))
        metas.append({"num": i + 1, "tag": tag, "note": note, "depth": depth,
                      "emoji": emoji, "rel": rel, "mod": mod,
                      "cat": role_cat(emoji, rel, tag),
                      "bg": bg, "fg": fg, "html": t})

    # 本层末行标记：看后面还有没有同层或更深层的行
    for i, m in enumerate(metas):
        m["last"] = not any(x["depth"] >= m["depth"] for x in metas[i + 1:])
    prefixes = build_branches([(m["num"], m["depth"], m["last"]) for m in metas])

    lys = []
    for m, prefix in zip(metas, prefixes):
        branch = ('<span class="tbranch">%s</span>' % prefix) if prefix else ''
        # 主视觉 = mod（这块在给谁补充信息）；语法术语只作小字参考
        mod = m["mod"]
        if mod == m["tag"]:
            mod = ""
        mod_html = ('<span class="mod">%s</span>' % mod) if mod else ''
        lys.append('<div class="ly d%d">%s'
                   '<span class="chip" style="background:%s">%d</span>'
                   '<span class="role" data-cat="%s" title="%s %s"></span>'
                   '<span class="sg" style="color:%s">%s</span>'
                   '%s<span class="tg">%s</span>'
                   '<span class="note">%s</span></div>'
                   % (m["depth"], branch, m["fg"], m["num"], m["cat"],
                      m["emoji"], m["rel"], m["fg"], m["html"], mod_html, m["tag"], m["note"]))
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

%s

%s""" % (TITLE, SUB, DATE, g("BACKGROUND", ""), role_legend(), render_speech(PARAS)))

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
    if warnings:
        print("\n⚠️  内容模块写法告警 %d 条（不影响生成，但建议改）：" % len(warnings))
        for w in dict.fromkeys(warnings):   # 去重、保序
            print("   -", w)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("用法: python3 build_article.py <内容模块.py> <输出.html>")
    build(sys.argv[1], sys.argv[2])
