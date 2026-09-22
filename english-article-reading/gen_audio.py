#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""english-article-reading 技能：为精读页生成逐句朗读音频（edge-tts 神经网络）。

用法:
    python3 gen_audio.py <页面.html> [--voice en-US-AriaNeural] [--force] [--concurrency 8]

产出与注入：
- 逐句：音频存到与 HTML 同目录的 `<文件名>.audio/sNNN.mp3`；
  每句 `<div class="sent">` 会加上 `data-audio="<...>.audio/sNNN.mp3"`。
- **词源表的单词**（`<b class="w">`）：`wNNN.mp3`，并把 `data-audio` 挂在 `<b>` 上。
- **名言金句**（`<span class="t quote">`）：`qNNN.mp3`，同样注入 `data-audio`。
  这两类让「重点词汇词源」和「名言金句」两节也能点读。

其它：
- **增量**：默认只合成缺失的音频文件（`--force` 才全部重合成），
  所以给老页面补单词/金句音频时不必重跑几百句。
- 页面侧由 `read_aloud.js` 挂 🔊 按钮：优先系统语音，缺失时回放这里的 MP3。
- 需联网。
"""
import argparse
import asyncio
import html as html_mod
import io
import os
import re
import sys

try:
    import edge_tts
except ImportError:
    sys.exit("未安装 edge-tts，请先: python3 -m pip install --user --break-system-packages edge-tts")


def extract(seg):
    seg = re.sub(r'<span class="pnum">.*?</span>', '', seg, flags=re.S)
    seg = re.sub(r'<span class="sup">.*?</span>', '', seg, flags=re.S)
    seg = re.sub(r'<[^>]+>', '', seg)
    seg = html_mod.unescape(seg)
    seg = re.sub(r'\s+', ' ', seg).strip()
    return re.sub(r'\s+([.,!?;:])', r'\1', seg)


async def synth_one(text, voice, path, sem, tries=3):
    async with sem:
        for i in range(tries):
            try:
                await edge_tts.Communicate(text, voice).save(path)
                return
            except Exception:  # noqa
                if i == tries - 1:
                    raise
                await asyncio.sleep(1.0 + i)


async def _run(tasks):
    await asyncio.gather(*tasks)


def normalize(src):
    """清掉页面里旧的 data-audio（逐句/单词/金句），让解析与注入都可重复运行。

    **必须在 collect_jobs 之前调用**：否则 `<div class="sent">` 因为已经带了
    data-audio 属性而匹配不上，会报「没解析到句子」。
    """
    src = re.sub(r'(<div class="sent")\s+data-audio="[^"]*"', r'\1', src)
    src = re.sub(r'(<b class="w")\s+data-audio="[^"]*"', r'\1', src)
    src = re.sub(r'(<span class="t quote")\s+data-audio="[^"]*"', r'\1', src)
    return src


def collect_jobs(src, folder, with_extras=True):
    """从页面里取出全部 (文本, 文件名, 注入用的正则) 任务，顺序稳定、可重复。"""
    jobs = []

    # 1) 逐句：s001…
    for i, seg in enumerate(re.findall(r'<div class="sent">(.*?)(?=<div class="brk">)', src, re.S), 1):
        jobs.append((extract(seg), "s%03d.mp3" % i, "sent", i))

    # 2) 词源表单词：w001…
    if with_extras:
        for i, m in enumerate(re.finditer(r'<b class="w">(.*?)</b>', src, re.S), 1):
            jobs.append((extract(m.group(1)), "w%03d.mp3" % i, "word", i))

    # 3) 名言金句：q001…
    if with_extras:
        for i, m in enumerate(re.finditer(r'<span class="t quote">(.*?)</span>', src, re.S), 1):
            jobs.append((extract(m.group(1)), "q%03d.mp3" % i, "quote", i))

    return jobs


def inject(src, folder, jobs):
    """把 data-audio 注入到对应元素上（先清旧值，保证可重复运行）。"""
    # 旧值已在 normalize() 里清过
    counters = {"sent": [0], "word": [0], "quote": [0]}
    pats = {
        "sent": (re.compile(r'<div class="sent">'),
                 '<div class="sent" data-audio="%s/%s">'),
        "word": (re.compile(r'<b class="w">'),
                 '<b class="w" data-audio="%s/%s">'),
        "quote": (re.compile(r'<span class="t quote">'),
                  '<span class="t quote" data-audio="%s/%s">'),
    }
    out = src
    for kind in ("sent", "word", "quote"):
        rx, tpl = pats[kind]
        names = [j[1] for j in jobs if j[2] == kind]
        state = {"i": 0}

        def repl(m, tpl=tpl, names=names, state=state):
            if state["i"] >= len(names):
                return m.group(0)
            name = names[state["i"]]
            state["i"] += 1
            return tpl % (folder, name)

        out = rx.sub(repl, out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--voice", default="en-US-AriaNeural")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--no-extras", action="store_true",
                    help="只做逐句音频，跳过词源单词与名言金句")
    a = ap.parse_args()

    path = os.path.abspath(a.html)
    src = normalize(io.open(path, encoding="utf-8").read())
    with_extras = not a.no_extras

    stem = os.path.splitext(os.path.basename(path))[0]
    folder = stem + ".audio"
    outdir = os.path.join(os.path.dirname(path), folder)
    os.makedirs(outdir, exist_ok=True)

    jobs = collect_jobs(src, folder, with_extras)
    n_sent = sum(1 for j in jobs if j[2] == "sent")
    n_word = sum(1 for j in jobs if j[2] == "word")
    n_quote = sum(1 for j in jobs if j[2] == "quote")
    if not n_sent:
        sys.exit("没解析到句子（<div class=\"sent\">），确认这是精读页吗？")

    # 增量：默认只补缺失的
    todo = [j for j in jobs if a.force or not os.path.exists(os.path.join(outdir, j[1]))]
    print("voice=%s  句=%d 词=%d 金句=%d  待合成=%d  -> %s"
          % (a.voice, n_sent, n_word, n_quote, len(todo), outdir))

    sem = asyncio.Semaphore(a.concurrency)
    tasks = [synth_one(t, a.voice, os.path.join(outdir, name), sem)
             for t, name, _kind, _i in todo if t]
    if tasks:
        asyncio.run(_run(tasks))
    print("audio done: 新合成 %d 个文件" % len(tasks))

    io.open(path, "w", encoding="utf-8").write(inject(src, folder, jobs))
    print("injected data-audio into", path)


if __name__ == "__main__":
    main()
