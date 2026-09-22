#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将历史每日词根词缀 HTML 汇总为 markdown 总表。
用法: python3 build_summary_md.py [--out 输出路径]
"""
import sys
import re
from pathlib import Path
import html as html_mod
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_review import parse_daily_file, ENGLISH_DIR

SKILL_DIR = Path(__file__).resolve().parent


def esc_text(s):
    return html_mod.unescape(s).strip()


def main():
    out = None
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == "--out" and args:
            out = Path(args.pop(0))

    files = sorted(ENGLISH_DIR.glob("*-词根词缀.html"))
    files = [f for f in files if "复习" not in f.name]
    days = []
    for f in files:
        d = parse_daily_file(f)
        if d["cards"]:
            days.append(d)
    days.sort(key=lambda d: (d["date"], d["day"] or 99))

    total_roots = sum(1 for d in days for c in d["cards"] if not c["affix"])
    total_affix = sum(1 for d in days for c in d["cards"] if c["affix"])
    total_words = sum(len(c["words"]) for d in days for c in d["cards"])
    total_all = total_roots + total_affix
    day_labels = []
    for d in days:
        day_labels.append(f"Day {d['day']}" if d["day"] else "补")
    day_span = f"{day_labels[0]}–{day_labels[-1]}"

    lines = []
    lines.append(f"# 词根词缀总表 · 累计 {total_all} 个")
    lines.append("")
    lines.append(f"> 覆盖 {len(days)} 天（{day_span}）｜ 词根 {total_roots} 个 · 词缀 {total_affix} 个 · 相关单词 {total_words} 个")
    lines.append(f"> 整理日期：{date.today().year} 年 {date.today().month} 月 {date.today().day} 日")
    lines.append("")

    # 速查表
    lines.append("## 速查表")
    lines.append("")
    lines.append("| Day | 类型 | 词根/词缀 | 含义 | 代表词 |")
    lines.append("|-----|------|-----------|------|--------|")
    for d in days:
        day_label = f"Day {d['day']}" if d["day"] else "补"
        for c in d["cards"]:
            typ = "词缀" if c["affix"] else "词根"
            root = esc_text(c["root"])
            mean = esc_text(c["meaning"]).lstrip("=").strip()
            sample = esc_text(c["words"][0]["word"]) if c["words"] else ""
            lines.append(f"| {day_label} | {typ} | **{root}** | {mean} | {sample} |")
    lines.append("")

    # 详细清单
    lines.append("## 详细清单")
    lines.append("")
    lines.append("按 Day 分组，每项含词源、演化、单词列表与生活例句。")
    lines.append("")

    for d in days:
        day_label = f"Day {d['day']}" if d["day"] else "补"
        rn = sum(1 for c in d["cards"] if not c["affix"])
        an = sum(1 for c in d["cards"] if c["affix"])
        lines.append(f"### {day_label}（{d['date']}）· 词根 {rn} 个 + 词缀 {an} 个")
        lines.append("")
        for c in d["cards"]:
            tag = "**词缀** " if c["affix"] else ""
            root = esc_text(c["root"])
            mean = esc_text(c["meaning"]).lstrip("=").strip()
            lines.append(f"- **{root}** {tag}＝ {mean}")
            if c["trick"]:
                trick = esc_text(c["trick"])
                trick = trick.replace("💡 记法：", "").replace("💡 ", "").strip()
                lines.append(f"  - 💡 {trick}")
            if c["etym"]:
                lines.append(f"  - 词源：{esc_text(c['etym'])}")
            if c["evo"]:
                lines.append(f"  - 演化：{esc_text(c['evo'])}")
            if c["words"]:
                parts = []
                for w in c["words"]:
                    if not w["word"]:
                        continue
                    m = esc_text(w["meaning"])
                    m = re.sub(r"（[^（）]*）", "", m).strip()
                    parts.append(f"{esc_text(w['word'])}（{m}）")
                lines.append(f"  - 单词：{'；'.join(parts)}")
            if c["usage"]:
                u = c["usage"]
                lines.append(f"  - 例句：{u['en']} — {u['zh']}")
            lines.append("")

    out_path = out or ENGLISH_DIR / "词根词缀总表.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"词根 {total_roots} + 词缀 {total_affix} = {total_roots + total_affix} 个")
    print(f"输出: {out_path}")


if __name__ == "__main__":
    main()
