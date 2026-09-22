---
name: english-article-reading
description: 把英语文章做成「全文精读」页时使用：用户给原文/链接/文件/主题，要求精读、逐句分析、词源、修辞、跟读、自测，或要求批量生成英语文章。产出桌面版 HTML + A4 PDF + 手机版 HTML，结构为「背景—全文精读（分层拆解：每块在给谁补充什么）—重点词源—修辞分析—跟读要点—金句—自测」。触发场景：用户说「精读这篇文章」「把这篇英语文章做成精读」「英语文章」「像 I Have a Dream 那样」「批量生成英语文章」等。
---

# 英语文章全文精读 → HTML / PDF / 手机版

把一篇英语文章（演讲、散文、社论、课文等）做成结构化的「全文精读」页。
标准范例见 `/home/crf/english/speech/2026-08-27-I-Have-a-Dream.html`（桌面）、
`...-手机版.html`（手机）与 `...pdf`（A4），本技能就是从它抽象出来的。

**工具文件**：`template.html`（桌面模板）、`build_article.py`（数据 → HTML 生成器，含层级自动推断）、
`build_mobile.py`（桌面 HTML → 手机版）、`read_aloud.css` / `read_aloud.js`（朗读功能）、
`add_read_aloud.py`（给已有页面补朗读）、`relayout.py`（把旧页面迁移到分层格式）、
`examples/steve_jobs_stanford.py`（长文完整示例）。

> **每篇文章都必须产出「三件套」，缺一不可：**
> ① 桌面版 HTML　② 手机版 HTML　③ A4 PDF。
> 除非用户明确说不要其中某项，否则第 8 步的三样全部生成并逐一验证。

## 输出物

| 文件 | 说明 |
| --- | --- |
| `/home/crf/english/speech/<YYYY-MM-DD>-<Title>.html` | 桌面 / A4 版（用于打印 PDF） |
| `/home/crf/english/speech/<YYYY-MM-DD>-<Title>.pdf` | A4 PDF |
| `/home/crf/english/speech/<YYYY-MM-DD>-<Title>-手机版.html` | 手机版（由脚本生成） |

- `<Title>` 用英文标题、连字符连接，如 `I-Have-a-Dream`。
- 日期取当天；HTML 源文件一律保留，方便改排版后重新生成。
- 全部完成后可选跑一次 `python3 /home/crf/english/build_index.py` 更新索引。

## 第 1 步：取文与分段

1. 来源：用户粘贴原文 / 给出 URL（用 webfetch 抓正文）/ 本地文件 / 只给主题（则先挑一篇经典短文并说明来源）。
2. 按自然段编号 `P1 … Pn`，保留原文标点；英文引号统一用 `'`（模板里是英文单引号）。
3. 通读并确定：全篇主旨、反复出现的句式/短语（排比、呼告）、贯穿的隐喻系统、引用来源（圣经/文献/名句）——这些是第 4 步修辞分析的依据。
4. 圈出要讲的重点词（生词、关键概念、词源精彩的词），编号 ① ② ③…，与正文上标一一对应。

## 第 2 步：全文精读（核心 —— 分色 + 分层拆解）

对**每个句子**做三件事：正文分色 + 句后分层拆解框 + 汉语解释。三者必须严格对应。

> **英语是「右分支」语言：骨架很短，修饰成分一层层往右挂。**
> 拆解框要回答的是**「这块在给谁补充什么信息」**，而不是「这是什么语法成分」。
> 语法术语只作小字索引；主视觉是修饰关系。缩进用 `.ly.d1 / .d2 / .d3 / .d4`（每级 20px）。

### 2.1 正文分色 `.ck`

把句子按「意群 / 句子成分」切成若干块，每块一个 `<span class="ck">`，块间用空格分隔：

```html
<div class="sent"><span class="pnum">P1</span><span class="ck" style="background:#c3d9f7;color:#16306b">I am happy</span> <span class="ck" style="background:#c2e6ce;color:#14532d">to join with you</span> <span class="ck" style="background:#f8dd9e;color:#6b3f02">today</span> <span class="ck" style="background:#f6c2db;color:#8a1244">in what will go down in history as</span> <span class="ck" style="background:#d7cbf5;color:#4a1a9e">the greatest demonstration<span class="sup">①</span> for freedom</span> <span class="ck" style="background:#bde3d7;color:#0a4f4d">in the history of our nation</span>.</div>
```

