#!/usr/bin/env python3
"""
render_wechat_html.py - sqsl-article-to-wechat 通用多风格微信公众号排版引擎

特性：
1. 多风格架构（Multi-Style Registry）：支持 --style editorial（先锋大刊风，默认）、olive_artisan（阿芋·草木山野生活大刊风），支持动态扩充新风格。
2. 全面 Markdown 语法支持：支持标题、代码块、表格、Quote 引言卡、列表、行内标注 (==高亮==, `code`, **加粗**) 等。
3. 首图识别与提取：自动提取正文首张图片，供封面图提取模块使用。
4. 微信内联样式生成与一键复制预览页：完全免疫微信格式过滤，浏览器端一键复制。
"""

import os
import sys
import re
import json
import base64
import html
import subprocess
from pathlib import Path

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ==============================================================================
# 1. 章节大标题渲染器（先锋大刊风 - Didot/宋体 渐变水印图层）
# ==============================================================================

def render_editorial_title_png(part_str, main_title, sub_title="", out_png_path=None):
    """
    使用无头 Chrome 渲染 Retina 级 1:1 SQSL Editorial 杂志大刊风格章节标题图层
    Didot/Bodoni 72 瘦长高对比衬线水印 + 宋体中文前景，双向渐变交织
    """
    if not out_png_path:
        out_png_path = f"/tmp/sqsl_chapter_title_{part_str}.png"
        
    grad_part_id = f"grad_part_{part_str}"
    grad_num_id = f"grad_num_{part_str}"
    
    sub_element = f"""
    <g transform="translate(600, 310) scale(0.94, 1.12)">
      <text class="cn-title" x="0" y="0" text-anchor="middle" font-size="44" letter-spacing="2.5">{html.escape(sub_title)}</text>
    </g>""" if sub_title else ""
    
    main_y = "230" if sub_title else "260"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 0;
    background: transparent;
    overflow: hidden;
  }}
  .cn-title {{
    font-family: "Didot", "Bodoni 72", "Songti SC", "FZShuSong-Z01S", "STSong", "SimSun", serif;
    fill: #08285E;
    font-weight: 700;
  }}
  .en-watermark {{
    font-family: "Didot", "Bodoni 72", "Big Caslon", "Times New Roman", Georgia, serif;
    font-weight: 900;
  }}
</style>
</head>
<body>
  <svg width="1200" height="480" viewBox="0 0 1200 480" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="{grad_part_id}" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#BDCCDC" stop-opacity="0.95"/>
        <stop offset="40%" stop-color="#D0DFED" stop-opacity="0.6"/>
        <stop offset="80%" stop-color="#FFFFFF" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="{grad_num_id}" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="15%" stop-color="#FFFFFF" stop-opacity="0"/>
        <stop offset="60%" stop-color="#D0DFED" stop-opacity="0.6"/>
        <stop offset="100%" stop-color="#BDCCDC" stop-opacity="0.95"/>
      </linearGradient>
    </defs>
    
    <!-- 水印 PART -->
    <g transform="translate(600, 225) scale(1.02, 1.25)">
      <text class="en-watermark" x="0" y="0" text-anchor="middle" font-size="200" letter-spacing="24" fill="url(#{grad_part_id})">PART</text>
    </g>
    
    <!-- 水印 01/02 -->
    <g transform="translate(600, 425) scale(0.9, 1.3)">
      <text class="en-watermark" x="0" y="0" text-anchor="middle" font-size="200" letter-spacing="12" fill="url(#{grad_num_id})">{part_str}</text>
    </g>
    
    <!-- 中文主标题 -->
    <g transform="translate(600, {main_y}) scale(0.94, 1.12)">
      <text class="cn-title" x="0" y="0" text-anchor="middle" font-size="70" letter-spacing="4">{html.escape(main_title)}</text>
    </g>
    
    <!-- 中文副标题 -->
    {sub_element}
  </svg>
