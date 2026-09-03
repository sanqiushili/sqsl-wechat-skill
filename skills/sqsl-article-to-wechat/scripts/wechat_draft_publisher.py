#!/usr/bin/env python3
"""
wechat_draft_publisher.py - sqsl-article-to-wechat 微信公众平台草稿箱自动推送工具

核心特性：
1. 自动提取首图作为微信封面（First-image-as-cover）：
   - 自动扫描 HTML / Markdown 中的第一张图片（支持本地路径、网络 URL、Base64）
   - 自动上传至微信永久素材库获取 thumb_media_id 作为头条封面
   - 同时支持 --cover 手动指定封面覆盖
2. 图文插图自动转存微信图床：
   - 扫描 HTML 中的所有本地图片与 Base64，调用 media/uploadimg 批量转存并替换链接
3. 一键推送到公众号草稿箱（draft/add）
"""

import os
import sys
import re
import json
import html
import urllib.request
import urllib.parse
import subprocess
import base64
import tempfile
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "wechat_config.json"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def get_credentials():
    app_id = os.environ.get("WECHAT_APPID") or os.environ.get("WECHAT_APP_ID")
    app_secret = os.environ.get("WECHAT_APPSECRET") or os.environ.get("WECHAT_APP_SECRET")
    
    if (not app_id or not app_secret) and CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                app_id = app_id or cfg.get("app_id") or cfg.get("appid")
                app_secret = app_secret or cfg.get("app_secret") or cfg.get("secret")
        except Exception:
            pass
            
    return app_id, app_secret

def get_access_token(app_id, app_secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        
    if "access_token" in res:
        return res["access_token"]
    else:
        errcode = res.get("errcode")
        errmsg = res.get("errmsg", "")
        if errcode == 40164:
            raise PermissionError(
                f"微信接口报错 [40164]：当前 IP 不在公众号白名单内。\n"
                f"微信返回提示：{errmsg}\n"
                f"请将提示中的 IP 地址添加到公众号后台 [设置与开发 -> 基本配置 -> IP白名单] 中。"
            )
        raise RuntimeError(f"获取微信 access_token 失败 [{errcode}]: {errmsg}")

def upload_intext_image(access_token, image_path):
    """上传图文内插图（返回微信 CDN URL）"""
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
    img_file = Path(image_path).resolve()
    if not img_file.exists():
        return ""

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    filename = img_file.name
    content_type = "image/png" if filename.endswith(".png") else ("image/gif" if filename.endswith(".gif") else "image/jpeg")
    
    with open(img_file, "rb") as f:
        file_bytes = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    })
    
    with urllib.request.urlopen(req, timeout=20) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if "url" in res:
            return res["url"]
        else:
            print(f"上传插图失败: {res}", file=sys.stderr)
            return ""

def upload_cover_material(access_token, image_path):
    """上传封面图素材至永久素材库（返回 thumb_media_id）"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    img_file = Path(image_path).resolve()
    if not img_file.exists():
        return ""

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    filename = img_file.name
    content_type = "image/png" if filename.endswith(".png") else ("image/gif" if filename.endswith(".gif") else "image/jpeg")
    
    with open(img_file, "rb") as f:
        file_bytes = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    })
    
    with urllib.request.urlopen(req, timeout=20) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if "media_id" in res:
            return res["media_id"]
        else:
            print(f"上传封面素材失败: {res}", file=sys.stderr)
            return ""

def create_wechat_draft(access_token, title, content_html, thumb_media_id="", author="AI 工作台", digest=""):
    """创建图文草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    payload = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest or title,
                "content": content_html,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
        ]
    }

    req_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, headers={"Content-Type": "application/json; charset=utf-8"})
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        
    if "media_id" in res:
        return res["media_id"]
    else:
        raise RuntimeError(f"创建微信草稿箱失败: {res}")

