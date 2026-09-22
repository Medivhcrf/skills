---
name: daily-root-affix
description: 每天整理10个英语词根词缀及相关单词、词组，附词源与演化过程，侧重生活常用，生成精美PDF保存。触发场景：用户说"今天的词根词缀""每日词根""词根词缀""来10个词根"等。注意——即使用户只说"词根""词缀"（不带"每天/今日"），也应使用本skill，因为这表示用户想要词根词缀内容。
---

# 每日词根词缀 → PDF

用户每天来问一次词根词缀内容。每次整理 10 个（约 7 个词根 + 3 个词缀混合），配相关单词和词组，侧重日常生活常用，附词源信息和演化过程，生成排版精美的 PDF 保存到 `/home/crf/english/daily/`。

## 第 1 步：选题（避免重复）

1. 读取记忆文件 `/home/crf/.claude/projects/-home-crf/memory/daily-root-affix-pdf-routine.md`，查看"进度"段落已出过哪些词根词缀。
2. 选择 10 个新的词根词缀（约 7+3），确保不与历史 Day 重复。
3. 优先选择：
   - 使用频率最高的词根（如 fac/fact=做、scrib/script=写、mit/miss=送、struct=建、voc/vok=喊）
   - 生活中最常见的词缀（如 pre-、-tion、-ly、un-、-ful、dis-、-ment）
   - 每天保持多样性，不要连续两天都是同一类（如全拉丁或全希腊）

## 第 2 步：整理内容（每张卡片 5 个要素）

对每个词根/词缀，准备：

1. **词根/词缀 + 含义**：标注拉丁/希腊/古英语来源
2. **词源**：原始语言的具体词和含义，如有印欧语词根也注明。用紫色（`.etym`）呈现
3. **演化过程**：从本义出发 → 各前缀/后缀组合 → 现代英语派生词的语义演变链。用橙色（`.evo`）呈现
4. **相关单词**：5-6 个高频派生词，每个配中文释义和构词解析
5. **口语/生活用例句**：1 句贴近日常生活的英文例句 + 中文翻译
6. **记法提示**（可选，放在 `.trick`）：帮助记忆的联想

### 词缀深度分析规范（仅适用于词缀，词根不必遵循）

词缀（尤其是前缀）往往有**多个义项**以及**与其他近义前缀的微妙区别**。当词缀满足以下条件时，应添加深度分析：

**触发条件**（满足任一即可）：
- 该词缀有 2 个以上不同义项（如 dis- 有否定/剥夺/分开三个含义）
- 该词缀有近义兄弟前缀（如 dis- vs un- vs non- vs in-/im-）
- 该前缀会显著改变词干含义方向（如从"无"变成"主动去除"）

**分析要素**（按以下结构写入卡片）：

1. **义项分类**：用「1. 表示…  2. 表示…  3. 表示…」分项列出，每项配 3-4 个高频词例和箭头变换（如 `Agree → Disagree`）
2. **近义前缀辨析**：列出竞争前缀并解释核心区别。例如：
   - `dis-` 主动改变状态 / 反向动作
   - `un-` 单纯否定、无状态
   - `non-` 客观分类上的"非"
   - `in-/im-` 形容词否定（拉丁来源）
   每类配 1-2 个对照词（如 `uninterested` vs `disinterested`）
3. **进阶词源细节**：如有必要补充词缀本身的历史演化（如 `dis-` 的印欧语词根 \*dwis「二/分开」如何演变为"否定"的语义逻辑）

此段内容用 `.confuse` 块包裹，放在卡片的定语/单词列表之后、例句之前，用浅黄色背景区分。

### 多形词根辨析规范（仅适用于有变体的词根）

同一拉丁动词语法形式不同，进入英语后产生多个形态，学生容易误认为不同词根。常见如：
- `fac / fic / fect`（做） — factory / efficient / perfect
- `cap / cip / cept / ceive`（拿） — capture / recipient / concept / receive
- `ten / tin / tent / tain`（持） — contain / continent / extend / obtain
- `ced / ces / cess`（走） — proceed / success / excess
- `vid / vis / view`（看） — evidence / vision / review
- `duc / duct`（引导） — educate / product
- `scrib / script`（写） — describe / manuscript
- `mit / miss`（送） — admit / mission
- `pon / pos / posit`（放） — postpone / compose / position
- `vert / vers`（转） — convert / reverse

