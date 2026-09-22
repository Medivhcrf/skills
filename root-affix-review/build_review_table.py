#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""root-affix-review 方案A：三栏回忆表生成器
扫描 /home/crf/english 下所有历史词根词缀 HTML，解析卡片数据，
生成"词根 | 含义(书写) | 代表词(书写)"三栏回忆表 + 答案区。
用法: python3 build_review_table.py [--out 输出文件名] [--max-days N]
"""
import sys
from pathlib import Path
from datetime import date, datetime
import html as html_mod

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_review import parse_daily_file, ENGLISH_DIR, fmt_day

SKILL_DIR = Path(__file__).resolve().parent
TEMPLATE = SKILL_DIR / "template-table.html"


def esc(s):
    return html_mod.escape(str(s), quote=False)


def build():
    out_name = None
    max_days = None
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == "--out" and args:
            out_name = args.pop(0)
        elif a == "--max-days" and args:
            max_days = int(args.pop(0))

    # 每日词根词缀页已归档到 daily/ 子目录；根目录兜底以便兼容旧文件
    daily_files = sorted(ENGLISH_DIR.glob("daily/*-词根词缀.html"))
    daily_files += sorted(ENGLISH_DIR.glob("*-词根词缀.html"))
    daily_files = [f for f in daily_files if "复习" not in f.name]
    days = []
    for f in daily_files:
        d = parse_daily_file(f)
        if d["cards"]:
            days.append(d)
    days.sort(key=lambda d: (d["date"], d["day"] or 0))
    if max_days:
        days = days[-max_days:]
    if not days:
        sys.exit("未找到历史词根词缀 HTML 文件")

    total_root = sum(1 for d in days for c in d["cards"] if not c["affix"])
    total_affix = sum(1 for d in days for c in d["cards"] if c["affix"])
    total_all = total_root + total_affix
    first_day, last_day = days[0], days[-1]

    # ---------- 三栏回忆表（练习） ----------
    practice = []
    answer = []
    qno = 0
    for d in days:
        day_label = f"Day {d['day']}" if d["day"] else "补"
        head = f'<h2 class="section">{day_label} ｜ {fmt_day(d["date"])} ｜ 词根 {sum(1 for c in d["cards"] if not c["affix"])} 个 · 词缀 {sum(1 for c in d["cards"] if c["affix"])} 个</h2>'
        pt = ['<table class="mem">']
        at = ['<table class="mem ans">']
        for c in d["cards"]:
            qno += 1
            cls = "affix" if c["affix"] else "root"
            root = esc(c["root"])
            mean = esc(c["meaning"])
            words = " 　".join(esc(w["word"]) for w in c["words"] if w["word"])
            pt.append(
                f'<tr class="{cls}">'
                f'<td class="root-col"><span class="no">{qno}</span>{root}</td>'
                f'<td class="mean-col"></td>'
                f'<td class="word-col"></td>'
                f'</tr>'
            )
            at.append(
                f'<tr class="{cls}">'
                f'<td class="root-col"><span class="no">{qno}</span>{root}</td>'
                f'<td class="mean-col">{mean}</td>'
                f'<td class="word-col">{words}</td>'
                f'</tr>'
            )
        pt.append("</table>")
        at.append("</table>")
        practice.append(head + "".join(pt))
        answer.append(head + "".join(at))

    today = date.today()
    title = f"覆盖 Day {first_day['day']}–{last_day['day']}"
    meta = (f"{today.year} 年 {today.month} 月 {today.day} 日 ｜ 覆盖 {len(days)} 天 · "
            f"词根 {total_root} · 词缀 {total_affix} · 共 {total_all} 个 ｜ 三栏回忆表")

    template = TEMPLATE.read_text(encoding="utf-8")
    html_out = (template
                .replace("【标题】", title)
                .replace("【统计】", meta)
                .replace("【练习内容】", "".join(practice))
                .replace("【答案内容】", "".join(answer)))

    if not out_name:
        out_name = f"{today.isoformat()}-词根词缀复习.html"
    out_path = ENGLISH_DIR / out_name
    out_path.write_text(html_out, encoding="utf-8")

    print(f"解析 {len(days)} 天: " + ", ".join(f"Day{d['day']}" for d in days))
    print(f"词根 {total_root} + 词缀 {total_affix} = {total_all} 个")
    print(f"输出: {out_path}")


if __name__ == "__main__":
    build()
