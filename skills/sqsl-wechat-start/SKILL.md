---
name: sqsl-wechat-start
description: |
  SQSL (三秋十李) 微信公众号创作与排版家族总路由主技能。
  双模式智能调度：
  1. 任务前路由：智能识别用户意图（发文章、克隆排版、配置微信API、查看引导），自动流转到对应的专业子技能；
  2. 任务后导航：风格克隆完成后自动引导调用排版直推，排版完成后提供草稿箱直推与多风格切换指引。
  触发方式：/sqsl-wechat-start、/sqsl-start、/sqsl、/三秋十李、/公众号全家桶、「发公众号」「帮我排版」「克隆公众号排版」「使用引导」「新手帮助」
---

# 🏛️ SQSL WeChat Start (三秋十李 · 微信公众号创作总路由)

欢迎来到 **SQSL 微信公众号高品质创作与排版全家桶**。本技能 (`sqsl-wechat-start`) 是整个工具箱的主调度入口，负责识别你的需求并自动协同下属专业子技能。

---

## 🧭 技能家族矩阵与能力分工

```mermaid
flowchart TD
    User["用户输入 (/sqsl-wechat-start)"] --> Router{"意图识别总路由 (/sqsl-wechat-start)"}
    
    Router -->|输入微信文章 URL / 要求提取样式| Cloner["🎨 sqsl-style-cloner (风格克隆工坊)\n- 逆向解析目标文章 CSS/调色板\n- 提取大标题图片序号与胶带高亮底色\n- 自动编译并注入公共风格池"]
    
    Router -->|输入 Markdown 文档 / 要求排版发布| Publisher["📰 sqsl-article-to-wechat (排版直推引擎)\n- 多风格高水准杂志排版 (大刊风/极简风/手作风)\n- 自动提取正文首图为 900x383 头条封面\n- 图片全自动转存微信官方 CDN\n- 官方草稿箱 API 一键直推 + 本地预览复制"]
    
    Router -->|输入 '使用引导' / '新手' / '帮助'| Guide["📖 全景引导与微信 API 5步配置说明"]
    
    Cloner -->|克隆出新风格 style_{name}.py| Publisher
```

---

## 🚀 路由与分流规则（Agent 必须严格遵守）

当用户唤起 `/sqsl-wechat-start`（或简写 `/sqsl`）或用自然语言提问时，按以下逻辑进行精准意图分流：

### 意图 1：新手帮助与全景指引
* **触发特征**：包含「使用引导」「新手」「怎么用」「帮助」「API怎么配」或初次唤起未提供文章/链接；
* **动作**：直接输出下方 **【新手全景指引】**，告知全家桶能力、微信公众号 API 配置步骤以及两步极速上手示范。

### 意图 2：排版文稿并发布到微信
* **触发特征**：提供了 `.md` 文件路径、直接粘贴了 Markdown 文稿文本、或包含「排版」「发文章」「推送到草稿箱」；
* **动作**：无缝调用 **`sqsl-article-to-wechat`** 子技能：
  - 默认使用 `editorial`（先锋大刊风）或根据用户要求使用 `olive_artisan`（草木山野生活大刊风）；
  - 输出本地预览 HTML 并根据配置直推草稿箱。

### 意图 3：逆向克隆别人家公众号排版
* **触发特征**：输入包含微信公众号文章 URL（`https://mp.weixin.qq.com/s/...`）、HTML 源码片段、或要求「复刻排版」「克隆风格」「提取这个样式」；
* **动作**：无缝调用 **`sqsl-style-cloner`** 子技能：
  - 启动代码逆向与视觉回看，提取视觉 DNA（大标题图片序号、胶带色、卡片底色）；
  - 自动编译生成新风格模块并注册进 `sqsl-article-to-wechat/styles/`；
  - 任务完成后主动提示用户：“已为您克隆出新风格 `{style_name}`，是否立即用该风格排版您的文章？”

---

## 📖 新手全景指引（用户说“使用引导”时输出）

> ### 欢迎使用 SQSL 微信公众号创作全家桶！
> 
> 本全家桶专为微信公众号创作者打造，提供从**「风格复刻」**到**「高颜值排版」**再到**「官方草稿箱直推」**的全链路闭环：
> 
> 1. **想排版发布文稿？**
>    - 发送：`/sqsl-wechat-start 帮我排版 docs/my_post.md 并推送到公众号`（或简写 `/sqsl`）
>    - 或发送：`/sqsl-article-to-wechat docs/my_post.md --style olive_artisan`
> 2. **看到别人家排版好看，想据为己有？**
>    - 发送：`/sqsl-wechat-start 帮我克隆这篇公众号排版：https://mp.weixin.qq.com/s/...`
>    - 或发送：`/sqsl-style-cloner https://mp.weixin.qq.com/s/... --name my_style`
> 3. **如何配置微信官方 API（5步极速配置）**：
>    - 登录微信开发者平台：`https://developers.weixin.qq.com/`
>    - 首页下方「我的业务」找到公众号 ➔「基础能力」➔「开发秘钥」复制 `AppID` 并保存 `AppSecret`；
>    - 同区域找到「IP 白名单」，将本机公网 IP（终端运行 `curl cip.cc`）添加进去；
>    - 在根目录复制模板创建 `wechat_config.json` 填入凭证即可！
>    *(注：未配置 API 也完全不影响使用，系统支持浏览器一键无损复制粘贴)*