**触发条件**：所选的拉丁词根恰好有 2 个以上变体（如 fac/fic/fect）。

**分析要素**：
1. 列出所有变体形态及其语法来源（如 fac- = 现在时词干，fect- = 完成时分词词干）
2. 每个变体配 2-3 个代表词，按变体分组呈现

此段内容用 `.variant` 块包裹，紫色系背景区分。

### 拉丁-日耳曼同源对照规范（用到时添加）

印欧语（PIE）同一祖先词，经拉丁和日耳曼两条路进入英语，形成一对有系统音变对应的双词。核心音变规律：
- `p → f`：paternal / father, pedal / foot, piscis / fish
- `c → h`：cornu / horn, centum / hundred, canis / hound
- `d → t`：dental / tooth, duo / two, decem / ten
- `g → k/c`：genus / kin, gelu / cold, ager / acre
- `t → th`：tenuis / thin, tres / three, tu / thou

**触发条件**：所选的词根/词缀恰好有日耳曼同源词（比如选了 ped-「脚」，就自然引出 foot）。

**使用方式**：在词源的 `.etym` 行末尾顺带一句，如「与日耳曼同源词 **foot** 对应（p→f 音变）」，不需要单独成块。如果有 3 对以上同源词可展示，用 `.cognate` 块集中列出。

### 内容准确度要求

- 词源必须是真实可靠的拉丁/希腊/古英语来源，不得编造
- 演化链条必须合乎历史语言学逻辑（本义 → 引申义 → 现代义）
- 例句必须地道自然，像母语者实际会说的话
- 如果某词根有两个不同来源（如 port = portare「搬运」vs portus「港口」），必须明确区分

## 第 3 步：生成 PDF

1. 读取本 skill 目录下 `template.html`。
2. 替换三个占位符：
   - `【序号】` → Day 编号（从 memory 文件的进度推算）
   - `【日期】` → 当天日期（如 `2026 年 8 月 5 日`）和统计信息（如 `词根 7 个 · 词缀 3 个`）
   - `【卡片内容】` → 替换为生成的 10 张卡片 HTML（词根用 `<div class="card">`，词缀用 `<div class="card affix">`），内部结构参看 template.html 的 CSS 定义
3. **CSS 样式保持不变**，不增删改任何 CSS 规则。
4. 写入 `/home/crf/english/daily/<YYYY-MM-DD>-词根词缀.html`。
5. 用 headless Chrome 转换：
```bash
google-chrome --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="/home/crf/english/daily/<YYYY-MM-DD>-词根词缀.pdf" \
  "file:///home/crf/english/daily/<YYYY-MM-DD>-词根词缀.html"
```
6. **验证**：`pdfinfo "/home/crf/english/daily/<YYYY-MM-DD>-词根词缀.pdf" | grep Pages` 检查页数正常（一般 4 页左右）。
7. 保留 HTML 源文件不删除（用户可能修改排版后重新生成）。

## 第 4 步：汇报 + 更新记忆

1. 向用户汇报：文件路径、页数、今日 10 个词根词缀的快速列表。
2. 更新 memory 文件 `/home/crf/.claude/projects/-home-crf/memory/daily-root-affix-pdf-routine.md`，在"进度"段追加当天的 Day 编号、日期、10 个词根词缀名称。

## 卡片 HTML 结构（内部）

每张词根卡片应遵循此结构（`.card.affix` 用于词缀，加绿色左边条）：

### 词根卡片结构

```html
<div class="card">
  <div class="root-head"><span class="num">N</span><span class="root">词根</span> <span class="meaning">= 含义（英文对应）</span></div>
  <span class="trick">💡 记法：记忆联想</span>
  <span class="etym"><span class="lab">词源</span>：拉丁语 <b>xxx</b>「含义」，源自...</span>
  <span class="evo"><span class="lab">演化</span>：<b>本义</b> → 派生词1 ｜ <b>引申义</b> → 派生词2</span>
  <ul>
    <li><b>word</b> 释义 <span class="note">（构词解析）</span></li>
    ...
  </ul>
  <div class="usage">口语/生活用：<b>例句</b> 中文翻译</div>
</div>
```

