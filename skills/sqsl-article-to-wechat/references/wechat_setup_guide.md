# 🔑 微信公众号 API 配置与全流程使用指南

本指南将帮助你从零获取微信公众号的开发者 API 凭证，并完成与 **SQSL Article to WeChat** 的无缝对接。

---

## 一、获取微信公众号 API 凭证 (AppID & AppSecret)

获取微信公众平台 API 凭证的官方统一入口为 **微信开发者平台**：

### 1. 登录微信开发者平台
访问官方网址：[https://developers.weixin.qq.com/](https://developers.weixin.qq.com/) 并使用微信扫码登录。

### 2. 找到你的公众号业务
在首页下方找到 **「我的业务」**，点击列表中你所管理的微信公众号。

```text
微信开发者平台首页 ➔ 页面下方「我的业务」 ➔ 选择对应公众号
```

### 3. 获取开发秘钥 (AppID & AppSecret)
进入公众号控制面板后：
1. 在左侧或页面中找到 **「基础能力」** 栏目；
2. 找到 **「开发秘钥」**（或基本配置中的开发者ID与密码）；
3. 复制你的 **`AppID`**（开发者ID）；
4. 点击生成/重置并保存你的 **`AppSecret`**（开发者密码，系统只显示一次，请妥善保存）。

### 4. 配置 IP 白名单 (重要 ⚠️)
微信公众平台出于安全防护机制，要求所有 API 调用请求必须来自经过认证的 IP 白名单：
1. 在「开发秘钥」同区域找到 **「IP 白名单」** 配置入口；
2. 点击修改，将你当前电脑/服务器的 **公网出口 IP** 添加到列表中；
3. *如何查询本机公网 IP？* 终端运行 `curl cip.cc` 或 `curl ifconfig.me` 即可查询。

> **💡 智能容错**：如果你在推送时遇到 `40164` 错误，错误信息中会自动提示你当前的公网 IP，只需将提示中的 IP 复制添加到微信白名单即可。

---

## 二、本地填入凭证配置

获取到 `AppID` 和 `AppSecret` 后，有两种配置方式（任选其一）：

### 方式 1：使用配置文件（推荐）
在技能根目录下，复制模板并创建 `wechat_config.json`：
```bash
cp wechat_config.template.json wechat_config.json
```
打开 `wechat_config.json`，填入你的凭证：
```json
{
  "app_id": "你的微信公众号AppID",
  "app_secret": "你的微信公众号AppSecret"
}
```
*(注：项目自带的 `.gitignore` 已默认忽略 `wechat_config.json`，绝不会上传到 GitHub 造成凭证泄露)*

### 方式 2：使用系统环境变量
你也可以直接在终端或系统环境变量中设置：
```bash
export WECHAT_APPID="你的微信公众号AppID"
export WECHAT_APPSECRET="你的微信公众号AppSecret"
```

---

## 三、用户使用指南 (三种使用场景)

### 场景 1：在 AI Agent 中直接对话使用（最简单）
在 Claude Code、Codex、Antigravity 或支持 Agent Skills 的对话窗口中：

* **默认大刊风排版并直推草稿箱**：
  ```text
  /sqsl-article-to-wechat 帮我把 docs/my_article.md 排版并发到公众号草稿箱
  ```
* **指定草木生活大刊风**：
  ```text
  /文章发公众号 用 olive_artisan 风格排版 docs/my_article.md
  ```
* **直接粘贴文稿内容**：
  ```text
  /sqsl-article-to-wechat 这是我今天的推文草稿：[直接粘贴你的Markdown文本]，帮我排版并推送。
  ```

**Agent 自动执行闭环**：
1. 提取文章正文中的**第一张图片**，自动上传微信素材库作为 **900×383 头条封面**；
2. 无头 Chrome 动态生成 Retina 级透明渐变标题图层，完成大刊排版；
3. 扫描正文插图并全自动转存微信官方 CDN；
4. 调用 `draft/add` API 直推草稿箱；
5. 输出草稿 Media ID，你的手机【微信公众平台助手】小程序或网页后台将立刻收到新草稿。

---

### 场景 2：在终端通过 Python 脚本运行（开发者模式）

#### 1. 仅生成排版 HTML 与本地预览
```bash
# 生成大刊风 (editorial)
python3 scripts/render_wechat_html.py "你的文章.md" --style editorial

# 生成阿芋·草木生活大刊风 (olive_artisan)
python3 scripts/render_wechat_html.py "你的文章.md" --style olive_artisan
```
*生成两个文件：`你的文章_微信排版.html`（内联样式版）与 `你的文章_预览.html`（浏览器预览版）。*

#### 2. 一键直推微信公众平台草稿箱
```bash
python3 scripts/wechat_draft_publisher.py "你的文章_微信排版.html" --title "文章标题"
```
*常用可选参数：*
* `--cover "/path/to/custom_cover.png"`：手动指定封面图（若不指定则自动提取文章首图）；
* `--author "作者名"`：设置公众号文章展示的作者名字；
* `--digest "自定义摘要"`：设置文章摘要（默认截取正文前段或标题）。

---

### 场景 3：无 API 权限或白名单变动时的「一键复制」兜底

如果你在没有配置微信 API、或外出办公网络 IP 变动暂时无法添加白名单时：
1. 系统依然会为你正常生成 `你的文章_预览.html`；
2. 双击在任意浏览器中打开预览页；
3. 页面顶部有一条深色磨砂悬浮工具栏，点击 **「一键复制到公众号」** 按钮；
4. 打开微信公众平台后台新建图文，直接按 `Ctrl/⌘ + V` 粘贴即可，样式 100% 完美还原！
