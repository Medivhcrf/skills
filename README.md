# My opencode / Claude Code Skills

我自定义的一组 skill（外部技能，opencode 会自动加载 `~/.claude/skills/<name>/SKILL.md`）。
主要面向英语学习：词根词缀、动词词组、文章精读、题目解析，产出精美 HTML / PDF，并支持手机版与朗读。

## 包含的 skill

| skill | 作用 | 主要产出 |
| --- | --- | --- |
| `daily-root-affix` | 每日 10 个英语词根词缀（含词源、演化、例句）；另含手机版与单词发音工具 | `YYYY-MM-DD-词根词缀.html` / `.pdf` |
| `daily-phrasal-verbs` | 每日辨析英语动词词组（phrasal verbs） | HTML / PDF |
| `english-article-reading` | 英语文章全文精读：背景—逐句分色—词源—修辞—跟读—金句—自测；含数据→HTML 生成器、手机版、朗读 | 桌面 HTML + A4 PDF + 手机版 HTML |
| `exam-question-analysis` | 考试/习题解析 + 知识体系扩展 | PDF |
| `root-affix-review` | 复习历史每日词根词缀，生成复习练习 | PDF |

## 在新机器上安装

opencode / Claude Code 会自动扫描 `~/.claude/skills/`。把它 clone 到该目录即可：

```bash
# 若 ~/.claude/skills 不存在
git clone git@github.com:Medivhcrf/skills.git ~/.claude/skills
```

若该目录已存在，可 clone 到别处再软链接：

```bash
git clone git@github.com:Medivhcrf/skills.git ~/repos/skills
ln -s ~/repos/skills/* ~/.claude/skills/
```

也可放进 opencode 的原生技能目录：`~/.config/opencode/skills/`（在 `opencode.json` 里用
`skills.paths` 指向本仓库亦可）。

## 依赖

- `python3`（脚本均为标准库 + 少量第三方）
- `edge-tts`（神经网络发音，用于生成朗读/单词音频）
  ```bash
  python3 -m pip install --user --break-system-packages edge-tts
  ```
- `google-chrome`（headless 把 HTML 转成 PDF；命令里带 `--no-pdf-header-footer`）
- 字体：`Noto Sans CJK SC`（中文 PDF 依赖）、`DejaVu Sans`（英文/音标）
- 可选：`pdfinfo` / `pdftotext`（poppler-utils，用于验证 PDF）

## 注意

- 部分 skill 里的路径是作者机器上的绝对路径（如 `/home/crf/english/`、
  `/home/crf/.claude/projects/.../memory/...`）。换机器后按需修改 SKILL.md 中的路径。
- 运行前请重启 opencode，使其重新加载技能。