**六色盘**（按出现顺序循环取用；background / 文字色）：

| # | background | color | 色相 |
| --- | --- | --- | --- |
| 1 | `#c3d9f7` | `#16306b` | 蓝 |
| 2 | `#c2e6ce` | `#0f4023` | 绿 |
| 3 | `#f8dd9e` | `#6b3f02` | 琥珀 |
| 4 | `#f6c2db` | `#8a1244` | 玫红 |
| 5 | `#d7cbf5` | `#4a1a9e` | 紫 |
| 6 | `#bde3d7` | `#0a4f4d` | 青 |

> 色块走**明显**档：底色饱和度足够高、块与块一眼可分，文字色同步加深，
> 对比度实测 **6.1–8.7:1**（远超 WCAG AA 的 4.5），所以"明显"并没有牺牲可读性。
> **只保证相邻可辨，不承载语法含义**；真正表意的是角色色点与修饰关系。换色必须重测对比度。

### 2.2 句后拆解框 `.brk`（**以「修饰谁」为主**）

紧跟句子后面，放一个 `.brk`，里面每个 `.ly` 对应一个色块，**数量、编号、颜色、文本完全一致**。

每行结构：`树形连线 + .chip 编号 + .role 角色色点 + .sg 原文 + .mod 修饰关系 + .tg 语法术语 + .note 解释`

```html
<div class="brk">
<div class="ly d0"><span class="chip" style="background:#c3d9f7">1</span><span class="role" data-cat="skeleton" title="🔵 骨架"></span><span class="sg" style="color:#16306b">She felt very strongly</span><span class="mod">全句的主干</span><span class="tg">主句</span><span class="note">骨架只有四个词。feel 是系动词，要用副词 strongly</span></div>
<div class="ly d1"><span class="tbranch">├─</span><span class="chip" style="background:#c2e6ce">2</span><span class="role" data-cat="clause" title="🩵 宾语从句"></span><span class="sg" style="color:#14532d">that I should be adopted</span><span class="mod">补充：她坚决认定的内容</span><span class="tg">宾语从句</span><span class="note">should be adopted 是应然 + 被动</span></div>
<div class="ly d1"><span class="tbranch">└─</span><span class="chip" style="background:#f8dd9e">3</span><span class="role" data-cat="adv" title="🟣 时间"></span><span class="sg" style="color:#6b3f02">at birth</span><span class="mod">补充：那件「被收养」发生在什么时候</span><span class="tg">时间状语</span><span class="note">一出生——时间点</span></div>
<div class="ly d2"><span class="tbranch">　└─</span><span class="chip" style="background:#f6c2db">4</span><span class="role" data-cat="obj" title="🟠 施事"></span><span class="sg" style="color:#8a1244">by a lawyer and his wife</span><span class="mod">补充：那件「被收养」由谁来做</span><span class="tg">施事</span><span class="note">三个介词短语排队右挂，汉语要倒过来译</span></div>
</div>
```

- **`.mod` 是主视觉**（深色加粗，紧跟在英文后面）：一句话说清「这块在给哪一块、补充什么信息」。
  写法：**动词开头 + 具体指向**——`补充：…发生的时候` / `限定：是哪个 man` / `交代：动作由谁来做` /
  `另起一条主干——前面是打算，这里是结果`。**不要只写「时间状语」「宾语从句」这类术语**（脚本会告警）。
- **`.role` 是 CSS 画的色点**，不写 emoji：`<span class="role" data-cat="clause" title="🩵 宾语从句"></span>`。
  `data-cat` 取 `skeleton / pred / obj / attr / adv / clause / coord / contrast`（见下表），
  emoji 只放在 `title` 里做提示。**不要用 emoji 当可见标记**——缺 emoji 字体的环境（很多 Linux /
  无头 Chrome）会把它们渲染成单色方块，整列标记变成一片灰，配色设计直接失效。
