# 🏛️ SQSL WeChat Skill (三秋十李 · 微信公众号创作全家桶)

<p align="center">
  <strong>专为微信公众号创作者打造的一站式 Agent 技能矩阵：从「大号风格逆向复刻」到「杂志大刊排版」再到「官方草稿箱直推」</strong>
</p>

<p align="center">
  <a href="VERSION"><img src="https://img.shields.io/badge/version-1.0.0-2563EB.svg?style=flat-square" alt="Version 1.0.0"/></a>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+"/>
  <img src="https://img.shields.io/badge/Target-WeChat%20Official%20Account-07C160?style=flat-square&logo=wechat&logoColor=white" alt="WeChat Official Account"/>
  <img src="https://img.shields.io/badge/Architecture-Monorepo-orange.svg?style=flat-square" alt="Monorepo"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Personal%20Free%20%7C%20Commercial%20Contact-blue.svg?style=flat-square" alt="License"/></a>
</p>

<p align="center">
  简体中文 | <a href="README.en.md">English</a>
</p>

---

## 🌟 为什么选择 SQSL WeChat Skill 全家桶？

传统的微信公众号排版工具（微信自带编辑器、第三方排版网站）操作繁琐、格式经常错乱、难以批量自动化。

**SQSL WeChat Skill** 将微信内容生产全流程拆解为标准化、可插拔的 Agent 技能矩阵：
1. **🎬 视频转文章引擎 (`sqsl-video-to-article`)**：输入本地视频，本地 Whisper 极速转写，专有词典自动纠错，根据字幕时间戳精准截取高清帧，高度保留作者第一人称原汁原味撰写图文 Markdown；
2. **🎨 风格克隆工坊 (`sqsl-style-cloner`)**：只要你看到别人家公众号排版好看，发来链接，自动逆向解析其视觉 DNA（大标题艺术数字图片、胶带高亮底色、燕麦米灰卡片、字距呼吸感），生成可插拔风格；
3. **📰 排版直推引擎 (`sqsl-article-to-wechat`)**：Markdown 文档一键渲染为高颜值内联 HTML，自动提取正文首图为 900×383 头条封面，插图自动转存微信官方 CDN，接口直推后台草稿箱，手机端一键审核群发；
4. **🧭 智能总调度路由 (`sqsl-wechat-start`)**：类似 `/dbs`，一个统一入口（`/sqsl-wechat-start` 或简写 `/sqsl`），输入视频转文章，发文章自动排版，发链接自动克隆，说引导自动导航！

---

## 🎨 核心排版风格样例展厅 (Style Gallery)

SQSL 内置杂志大刊级排版美学风格，所有风格均采用**微信内联样式引擎**与 **Retina 级视觉图层**渲染，排版零杂色污染、零格式损耗，支持直接推送微信草稿箱或在浏览器中一键无损复制：

| 风格名称 | 风格参数 | 视觉 DNA 与特征 | 核心色调 | 推荐场景 |
| :--- | :--- | :--- | :--- | :--- |
| **Editorial**<br>*(先锋大刊风)* | `--style editorial` | Didot 艺术大水印 (`PART 01`)、宋体高对比中文、88% 黄金留白画幅、微阴影卡片 | `#08285E`<br>`#EA580C` | 深度行业洞见、先锋思想长文、科技与设计大刊 |
| **阿芋 · 草木生活**<br>*(生活美学大刊)* | `--style olive_artisan` | Bodoni 粗斜体艺术数字 (`01`/`02`)、黄绿胶带高亮大标题、温润燕麦米灰卡片、1.8 呼吸行高 | `#2B2F23`<br>`#E0DEA8` | 人物专访、山野户外、手作匠人、旅行随笔 |

<br/>

<div align="center">

### 1. 🏛️ `editorial` · 先锋大刊风（默认核心）
<p align="center"><em>Didot 艺术大水印 · 宋体高对比中文 · 88% 黄金留白画幅 · 经典沉静墨蓝</em></p>

<img src="assets/preview_editorial.png" alt="先锋大刊风样例" width="680" style="max-width: 100%; border-radius: 12px;" />

