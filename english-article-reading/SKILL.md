---
name: english-article-reading
description: 把英语文章做成「全文精读」页时使用：用户给原文/链接/文件/主题，要求精读、逐句分析、词源、修辞、跟读、自测，或要求批量生成英语文章。产出桌面版 HTML + A4 PDF + 手机版 HTML，结构为「背景—全文精读（色块拆解）—重点词源—修辞分析—跟读要点—金句—自测」。触发场景：用户说「精读这篇文章」「把这篇英语文章做成精读」「英语文章」「像 I Have a Dream 那样」「批量生成英语文章」等。
---

# 英语文章全文精读 → HTML / PDF / 手机版

把一篇英语文章（演讲、散文、社论、课文等）做成结构化的「全文精读」页。
标准范例见 `/home/crf/english/2026-08-27-I-Have-a-Dream.html`（桌面）、
`...-手机版.html`（手机）与 `...pdf`（A4），本技能就是从它抽象出来的。

**工具文件**：`template.html`（桌面模板）、`build_article.py`（数据 → HTML 生成器）、
`build_mobile.py`（桌面 HTML → 手机版）、`read_aloud.css` / `read_aloud.js`（朗读功能）、
`add_read_aloud.py`（给已有页面补朗读）、`examples/steve_jobs_stanford.py`（长文完整示例）。

> **每篇文章都必须产出「三件套」，缺一不可：**
> ① 桌面版 HTML　② 手机版 HTML　③ A4 PDF。
> 除非用户明确说不要其中某项，否则第 8 步的三样全部生成并逐一验证。

## 输出物

| 文件 | 说明 |
| --- | --- |
| `/home/crf/english/<YYYY-MM-DD>-<Title>.html` | 桌面 / A4 版（用于打印 PDF） |
| `/home/crf/english/<YYYY-MM-DD>-<Title>.pdf` | A4 PDF |
| `/home/crf/english/<YYYY-MM-DD>-<Title>-手机版.html` | 手机版（由脚本生成） |

- `<Title>` 用英文标题、连字符连接，如 `I-Have-a-Dream`。
- 日期取当天；HTML 源文件一律保留，方便改排版后重新生成。
- 全部完成后可选跑一次 `python3 /home/crf/english/build_index.py` 更新索引。

## 第 1 步：取文与分段

1. 来源：用户粘贴原文 / 给出 URL（用 webfetch 抓正文）/ 本地文件 / 只给主题（则先挑一篇经典短文并说明来源）。
2. 按自然段编号 `P1 … Pn`，保留原文标点；英文引号统一用 `'`（模板里是英文单引号）。
3. 通读并确定：全篇主旨、反复出现的句式/短语（排比、呼告）、贯穿的隐喻系统、引用来源（圣经/文献/名句）——这些是第 4 步修辞分析的依据。
4. 圈出要讲的重点词（生词、关键概念、词源精彩的词），编号 ① ② ③…，与正文上标一一对应。

## 第 2 步：全文精读（核心 —— 句子结构分色）

对**每个句子**做两件事：正文上色 + 句后拆解框。二者必须严格对应。

### 2.1 正文上色 `.ck`

把句子按「意群 / 句子成分」切成若干块，每块一个 `<span class="ck">`，块间用空格分隔：

```html
<div class="sent"><span class="pnum">P1</span><span class="ck" style="background:#dbeafe;color:#1e3a8a">I am happy</span> <span class="ck" style="background:#bbf7d0;color:#14532d">to join with you</span> <span class="ck" style="background:#fde68a;color:#78350f">today</span> <span class="ck" style="background:#fbcfe8;color:#831843">in what will go down in history as</span> <span class="ck" style="background:#ddd6fe;color:#4c1d95">the greatest demonstration<span class="sup">①</span> for freedom</span> <span class="ck" style="background:#fed7aa;color:#7c2d12">in the history of our nation</span>.</div>
```

**六色盘**（按出现顺序循环取用；background / 文字色）：