> 多形词根加 `.variant` 块（在 `<ul>` 之后、`.usage` 之前）：
> ```html
> <div class="variant">
>   <span class="var-title">🧩 变体家族</span>
>   <b>fac-</b>  factory, facile<br>
>   <b>fic-</b>  efficient, deficit<br>
>   <b>fect-</b>  perfect, affect
> </div>
> ```

### 词缀卡片结构（含深度分析块）

词缀卡片除上述基础结构外，可选择性加入 `.confuse` 块（触发条件见上文「词缀深度分析规范」）：

```html
<div class="card affix">
  <div class="root-head"><span class="num">N</span><span class="root">前缀</span> <span class="meaning">= 核心含义</span></div>
  <span class="etym"><span class="lab">词源</span>：...</span>
  <span class="evo"><span class="lab">演化</span>：...</span>
  <span class="trick">💡 记法：...</span>
  <ul>
    <li><b>word</b> 释义 <span class="note">（构词解析）</span></li>
    ...
  </ul>
  <div class="confuse">
    <span class="confuse-title">💡 深度辨析</span>
    <!-- 义项分类、近义前缀对比、进阶词源等 -->
  </div>
  <div class="usage">口语/生活用：<b>例句</b> 中文翻译</div>
</div>
```

## 命名与位置

- 一律保存到 **`/home/crf/english/daily/`**；
- 文件名：`YYYY-MM-DD-词根词缀.html` 和 `YYYY-MM-DD-词根词缀.pdf`。

## 排版规范（template.html 已内置，勿改动核心样式）

- 字体：`Noto Sans CJK SC`（系统已装，中文 PDF 依赖它）
- 词根卡片：蓝色左边条 `#2563eb`，蓝色圆形序号
- 词缀卡片：绿色左边条 `#059669`，绿色圆形序号（加 `class="affix"`）
- 词源行 `.etym`：紫色 `#6d28d9`
- 演化行 `.evo`：橙色 `#b45309`
- 记法行 `.trick`：绿色 `#047857`
- 例句框 `.usage`：浅蓝底 `#eff6ff`
- 每张卡片加 `page-break-inside: avoid`（CSS 已设）

## 手机版 + 单词发音（可选，一键批处理）

词根/词缀页除了 A4 PDF，还可以生成「手机版 + 发音」。三个脚本都在本技能目录下：

```bash
SK=/home/crf/.claude/skills/daily-root-affix
# 1) 注入发音功能（CSS + JS，可重复运行）
python3 $SK/add_pronounce.py <页面.html> ...
# 2) 生成神经网络发音音频（edge-tts，按文本去重到 words-audio/，并注入 data-say）
python3 $SK/gen_word_audio.py <页面.html> ... --voice en-US-AriaNeural
# 3) 生成手机版（加 viewport + 响应式样式，输出 <名>-手机版.html）
python3 $SK/build_mobile_generic.py <页面.html> ...
```

- 发音目标：每个 `<li>` 与 `.usage` 的第一个 `<b>`，以及 `<td class="w">` 里的词；
  表格单元格混有中文时只对英文部分发音。
- `words-audio/` 为跨页共享目录（按内容 md5 命名），固定在**站点根目录** `/home/crf/english/words-audio/`；页面已归档在 `daily/` 等子目录，脚本会自动算出 `../words-audio/` 前缀（可用 `--site-root` 指定站点根）。
- 页面 `pronounce.js`：每词一个 🔊，另有左下角「🔤 点词发音」开关（点任意英文词即发音）；
  优先播放 MP3，缺失回退系统 `speechSynthesis`；打印/PDF 自动隐藏。
- 索引 `build_index.py` 会自动识别 `-手机版.html`：手机只显示手机版、电脑显示桌面版 + PDF。
- 需要联网（edge-tts 在线合成）。首次用：`python3 -m pip install --user --break-system-packages edge-tts`。

## 注意事项

- 词源和演化必须准确，不能编造——如果不确定某个词根的确切来源，选择其他有把握的词根。
- port 有两个不同来源（portare「搬运」/ portus「港口」），涉及 port 时必须区分清楚。
- Chrome 转换必须带 `--no-pdf-header-footer`，否则 PDF 有浏览器页眉页脚。
- HTML 源文件保留不删，方便用户后续改排版重新生成 PDF。
- 每天 10 个不重样，由 memory 文件追踪进度。
