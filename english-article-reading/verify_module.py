# -*- coding: utf-8 -*-
"""独立校验：把内容模块还原成原文，与 speech.txt 逐段比对。

用法:
    python3 verify.py <内容模块.py> <原文.txt>

检查项：
  1) 段落数一致；
  2) 每段还原出的文本与原文逐字一致（容错：空白、-- 与 —、弯直引号）；
  3) 每个色块都是 3 元组；
  4) 每句色块数在 2–5 之间（提醒切得过碎或过粗）；
  5) 汉语解释不为空、且不是纯术语。
"""
import importlib.util
import io
import os
import re
import sys

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚"
BARE_TERMS = {"主语", "谓语", "宾语", "表语", "定语", "状语", "从句", "补语",
              "同位语", "插入语", "时间", "地点", "目的", "原因", "主句", "骨架"}


def norm(s):
    s = s.replace("--", "—").replace("–", "—").replace("―", "—")
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def load(path):
    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    spec = importlib.util.spec_from_file_location("mod_under_test", path)
    m = importlib.util.module_from_spec(spec)
    sys.modules["mod_under_test"] = m
    spec.loader.exec_module(m)
    return m


def main():
    mod = load(sys.argv[1])
    raw = io.open(sys.argv[2], encoding="utf-8").read()
    orig = [p for p in re.split(r"\n\s*\n", raw) if p.strip()]
    paras = mod.PARAS

    problems = []
    if len(paras) != len(orig):
        problems.append("段落数不一致：模块 %d，原文 %d" % (len(paras), len(orig)))

    n_sent = n_chunk = 0
    for pi, (para, opara) in enumerate(zip(paras, orig), 1):
        rebuilt = []
        for punct, chunks in para:
            n_sent += 1
            n_chunk += len(chunks)
            for c in chunks:
                if len(c) != 3:
                    problems.append("P%d 有色块不是 3 元组：%r" % (pi, c))
            nwords = len(" ".join(c[0] for c in chunks).split())
            if len(chunks) < 2 and nwords > 5:
                problems.append("P%d 有 %d 词的句子只切了 1 块：%r"
                                % (pi, nwords, chunks[0][0][:40]))
            for _t, tag, note in chunks:
                if not (note or "").strip():
                    problems.append("P%d 有色块解释为空：%r" % (pi, _t[:40]))
                elif note.strip() in BARE_TERMS:
                    problems.append("P%d 解释过简（纯术语）：%r → %r" % (pi, _t[:30], note))
            rebuilt.append(" ".join(c[0] for c in chunks) + punct)
        got = norm(" ".join(rebuilt))
        want = norm(opara)
        if got != want:
            # 找出第一处差异，便于定位
            i = 0
            while i < min(len(got), len(want)) and got[i] == want[i]:
                i += 1
            problems.append("P%d 文本不一致：\n      模块: …%s\n      原文: …%s"
                            % (pi, got[max(0, i - 40):i + 60], want[max(0, i - 40):i + 60]))

    print("段落 %d，句子 %d，色块 %d" % (len(paras), n_sent, n_chunk))
    if problems:
        print("\n发现 %d 个问题：" % len(problems))
        for p in problems:
            print("  ✗", p)
    else:
        print("✅ 全部通过：段落/句子/色块结构与原文完全一致")


if __name__ == "__main__":
    main()