| # | background | color | 常用角色 |
| --- | --- | --- | --- |
| 1 | `#dbeafe` | `#1e3a8a` | 主语 / 骨架 |
| 2 | `#bbf7d0` | `#14532d` | 谓语 / 动作 |
| 3 | `#fde68a` | `#78350f` | 时间 / 宾语 |
| 4 | `#fbcfe8` | `#831843` | 从句 / 转折 |
| 5 | `#ddd6fe` | `#4c1d95` | 核心名词 / 揭示 |
| 6 | `#fed7aa` | `#7c2d12` | 地点 / 范围 |

### 2.2 句后拆解框 `.brk`

紧跟句子后面，放一个 `.brk`，里面每个 `.ly` 对应一个色块，**数量、编号、颜色、文本完全一致**：

```html
<div class="brk"><div class="ly"><span class="chip" style="background:#dbeafe">1</span><span class="tg">骨架</span><span class="sg" style="color:#1e3a8a">I am happy</span><span class="note">先亮情绪：我很高兴——说话人开门见山给心情</span></div>
<div class="ly"><span class="chip" style="background:#bbf7d0">2</span><span class="tg">做什么</span><span class="sg" style="color:#14532d">to join with you</span><span class="note">高兴去做的事。注意是 join with you 而不是 join you：with 表“并肩”</span></div>
<div class="ly"><span class="chip" style="background:#fde68a">3</span><span class="tg">时间</span><span class="sg" style="color:#78350f">today</span><span class="note">再叠时间点：就在今天</span></div>
</div>
```

- `.chip` 的 `background` = 对应 `.ck` 的 `background`（编号 1、2、3…）。
- `.tg` 写语法角色（骨架 / 时间 / 主语+同位 / 谓语 / 定语从句 / 目的 / 转折 / 收束 …）。
- `.sg` 的 `color` 和文本 = 对应 `.ck` 的 `color` 和文本。
- `.note` 用汉语说清「这块在句中干什么」+ 语法点 / 易错点 / 修辞作用。

> **只写一次标题**：不要每句重复「句子结构分色 · 色块 ↔ 拆解行 ↔ 汉语解释」。
> 在第二节标题下放一个 `.legend` 说明一次即可（见模板）。

## 第 3 步：重点词汇词源

- 只收真正值得讲的词（10–28 个），编号 ① ② ③… 与正文上标一一对应。
- 三列表：**单词（含音标）/ 词源本义 / 在文中的含义**。
- 词源必须真实：拉丁 / 希腊 / 古英语原词 + 构词拆解（前缀 + 词根 + 后缀），不确定就换一个词或省略词源。
- 标签：`.n` 编号、`<b>` 单词、`.ipa` 音标、`.e` 词源、第三列写文中含义。

```html
<tr><td><span class="n">①</span><b>demonstration</b> <span class="ipa">/ˌdemənˈstreɪʃn/</span></td><td class="e">拉丁 <b>demonstrare</b>「指出、展示」（de- + monstrare「显示」）</td><td>示威游行——「把（不公）亮出来给大家看」</td></tr>
```

## 第 4 步：修辞分析

- 4–5 张 `.card`，覆盖文中主要修辞（按实际选取）：**排比 anaphora、隐喻 metaphor、引喻 allusion、对偶 antithesis、递进 climax** 等。
- `.head .num` 编号，`.head .t` 修辞名；`.why` 引原文、点结构、说效果；`.usage` 给朗读建议。
- 反复出现的短语用 `.refrain` 高亮，现有色名：`dream / hundred / now / satisfied / goback / ring / free`（对应 CSS 里 `.refrain.xxx`）。若新文章需要新色，在模板 `<style>` 的 `.refrain` 区补一条规则。

## 第 5 步：跟读要点

一段 `.intro` 讲总原则（语速、停顿、升降调、语气词），一张两列表格（要点 / 操作建议），5–7 条。

## 第 6 步：名言金句

3–6 张 `.card`，序号 `A B C…`，`.head .t` 放英文原句，`.why` 讲为什么值得背（修辞点 + 用法）。

## 第 7 步：自测 + 答案