<br/><br/>

### 2. 🌿 `olive_artisan` · 阿芋 · 草木山野生活大刊风
<p align="center"><em>Bodoni 粗斜体艺术大数字（01/02）· 黄绿胶带高亮居中大标题 · 燕麦米灰软卡片 · 1.8 极适呼吸行高</em></p>

<img src="assets/preview_olive_artisan.png" alt="阿芋 · 草木山野生活风样例" width="680" style="max-width: 100%; border-radius: 12px;" />

</div>

---

```mermaid
flowchart TD
    subgraph Client["用户与 Agent 交互层"]
        Cmd0["/sqsl-video-to-article (视频转文章)"]
        Cmd1["/sqsl-wechat-start (或简写 /sqsl)"]
        Cmd2["/sqsl-article-to-wechat (排版直推)"]
        Cmd3["/sqsl-style-cloner (风格克隆)"]
    end

    subgraph Suite["SQSL 技能矩阵 (Monorepo)"]
        Router["skills/sqsl-wechat-start\n总路由器 (智能意图分流与状态导航)"]
        
        subgraph Sub0["skills/sqsl-video-to-article (视频转文章引擎)"]
            Whisper["本地 Whisper 硬件加速转写"] --> Glossary["专有词典 ASR 自动纠错"]
            Glossary --> Frame["依据 SRT 时间戳精准抽帧校验"]
            Frame --> DraftMD["还原作者口吻撰写图文 Markdown"]
        end

        subgraph Sub1["skills/sqsl-style-cloner (风格克隆工坊)"]
            Crawler["网页爬取与 DOM 提取"] --> Analyzer["视觉 DNA 逆向分析\n- 胶带高亮底色探测\n- 章节序号图片化 (01/02)\n- 零杂色渗透法则"]
            Analyzer --> Compiler["动态编译风格类 style_{name}.py"]
        end

        subgraph Sub2["skills/sqsl-article-to-wechat (排版直推引擎)"]
            Pool["公共风格池 (styles/)\n- editorial (先锋大刊风)\n- olive_artisan (草木生活大刊风)"]
            MD["Markdown 解析与渲染"]
            Cover["首图自适应 900x383 封面"]
            CDN["正文图片自动转存微信 CDN"]
            Draft["微信草稿箱 draft/add API 直推"]
        end
    end

    Cmd0 --> Sub0
    Cmd1 --> Router
    Router -->|输入视频/整理成文| Sub0
    Router -->|发文章/Markdown| Sub2
    Router -->|发链接/学排版| Sub1
    DraftMD -->|无缝流转排版| Sub2
    Compiler -->|新风格自动注入| Pool
    Pool --> MD
    MD --> Cover & CDN --> Draft --> Output["📱 手机微信公众平台助手收到新草稿"]
```

---

## 📦 目录结构 (Monorepo)

```text
sqsl-wechat-skill/                            # GitHub 唯一根仓库
├── README.md                                 # 中文主说明文档
├── README.en.md                              # 英文主说明文档
├── VERSION                                   # 全局语义化版本号 (1.0.0)
├── CHANGELOG.md                              # 版本更新记录
├── LICENSE                                   # MIT 许可证
├── .gitignore                                # 统一过滤规则（保护凭证）
├── AGENTS.md                                 # Multi-Agent 工作台规范
├── wechat_config.template.json               # 微信公众平台凭证模板
│
└── skills/                                   # 核心子技能目录
    ├── sqsl-wechat-start/                    # 1. 家族总路由主技能 (/sqsl-wechat-start 或 /sqsl)
    │   └── SKILL.md
    │
    ├── sqsl-video-to-article/                # 2. 视频转图文文章生成引擎 (/sqsl-video-to-article)
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── scripts/
    │   │   └── video_to_article.py           # 音频提取、Whisper转写、词典纠错与抽帧
    │   └── references/
    │       └── glossary.json                 # 常用专有名词与同音字纠错词典
    │
    ├── sqsl-article-to-wechat/               # 3. 排版与微信草稿直推引擎
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   ├── render_wechat_html.py         # 多风格 Markdown 渲染器
    │   │   └── wechat_draft_publisher.py     # 首图封面提取、CDN转存与草稿直推
    │   ├── styles/                           # 动态热加载风格池
    │   │   └── style_olive_artisan.py        # 阿芋·草木山野生活大刊风 (内置 editorial 先锋大刊风)
    │   ├── templates/
    │   ├── references/
    │   │   ├── editorial_inspiration.md      # 大刊排版美学灵感
    │   │   └── wechat_setup_guide.md         # 微信公众号 API 详细配置手册
    │   └── examples/
    │       └── sample_editorial_article.md   # 排版测试样例文章
    │
    └── sqsl-style-cloner/                    # 4. 风格逆向与克隆工坊
        ├── SKILL.md
        ├── scripts/
        │   └── clone_wechat_style.py         # 视觉 DNA 逆向提取与风格代码生成
        ├── templates/
        │   └── style_template.py             # 风格类代码模板
        └── examples/
            └── sample_wechat_article.html    # 离线测试样例
```

