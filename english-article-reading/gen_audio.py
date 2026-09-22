#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 edge-tts（微软神经网络语音）为每句英文预生成 MP3，并写回 data-audio。

用法:
    python3 gen_audio.py <桌面.html> [--voice en-US-AriaNeural] [--force] [--concurrency 8]

- 音频存到与 HTML 同目录的 `<文件名>.audio/s001.mp3 …`；
- 每句 `<div class="sent">` 会加上 data-audio="<...>.audio/sNNN.mp3"；
- 页面 read_aloud.js 优先播放该音频，缺失时回退到系统 speechSynthesis；
- 需要联网（edge-tts 在线合成）。幂等：已注入则跳过，--force 可重生成。
可选音色：en-US-AriaNeural / JennyNeural / GuyNeural / ChristopherNeural /
          MichelleNeural / EricNeural / RogerNeural / SteffanNeural
"""
import argparse, asyncio, html as html_mod, io, os, re, sys

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
            except Exception as e:  # noqa
                if i == tries - 1:
                    raise
                await asyncio.sleep(1.0 + i)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--voice", default="en-US-AriaNeural")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--concurrency", type=int, default=8)
    a = ap.parse_args()

    path = os.path.abspath(a.html)
    src = io.open(path, encoding="utf-8").read()
    if "data-audio=" in src and not a.force:
        print("skip (already has data-audio; use --force):", path)
        return

    # 归一化：先去掉旧的 data-audio
    src = re.sub(r'(<div class="sent")\s+data-audio="[^"]*"', r'\1', src)

    segs = re.findall(r'<div class="sent">(.*?)(?=<div class="brk">)', src, re.S)
    n_tags = src.count('<div class="sent">')
    if not segs or len(segs) != n_tags:
        sys.exit("句子解析失败: segs=%d tags=%d" % (len(segs), n_tags))
    texts = [extract(s) for s in segs]

    stem = os.path.splitext(os.path.basename(path))[0]
    folder = stem + ".audio"
    outdir = os.path.join(os.path.dirname(path), folder)
    os.makedirs(outdir, exist_ok=True)
    print("voice=%s  sentences=%d  -> %s" % (a.voice, len(texts), outdir))

    sem = asyncio.Semaphore(a.concurrency)
    tasks = [synth_one(t, a.voice, os.path.join(outdir, "s%03d.mp3" % (i + 1)), sem)
             for i, t in enumerate(texts)]
    asyncio.run(_run(tasks))
    print("audio done:", len(tasks), "files")

    counter = [0]

    def repl(m):
        i = counter[0]
        counter[0] += 1
        return '<div class="sent" data-audio="%s/s%03d.mp3">' % (folder, i + 1)

    out = re.sub(r'<div class="sent">', repl, src)
    io.open(path, "w", encoding="utf-8").write(out)
    print("injected data-audio into", path)


async def _run(tasks):
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    main()
