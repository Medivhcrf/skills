# 项目约定

## 改动后默认提交并推送（重要）

对以下两个仓库的任何改动，完成后**默认直接 `git add -A && git commit && git push origin main`**，
无需再询问用户：

| 目录 | 远程 | 说明 |
| --- | --- | --- |
| `/home/crf/.claude/skills` | `git@github.com:Medivhcrf/skills.git` | 自定义 skill 集合 |
| `/home/crf/english` | `git@github.com:Medivhcrf/english.git` | 英语学习站点 |

- 只提交**实际有改动**的仓库（`git status` 为空就跳过）。
- 提交信息简洁；不要提交 `__pycache__/`、`*.pyc`（已在 `.gitignore`）。
- SSH 已配置好（github.com 在 known_hosts），直接 `git push` 即可。

## 技能说明

- 每个技能一个目录：`<name>/SKILL.md`（含 frontmatter `name` + `description`），可附 `template.html` 与脚本。
- 改动技能后需**重启 opencode** 才会重新加载。
- 依赖：`python3`、`edge-tts`（发音）、`google-chrome`（转 PDF）、字体 `Noto Sans CJK SC`。