- `.chip` 的 `background` = 对应 `.ck` 的 `background`（编号 1、2、3…）。
- `.tbranch` 树形连线**手写**（`├─` / `└─` / `│` / 全角空格）；用生成器时自动算好。
- `.sg` 的 `color` 和文本 = 对应 `.ck` 的 `color` 和文本。
- `.tg` 语法术语（灰色小字）：只当索引，写规范说法即可；与 `.mod` 重复时可省略。
- `.note` 讲语法点 / 易错点 / 修辞作用，**不要重复 `.mod` 已经说过的**。
  若要在 note 里指代某个色点，**别写 emoji**（会变方块），写文字：`是从句（从句色）不是短语（状语色）`。
  生成器会自动把 note 里的角色 emoji 换成这套文字说法。

> ⚠️ **别让 `.mod` 换行**：实测把 `.mod` 或 `.sg` 改成块级（独占一行）会让 142 句的长文
> PDF 从 20 页涨到 32–39 页。层级靠「色点 + 深色粗体 vs 灰色小字」的对比来做，不靠换行。


**角色色点（`.role[data-cat]`）对照表** —— 判不准就按「从句优先于非谓语」定：

| data-cat | 色点 | 色值 | 用于 |
| --- | --- | --- | --- |
| `skeleton` | ⚫ | `#334155` | 骨架、主句、主语、主谓、分句一/二/三、倒装、形式主语、开场致谢、短句 |
| `pred` | 🟢 | `#0f766e` | 谓语、动作、系表、祈使、被动谓语 |
| `obj` | 🟠 | `#b45309` | 宾语、表语、双宾、补语/宾补、引语、施事/受事 |
| `attr` | 🟣 | `#6d28d9` | 定语、同位语、补充修饰 |
| `adv` | 🔵 | `#1d4ed8` | **非谓语**状语：不定式、分词、动名词、介词短语 |
| `clause` | 🔷 | `#0e7490` | **限定从句**：宾语/表语/主语/同位语/定语/状语从句、存在句 |
| `coord` | 🟢 | `#4d7c0f` | 并列（并列谓语、并列主语、并列结果） |
| `contrast` | 🔴 | `#be123c` | 转折、让步、对比、过渡、判断、结论、收束 |

> 色值定义在 `template.html` 与 `build_mobile.py` 的 `:root`（`--r-skeleton` 等），两份**必须一致**。
> 生成器里的 `ROLE_TABLE` 是唯一色源，图例由它生成——改色只改这三处，别在图例里硬编码。

> ⚠️ **🟣 与 🩵 的边界**：同样是"时间"，`at birth`（短语）用 🟣，`when I popped out`（从句）用 🩵。
> 判据是**有没有主谓**，不是语义类别。


### 2.3 分层设计要点

1. **先定骨架**：最左边那个独立主谓（通常 2–5 个词）永远 `d0`、标 🔵。
2. **`mod` 写"给谁补充什么"**，`tag` 只写术语——先写 `mod` 再想 `tag`，顺序别倒。
3. **只标「与上级的关系」**，不要标它的内部分类：`by a lawyer and his wife` 相对 `adopted`
   是施事（🟠），不必再拆成"介词 + 名词"。
4. **层级不跳级**：`d2` 必须能找到它上面那层 `d1`，否则缩进会看起来悬空。
5. **一句话里骨架可以有多个**（并列句）：`so everything was all set` 与主句并列，
   也回到 `d0`、标 🟤。
6. 层级建议**不超过 4 层**（`d0`–`d3`）；真到 4 层以上，考虑拆成两句讲。

> **按 `mod` 的写法自查**：读一遍所有 `.mod`，如果读出来的是一串语法名词，
> 说明写失败了；如果读出来像「这块在告诉我被收养的时间和由谁来做」，就对了。

### 2.4 层级可以自动推断（老模块不必手写层级）

`build_article.py` 里 `INFER_LAYOUT = True`（默认开）。**当一句里的色块都没写第 4 个元素
（层级）时**，脚本按下面的规则自动推断，老的三元组模块也能得到树形：

