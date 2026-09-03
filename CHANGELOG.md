# 更新日志 (Changelog)

所有关键版本的更新与重要变更都会记录在此文件中。
版本号遵循 [语义化版本规范 (SemVer)](https://semver.org/lang/zh-CN/)。

---

## [v1.0.0] - 2026-09-03

### 🚀 初始版本发布 (Initial Release of SQSL Skills Monorepo)
- **Monorepo 架构统一**：整合 `sqsl` 总路由、`sqsl-article-to-wechat` 排版直推引擎与 `sqsl-style-cloner` 风格克隆工坊三大子技能；
- **总路由器 (`skills/sqsl`)**：支持 `/sqsl` 双模意图分流，发文章自动排版，发链接自动克隆，说引导自动导航；
- **排版发布引擎 (`skills/sqsl-article-to-wechat`)**：支持大刊风、极简风与阿芋草木山野生活风，首图自适应 900x383 头条封面，微信官方 CDN 图床转存与草稿箱 API 直推；
- **风格克隆工坊 (`skills/sqsl-style-cloner`)**：支持公众号文章视觉 DNA 逆向解构，支持大标题图片序号（01/02）与高亮胶带底色探测，零外来色渗透约束；
- **包管理器无缝支持**：支持通过 `npx skills add <repo> -g --all` 一键全量安装或按需安装指定子技能。
