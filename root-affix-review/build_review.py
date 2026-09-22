#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""root-affix-review: 扫描 /home/crf/english 下所有历史词根词缀 HTML，
解析卡片数据，生成复习 HTML（知识清单 + 填词练习 + 例句挖空 + 配对练习 + 答案）。
用法: python3 build_review.py [--out 输出文件名] [--template 模板路径]
"""
import re
import sys
import html as html_mod
import random
from datetime import date, datetime
from pathlib import Path

ENGLISH_DIR = Path("/home/crf/english")
SKILL_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = SKILL_DIR / "template.html"
CARD_RE = re.compile(r'<div class="card([^"]*)"(.*?)</div>\s*(?=<div class="card|</body>)', re.S)


def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return html_mod.unescape(s).strip()


def split_cards(text):
    """按 <div class=card> 切分，用 div 配平找到每张卡片的结束位置。"""
    out = []
    i = 0
    while True:
        start = text.find('<div class="card', i)
        if start == -1:
            break
        depth = 1
        j = text.find(">", start) + 1
        while j < len(text) and depth > 0:
            n_open = text.find("<div", j)
            n_close = text.find("</div>", j)
            if n_close == -1:
                break
            if n_open != -1 and n_open < n_close:
                depth += 1
                j = text.find(">", n_open) + 1
            else:
                depth -= 1
                j = n_close + 6
        out.append(text[start:j])
        i = j
    return out


def parse_card(chunk):
    affix = 'class="card affix"' in chunk or 'class="cardaffix"' in chunk
    card = {"affix": affix, "num": None, "root": "", "meaning": "",
            "trick": "", "etym": "", "evo": "", "words": [], "usage": None}

    m = re.search(r'class="num">\s*(\d+)\s*<', chunk)
    if m:
        card["num"] = int(m.group(1))

    m = re.search(r'class="root">\s*([^<]+?)\s*<', chunk)
    if m:
        card["root"] = strip_tags(m.group(1)).strip()

    m = re.search(r'class="meaning">\s*([^<]+?)\s*<', chunk)
    if m:
        card["meaning"] = strip_tags(m.group(1)).strip()

    for field in ("trick", "etym", "evo"):
        m = re.search(r'<span class="%s">' % field, chunk)
        if m:
            rest = chunk[m.end():]
            nxt = re.search(r'<span class="(?:trick|etym|evo)">|<ul>|<div class="usage"', rest)
            body = rest[: nxt.start()] if nxt else rest
            card[field] = strip_tags(body).strip()
            card[field] = re.sub(r"^(词源|演化|记法)\s*[:：]\s*", "", card[field])

    for li in re.findall(r"<li>(.*?)</li>", chunk, re.S):
        for seg in re.split(r"(<b>.*?</b>)", li, flags=re.S):
            if not seg.strip():
                continue
            if seg.startswith("<b>"):
                word = strip_tags(seg).strip()
                card["words"].append({"word": word, "meaning": ""})
            else:
                meaning = strip_tags(seg).strip()
                if card["words"]:
                    card["words"][-1]["meaning"] = meaning
                elif meaning:
                    card["words"].append({"word": "", "meaning": meaning})

    m = re.search(r'class="usage">(.*?)</div>', chunk, re.S)
    if m:
        inner = m.group(1)
        bm = re.search(r"<b>(.*?)</b>", inner, re.S)
        if bm:
            en = strip_tags(bm.group(1)).strip()
            pre = strip_tags(inner[: bm.start()]).strip("：:")
            post = strip_tags(inner[bm.end():]).strip("：:")
            post = re.split(r"[｜|]", post)[0].strip()
            card["usage"] = {"label": pre, "en": en, "zh": post}

    return card


def split_by_section(text):
    """按 <h2 class="section"> 把正文切成段落，识别『词根』『词缀』标题。"""
    sections = []
    parts = re.split(r'(<h2 class="section">.*?</h2>)', text, flags=re.S)
    for part in parts:
        if part.startswith("<h2"):
            m = re.search(r">(.*?)<", part, re.S)
            sections.append({"title": strip_tags(m.group(1)) if m else "", "html": ""})
        elif part.strip():
            if sections:
                sections[-1]["html"] = part
    return sections


def parse_daily_file(path):
    text = path.read_text(encoding="utf-8")
    date_m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    title_m = re.search(r"<title>(.*?)</title>", text, re.S)
    title = title_m.group(1) if title_m else ""
    day_m = re.search(r"Day\s*(\d+)", title)
    cards = []
    for chunk in split_cards(text):
        card = parse_card(chunk)
        if card["root"]:
            cards.append(card)
    cards.sort(key=lambda c: c["num"] or 99)
    return {
        "date": date_m.group(1) if date_m else "",
        "day": int(day_m.group(1)) if day_m else None,
        "file": path.name,
        "cards": cards,
    }


def fmt_day(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        days_ago = (date.today() - d).days
        return f"{d.year} 年 {d.month} 月 {d.day} 日（{days_ago} 天前）"
    except ValueError:
        return date_str


def blank_for(word):
    n = max(5, len(word))
    return "＿" * n


def esc(s):
    return html_mod.escape(str(s), quote=False)


def main():
    out_name = None
    template_path = DEFAULT_TEMPLATE
    max_per_card = 3
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == "--out" and args:
            out_name = args.pop(0)
        elif a == "--template" and args:
            template_path = Path(args.pop(0))
        elif a == "--max-per-card" and args:
            max_per_card = int(args.pop(0))

    # 每日词根词缀页已归档到 daily/ 子目录；根目录兜底以便兼容旧文件
    daily_files = sorted(ENGLISH_DIR.glob("daily/*-词根词缀.html"))
    daily_files += sorted(ENGLISH_DIR.glob("*-词根词缀.html"))
    daily_files = [f for f in daily_files if "复习" not in f.name]
    days = [parse_daily_file(f) for f in daily_files]
    days.sort(key=lambda d: (d["date"], d["day"] or 0))

    if not days:
        sys.exit("未找到历史词根词缀 HTML 文件")

    total_roots = sum(1 for d in days for c in d["cards"] if not c["affix"])
    total_affix = sum(1 for d in days for c in d["cards"] if c["affix"])
    total_words = sum(len(c["words"]) for d in days for c in d["cards"])
    total_usage = sum(1 for d in days for c in d["cards"] if c["usage"])
    first_day, last_day = days[0], days[-1]

    # ---------- 一、知识清单回顾 ----------
    list_html = []
    for d in days:
        head = f'<div class="day-head">Day {d["day"]} ｜ {fmt_day(d["date"])} ｜ 词根 {sum(1 for c in d["cards"] if not c["affix"])} 个 · 词缀 {sum(1 for c in d["cards"] if c["affix"])} 个</div>'
        cards = []
        for c in d["cards"]:
            cls = "card affix" if c["affix"] else "card"
            words = " ・ ".join(f"<b>{esc(w['word'])}</b>{(' ' + esc(w['meaning'])) if w['meaning'] else ''}" for w in c["words"] if w["word"])
            usage = ""
            if c["usage"]:
                usage = f'<div class="u">{esc(c["usage"]["label"])}：<b>{esc(c["usage"]["en"])}</b> {esc(c["usage"]["zh"])}</div>'
            evo = f'<div class="evo2">{esc(c["evo"])}</div>' if c["evo"] else ""
            cards.append(
                f'<div class="{cls}"><div class="rh"><span class="num">{c["num"]}</span>'
                f'<span class="root">{esc(c["root"])}</span> <span class="mean">{esc(c["meaning"])}</span></div>'
                f'<div class="words">{words}</div>{evo}{usage}</div>'
            )
        list_html.append(head + "".join(cards))

    # ---------- 二、填词练习 ----------
    fill_qs, fill_ans = [], []
    qno = 0
    seen_words = set()
    for d in days:
        for c in d["cards"]:
            picked = 0
            for w in c["words"]:
                if not (w["word"] and w["meaning"]):
                    continue
                key = w["word"].strip().lower()
                if key in seen_words:
                    continue
                if picked >= max_per_card:
                    break
                seen_words.add(key)
                picked += 1
                qno += 1
                mean = re.sub(r"（[^）]*）", "", w["meaning"]).strip()
                fill_qs.append(
                    f'<div class="q"><span class="qn">{qno}</span>'
                    f'【{esc(c["root"])}】{esc(mean)} → {blank_for(w["word"])}</div>'
                )
                fill_ans.append(f'<div class="a"><span class="qn">{qno}</span>{esc(w["word"])}</div>')

    # ---------- 三、例句挖空 ----------
    blank_qs, blank_ans = [], []
    qno = 0
    for d in days:
        for c in d["cards"]:
            if not c["usage"]:
                continue
            u = c["usage"]
            sentence = u["en"]
            target = ""
            for w in c["words"]:
                if w["word"] and re.search(r"\b" + re.escape(w["word"]) + r"\b", sentence):
                    target = w["word"]
                    break
            if not target:
                words = re.findall(r"[A-Za-z][A-Za-z'-]+", sentence)
                target = max(words, key=len) if words else sentence
            shown = re.sub(r"\b" + re.escape(target) + r"\b", blank_for(target), sentence, count=1)
            qno += 1
            blank_qs.append(
                f'<div class="q"><span class="qn">{qno}</span>{esc(shown)}'
                f'<div class="qt">{esc(u["zh"])}（词根 {esc(c["root"])}，共 {len(target)} 个字母）</div></div>'
            )
            blank_ans.append(f'<div class="a"><span class="qn">{qno}</span>{esc(sentence)}</div>')

    # ---------- 四、配对练习 ----------
    rng = random.Random(20260805)
    pairs = []
    for d in days:
        for c in d["cards"]:
            pairs.append((c["root"], c["meaning"], c["affix"], d["day"]))
    roots_col = [p[0] for p in pairs]
    meanings = [p[1] for p in pairs]
    shuf = list(range(len(meanings)))
    rng.shuffle(shuf)
    letters = [chr(ord("A") + i) for i in range(len(meanings))]
    right_col = list(zip(shuf, letters))

    match_html = []
    colA = "".join(
        f'<div class="m-row"><span class="mno">{i+1}</span>{esc(r)}</div>' for i, r in enumerate(roots_col)
    )
    colB = "".join(
        f'<div class="m-row"><span class="mno">{letters[i]}</span>{esc(meanings[s])}</div>'
        for i, s in enumerate(shuf)
    )
    match_html.append(f'<div class="match"><div class="mcol">{colA}</div><div class="mcol">{colB}</div></div>')
    match_ans = " ・ ".join(f"{i+1}-{letters[shuf.index(i)]}" for i in range(len(pairs)))

    # ---------- 答案区 ----------
    ans_html = []
    ans_html.append('<h3 class="sub">一、填词练习答案</h3>' + "".join(fill_ans))
    ans_html.append('<h3 class="sub">二、例句挖空答案</h3>' + "".join(blank_ans))
    ans_html.append(f'<h3 class="sub">三、配对练习答案</h3><div class="a-key">{esc(match_ans)}</div>')

    template = template_path.read_text(encoding="utf-8")
    title = f"词根词缀复习 · 覆盖 Day {first_day['day']}–{last_day['day']}"
    today = date.today()
    meta = (f"{today.year} 年 {today.month} 月 {today.day} 日 ｜ 覆盖 {len(days)} 天 · "
            f"词根 {total_roots} 个 · 词缀 {total_affix} 个 ｜ "
            f"单词 {total_words} 个 · 例句 {total_usage} 句")

    html_out = (template
                .replace("【标题】", title)
                .replace("【统计】", meta)
                .replace("【清单内容】", "".join(list_html))
                .replace("【填词内容】", "".join(fill_qs))
                .replace("【挖空内容】", "".join(blank_qs))
                .replace("【配对内容】", "".join(match_html))
                .replace("【答案内容】", "".join(ans_html)))

    if not out_name:
        out_name = f"{today.isoformat()}-词根词缀复习.html"
    out_path = ENGLISH_DIR / out_name
    out_path.write_text(html_out, encoding="utf-8")

    print(f"解析 {len(days)} 天: " + ", ".join(f"Day{d['day']}" for d in days))
    print(f"词根 {total_roots} + 词缀 {total_affix} = {total_roots+total_affix} 个卡片，单词 {total_words}，例句 {total_usage}")
    print(f"填词 {len(fill_qs)} 题，挖空 {len(blank_qs)} 题，配对 {len(pairs)} 题")
    print(f"输出: {out_path}")


if __name__ == "__main__":
    main()
