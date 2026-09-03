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

## 🙏 Acknowledgements & Inspirations

The architectural design and aesthetic foundation of this project are deeply inspired by the following open-source creators:

* **[dontbesilent2025/dbskill](https://github.com/dontbesilent2025/dbskill)**:
  Special thanks to the dbs team for pioneering Agent skill engineering! SQSL Skills adopts dbskill's **Monorepo suite layout**, **`/sqsl` pre-task routing & post-task navigation pattern**, and multi-agent **`AGENTS.md` workbench specifications**.
* **[Guizang (归藏)](https://github.com/op7418)**:
  Heartfelt thanks to Guizang for exceptional contributions to WeChat Official Account visual narrative, social card design systems, and Swiss editorial aesthetics.

### 🎨 Built-in Style Origins
1. **`editorial` (SQSL Editorial)**: Inspired by *Nowre* and *GQ*, utilizing Didot/Songti watermark typography, 88% whitespace media containers, and deep midnight navy aesthetics.
2. **`olive_artisan` (Olive Artisan)**: Reverse-engineered from *Voicer* magazine's acclaimed feature *[Revisiting Ayu: A Hat Maker and the Free Spirit in the Hills](https://mp.weixin.qq.com/s/2a85ue2uWT9JJpIcTqYYvA)*, recreating the signature Bodoni/Didot graphic numeral headers (`01`/`02`), olive-khaki highlighter tape titles (`#E0DEA8`), warm oat-beige card surfaces (`#F7F6F3`), and 1.8 relaxed line-height.

---

## 📄 License

MIT License.
