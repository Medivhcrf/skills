#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为词根/词缀页的单词与例句生成神经网络发音，并注入 data-say（按内容去重共享）。

用法:
    python3 gen_word_audio.py <file1.html> [file2.html ...] [--voice en-US-AriaNeural] [--force]

- 音频存到 <首文件所在目录>/words-audio/<md5>.mp3，跨页按文本去重；
- 目标：每个 <li> 与 .usage 里的第一个 <b>，以及表格 <td class="w"> 里的第一个 <b>；
  表格单元格若混有中文（如 "capture 捕获, receive"），只对英文部分发音；
- 页面 pronounce.js 优先播放音频，缺失时回退系统语音。需要联网。
"""
import argparse, asyncio, hashlib, html as html_mod, io, os, re, sys

try:
    import edge_tts
except ImportError:
    sys.exit("未安装 edge-tts，请先: python3 -m pip install --user --break-system-packages edge-tts")


def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = html_mod.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def english_only(s):
    s = re.sub(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+", " ", s)
    s = re.sub(r"[^A-Za-z0-9 ,.'’\-/]+", " ", s)
    s = re.sub(r"\s*,\s*", ", ", s)
    s = re.sub(r"\s+", " ", s).strip(" ,")
    return s


def is_en(t):
    return bool(t) and bool(re.search(r"[A-Za-z]", t)) and not re.search(r"[\u4e00-\u9fff]", t) and len(t) <= 200


def first_b(block):
    m = re.search(r"<b(?:\s[^>]*)?>(.*?)</b>", block, re.S)
    return m


def say_text(block, mode):
    m = first_b(block)
    if not m:
        return None
    t = clean(m.group(1))
    if mode == "tdw":
        t = english_only(t)
    return t


def contexts(h):
    """yield (mode, block) 三元组对应所有目标容器。"""
    for m in re.finditer(r"<li>.*?</li>", h, re.S):
        yield "plain", m.group(0)
    for m in re.finditer(r'<div class="usage">.*?</div>', h, re.S):
        yield "plain", m.group(0)
    for m in re.finditer(r'<td class="w">.*?</td>', h, re.S):
        yield "tdw", m.group(0)


def targets(h):
    out = set()
    for mode, block in contexts(h):
        t = say_text(block, mode)
        if is_en(t):
            out.add(t)
    return out


def inject(h, textmap):
    def mk(mode, block):
        t = say_text(block, mode)
        if not (t and t in textmap):
            return block

        def rep(mm):
            if "data-say" in (mm.group(1) or ""):
                return mm.group(0)
            return '<b data-say="%s">%s</b>' % (textmap[t], mm.group(2))

        return re.sub(r"<b(\s[^>]*)?>(.*?)</b>", rep, block, count=1, flags=re.S)

    h = re.sub(r"<li>.*?</li>", lambda m: mk("plain", m.group(0)), h, flags=re.S)
    h = re.sub(r'<div class="usage">.*?</div>', lambda m: mk("plain", m.group(0)), h, flags=re.S)
    h = re.sub(r'<td class="w">.*?</td>', lambda m: mk("tdw", m.group(0)), h, flags=re.S)
    return h


async def synth(text, voice, path, sem, tries=3):
    async with sem:
        for i in range(tries):
            try:
                await edge_tts.Communicate(text, voice).save(path)
                return
            except Exception:
                if i == tries - 1:
                    raise
                await asyncio.sleep(1.0 + i)


async def run(tasks):
    await asyncio.gather(*tasks)


def find_site_root(page_dir):
    """向上找站点根：含 words-audio/ 的目录，其次含 index.html 的目录。

    页面已按分类放进 daily/ topic/ review/ 等子目录，而 words-audio/ 是
    跨页共享的、固定在站点根。所以不能再用「页面所在目录」当根。
    """
    d = os.path.abspath(page_dir)
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "words-audio")) or os.path.isfile(os.path.join(d, "index.html")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.path.abspath(page_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--voice", default="en-US-AriaNeural")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--site-root", default="/home/crf/english",
                    help="站点根目录（words-audio/ 所在处）；默认 /home/crf/english")
    a = ap.parse_args()

    files = [os.path.abspath(f) for f in a.files]
    root = a.site_root if a.site_root and os.path.isdir(a.site_root) else find_site_root(os.path.dirname(files[0]))
    adir = os.path.join(root, "words-audio")
    os.makedirs(adir, exist_ok=True)

    # 页面在 daily/ 等子目录里，引用共享音频要上跳一级；
    # 不同目录前缀不同，所以按「文本 → 文件名」存，注入时再逐文件拼前缀。
    def prefix_for(f):
        rel = os.path.relpath(adir, os.path.dirname(f))
        return (rel.replace(os.sep, "/") + "/") if rel != "." else ""

    basemap, all_text = {}, set()
    for f in files:
        h = io.open(f, encoding="utf-8").read()
        all_text |= targets(h)
    for t in all_text:
        basemap[t] = "%s.mp3" % hashlib.md5(t.encode("utf-8")).hexdigest()

    missing = [t for t in all_text
               if a.force or not os.path.exists(os.path.join(adir, basemap[t]))]
    print("文本 %d 条，需生成 %d 条，voice=%s" % (len(all_text), len(missing), a.voice))

    sem = asyncio.Semaphore(a.concurrency)
    tasks = [synth(t, a.voice, os.path.join(adir, basemap[t]), sem) for t in missing]
    if tasks:
        asyncio.run(run(tasks))
    print("音频就绪，目录:", adir)

    for f in files:
        h = io.open(f, encoding="utf-8").read()
        pre = prefix_for(f)
        textmap = {t: pre + b for t, b in basemap.items()}
        io.open(f, "w", encoding="utf-8").write(inject(h, textmap))
    print("已注入 data-say 到 %d 个文件" % len(files))


if __name__ == "__main__":
    main()
