---
name: word-shift-notes
description: 记录「英文词的原义 / 语义核心」与「汉语对应词」之间的错位时使用。用户问「这句怎么理解」「是『终于』还是『最后还是』」「这个词为什么不能这译」，或要求把某组词义差异（译法之争、近义词群、词典互列同义词）做成图文笔记、章节、辨析页时，用本技能。产出带「词典释义（英文原文）—词源本义—错位成因—分工表—可迁移规律」五节的 HTML，同时出桌面版与手机版，发布到英语学习站的「词义错位」章节。触发语：「这句怎么理解」「是 A 还是 B」「这几个词有什么区别」「中英不对应」「词义错位」「开辟章节记录这个」等。
---

# 词义错位 · 章节写作

记录一类特定问题：**英文词的语义核心，和汉语对应词的语义核心，并不重合。**
词典把几个词互列为同义词，只说明"大意相通"，不说明"能互换"——差别藏在**义项数、词源本义、语域和语法限制**里。
本技能就是把这层差别写成可查、可复用的图文笔记。

标准范例：`/home/crf/english/shift/2026-09-23-词义错位-at-last.html`
（数据源：`examples/at_last.py`，**写新篇前先读这两个文件**）。

## 章节位置（重要）

「词义错位」是英语学习站上**独立的一章**，**不放进 `daily/`**，不与每日系列混排。

| 项目 | 值 |
| --- | --- |
| 目录 | `/home/crf/english/shift/` |
| 桌面版 | `<DATE>-词义错位-<SLUG>.html` |
| 手机版 | `<DATE>-词义错位-<SLUG>-手机版.html` |
| 索引分类 key | `shift`，显示名「词义错位」 |

- **只出 HTML，不出 PDF**（用户明确要求：出手机版就行）。
- 桌面版是手机版的**源**（手机版要加 `viewport` 与移动排版），所以两个文件都要生成。
- 索引由 `python3 /home/crf/english/build_index.py` 重建，`shift` 已在 `CATEGORIES` 里注册。

## 工作流程

1. **取词**：确认这一篇要讲的「纠结点」是什么——通常是**一个汉语词对多个英语词**（如「最后」对 at last / finally / in the end / eventually），
   或**一个英文短语被汉语习惯带偏**（如 `Free at last!`）。
2. **查证（不许跳）**：见下方「核实规范」。
3. **写内容模块**：复制 `examples/at_last.py` 改内容，存到 `examples/<slug>.py`。
4. **生成**：

   ```bash
   python3 /home/crf/.claude/skills/word-shift-notes/build_shift.py \
     /home/crf/.claude/skills/word-shift-notes/examples/<slug>.py
   ```

   默认输出到 `/home/crf/english/shift/`；改目标目录加 `--out-dir DIR`。
5. **重建索引**：`python3 /home/crf/english/build_index.py`，确认「词义错位」篇数 +1。
6. **验证**：见下方「验证」。
7. **提交推送**：`/home/crf/english` 与 `/home/crf/.claude/skills` 两个仓库（见末尾约定）。

## 核实规范（本技能的核心价值，别省）

**释义必须引真实辞书，词源必须查 etymonline。宁可少写一条，不可编造。**

| 查什么 | 去哪查 | 注意 |
| --- | --- | --- |
| 英语释义原文 | `vocabulary.com/dictionary/<词>`（可直接 fetch） | 照抄原文，不改写；连同义词列表一起抄，那是判断"能不能互换"的依据 |
| Longman / Oxford / Cambridge | 常被 Cloudflare 拦（403） | 拦住了就**不要凭印象冒充原文**，改用可访问的辞书，或在页脚注明"未能直取" |
| 词源、最早形态、年代 | `etymonline.com/word/<词>`（可直接 fetch） | 记下**最早年代**和**词根**；引用时在 `ETYM_QUOTE` 里附出处与取用日期 |
| 专名 / 引文出处 | 必要时检索确认 | 如 *Free at Last* 灵歌、马丁·路德·金 1963 演讲 |

**最有价值的发现，往往在词源里**：at last 之所以是"终于"，是因为 `last` 是 `late` 的**最高级**
（古英语 `latost`）。写每一篇时都先问一句——**这个词的词根有没有比较级 / 最高级？** 有的话，那才是它的语义核心。

## 内容模块格式