def process_and_upload_html_images(access_token, html_content, base_dir=None):
    """
    扫描 HTML 中的所有 img src（包括 Base64 和本地文件路径）
    自动上传至微信图床 media/uploadimg，并将其替换为 mmbiz.qpic.cn 链接
    """
    img_src_pattern = re.compile(r'<img\s+([^>]*?)src=["\']([^"\']+)["\']([^>]*?)>', re.IGNORECASE)
    
    def replacer(match):
        prefix = match.group(1)
        src = match.group(2)
        suffix = match.group(3)
        
        wechat_url = ""
        
        # 1. Base64 图片处理
        if src.startswith("data:image/"):
            try:
                header, encoded = src.split(",", 1)
                ext = "png"
                if "jpeg" in header or "jpg" in header:
                    ext = "jpg"
                elif "gif" in header:
                    ext = "gif"
                img_data = base64.b64decode(encoded)
                with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp_f:
                    tmp_f.write(img_data)
                    tmp_path = tmp_f.name
                
                wechat_url = upload_intext_image(access_token, tmp_path)
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
            except Exception as e:
                print(f"处理 Base64 图片异常: {e}", file=sys.stderr)
                
        # 2. 本地文件处理
        elif not src.startswith("http://") and not src.startswith("https://"):
            local_path = Path(src)
            if not local_path.is_absolute() and base_dir:
                local_path = (Path(base_dir) / src).resolve()
            if local_path.exists():
                wechat_url = upload_intext_image(access_token, str(local_path))
                
        if wechat_url:
            print(f"  ✓ 成功上传正文插图至微信图床: {wechat_url[:45]}...")
            return f'<img {prefix}src="{wechat_url}"{suffix}>'
        else:
            return match.group(0)

    print("2. 扫描并上传正文中的所有图文插图至微信图床...")
    return img_src_pattern.sub(replacer, html_content)


def extract_first_image_candidate(html_content, base_dir=None):
    """
    从 HTML 中提取第一张实际图片作为封面候选
    （排除生成的章节水印小图，优先提取正文大图）
    返回本地临时文件路径或文件真实路径
    """
    img_tags = re.findall(r'<img\s+[^>]*?src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    
    for src in img_tags:
        # 排除包含 SVG data url 的纯矢量水印（如果需要）或者寻找第一个实体图
        if src.startswith("data:image/"):
            try:
                header, encoded = src.split(",", 1)
                ext = "png"
                if "jpeg" in header or "jpg" in header:
                    ext = "jpg"
                elif "gif" in header:
                    ext = "gif"
                img_data = base64.b64decode(encoded)
                tmp_f = tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False)
                tmp_f.write(img_data)
                tmp_f.close()
                return tmp_f.name
            except Exception:
                continue
        elif src.startswith("http://") or src.startswith("https://"):
            try:
                req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()
                ext = "jpg" if ".jpg" in src or ".jpeg" in src else "png"
                tmp_f = tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False)
                tmp_f.write(data)
                tmp_f.close()
                return tmp_f.name
            except Exception:
                continue
        else:
            local_p = Path(src)
            if not local_p.is_absolute() and base_dir:
                local_p = (Path(base_dir) / src).resolve()
            if local_p.exists():
                return str(local_p)
                
    return None

def generate_fallback_cover(title="文章推荐", headline="", out_png_path="/tmp/sqsl_default_cover.png"):
    """
    文章无插图时的兜底封面生成器（优雅渐变 + 标题文字）
    """
    display_title = title if len(title) <= 24 else title[:22] + "..."
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 0;
    width: 900px;
    height: 383px;
    background: linear-gradient(135deg, #08285E 0%, #1E3A8A 50%, #0F172A 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #FFFFFF;
    font-family: "Songti SC", "Noto Serif CJK SC", "PingFang SC", sans-serif;
    box-sizing: border-box;
    padding: 40px;
    text-align: center;
  }}
  .badge {{
    font-size: 14px;
    letter-spacing: 4px;
    color: #F59E0B;
    font-weight: 700;
    margin-bottom: 16px;
    text-transform: uppercase;
  }}
  .title {{
    font-size: 38px;
    font-weight: 700;
    line-height: 1.35;
    letter-spacing: 2px;
    max-width: 800px;
    text-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }}
