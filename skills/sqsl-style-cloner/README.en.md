# 🎨 SQSL Style Cloner

<p align="center">
  <strong>Reverse-engineering & Style Cloning Workshop for WeChat Official Account Articles.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-2563EB.svg?style=flat-square" alt="Version 1.0.0"/>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+"/>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="MIT License"/>
</p>

[简体中文](README.md) | English

---

## 🌟 Highlights

1. **1-Click Style Reverse Engineering**: Give it any WeChat Official Account article URL or HTML snippet, and it extracts primary colors, accent colors, callout borders, and typography settings automatically.
2. **Auto-Compiled Style Module**: Transforms the extracted visual DNA into a clean Python style class compatible with `sqsl-article-to-wechat`.
3. **Seamless Engine Integration**: Injects the cloned style into the typesetter's `styles/` pool, allowing you to typeset your Markdown articles using `--style <cloned_name>` right away!

---

## ⚡ 1-Click Installation

```bash
npx -y skills add <your-github-username>/sqsl-style-cloner -g
```

---

## 💻 CLI Usage

```bash
# Clone directly from a WeChat article URL
python3 scripts/clone_wechat_style.py "https://mp.weixin.qq.com/s/xxx" --name "tech_blue" --display-name "Tech Blue"
```

---

## 📄 License

MIT License.