1. 骨架类标签（主句/分句/主谓/主语/谓语/祈使/并列/短句/插入语…）→ `d0`；
2. 句首的修饰语（前面还没出现骨架）→ 也留 `d0`，避免句子以缩进行开头；
3. 其余修饰语 → 紧跟骨架时 `d1`，连续出现则逐层 +1，**上限 `d3`**。

这只是可预期的近似（例如把并列分句当成修饰语时会偏深）。要覆盖某句的判断，
在该句色块里显式写第 4 个元素即可——**只要有一块显式写了层级，整句就不再自动推断**。
设 `INFER_LAYOUT = False` 可整体关闭。

### 2.5 把旧页面迁移到新格式：`relayout.py`

早期生成的精读页是平铺列表 + 旧色盘。迁移不必重做内容：

```bash
python3 /home/crf/.claude/skills/english-article-reading/relayout.py <页面.html>
```

它**只重写两处**：`<style>`（换成当前模板 CSS，并保留该页原有的自定义 `.refrain.*` 配色）
与每个 `.sent`/`.brk` 块（新色盘、层级、角色色点、mod）。**其它一律不动**——背景、词源、
修辞、跟读、金句、自测、答案，以及 `data-audio` 等音频属性都原样保留，所以对有音频的页面安全。
迁移后记得重跑 `build_mobile.py` 与 PDF。

> ⚠️ **前提是拆解行与色块 1:1**。若旧页面里作者把多个色块合并成了一行（`.sg` 用「…」缩写），
> 先补齐再迁移，或用 `--fix` 传入逐块覆盖：
> ```bash
> python3 relayout.py <页面.html> --fix examples/i-have-a-dream-fix.json
> ```
> JSON 形如 `{"8": [["时间状语", "排比第三击：一百年后"], ...]}`，键是句中序号（从 1 开始）。
> `examples/i-have-a-dream-fix.json` 是修 `I Have a Dream` 6 句合并行的实例。



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