</style>
</head>
<body>
  <div class="badge">精选图文</div>
  <div class="title">{html.escape(display_title)}</div>
</body>
</html>"""

    tmp_html = "/tmp/sqsl_cover_fallback.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    if Path(CHROME_BIN).exists():
        cmd = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--window-size=900,383",
            f"--screenshot={out_png_path}",
            tmp_html
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            if Path(out_png_path).exists():
                return out_png_path
        except Exception:
            pass
    return ""


def push_article_to_draft(html_file_path, title, cover_image_path=None, author="AI 工作台", digest=""):
    app_id, app_secret = get_credentials()
    if not app_id or not app_secret:
        raise ValueError(
            "未检测到微信公众号凭证！请在环境变量中设置 WECHAT_APPID 与 WECHAT_APPSECRET，"
            f"或在配置文件 {CONFIG_PATH} 中填入凭证。\n"
            "若暂无 API 权限，请直接使用生成的本地预览网页中的【一键复制到公众号】功能。"
        )

    html_file = Path(html_file_path).resolve()
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    print("1. 获取微信公众号 access_token...")
    token = get_access_token(app_id, app_secret)

    # 1. 首图提取作为封面
    thumb_media_id = ""
    cover_file_to_upload = None

    if cover_image_path and Path(cover_image_path).exists():
        print(f"3. 使用指定封面图：{cover_image_path}")
        cover_file_to_upload = cover_image_path
    else:
        print("3. 正在提取文章正文第一张图片作为封面...")
        first_img = extract_first_image_candidate(html_content, base_dir=html_file.parent)
        if first_img and Path(first_img).exists():
            print(f"  ✓ 成功提取正文首图作为封面素材：{first_img}")
            cover_file_to_upload = first_img
        else:
            print("  ℹ 正文未发现可用插图，自动生成高质感纯文本头条封面...")
            fallback_cover = generate_fallback_cover(title=title)
            if fallback_cover and Path(fallback_cover).exists():
                cover_file_to_upload = fallback_cover

    if cover_file_to_upload and Path(cover_file_to_upload).exists():
        print(f"  → 上传封面素材至微信永久素材库：{cover_file_to_upload}...")
        thumb_media_id = upload_cover_material(token, cover_file_to_upload)
        if thumb_media_id:
            print(f"  ✓ 封面素材上传成功，thumb_media_id: {thumb_media_id}")
    else:
        print("警告：未找到或未能生成有效封面图素材", file=sys.stderr)

    # 2. 替换正文中的所有图片为微信 CDN URL
    html_content = process_and_upload_html_images(token, html_content, base_dir=html_file.parent)

    # 3. 摘要截断
    if not digest:
        digest = title
    if len(digest) > 115:
        digest = digest[:112] + "..."

    print(f"4. 推送图文至微信公众号草稿箱 (标题: {title}, 摘要: {digest[:30]}...)...")
    draft_media_id = create_wechat_draft(
        access_token=token,
        title=title,
        content_html=html_content,
        thumb_media_id=thumb_media_id,
        author=author,
        digest=digest
    )

    print(f"🎉 推送成功！草稿 Media ID: {draft_media_id}")
    print("你现在可以打开手机【微信公众平台助手】小程序或电脑后台进行最终审核与群发。")
    return draft_media_id


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Push article HTML to WeChat Draft Box (First-image cover)")
    parser.add_argument("html_file", help="Path to formatted HTML file")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--cover", help="Explicit cover image path (default: auto-extract 1st image from article)")
    parser.add_argument("--author", default="AI 工作台", help="Author name")
    parser.add_argument("--digest", default="", help="Summary digest")
    args = parser.parse_args()

    try:
        push_article_to_draft(args.html_file, args.title, args.cover, args.author, args.digest)
    except Exception as e:
        print(f"❌ 推送失败: {e}", file=sys.stderr)
        sys.exit(1)
