---
name: daily-phrasal-verbs
description: 每日辨析英语动词词组（phrasal verbs），如 take off / take up / take over 这类。每次以一个动词为中心，整理 8-10 个它最常见的动词词组，每个词组附含义、及物性、可分离性、易混辨析与生活例句，生成精美 PDF 保存。触发场景：用户说"今天的动词词组""动词词组""phrasal verbs""take off 这样的""词组辨析"等。
---

# 每日动词词组辨析 → PDF

用户想要专门区分英语动词词组（phrasal verbs）。每次选一个核心动词（如 take、get、turn、look、come、put），围绕它整理 8-10 个最常见的动词词组，配含义、语法要点、易混辨析和生活例句，生成排版精美的 PDF 保存到 `/home/crf/english/phrasal/`。

## 第 1 步：选题（避免重复）

1. 读取记忆文件 `/home/crf/.claude/projects/-home-crf/memory/daily-phrasal-verbs-pdf-routine.md`，查看"进度"段落已出过哪些动词。
2. 选择一个新的核心动词，确保不与历史重复。
3. 优先选择词组数量最多的核心动词：
   - get（最万能，十几个常用词组）
   - take、turn、look、come、put、go、give、break、bring、call、carry、cut、fill、give、hold、keep、leave、make、pick、pull、push、run、set、show、stand、work
4. 每天保持动词类别的多样性（不要连续两天都是"运动类"或"说话类"）。

## 第 2 步：整理内容（每个词组一张卡片）

对每个动词词组，准备：

1. **词组 + 核心含义**：标注是否及物（vt.）或不及物（vi.）、宾语可否放中间（separable）
2. **字面义 → 引申义**：解释小词（off/up/over/down）如何给动词增加方向感，这是记忆关键
3. **近义/易混辨析**：同一动词的其他词组、或意思相近的其他动词词组（如 take off 起飞 vs land 降落）
4. **生活例句**：1-2 句贴近日常的英文例句 + 中文翻译

### 小词含义速查（核心记忆工具）

词组最难的是小词（particle）的意义。每期开头固定放这张速查表，帮助读者"猜"出新词组：

| 小词 | 核心空间义 | 常见引申 |
|------|-----------|---------|
| up | 向上 | 完成、增加、出现、准备好 |
| down | 向下 | 减少、失败、记下 |
| off | 离开 | 出发、关闭、完成、减少 |
| on | 在上 | 继续、打开、穿上 |
| in | 进入 | 进去、提交、包含 |
| out | 向外 | 出去、分发、耗尽、熄灭 |
| over | 越过 | 翻转、结束、检查、重复 |
| back | 向后 | 归还、退让、恢复 |
| away | 远离 | 离开、一直、积攒 |
| through | 穿过 | 完成、检查、电话接通 |

### 内容准确度要求

- 词组含义必须是真实常见的，不能编造（不确定的动词词组宁可不收）
- 及物/不及物、可否分离必须标注准确（这是中国学习者最易错的地方）
- 例句必须地道自然，像母语者实际会说的话
- 如果某个词组有多个义项（如 take off 有"起飞/脱下/突然成功"），必须用 1/2/3 分项列出

## 第 3 步：生成 PDF

1. 读取本 skill 目录下 `template.html`。
2. 替换占位符：
   - `【动词】` → 本期核心动词
   - `【日期】` → 当天日期（如 `2026 年 8 月 21 日`）和统计信息（如 `8 个词组`）
   - `【小词表】` → 小词含义速查表
   - `【词组内容】` → 替换为生成的词组卡片 HTML
3. **CSS 样式保持不变**，不增删改任何 CSS 规则。
4. 写入 `/home/crf/english/phrasal/<YYYY-MM-DD>-动词词组.html`。
5. 用 headless Chrome 转换：
```bash
google-chrome --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="/home/crf/english/phrasal/<YYYY-MM-DD>-动词词组.pdf" \
  "file:///home/crf/english/phrasal/<YYYY-MM-DD>-动词词组.html"
```
6. **验证**：`pdfinfo "/home/crf/english/phrasal/<YYYY-MM-DD>-动词词组.pdf" | grep Pages` 检查页数正常（一般 4 页左右）。
7. 保留 HTML 源文件不删除（用户可能修改排版后重新生成）。

## 第 4 步：汇报 + 更新记忆

1. 向用户汇报：文件路径、页数、今日核心动词、词组快速列表。
2. 更新 memory 文件 `/home/crf/.claude/projects/-home-crf/memory/daily-phrasal-verbs-pdf-routine.md`，在"进度"段追加当天的日期、核心动词、词组清单。

## 卡片 HTML 结构（内部）

每张词组卡片遵循此结构：

```html
<div class="card">
  <div class="head"><span class="num">N</span><span class="phr">take off</span> <span class="tag">vi. 可分离</span></div>
  <div class="mean">① 起飞 ② 脱下 ③ 突然成功</div>
  <div class="logic"><span class="lab">逻辑</span>：off = 离开；离开地面=起飞，离开身体=脱下</div>
  <div class="confuse"><span class="lab">易混</span>：take off（起飞/脱下）vs put on（穿上）vs land（降落）</div>
  <div class="usage">口语/生活用：<b>例句</b> 中文翻译</div>
</div>
```

## 命名与位置

- 一律保存到 **`/home/crf/english/phrasal/`**；
- 文件名：`YYYY-MM-DD-动词词组.html` 和 `YYYY-MM-DD-动词词组.pdf`。

## 排版规范（template.html 已内置，勿改动核心样式）

- 字体：`Noto Sans CJK SC`（系统已装，中文 PDF 依赖它）
- 词组卡片：蓝色左边条 `#2563eb`，蓝色圆形序号
- 动词词组：橙色 `#b45309`（区别于词根词缀的蓝色）
- 语法标签：灰色小字（如 `vi. 可分离`）
- 逻辑行：紫色 `#6d28d9`
- 易混行：浅黄底 `#fefce8`（同词根词缀的 confuse 风格）
- 例句框：浅蓝底 `#eff6ff`
- 每张卡片加 `page-break-inside: avoid`

## 注意事项

- 词组含义必须真实，不确定就不收。
- 必须标注及物性 + 可分离性，这是学习者最易错点。
- 一期聚焦一个动词的多个词组，不跨动词。
- Chrome 转换必须带 `--no-pdf-header-footer`。
- HTML 源文件保留不删。
- 每个动词不重样，由 memory 文件追踪进度。