</body>
</html>"""
    
    tmp_html = f"/tmp/sqsl_title_tmp_{part_str}.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    # SVG 兜底
    svg_raw = f"""<svg width="1200" height="480" viewBox="0 0 1200 480" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="{grad_part_id}" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#BDCCDC" stop-opacity="0.95"/>
        <stop offset="40%" stop-color="#D0DFED" stop-opacity="0.6"/>
        <stop offset="80%" stop-color="#FFFFFF" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="{grad_num_id}" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="15%" stop-color="#FFFFFF" stop-opacity="0"/>
        <stop offset="60%" stop-color="#D0DFED" stop-opacity="0.6"/>
        <stop offset="100%" stop-color="#BDCCDC" stop-opacity="0.95"/>
      </linearGradient>
    </defs>
    <g transform="translate(600, 225) scale(1.02, 1.25)">
      <text font-family="'Didot', 'Bodoni 72', 'Big Caslon', serif" font-weight="900" x="0" y="0" text-anchor="middle" font-size="200" letter-spacing="24" fill="url(#{grad_part_id})">PART</text>
    </g>
    <g transform="translate(600, 425) scale(0.9, 1.3)">
      <text font-family="'Didot', 'Bodoni 72', 'Big Caslon', serif" font-weight="900" x="0" y="0" text-anchor="middle" font-size="200" letter-spacing="12" fill="url(#{grad_num_id})">{part_str}</text>
    </g>
    <g transform="translate(600, {main_y}) scale(0.94, 1.12)">
      <text font-family="'Songti SC', 'Noto Serif CJK SC', 'SimSun', serif" fill="#08285E" font-weight="700" x="0" y="0" text-anchor="middle" font-size="70" letter-spacing="4">{html.escape(main_title)}</text>
    </g>
    {sub_element}
  </svg>"""

    if Path(CHROME_BIN).exists():
        cmd = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--window-size=1200,480",
            "--default-background-color=00000000",
            f"--screenshot={out_png_path}",
            tmp_html
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            if Path(out_png_path).exists() and os.path.getsize(out_png_path) > 100:
                with open(out_png_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/png;base64,{b64}"
        except Exception:
            pass

    svg_b64 = base64.b64encode(svg_raw.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{svg_b64}"


# ==============================================================================
# 2. 风格配置系统 (Styles Registry)
# ==============================================================================

class BaseStyle:
    name = "base"
    display_name = "基础风格"
    
    def render_doc_start(self):
        return """<section style="max-width:677px;margin:0 auto;background:#FFFFFF;font-family:PingFangSC-light,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:rgb(28,28,28);line-height:1.75;letter-spacing:0.3px;box-sizing:border-box;">"""
        
    def render_h1(self, title, tag=""):
        tag_html = f'<p style="font-size:11px;font-weight:600;color:#08285E;letter-spacing:3px;margin:0 0 10px;text-transform:uppercase;"><span leaf="">{tag}</span></p>' if tag else ""
        return f"""
  <!-- 主标题 -->
  <section style="padding:28px 22px 12px;text-align:center;box-sizing:border-box;">
    {tag_html}
    <p style="font-family:'Songti SC','Noto Serif CJK SC',serif;font-size:24px;font-weight:700;line-height:1.35;color:#08285E;margin:0 0 10px;letter-spacing:1px;"><span leaf="">{title}</span></p>
  </section>
  <section style="text-align:center;margin:6px 0 24px;line-height:0;box-sizing:border-box;">
    <section style="display:inline-block;width:36px;height:2px;background:#08285E;"><span leaf=""><br/></span></section>
  </section>"""

    def render_h2(self, idx, text):
        num_str = f"{idx:02d}"
        return f"""
  <!-- H2 章节标题 -->
  <section style="margin:28px 22px 14px;box-sizing:border-box;">
    <p style="font-size:18px;font-weight:700;color:#08285E;margin:0;"><span leaf="">{num_str}. {text}</span></p>
  </section>"""

    def render_h3(self, text, is_highlight=False):
        badge = '<span style="background:#FFF0E6;color:#EA580C;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;margin-left:8px;vertical-align:middle;display:inline-block;"><span leaf="">核心</span></span>' if is_highlight else ''
        return f"""
  <!-- H3 小标题 -->
  <section style="padding:14px 22px 6px;box-sizing:border-box;">
    <p style="font-size:16px;font-weight:700;line-height:1.4;color:#08285E;margin:0;letter-spacing:0.5px;">
      <span leaf="">{text}</span>{badge}
    </p>
  </section>"""

    def render_callout(self, content):
        return f"""
  <!-- 重点引言卡 -->
  <section style="background:#F4F7FA;border-left:3px solid #08285E;padding:14px 18px;margin:18px 22px;border-radius:0 4px 4px 0;box-sizing:border-box;">
    <p style="margin:0;font-size:13.5px;color:#08285E;line-height:1.65;text-align:justify;"><span leaf="">{content}</span></p>
  </section>"""

    def render_paragraph(self, content):
        return f"""
  <!-- 段落正文 -->
  <section style="font-size:14px;font-family:PingFangSC-light;padding:0px 22px;line-height:1.75;box-sizing:border-box;margin:12px 0;">
    <p style="white-space:normal;margin:0px;padding:0px;box-sizing:border-box;text-align:justify;"><span leaf="">{content}</span></p>
  </section>"""

    def render_list_item(self, content, is_ordered=False, num=1):
        bullet = f"{num}." if is_ordered else "•"
        return f"""
  <!-- 列表项 -->
  <section style="font-size:14px;font-family:PingFangSC-light;padding:3px 22px 3px 36px;line-height:1.75;box-sizing:border-box;position:relative;">
    <p style="white-space:normal;margin:0px;padding:0px;box-sizing:border-box;text-align:justify;">
      <span style="position:absolute;left:22px;color:#08285E;font-weight:bold;">{bullet}</span><span leaf="">{content}</span>
    </p>
  </section>"""

    def render_image(self, b64_or_src, caption=""):
        caption_html = f"""
  <section style="text-align:center;margin:0 0 20px;line-height:1.5;box-sizing:border-box;padding:0 22px;">
    <p style="margin:4px 0 0;font-size:12px;color:#888888;font-family:PingFangSC-light;"><span leaf="">{caption}</span></p>
  </section>""" if caption else '<section style="margin-bottom:14px;"></section>'
        
        return f"""
  <!-- 插图卡片 -->
  <section style="text-align:center;margin:18px 0 8px;line-height:0;width:100%;box-sizing:border-box;">
    <section style="max-width:100%;vertical-align:middle;display:inline-block;width:92%;height:auto;box-sizing:border-box;">
      <img src="{b64_or_src}" style="vertical-align:middle;max-width:100%;width:100%;box-sizing:border-box;display:block;border-radius:4px;box-shadow:0 2px 10px rgba(0,0,0,0.05);" alt="{caption}"/>
    </section>
  </section>{caption_html}"""

    def render_code_block(self, code_text, lang=""):
        escaped_code = html.escape(code_text)
        return f"""
  <!-- 代码块 -->
  <section style="margin:16px 22px;border-radius:6px;background:#1E293B;padding:14px 16px;box-sizing:border-box;overflow-x:auto;">
    <p style="margin:0 0 6px;font-size:11px;color:#94A3B8;font-family:ui-monospace,Menlo,monospace;text-transform:uppercase;">{lang or 'CODE'}</p>
    <pre style="margin:0;font-family:ui-monospace,Menlo,Monaco,Consolas,monospace;font-size:12.5px;color:#F8FAFC;line-height:1.55;white-space:pre-wrap;word-break:break-all;"><code>{escaped_code}</code></pre>
  </section>"""

    def render_table(self, headers, rows):
        th_cells = "".join([f'<th style="border:1px solid #E2E8F0;background:#F8FAFC;color:#08285E;font-size:13px;font-weight:600;padding:8px 12px;text-align:left;">{h}</th>' for h in headers])
        tr_rows = []
        for r in rows:
            td_cells = "".join([f'<td style="border:1px solid #E2E8F0;font-size:12.5px;color:#334155;padding:8px 12px;">{cell}</td>' for cell in r])
            tr_rows.append(f'<tr>{td_cells}</tr>')
        tbody_html = "".join(tr_rows)
        return f"""
  <!-- 表格 -->
  <section style="margin:16px 22px;overflow-x:auto;box-sizing:border-box;">
    <table style="width:100%;border-collapse:collapse;border:1px solid #E2E8F0;text-align:left;">
      <thead><tr>{th_cells}</tr></thead>
      <tbody>{tbody_html}</tbody>
    </table>
  </section>"""

    def render_hr(self):
        return """
  <section style="text-align:center;margin:28px 22px;line-height:0;box-sizing:border-box;">
    <section style="display:inline-block;width:30px;height:1px;background:#E2E8F0;"><span leaf=""><br/></span></section>
  </section>"""

    def render_footer(self, author="AI 工作台", note=""):
        return f"""
  <section style="text-align:center;margin:32px 22px 18px;line-height:0;box-sizing:border-box;">
    <section style="display:inline-block;width:30px;height:1px;background:#CBD5E1;"><span leaf=""><br/></span></section>
  </section>
  <section style="text-align:center;color:rgb(28,28,28);font-size:12px;font-family:PingFangSC-light;padding:0px 22px;line-height:1.75;margin:16px 0px 24px;box-sizing:border-box;">
    <p style="margin:0px;padding:0px;font-weight:500;color:#08285E;box-sizing:border-box;"><span leaf="">编辑 / 整理：{author}</span></p>
    {f'<p style="margin:4px 0px 0px;padding:0px;color:#888888;font-size:11.5px;box-sizing:border-box;"><span leaf="">{note}</span></p>' if note else ''}
  </section>"""


class EditorialStyle(BaseStyle):
    name = "editorial"
    display_name = "Editorial 先锋大刊风"

    def render_h2(self, idx, text):
        num_str = f"{idx:02d}"
        parts = re.split(r'[:：，,]', text, maxsplit=1)
        main_h = parts[0].strip()
        sub_h = parts[1].strip() if len(parts) > 1 else ""
        
        title_b64 = render_editorial_title_png(num_str, main_h, sub_h)
        if title_b64:
            return f"""
  <!-- 章节标题：Retina 级渐变水印图层 -->
  <section style="text-align:center;margin:36px 0 14px;line-height:0;box-sizing:border-box;">
    <img src="{title_b64}" style="vertical-align:middle;max-width:100%;width:100%;box-sizing:border-box;display:block;margin:0 auto;" alt="PART {num_str} {main_h}"/>
  </section>"""
        return super().render_h2(idx, text)

    def render_image(self, b64_or_src, caption=""):
        caption_html = f"""
  <section style="text-align:center;margin:0 0 20px;line-height:1.5;box-sizing:border-box;padding:0 22px;">
    <p style="margin:4px 0 0;font-size:12px;color:#888888;font-family:PingFangSC-light;"><span leaf="">{caption}</span></p>
  </section>""" if caption else '<section style="margin-bottom:14px;"></section>'
        
        return f"""
  <!-- 动效/截图容器：88% 留白，带微阴影与圆角 -->
  <section style="text-align:center;margin:18px 0 8px;line-height:0;width:100%;box-sizing:border-box;">
    <section style="max-width:100%;vertical-align:middle;display:inline-block;width:88%;height:auto;box-sizing:border-box;">
      <img src="{b64_or_src}" style="vertical-align:middle;max-width:100%;width:100%;box-sizing:border-box;display:block;border-radius:4px;box-shadow:0 2px 10px rgba(0,0,0,0.05);" alt="{caption}"/>
    </section>
  </section>{caption_html}"""


# 注册内置风格（对外仅展示正式风格）
STYLES_REGISTRY = {
    "editorial": EditorialStyle(),
}

# 兼容别名映射（静默兼容，不对外作为独立风格暴露）
STYLE_ALIASES = {
    "dakan": "editorial",
    "base": "editorial",
}

def load_external_styles():
    """动态扫描并加载 styles/ 目录下的自定义风格扩展（如由 sqsl-style-cloner 生成的风格）"""
    import importlib.util
    styles_dirs = [
        Path(__file__).resolve().parent.parent / "styles",
        Path.cwd() / "styles"
    ]
    for s_dir in styles_dirs:
        if not s_dir.exists():
            continue
        for p in s_dir.glob("*.py"):
            if p.name.startswith("__"):
                continue
            try:
                spec = importlib.util.spec_from_file_location(p.stem, str(p))
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if hasattr(mod, "STYLE_INSTANCE"):
                        inst = mod.STYLE_INSTANCE
                        STYLES_REGISTRY[inst.name.lower()] = inst
                    for attr_name in dir(mod):
                        attr = getattr(mod, attr_name)
                        if isinstance(attr, type) and issubclass(attr, BaseStyle) and attr not in (BaseStyle, EditorialStyle):
                            inst = attr()
                            STYLES_REGISTRY[inst.name.lower()] = inst
            except Exception as e:
                pass

load_external_styles()

def get_style(style_name="editorial"):
    load_external_styles()
    key = style_name.lower()
    if key in STYLE_ALIASES:
        key = STYLE_ALIASES[key]
    return STYLES_REGISTRY.get(key, STYLES_REGISTRY["editorial"])


# ==============================================================================
# 3. Markdown 解析与渲染引擎
# ==============================================================================

def extract_first_image_from_md(md_content, base_dir=None):
    """
    扫描 Markdown 文本，提取第一张图片的路径/URL
    返回 (image_src, caption)
    """
    img_matches = re.findall(r'!\[(.*?)\]\((.*?)\)', md_content)
    if img_matches:
        caption, src = img_matches[0]
        src = src.strip()
        if base_dir and not src.startswith(("http://", "https://", "data:")):
            local_p = Path(base_dir) / src
            if local_p.exists():
                return str(local_p.resolve()), caption
        return src, caption
    return None, None

def format_inline_markdown(text, style=None):
    """格式化行内高亮、加粗、行内代码，完全对齐当前选定风格，严防蓝色污染"""
    s_name = getattr(style, 'name', '').lower() if style else ''

    if 'olive' in s_name:
        # 阿芋·草木山野生活大刊风专属内联样式：高雅黄绿高亮底、柔和炭黑加粗、暖米灰代码
        text = re.sub(r'==(.*?)==', r'<mark style="background:#E0DEA8;color:#000000;padding:2px 6px;border-radius:2px;font-weight:700;"><span leaf="">\1</span></mark>', text)
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:#000000;font-weight:700;"><span leaf="">\1</span></strong>', text)
        text = re.sub(r'`(.*?)`', r'<code style="background:#F7F6F3;color:#3E3E3E;padding:2px 6px;border-radius:3px;font-size:13px;font-family:ui-monospace,Menlo,monospace;"><span leaf="">\1</span></code>', text)
        return text

    bold_color = getattr(style, 'primary_color', '#08285E') if style else '#08285E'
    text = re.sub(r'==(.*?)==', r'<mark style="background:#FFF0E6;color:#EA580C;padding:1px 5px;border-radius:3px;font-weight:600;"><span leaf="">\1</span></mark>', text)
    text = re.sub(r'\*\*(.*?)\*\*', f'<strong style="color:{bold_color};font-weight:700;"><span leaf="">\\1</span></strong>', text)
    text = re.sub(r'`(.*?)`', f'<code style="background:#F0F4F8;color:{bold_color};padding:2px 6px;border-radius:3px;font-size:13px;font-family:ui-monospace,Menlo,monospace;"><span leaf="">\\1</span></code>', text)
    return text

def render_markdown_to_wechat_html(md_file_path, out_html_path, out_preview_path=None, style_name="editorial", tag=""):
    md_file = Path(md_file_path).resolve()
    base_dir = md_file.parent
    
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    style = get_style(style_name)

    def img_to_b64(rel_p):
        full_p = (base_dir / rel_p).resolve()
        if not full_p.exists():
            if Path(rel_p).exists():
                full_p = Path(rel_p).resolve()
            else:
                return rel_p
        with open(full_p, "rb") as img_f:
            ext = full_p.suffix.lower().replace(".", "")
            mime = "image/gif" if ext == "gif" else ("image/png" if ext == "png" else "image/jpeg")
            return f"data:{mime};base64,{base64.b64encode(img_f.read()).decode('utf-8')}"

    lines = content.splitlines()
    title = md_file.stem
    chapter_idx = 0
    sections = [style.render_doc_start()]

    in_code_block = False
    code_lang = ""
    code_lines = []

    in_callout = False
    callout_lines = []

    in_table = False
    table_headers = []
    table_rows = []

    i = 0
    while i < len(lines):
        line = lines[i]
        raw = line.rstrip("\r\n")

        # 1. 代码块处理
        if raw.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lang = raw[3:].strip()
                code_lines = []
            else:
                in_code_block = False
                sections.append(style.render_code_block("\n".join(code_lines), code_lang))
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(raw)
            i += 1
            continue

        # 2. 表格处理
        if "|" in raw and not in_callout:
            if not in_table:
                # 检查下一行是否是分隔行 |---|---|
                if i + 1 < len(lines) and re.match(r'^\s*\|?\s*[-:]+[-| :]*\s*\|?\s*$', lines[i+1]):
                    in_table = True
                    table_headers = [c.strip() for c in raw.strip().strip("|").split("|")]
                    i += 2  # 跳过表头和分隔线
                    continue
            else:
                cells = [format_inline_markdown(c.strip(), style=style) for c in raw.strip().strip("|").split("|")]
                table_rows.append(cells)
                i += 1
                continue
        elif in_table:
            in_table = False
            sections.append(style.render_table(table_headers, table_rows))
            table_headers = []
            table_rows = []
            # 继续处理当前行，不 continue

        # 3. 引用块 / Callout 处理
        if raw.startswith("> "):
            callout_text = raw[2:].strip()
            callout_lines.append(callout_text)
            in_callout = True
            i += 1
            continue
        elif in_callout:
            in_callout = False
            full_callout = "<br/>".join(callout_lines)
            full_callout = format_inline_markdown(full_callout, style=style)
            callout_lines = []
            sections.append(style.render_callout(full_callout))

        # 4. H1 主标题
        if raw.startswith("# "):
            title = raw[2:].strip()
            sections.append(style.render_h1(title, tag=tag))
            i += 1
            continue

        # 5. H2 章节标题
        if raw.startswith("## "):
            chapter_idx += 1
            h2_text = raw[3:].strip()
            sections.append(style.render_h2(chapter_idx, h2_text))
            i += 1
            continue

        # 6. H3 小标题
        if raw.startswith("### "):
            h3_text = raw[4:].strip()
            is_highlight = '==highlight==' in h3_text or '{color="orange"}' in h3_text or '【核心】' in h3_text
            h3_clean = h3_text.replace('==highlight==', '').replace('{color="orange"}', '').replace('【核心】', '').strip()
            sections.append(style.render_h3(h3_clean, is_highlight=is_highlight))
            i += 1
            continue

        # 7. 分割线
        if raw.strip() in ("---", "***", "___"):
            sections.append(style.render_hr())
            i += 1
            continue

        # 8. 插图
        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', raw.strip())
        if img_match:
            caption = img_match.group(1)
            b64_src = img_to_b64(img_match.group(2))
            sections.append(style.render_image(b64_src, caption))
            i += 1
            continue

        # 9. 无序列表与有序列表
        list_match = re.match(r'^(\s*)([-*]|\d+\.)\s+(.+)$', raw)
        if list_match:
            marker = list_match.group(2)
            is_ordered = marker[0].isdigit()
            num = int(marker.replace(".", "")) if is_ordered else 1
            item_text = format_inline_markdown(list_match.group(3).strip(), style=style)
            sections.append(style.render_list_item(item_text, is_ordered=is_ordered, num=num))
            i += 1
            continue

        # 10. 普通段落
        if not raw.strip():
            i += 1
            continue

        p_text = format_inline_markdown(raw.strip(), style=style)
        sections.append(style.render_paragraph(p_text))
        i += 1

    # 处理收尾未闭合块
    if in_callout:
        full_callout = format_inline_markdown("<br/>".join(callout_lines), style=style)
        sections.append(style.render_callout(full_callout))
    if in_table:
        sections.append(style.render_table(table_headers, table_rows))

    sections.append(style.render_footer())
    sections.append("</section>")

    final_html = "\n".join(sections)
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    # 生成带一键复制的预览 HTML
    if out_preview_path:
        s_lower = style_name.lower()
        if 'olive' in s_lower:
            bar_bg = "rgba(46, 46, 46, 0.96)"
            bar_shadow = "0 8px 24px rgba(0,0,0,0.2)"
            btn_bg = "#E0DEA8"
            btn_color = "#000000"
            btn_hover = "#CECB92"
        elif 'editorial' in s_lower:
            bar_bg = "rgba(8, 40, 94, 0.95)"
            bar_shadow = "0 8px 24px rgba(8,40,94,0.25)"
            btn_bg = "#FFFFFF"
            btn_color = "#08285E"
            btn_hover = "#DBE7F6"
        else:
            bar_bg = "rgba(40, 40, 40, 0.95)"
            bar_shadow = "0 8px 24px rgba(0,0,0,0.2)"
            btn_bg = "#FFFFFF"
            btn_color = "#1A1A1A"
            btn_hover = "#E5E5E5"

        preview_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 微信排版预览 ({style.display_name})</title>
<style>
  body {{
    background: #eef2f7;
    margin: 0;
    padding: 20px 10px 60px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .toolbar {{
    position: sticky;
    top: 15px;
    z-index: 1000;
    margin-bottom: 20px;
    background: {bar_bg};
    backdrop-filter: blur(10px);
    padding: 10px 22px;
    border-radius: 30px;
    box-shadow: {bar_shadow};
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .toolbar span {{
    color: #fff;
    font-size: 13px;
    font-weight: 500;
    font-family: -apple-system, sans-serif;
  }}
  .copy-btn {{
    background: {btn_bg};
    color: {btn_color};
    border: none;
    padding: 8px 18px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .copy-btn:hover {{
    background: {btn_hover};
    transform: scale(1.04);
  }}
  .article-card {{
    background: #fff;
    max-width: 677px;
    width: 100%;
    box-shadow: 0 4px 30px rgba(0,0,0,0.06);
    border-radius: 8px;
    overflow: hidden;
  }}
</style>
</head>
<body>
  <div class="toolbar">
    <span>✨ 当前风格：{style.display_name}</span>
    <button class="copy-btn" onclick="copyContent()">一键复制到公众号</button>
  </div>
  <div class="article-card" id="article-root">
    {final_html}
  </div>

  <script>
    function copyContent() {{
      const root = document.getElementById('article-root');
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(root);
      selection.removeAllRanges();
      selection.addRange(range);
      try {{
        document.execCommand('copy');
        const btn = document.querySelector('.copy-btn');
        btn.innerText = '✅ 已成功复制！';
        btn.style.background = '#059669';
        btn.style.color = '#fff';
        setTimeout(() => {{
          btn.innerText = '一键复制到公众号';
          btn.style.background = '{btn_bg}';
          btn.style.color = '{btn_color}';
        }}, 2500);
      }} catch (err) {{
        alert('复制失败，请手动 Ctrl+A / ⌘+A 全选复制');
      }}
      selection.removeAllRanges();
    }}
  </script>
</body>
</html>"""
        with open(out_preview_path, "w", encoding="utf-8") as f:
            f.write(preview_doc)

    return out_html_path, out_preview_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Render Markdown to WeChat Formatted HTML with multiple styles")
    parser.add_argument("markdown_file", help="Input Markdown file path")
    parser.add_argument("--output-html", help="Output HTML file path")
    parser.add_argument("--output-preview", help="Output Preview HTML file path")
    parser.add_argument("--style", default="editorial", choices=list(STYLES_REGISTRY.keys()), help="Style name (default: editorial)")
    parser.add_argument("--tag", default="", help="Header category tag")
    args = parser.parse_args()

    in_md = Path(args.markdown_file).resolve()
    base_stem = in_md.stem
    out_dir = in_md.parent

    out_html = Path(args.output_html).resolve() if args.output_html else out_dir / f"{base_stem}_微信排版.html"
    out_prev = Path(args.output_preview).resolve() if args.output_preview else out_dir / f"{base_stem}_预览.html"

    print(f"正在以 [{args.style}] 风格排版：{in_md}")
    render_markdown_to_wechat_html(in_md, out_html, out_prev, style_name=args.style, tag=args.tag)
    print(f"✅ 排版生成完成：\n- HTML 文件: {out_html}\n- 预览文件: {out_prev}")