三个练习：
1. **词源连线**：`.qhead` + `<table class="match">`（左单词、右词源本义）。
2. **修辞辨识**：`.bank` 列选项 + `ol.fill` 逐句填答案。
3. **名句填空**：`ol.fill` 挖空。

答案统一放 `.answers`，按 `练习一/二/三` 分行。

## 长文 / 批量：用生成器（数据 → HTML，推荐）

长文（几十上百句）手工写 `.ck` / `.chip` / `.sg` 极易错位。此时改用生成器：把文章写成「内容模块」，脚本自动分色，保证三者严格对齐。

- 生成器：`build_article.py`
- 完整示例：`examples/steve_jobs_stanford.py`（乔布斯 2005 斯坦福演讲，142 句 / 384 组色块 / 24 词源）

### 内容模块格式

```python
TITLE = "Stay Hungry. Stay Foolish."
SUB   = "Steve Jobs · 2005 斯坦福大学毕业典礼演讲"
DATE  = "2026 年 9 月 22 日"
BACKGROUND = "背景段落 HTML（可含 <b>、<span class='refrain settle'>…</span>）"
TIPS_INTRO = "跟读要点开头说明（可选）"

# 正文：段落 → 句子 → (句末标点, [ (色块英文, 语法标签, 汉语解释), ... ])
PARAS = [
    [ (".", [("I'm honored①", "主语+情感", "honored①：感到荣幸"),
             ("to be with you today", "不定式状语", "今天和你们在一起")]) ],
    # …每个段落一个列表，每句一个 (标点, [色块…])
]

VOCAB      = [("①", "honored", "/ˈɒnəd/", "拉丁 <b>honor</b>「荣誉」", "感到荣幸"), ...]
RHET       = [("1", "排比 Anaphora", "why 的 HTML", "usage 的 HTML 或 None"), ...]
TIPS       = [("① 先听再跟", "操作建议"), ...]
QUOTES     = [("A", "英文原句", "why 的 HTML"), ...]
QUIZ_MATCH = [("1. word", "a. 词源本义"), ...]
QUIZ_RHET  = ["题干 —— <b>___</b>", ...]
QUIZ_FILL  = ["挖空句 <b>___</b>", ...]
ANSWERS    = "练习一 …<br>练习二 …<br>练习三 …"
EXTRA_CSS  = ""            # 可选：新增 .refrain 配色等，追加到模板 CSS 后
FOOTER     = "页脚文字"     # 可选
```

- 色块文本里的圈号 ①… 会自动转成 `<span class="sup">`；编号按「首次出现」顺序给即可。
- 每句颜色从六色盘自动循环，**不用手写颜色**。
- 缺省的章节（如没有 `QUOTES`）会自动跳过。

### 命令

```bash
python3 /home/crf/.claude/skills/english-article-reading/build_article.py \
  <内容模块.py> "/home/crf/english/<YYYY-MM-DD>-<Title>.html"
```

生成后同样走下面的 PDF 与手机版步骤。批量时可对每篇文章各写一个内容模块，循环调用。

## 第 8 步：生成 HTML / PDF / 手机版

1. 产出桌面 HTML，二选一：
   - **短篇**：读取 `template.html`，替换所有 `【】` 占位符，**CSS 保持不变**；
   - **长文 / 批量**：写内容模块，用 `build_article.py` 生成（见上一节）。
2. 写入 `/home/crf/english/<YYYY-MM-DD>-<Title>.html`。
3. （推荐）生成神经网络朗读音频（需联网；详见「朗读」一节）。**必须在生成手机版之前**，手机版才会带上音频：

```bash
python3 /home/crf/.claude/skills/english-article-reading/gen_audio.py \
  "/home/crf/english/<YYYY-MM-DD>-<Title>.html" --voice en-US-AriaNeural
```

4. 转 PDF（**必须带 `--no-pdf-header-footer`**）：

```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf="/home/crf/english/<YYYY-MM-DD>-<Title>.pdf" \
  "file:///home/crf/english/<YYYY-MM-DD>-<Title>.html"
```

5. 生成手机版（自动加 viewport、移动端排版、表格转卡片、点按查词、返回顶部；**在 gen_audio 之后**才会带上音频）：

