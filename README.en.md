# 🏛️ SQSL Skills (WeChat Official Account Creator Suite)

<p align="center">
  <strong>An all-in-one Agent Skill Suite for WeChat Official Account creators: from Reverse-Engineering & Style Cloning to Editorial Typesetting and 1-Click Official Draft Push.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-2563EB.svg?style=flat-square" alt="Version 1.0.0"/>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+"/>
  <img src="https://img.shields.io/badge/Architecture-Monorepo-orange.svg?style=flat-square" alt="Monorepo"/>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="MIT License"/>
</p>

[简体中文](README.md) | English

---

## 🌟 Matrix Highlights

1. **🎨 `sqsl-style-cloner` (Style Cloner Workshop)**: Reverse-engineers the visual DNA of any WeChat article URL (extracting stylized number images `01/02`, highlight tape background colors, soft paper cards, line spacing) and compiles into a plug-and-play Python style class.
2. **📰 `sqsl-article-to-wechat` (Typesetter & Draft Publisher)**: Turns any Markdown file into high-aesthetic WeChat HTML, auto-extracts the first image as 900x383 header cover, uploads images to WeChat CDN, and pushes directly to your Official Account Draft Box.
3. **🧭 `sqsl` (Master Router)**: A unified entry point (like `/dbs`) that automatically identifies user intent and routes between publishing, cloning, and setup guides.

---

## ⚡ 1-Click Installation

Compatible with Claude Code, Codex, Antigravity, and any Agent supporting skills standards:

```bash
# Install the entire suite with all sub-skills
npx -y skills add <your-github-username>/sqsl-skills -g --all

# Or install only the typesetter
npx -y skills add <your-github-username>/sqsl-skills/skills/sqsl-article-to-wechat -g
```

---

## 📄 License

MIT License.