---

## ⚡ 极速上手

### 1. 一键安装（推荐：通过 `skills` 包管理器）

支持 Claude Code、Codex、Antigravity 等所有兼容 Agent Skills 规范的环境：

```bash
# 一键安装全家桶（包含总路由、排版发布、风格克隆）
npx -y skills add sanqiushili/sqsl-wechat-skill -g --all

# 或按需单装其中一个子技能
npx -y skills add sanqiushili/sqsl-wechat-skill/skills/sqsl-article-to-wechat -g
```

### 2. 配置微信公众平台凭证 (可选，免配置也能一键复制)

若需要使用官方 API 一键直推草稿箱：
1. **访问微信开发者平台**：[https://developers.weixin.qq.com/](https://developers.weixin.qq.com/) 登录；
2. **定位公众号**：在首页下方 **「我的业务」** 找到对应公众号 ➔ **「基础能力」➔「开发秘钥」** 获取 `AppID` 并生成保存 `AppSecret`；
3. **配置 IP 白名单**：同区域将本机公网 IP（终端运行 `curl cip.cc`）加入白名单；
4. **本地配置**：复制模板创建 `wechat_config.json`：
   ```bash
   cp wechat_config.template.json wechat_config.json
   ```
   填入你的 `app_id` 与 `app_secret`。*(也可通过环境变量 `export WECHAT_APPID="xxx"` 提供)*

> 💡 **不想配置 API？立刻就能用！** 系统每次排版都会生成本地 `_预览.html`，浏览器打开点顶部的「一键复制到公众号」即可无损粘贴！

---

## 💬 对话使用示例

直接在支持 Agent 的聊天框中输入：

* **总路由智能调度**：
  ```text
  /sqsl-wechat-start 帮我排版这篇文稿并推送到公众号：docs/post.md
  ```
  ```text
  /sqsl-wechat-start 帮我把这篇公众号的排版风格克隆下来：https://mp.weixin.qq.com/s/xxxxxxxxxxxx
  ```
  *(注：主技能支持简写命令 `/sqsl` 或 `/sqsl-start`)*
* **排版并直推草稿箱**：
  ```text
  /sqsl-article-to-wechat 用 olive_artisan 风格排版 docs/post.md
  ```
* **风格逆向克隆**：
  ```text
  /sqsl-style-cloner https://mp.weixin.qq.com/s/xxxxxxxxxxxx --name cool_lifestyle
  ```

---

## 🙏 致谢与灵感之源 (Acknowledgements & Inspirations)

本项目的架构设计与排版美学深受开源社区与先锋创作者的启发，特别致敬与感谢：

* **[dontbesilent2025/dbskill](https://github.com/dontbesilent2025/dbskill)**：
  感谢 dbs 团队在 Agent 技能工程化上的开拓性实践！本项目在 **Monorepo 全家桶矩阵架构**、**`/sqsl` 任务前路由与任务后导航模式** 以及多端 **`AGENTS.md` 工作台规范** 上均深度借鉴了 dbskill 的优秀架构思想。
* **[归藏 (Guizang)](https://github.com/op7418)**：
  感谢归藏在微信公众号视觉叙事、社交图文卡片排版美学上的持续输出与设计启发，为本项目奠定了追求“大刊呼吸感、克制版式与高级质感”的美学标准。

### 🎨 内置核心风格的灵感溯源

1. **`editorial`（先锋大刊风）**：
   - 逆向解构自 *ELLE* 杂志深度专栏名篇[《把“蓝色”交给 JISOO，她会怎么穿？》](https://mp.weixin.qq.com/s/63NfcghNomURBgBxyjIxGw)，复刻了其标志性的 Didot / 宋体水印标题图层（双向交错渐变 `PART` 与数字 `01`/`02`）、88% 黄金留白画幅与深邃墨蓝先锋质感；
2. **`olive_artisan`（阿芋 · 草木山野生活大刊风）**：
   - 逆向解构自 *Voicer* 杂志深度专访名篇[《重访阿芋：是制帽师，也是山野里的自在风》](https://mp.weixin.qq.com/s/2a85ue2uWT9JJpIcTqYYvA)，1:1 像素级还原了标志性的 Bodoni/Didot 粗斜体艺术大数字插图图层（`01`/`02`）、黄绿胶带高亮居中大标题（`#E0DEA8`）、温润燕麦米灰软卡片（`#F7F6F3`）以及极为松弛的 1.8 舒适行高与 1.5px 呼吸字距。

> ⚠️ **版权与免责声明**：  
> 本项目内置及逆向复刻的排版样式仅供个人学习、排版审美交流与开源技术研究使用，相关视觉元素与版面设计的知识产权均归原作者/出品机构所有。  
> **若原作者或相关权利方认为某些元素的使用存在不妥或涉及侵权，请随时通过 Issue 或邮件联系我们，我们将在第一时间予以核实并立即下架/移除对应样式，感谢理解与包容！**

---

## 📄 许可证与商业定制 (License & Commercial Use)

本项目采用 **双重授权模式（免费使用 / 商业集成授权与定制）**：

### 1. ✍️ 免费用于文章排版 (Free for Typesetting)
- **排版完全免费**：无论个人创作者、自媒体博主还是企业机构，均可**免费**使用本工具进行日常公众号文章的排版、样式生成与草稿推送。

### 2. 🏢 商业使用界定与风格免责 (Commercial Definition & Style Disclaimer)
- **商业产品集成授权**：将本项目的排版引擎底座、解析脚本或整个 Skill 架构打包集成进商业化 SaaS 平台、商业 APP、收费小程序或商用软件工具中，需事先与作者联系取得正式商业授权；
- **⚠️ 商业风格侵权规避特别声明**：本项目内置的参考案例风格（如参考特定杂志媒体排版的 `editorial`、`olive_artisan` 等）仅供开源学习研究与个人排版交流，**不包含在任何商业授权范围之内，亦严禁直接用于商业产品售卖或直接授权**。商业化产品集成如需配套风格，**必须为企业或品牌全新重新定制专属商业设计风格**，以彻底规避潜在版权侵权争议。

### 3. 🎨 品牌风格定制与技术支持 (Customization Services)
面向有更高审美与工程化需求的企业与品牌，我们提供专属定制服务：
- 🎨 **品牌专属视觉定制**：定制专属品牌色卡与字体排印系统；
- 🛠️ **专属排版组件开发**：特殊数据表格、SVG 动态交互卡片、专属品牌水印；
- 🚀 **自动化流水线私有化交付**：对接飞书文档、语雀、Notion 等团队知识库，实现多平台自动化排版直推公众号。

> 🤝 **商业合作与风格定制咨询**：欢迎联系邮箱 **[leeguiyu@qq.com](mailto:leeguiyu@qq.com)**，或通过 [GitHub Issues](https://github.com/sanqiushili/sqsl-wechat-skill/issues) 留言。详情参见 [LICENSE](LICENSE)。
