---
name: root-affix-review
description: 复习历史每日词根词缀内容——自动扫描 /home/crf/english/daily/ 下所有历史 HTML（每日词根词缀），解析已学过的词根词缀、单词、词组、例句，生成复习 PDF（知识清单 + 填词练习 + 例句挖空 + 配对练习 + 答案区）。触发场景：用户说"复习词根词缀""回顾一下""复习""来个复习""复习昨天的内容"等。
metadata:
  node_type: skill
---

# 词根词缀复习 → PDF

复习用户历史积累的词根词缀内容。自动检测 `/home/crf/english/daily/` 下的所有历史 HTML 源文件，解析已学卡片，生成一份复习 PDF 保存到 `/home/crf/english/review/`。

## 第 1 步：自动检测历史内容

1. 扫描 `/home/crf/english/daily/` 下所有 `*-词根词缀.html` 文件（排除文件名含「复习」的）。
2. 用本目录下 `build_review_table.py`（方案A·三栏回忆表）自动解析每张卡片并生成复习 HTML：
   ```bash
   python3 /home/crf/.claude/skills/root-affix-review/build_review_table.py
   ```
   - 脚本会自动：按日期排序 → 解析卡片（复用 build_review.py 的解析逻辑）→ 生成三栏回忆表（练习区）+ 同结构答案区。
   - 可选参数：
     - `--max-days N`：只复习最近 N 天（默认全部历史）
     - `--out 文件名`：自定义输出文件名
3. 脚本输出文件名：`YYYY-MM-DD-词根词缀复习.html`，写入 `/home/crf/english/review/`。

## 第 2 步：确认输出并微调（可选）

- 检查脚本输出统计（解析天数、词根/词缀数量）。
- 如需只复习最近几天：加 `--max-days 3`。
- 如脚本报错或某张卡片解析异常（如词根缺失），手动修复后重新生成。

## 第 3 步：生成 PDF

1. 保留 HTML 源文件。
2. 用 headless Chrome 转换：
```bash
google-chrome --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="/home/crf/english/review/<YYYY-MM-DD>-词根词缀复习.pdf" \
  "file:///home/crf/english/review/<YYYY-MM-DD>-词根词缀复习.html"
```
3. **验证**：`pdfinfo "/home/crf/english/review/<YYYY-MM-DD>-词根词缀复习.pdf" | grep Pages`。约 1 页可容纳 1–2 天（10–20 行）；覆盖全部历史时一般 6–10 页。

## 第 4 步：汇报 + 更新记忆

1. 向用户汇报：文件路径、页数、本次复习覆盖的天数与词根词缀数量、各分区题数。
2. 更新记忆文件 `/home/crf/.claude/projects/-home-crf/memory/root-affix-review-routine.md`，在「复习记录」段追加日期、覆盖天数、覆盖 Day 范围。

## 复习分区结构

复习 PDF 含 3 个部分（紫色主题，词缀仍用绿色区分）：

1. **一、三栏回忆表**：按 Day 分组，每个词根/词缀一行三栏——`词根 | 含义(书写格) | 代表词(书写格)`。词根已给，书写格带作业本横线，用户直接手写回忆。编号跨 Day 连续（1–70）。
2. **二、答案区**：与练习同结构同编号，填入含义和全部代表词。单独成页，可折页对照。
3. 文件首部有简短书写提示。

> 此方案（方案A）已替代旧的四分区方案（知识清单+填词+挖空+配对），因为旧方案内容多、排版密、书写区小，用户反馈不好用。新方案强调：**清晰**（三栏一眼看懂）、**方便书写**（大书写格+作业本横线）、**答案好找**（同编号折页对照）。

## 模板与脚本

- `template-table.html`：三栏回忆表模板，含占位符【标题】【统计】【练习内容】【答案内容】。**CSS 样式保持不变**，不增删改 CSS 规则。
- `build_review_table.py`：生成脚本，依赖 Python3 标准库，import 复用 `build_review.py` 的 `parse_daily_file`。可选参数：
  - `--out 输出文件名`：自定义输出文件名
  - `--max-days N`：只复习最近 N 天（不传则覆盖全部历史）
- `template.html` / `build_review.py`：旧方案（四分区）仍保留，如需旧版格式可手动运行，但默认改用方案A。

## 注意事项

- 复习内容完全来自历史 HTML 源文件，不新增不编造——解析到什么就复习什么。
- 例句挖空选词规则：优先挖掉与词根派生词完全匹配的词；若无匹配则挖句中最长单词。
- Chrome 转换必须带 `--no-pdf-header-footer`，否则 PDF 有浏览器页眉页脚。
- HTML 源文件保留不删，方便用户改排版后重新生成。
- 每天 10 个不重样由 daily-root-affix skill 追踪；本 skill 只管复习已学内容。