# 正文：段落 → 句子 → (句末标点, [ 色块, ... ])
# 色块 = (英文, 语法标签, 汉语解释)                              ← 旧格式，扁平，层级 0
#      = (英文, 语法标签, 汉语解释, 层级)                         ← 加挂接层级
#      = (英文, 语法标签, 汉语解释, 层级, 关系名, mod)             ← 完整写法（推荐）
#      = (英文, 语法标签, 汉语解释, 层级, 关系名, mod, emoji)      ← 再覆盖角色（emoji 作角色键）
#   其中 mod =「这块在给谁补充什么信息」，是主视觉，务必写具体
PARAS = [
    [(".", [
        ("I'm honored①", "主语+情感", "honored①：感到荣幸", 0, "骨架", "全句主干"),
        ("to be with you today", "不定式状语", "to be with 比 with 更庄重",
         1, "时间", "补充：这份荣幸发生在什么时候"),
    ])],
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
- **层级（第 4 个元素）**：`0` = 骨架；`1` = 直接挂骨架；`2` = 再挂一层……省略即 `0`。
  树形连线（`├─`/`└─`/`│`）由脚本按层级自动算，**不用手写**。
- **角色（第 7 个元素）**：填 emoji 作角色键（`🔵`/`🩵`…），脚本据此选色点颜色；
  省略时按语法标签自动推断（见 2.2 对照表）。**色点是 CSS 画的，不是 emoji**。
- **`mod`（第 6 个元素）强烈建议手写**：省略时脚本会用「关系名」兜底生成，
  但兜底只知道关系类别（如「补充：时间」），**说不出具体修饰了哪一块**，语义会偏泛。
  只有 3 项的旧模块能照常生成，只是 `mod` 偏模板化——重做该文时补上即可。
- 缺省的章节（如没有 `QUOTES`）会自动跳过。

### 命令

```bash
python3 /home/crf/.claude/skills/english-article-reading/build_article.py \
  <内容模块.py> "/home/crf/english/speech/<YYYY-MM-DD>-<Title>.html"
```

生成后同样走下面的 PDF 与手机版步骤。批量时可对每篇文章各写一个内容模块，循环调用。

## 第 8 步：生成 HTML / PDF / 手机版

1. 产出桌面 HTML，二选一：
   - **短篇**：读取 `template.html`，替换所有 `【】` 占位符，**CSS 保持不变**；
   - **长文 / 批量**：写内容模块，用 `build_article.py` 生成（见上一节）。
2. 写入 `/home/crf/english/speech/<YYYY-MM-DD>-<Title>.html`。
3. （推荐）生成神经网络朗读音频（需联网；详见「朗读」一节）。**必须在生成手机版之前**，手机版才会带上音频：

```bash
python3 /home/crf/.claude/skills/english-article-reading/gen_audio.py \
  "/home/crf/english/speech/<YYYY-MM-DD>-<Title>.html" --voice en-US-AriaNeural
```

4. 转 PDF（**必须带 `--no-pdf-header-footer`**）：

```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --no-pdf-header-footer \
  --print-to-pdf="/home/crf/english/speech/<YYYY-MM-DD>-<Title>.pdf" \
  "file:///home/crf/english/speech/<YYYY-MM-DD>-<Title>.html"
```

5. 生成手机版（自动加 viewport、移动端排版、表格转卡片、点按查词、返回顶部；**在 gen_audio 之后**才会带上音频）：

```bash
python3 /home/crf/.claude/skills/english-article-reading/build_mobile.py \
  "/home/crf/english/speech/<YYYY-MM-DD>-<Title>.html"
```

6. （可选）更新索引：`python3 /home/crf/english/build_index.py`。

### 验证

- **结构**（最容易漏、后果最重）：每个 `.para` 里 `<div class="sent">` 数必须等于 `<div class="brk">` 数；
  `.brk` 必须在 `.sent` **内部**。用文字处理脚本改写页面后**务必跑一次**——
  一旦句末标点被写成 `</div>`，句子结构会断、拆解框掉到 `.para` 外面，
  而「色块数 / 行数」这类计数检查**照样通过**，看不出问题。
- **对齐**：每句 `.ck` 数 == 该句 `.ly` 数。
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
  "/home/crf/english/speech/<...>.html" --voice en-US-AriaNeural --concurrency 8
```

可选美音音色：`AriaNeural`（清晰）、`JennyNeural`（友好）、`GuyNeural`（有力，适合演讲）、
`ChristopherNeural`、`MichelleNeural`、`EricNeural`、`RogerNeural`、`SteffanNeural`；重生成加 `--force`。

> 若某页回退到系统语音而嫌机械：iOS 到「设置 → 辅助功能 → 朗读内容 → 声音 → 英语」下载
> **Premium/Enhanced（Siri）** 语音；但首选还是跑 `gen_audio.py`，让页面直接用神经网络 MP3。

## 注意事项

- **准确第一**：词源、修辞术语、引文必须真实且与原文一致，不得编造；宁可少讲一个词，不可写错词源。
- **`mod` 是主视觉**：写「这块在给谁补充什么」（`补充：被收养的时间`），不是写「时间状语」。
  脚本会对只写语法术语的 `mod` 发告警——把它当 lint 用，别忽略。
- **三者对齐**：`.ck` 色块、`.chip` 编号、`.sg` 文本必须严格一一对应，否则拆解框会错位。
- **层级不跳级**：`d2` 上面必须能找到 `d1`。层级是相对**上一行**的挂接关系，不是绝对缩进。
- **🟣 / 🩵 边界**：非谓语状语（不定式、分词、介词短语）用 🟣；有主谓的限定从句用 🩵。
- 语法标签若不被映射表收录，色点会退成默认的蓝色（非谓语状语）——换成 2.2 表里的规范说法，或补映射。
- **标题只写一次**：句子结构说明放一个 `.legend`，不要每句重复。
- **CSS 不动**：模板样式是排好版的，只填内容；确需新色再在 `<style>` 里增补。
- Chrome 转 PDF 必须带 `--no-pdf-header-footer`，否则出现浏览器页眉页脚。
- HTML 源文件保留不删。
