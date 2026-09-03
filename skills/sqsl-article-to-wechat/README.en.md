# 📰 SQSL Article to WeChat

<p align="center">
  <strong>Editorial-grade automated Markdown typesetter & cloud publisher for WeChat Official Accounts.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-2563EB.svg?style=flat-square" alt="Version 1.0.0"/>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+"/>
  <img src="https://img.shields.io/badge/WeChat-Draft%20API-07C160?style=flat-square&logo=wechat&logoColor=white" alt="WeChat Draft API"/>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="MIT License"/>
</p>

[简体中文](README.md) | English

---

## 🌟 Highlights

1. **Editorial Magazine Aesthetics**: High-contrast Didot/Bodoni 72 serif watermarks intertwined with Songti serif typography, rendered dynamically via headless Chrome into immune Retina PNG layers.
2. **First-Image-as-Cover**: Automatically scans and extracts the very first image in your Markdown article (local path, web URL, or Base64), uploads it to WeChat permanent materials, and sets it as the 900×383 header cover.
3. **Automated WeChat CDN Re-hosting**: Scans all in-text images and re-hosts them to WeChat CDN (`media/uploadimg`), automatically replacing URLs with `mmbiz.qpic.cn`.
4. **1-Click Official Draft API Publishing**: Directly pushes formatted rich-text articles to your WeChat Official Account Draft Box (`draft/add`), ready for mobile review and broadcast.
5. **Pluggable Multi-Style Engine**: Built-in `editorial` (Magazine) and `minimal` (Modern clean) styles, with an extensible Python class registry (`STYLES_REGISTRY`).

---

## ⚡ 1-Click Installation

### Recommended: Via `skills` Package Manager (Claude Code, Codex, Antigravity, etc.)

```bash
npx -y skills add sanqiushili/sqsl-wechat-skill/skills/sqsl-article-to-wechat -g
```

### Direct Git Clone

```bash
git clone https://github.com/sanqiushili/sqsl-wechat-skill.git
```

---

## ⚙️ WeChat Official Account API Setup

To get your WeChat Developer API credentials:

1. **Visit WeChat Developers Platform**: Log in at [https://developers.weixin.qq.com/](https://developers.weixin.qq.com/);
2. **Find Your Official Account**: Under **"My Businesses" (我的业务)** at the bottom of the home page, click your account;
3. **Get Developer Keys**: Under **"Basic Capabilities" (基础能力)**, locate **"Developer Keys" (开发秘钥)** to retrieve your `AppID` and generate your `AppSecret`;
4. **Configure IP Whitelist**: In the same section, add your machine's public IP to the **"IP Whitelist" (IP 白名单)** (run `curl ifconfig.me` to check your IP);
5. **Local Configuration**:
   ```bash
   cp wechat_config.template.json wechat_config.json
   ```
   Edit `wechat_config.json`:
   ```json
   {
     "app_id": "YOUR_WECHAT_APP_ID",
     "app_secret": "YOUR_WECHAT_APP_SECRET"
   }
   ```
   *Or provide via environment variables: `export WECHAT_APPID="xxx"` and `export WECHAT_APPSECRET="xxx"`.*

> 📖 See [Full WeChat API Configuration Guide](references/wechat_setup_guide.md) for details.

---

## 💻 CLI Usage

```bash
# 1. Render Markdown to WeChat inline HTML + preview
python3 scripts/render_wechat_html.py "examples/sample_editorial_article.md" --style editorial

# 2. Push to WeChat Draft Box
python3 scripts/wechat_draft_publisher.py "sample_editorial_article_微信排版.html" --title "Article Title"
```

---

## 📄 License

MIT License. Feel free to use, star, and contribute!