`build_shift.py` 读一个 Python 模块，字段如下。**所有文本按 HTML 处理**（可写 `<b>` `<i>` `<code>` `<span class="box">`），
因为内容由作者核实后手写；只有 `DATE` / `SLUG` 这类结构性字段会被转义。

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `TITLE` | ✅ | 标题，可含 `<span class="en">` 包英文；`<title>` 里会自动去标签 |
| `SUB` | ✅ | 副标题，一句话点出纠结点 |
| `DATE` | ✅ | `YYYY-MM-DD`，进文件名与页头 |
| `SLUG` | ✅ | 文件名用，连字符小写，如 `at-last` |
| `KICKER` | | 页头小字，默认「词义错位 · 英文原义 × 汉语对应词」 |
| `META` | | 页头出处行，如「释义取自 Vocabulary.com ｜ 词源取自 etymonline」 |
| `VERDICT` | ✅ | 「一句话」结论：首选哪个译法 |
| `PUNCH` | ✅ | 最凝练的那句判断（本页的记忆点） |
| `SENSES` | ✅ | §1 词典释义，见下 |
| `ETYM` | ✅ | §2 词源表，见下 |
| `ETYM_QUOTE` | | §2 尾部引用块 `(原文, 出处)` |
| `INSIGHT` | ✅ | §3 错位成因，HTML 段落（用 `.box` / `.box.green` / `.box.amber` 做强调块） |
| `DUTY` | ✅ | §4 分工表，见下 |
| `RULES` | ✅ | §5 可迁移规律，字符串列表（2–4 条） |
| `EXTRA` | | 追加在五节之后的 HTML 块 |
| `FOOTER` | | 页脚；省略则给默认的"返回索引" |

**`SENSES` 每行**：`(词, 英文释义原文, 补充/同义词, ⚠️提醒, 出处URL)`
——第 4 项是**这一页的拳头**：写"它没有什么"（如「只有 1 个义项，没有『排列在最后』的意思」）。
后两项可省。

**`ETYM` 每行**：`(词, 最早形态 / 词根 / 年代, 字面本义)`

**`DUTY` 每行**：`(词, 英文原解, 中文对应, 用法限制)`
——「用法限制」写**能不能这么用**（能否用于列举、能否配将来时、语域），这是词典不查就写不出来的部分。

## 五个小节为什么这么排

1. **词典释义（英文原文）** —— 先给事实，且是**原文**，避免用汉语二手解释互相循环。
2. **词源本义** —— 解释"为什么"。这一节决定整页有没有洞察。
3. **错位是怎么产生的** —— 把 1 和 2 对撞，指出**汉语对应词缺了哪一层**（如「最后」是序数，缺「晚」）。
4. **分工表** —— 落到可操作：哪种场合用哪个词。
5. **可迁移的规律** —— 抽出能用到别的词上的方法（如"查词源里的比较级"）。

## 验证

```bash
ls -la /home/crf/english/shift/                       # 桌面版 + 手机版都在
python3 -c "import io,re;h=io.open('/home/crf/english/shift/<stem>-手机版.html',encoding='utf-8').read();print('viewport' in h, len(re.findall(r'<section',h)), len(h))"
```

- 手机版必须含 `viewport`；`<section` 数为 5（五节齐）。
- 抽查 390px 宽无横向溢出（长表格靠 `.scroll` 横向滚动，页面本身不应被撑宽）。
- 索引页 `/home/crf/english/index.html` 里「词义错位」区块出现该篇。

## 提交与推送（本机约定）

`/home/crf/english` 与 `/home/crf/.claude/skills` 两个仓库，改动完成后**默认直接提交推送**，无需再问：

```bash
cd /home/crf/english           && git add -A && git commit -m "shift: <新篇说明>" && git push origin main
cd /home/crf/.claude/skills    && git add -A && git commit -m "word-shift-notes: <改动说明>" && git push origin main
```

- 只提交实际有改动的仓库（`git status` 为空就跳过）。
- 站点由 GitHub Pages 发布：<https://medivhcrf.github.io/english/>，push 后自动更新。
- 新机器上 DSH 读的是 `~/.dsh/skills/`，本技能已软链：`ln -s ~/.claude/skills/word-shift-notes ~/.dsh/skills/`。

## 注意事项

- **语言陷阱题不是"翻译题"**：不要只给一句"应该译 X"。要给出**为什么**——词源、义项数、语法限制。
- **not A but B 的结论要放在最前面**（`VERDICT` / `PUNCH`），用户常常只想知道"到底哪个对"。
- **不要编词源**。拿不准就查 etymonline，或干脆不写那条。
- **不要用汉语解释去论证汉语**：能用英文辞书原文就用原文。
- **每篇只解决一个纠结点**。一组同义词或一个短语就是一个 SLUG；不要一篇塞三组。
- 表格列多时靠 `.scroll` 横滚，**不要**把表格改成图片或手写对齐。