```bash
python3 /home/crf/.claude/skills/english-article-reading/build_mobile.py \
  "/home/crf/english/<YYYY-MM-DD>-<Title>.html"
```

6. （可选）更新索引：`python3 /home/crf/english/build_index.py`。

### 验证

- `pdfinfo "<pdf>" | grep Pages` —— 页数正常（一般 4–12 页）。
- `pdftotext "<pdf>" - | head -40` —— 中文不乱码、章节标题齐全。
- 手机版：抽查 390px 宽无横向溢出（可用 headless Chrome 截图，或确认 `scrollWidth == innerWidth`）。

## 第 9 步：汇报

给用户：三份文件路径、PDF 页数、文章结构一览（背景 / 精读段数 / 词源个数 / 修辞种类 / 练习数）。
若用户一次给多篇，逐篇重复第 1–8 步，最后统一跑 `build_index.py`；可用并行 subagent 分篇处理，但每篇都要独立完成填充与验证。

## 排版规范（template.html 已内置，勿改核心 CSS）

- 字体：`Noto Sans CJK SC`（中文）+ `DejaVu Sans`（英文与音标）。
- 主色：标题深红 `#7f1d1d`，强调红 `#b91c1c`，分节蓝 `#1e3a8a`。
- 表格 `page-break-inside: avoid`；`h2.section` 有 `page-break-after: avoid`。
- 桌面版提示语用「鼠标悬停」；`build_mobile.py` 会自动改成「轻点」。

## 朗读（两级音源：神经网络 MP3 → 系统语音回退）

页面**优先播放预生成的神经网络音频**（`gen_audio.py` + edge-tts，接近真人），缺失时才回退到
浏览器内置 `speechSynthesis`。`build_article.py` 与 `build_mobile.py` 会自动注入
`read_aloud.css` / `read_aloud.js`。

- **每句一个 🔊**：点句子左侧按钮朗读该句（只读英文，自动剔除 ①②、P# 与拆解框）。
- **底部控制条**：`▶ 朗读全文`（逐句连读、自动滚动）、`■ 停止`、`0.95×`（点按切语速）。
- 音频按句存到 `<文件名>.audio/sNNN.mp3`，每句 `<div class="sent" data-audio="…">` 指向它；
  相对路径，桌面版与手机版通用（用本地服务器打开时一并提供）。
- **打印 / PDF 时自动隐藏**朗读控件（`@media print`），不影响 A4 排版。
- 给「已有」的桌面页补/刷新朗读：`python3 add_read_aloud.py <file.html>`，再重跑 `build_mobile.py`。

生成音频（需联网，edge-tts 神经网络音色）：

```bash
python3 /home/crf/.claude/skills/english-article-reading/gen_audio.py \
  "/home/crf/english/<...>.html" --voice en-US-AriaNeural --concurrency 8
```

可选美音音色：`AriaNeural`（清晰）、`JennyNeural`（友好）、`GuyNeural`（有力，适合演讲）、
`ChristopherNeural`、`MichelleNeural`、`EricNeural`、`RogerNeural`、`SteffanNeural`；重生成加 `--force`。

> 若某页回退到系统语音而嫌机械：iOS 到「设置 → 辅助功能 → 朗读内容 → 声音 → 英语」下载
> **Premium/Enhanced（Siri）** 语音；但首选还是跑 `gen_audio.py`，让页面直接用神经网络 MP3。

## 注意事项

- **准确第一**：词源、修辞术语、引文必须真实且与原文一致，不得编造；宁可少讲一个词，不可写错词源。
- **三者对齐**：`.ck` 色块、`.chip` 编号、`.sg` 文本必须严格一一对应，否则拆解框会错位。
- **标题只写一次**：句子结构说明放一个 `.legend`，不要每句重复。
- **CSS 不动**：模板样式是排好版的，只填内容；确需新色再在 `<style>` 里增补。
- Chrome 转 PDF 必须带 `--no-pdf-header-footer`，否则出现浏览器页眉页脚。
- HTML 源文件保留不删。
