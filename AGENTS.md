# 🤖 SQSL WeChat Skill Agent 工作台规范 (AGENTS.md)

本文档定义了 **SQSL WeChat Skill** 在不同 AI Agent 宿主环境（Claude Code、Codex、Antigravity、Cursor 等）中的加载机制与协同行为准则。

---

## 1. 技能拓扑与唯一定位

所有技能的真源文件位于 `skills/` 目录下：

| 技能名称 | 目录位置 | 角色定位 |
| :--- | :--- | :--- |
| **`sqsl-wechat-start`** | `skills/sqsl-wechat-start/SKILL.md` | **总路由入口**：负责任务前路由与任务后导航（支持 `/sqsl` 简写） |
| **`sqsl-video-to-article`** | `skills/sqsl-video-to-article/SKILL.md` | **视频转文章引擎**：本地 Whisper 转写、词典纠错、时间戳精准抽帧并撰写 Markdown 初稿 |
| **`sqsl-article-to-wechat`** | `skills/sqsl-article-to-wechat/SKILL.md` | **排版发布引擎**：Markdown 转公众号 HTML 并直推草稿箱 |
| **`sqsl-style-cloner`** | `skills/sqsl-style-cloner/SKILL.md` | **风格克隆工坊**：逆向解析微信文章并生成风格模块 |

---

## 2. 宿主适配机制

### (1) Claude Code
- 支持通过 `npx -y skills add <repo> -g --all` 安装到 `~/.claude/skills/`；
- 触发方式：输入 `/sqsl-wechat-start`（或简写 `/sqsl`）或对应子技能命令。

### (2) Google Antigravity
- 技能目录同步至 `~/.gemini/config/skills/`；
- 原生支持工具调用与三端指令无缝流转。

### (3) OpenAI Codex / CLI
- 可通过 Python CLI 工具直接执行 `scripts/` 下的独立自动化脚本。

---

## 3. 跨子技能协作协议

1. **风格池共享协议**：
   - `sqsl-style-cloner` 生成的新风格类必须存放于 `skills/sqsl-article-to-wechat/styles/style_{name}.py`；
   - `sqsl-article-to-wechat` 在初始化时会自动动态扫描并注册该目录下的所有扩展风格。
2. **零杂色污染协议**：
   - 所有子技能在排版和渲染时，严禁使用硬编码的外来颜色，必须严格遵循当前风格实例的调色规范。
3. **原作者措辞保真与反 AI 味协议**：
   - `sqsl-video-to-article` 在生成图文 Markdown 时，必须严格遵循克制修改原则：仅允许精简口水词与停顿词，严禁擅自篡改原作者的用词与表达风格，坚决杜绝 AI 假大空八股与公关汇报腔。
