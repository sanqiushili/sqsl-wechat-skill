#!/usr/bin/env python3
"""
clone_wechat_style.py - 微信公众号文章排版风格逆向与克隆引擎

功能：
1. 抓取微信公众号文章 URL (https://mp.weixin.qq.com/s/...) 或解析本地 HTML；
2. 提取其视觉设计系统（主色调、强调色、引言卡片、段落行高、标题边框、列表样式等）；
3. 自动生成兼容 sqsl-article-to-wechat 排版引擎的标准 Python 风格模块；
4. 输出风格视觉规范报告与组件预览 HTML。
"""

import os
import sys
import re
import json
import urllib.request
from pathlib import Path
from collections import Counter

DEFAULT_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch_wechat_article_html(url_or_path):
    """获取公众号文章 HTML 内容"""
    if url_or_path.startswith(("http://", "https://")):
        print(f"1. 正在抓取公众号文章: {url_or_path}...")
        req = urllib.request.Request(url_or_path, headers={"User-Agent": DEFAULT_UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw_html = resp.read().decode("utf-8", errors="ignore")
        return raw_html
    else:
        local_p = Path(url_or_path).resolve()
        if not local_p.exists():
            raise FileNotFoundError(f"找不到本地文件: {url_or_path}")
        with open(local_p, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def normalize_hex_color(col):
    """归一化颜色为标准大写 6 位 Hex"""
    col = col.strip().lower()
    if col.startswith("rgb"):
        nums = re.findall(r'\d+', col)
        if len(nums) >= 3:
            r, g, b = int(nums[0]), int(nums[1]), int(nums[2])
            return f"#{r:02X}{g:02X}{b:02X}"
    elif col.startswith("#"):
        col = col.replace("#", "")
        if len(col) == 3:
            col = "".join([c*2 for c in col])
        if len(col) == 6:
            return f"#{col.upper()}"
    return None

def analyze_visual_dna(html_content):
    """
    对公众号正文 (#js_content) 进行视觉逆向分析
    提取核心调色板与关键组件模式
    """
    # 提取文章标题
    title_match = re.search(r'<h1[^>]*class="[^"]*rich_media_title[^"]*"[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    if not title_match:
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    article_title = title_match.group(1).strip() if title_match else "未命名公众号文章"
    article_title = re.sub(r'<[^>]+>', '', article_title).strip()

    # 提取正文容器
    content_match = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*(?:<div|<!--|$)', html_content, re.DOTALL)
    body_html = content_match.group(1) if content_match else html_content

    # 1. 色彩收集器
    all_colors = []
    
    # 提取所有 color 声明
    text_colors = re.findall(r'(?:^|;|\s)color\s*:\s*([^;"]+)', body_html, re.IGNORECASE)
    for c in text_colors:
        hex_c = normalize_hex_color(c)
        if hex_c:
            all_colors.append(hex_c)
            
    # 提取所有 background 声明
    bg_colors = re.findall(r'(?:^|;|\s)background(?:-color)?\s*:\s*([^;"]+)', body_html, re.IGNORECASE)
    for c in bg_colors:
        hex_c = normalize_hex_color(c)
        if hex_c:
            all_colors.append(hex_c)

    # 提取 border 声明
    border_colors = re.findall(r'(?:^|;|\s)border(?:-[a-z]+)?\s*:\s*[^;"]*(#[0-9a-fA-F]{3,6}|rgba?\([^)]+\))', body_html, re.IGNORECASE)
    for c in border_colors:
        hex_c = normalize_hex_color(c)
        if hex_c:
            all_colors.append(hex_c)

    color_counts = Counter(all_colors)

    # 排除黑白灰等中性背景
    neutral_colors = {"#FFFFFF", "#000000", "#333333", "#222222", "#111111", "#CCCCCC", "#EEEEEE", "#F7F7F7", "#FAFAFA"}
    meaningful_colors = [c for c, count in color_counts.most_common() if c not in neutral_colors]

    # 智能判定：主品牌色、强调色（中性色兜底，绝不硬编码任何外来蓝）
    primary_color = meaningful_colors[0] if len(meaningful_colors) > 0 else "#2B2B2B"
    accent_color = meaningful_colors[1] if len(meaningful_colors) > 1 else primary_color
    
    # 正文文字颜色
    body_text_color = "#3E3E3E"
    for c, _ in color_counts.most_common():
        if c in ("#333333", "#2B2B2B", "#1C1C1C", "#262626", "#3E3E3E", "#3B3B3B"):
            body_text_color = c
            break

    # 2. 章节大标题与胶带高亮底色探测 (Tape/Highlighter)
    heading_tape_match = re.search(r'<span[^>]*background(?:-color)?\s*:\s*([^;"]+)[^>]*font-weight\s*:\s*bold[^>]*>', body_html, re.IGNORECASE)
    highlight_tape = normalize_hex_color(heading_tape_match.group(1)) if heading_tape_match else accent_color

    # 3. 序号图片化探测 (检查标题周围是否有艺术数字小装饰图)
    has_graphic_numbers = bool(re.search(r'<img[^>]*style="[^"]*width:\s*1\d\dpx[^"]*"[^>]*>', body_html, re.IGNORECASE))

    # 4. 引用块 / Callout / 表面卡片检测
    card_bg_match = re.search(r'background(?:-color)?\s*:\s*(rgb\(\s*24\d\s*,\s*24\d\s*,\s*24\d\s*\)|#[fF][4-7][fF][4-7][fF][0-7])', body_html)
    card_bg = normalize_hex_color(card_bg_match.group(1)) if card_bg_match else "#F7F6F3"

    callout_match = re.search(r'(?:border-left|border)\s*:\s*(\d+px)\s+solid\s+([^;"]+)[^>]*background(?:-color)?\s*:\s*([^;"]+)', body_html, re.IGNORECASE)
    if callout_match:
        b_color = normalize_hex_color(callout_match.group(2)) or primary_color
        bg_col = normalize_hex_color(callout_match.group(3)) or card_bg
    else:
        b_color = accent_color
        bg_col = card_bg

    return {
        "article_title": article_title,
        "primary_color": primary_color,
        "accent_color": accent_color,
        "text_color": body_text_color,
        "bg_color": "#FFFFFF",
        "highlight_tape": highlight_tape,
        "has_graphic_numbers": has_graphic_numbers,
        "callout_border": b_color,
        "callout_bg": bg_col,
        "all_extracted_colors": [c for c, _ in color_counts.most_common(10)]
    }

def generate_style_module(style_name, display_name, visual_dna, out_path):
    """套用模板生成 Python 风格模块"""
    tpl_path = Path(__file__).resolve().parent.parent / "templates" / "style_template.py"
    with open(tpl_path, "r", encoding="utf-8") as f:
        tpl = f.read()

    class_name = re.sub(r'[^a-zA-Z0-9_]', '', style_name.capitalize())

    content = tpl.replace("{{STYLE_NAME}}", style_name) \
                 .replace("{{STYLE_DISPLAY_NAME}}", display_name) \
                 .replace("{{STYLE_CLASS_NAME}}", class_name) \
                 .replace("{{PRIMARY_COLOR}}", visual_dna["primary_color"]) \
                 .replace("{{ACCENT_COLOR}}", visual_dna["accent_color"]) \
                 .replace("{{TEXT_COLOR}}", visual_dna["text_color"]) \
                 .replace("{{BG_COLOR}}", visual_dna["bg_color"]) \
                 .replace("{{CALLOUT_BG}}", visual_dna["callout_bg"]) \
                 .replace("{{CALLOUT_BORDER}}", visual_dna["callout_border"])

    out_file = Path(out_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    return out_file

def generate_style_spec_preview(style_name, display_name, visual_dna, out_preview_path):
    """生成克隆风格的视觉规范预览网页"""
    p_col = visual_dna["primary_color"]
    a_col = visual_dna["accent_color"]
    t_col = visual_dna["text_color"]
    c_bg = visual_dna["callout_bg"]
    c_bd = visual_dna["callout_border"]

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{display_name} ({style_name}) - 风格克隆规范预览</title>
<style>
  body {{
    background: #F1F5F9;
    margin: 0;
    padding: 30px 15px 80px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .spec-header {{
    max-width: 677px;
    width: 100%;
    background: #FFFFFF;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    box-sizing: border-box;
  }}
  .title {{
    font-size: 20px;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 16px;
  }}
  .swatches {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 12px;
  }}
  .swatch {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 6px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    font-size: 13px;
    font-family: ui-monospace, Menlo, monospace;
  }}
  .swatch-color {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid rgba(0,0,0,0.1);
  }}
  .preview-card {{
    background: #FFFFFF;
    max-width: 677px;
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 30px rgba(0,0,0,0.06);
  }}
</style>
</head>
<body>
  <div class="spec-header">
    <div class="title">🎨 风格克隆成功：{display_name} (<code>{style_name}</code>)</div>
    <div class="swatches">
      <div class="swatch"><div class="swatch-color" style="background:{p_col};"></div>主标题色: {p_col}</div>
      <div class="swatch"><div class="swatch-color" style="background:{a_col};"></div>强调点缀: {a_col}</div>
      <div class="swatch"><div class="swatch-color" style="background:{t_col};"></div>正文字体: {t_col}</div>
      <div class="swatch"><div class="swatch-color" style="background:{c_bg};border-color:{c_bd};"></div>引言卡片底色: {c_bg}</div>
    </div>
    <p style="margin:8px 0 0;font-size:13px;color:#64748B;">此风格已自动注册到 <code>sqsl-article-to-wechat</code> 风格池中，排版时可直接传入 <code>--style {style_name}</code> 使用。</p>
  </div>

  <div class="preview-card">
    <section style="max-width:677px;margin:0 auto;background:#FFFFFF;font-family:PingFangSC-light,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:{t_col};line-height:1.75;letter-spacing:0.3px;box-sizing:border-box;">
      <section style="padding:28px 22px 14px;text-align:center;box-sizing:border-box;">
        <p style="font-size:11px;font-weight:700;color:{a_col};letter-spacing:2.5px;margin:0 0 10px;text-transform:uppercase;">STYLE SHOWCASE</p>
        <p style="font-size:24px;font-weight:700;line-height:1.35;color:{p_col};margin:0 0 12px;letter-spacing:1px;">这是一篇使用克隆新风格渲染的排版示范</p>
      </section>
      <section style="text-align:center;margin:6px 0 24px;line-height:0;box-sizing:border-box;">
        <section style="display:inline-block;width:36px;height:2px;background:{p_col};"><br/></section>
      </section>

      <section style="background:{c_bg};border-left:3px solid {c_bd};padding:14px 18px;margin:18px 22px;border-radius:0 4px 4px 0;box-sizing:border-box;">
        <p style="margin:0;font-size:13.5px;color:{p_col};line-height:1.65;text-align:justify;">这是自动提取并重构的引用强调卡片（Callout），色调与原文边框、背景高度一致。</p>
      </section>

      <section style="margin:28px 22px 14px;box-sizing:border-box;">
        <p style="font-size:18px;font-weight:700;color:{p_col};margin:0;padding-left:10px;border-left:4px solid {p_col};line-height:1.4;">
          <span style="color:{a_col};margin-right:6px;font-family:ui-monospace,Menlo,monospace;">01</span>章节大标题样式示范
        </p>
      </section>

      <section style="font-size:14px;font-family:PingFangSC-light;padding:0px 22px;line-height:1.75;box-sizing:border-box;margin:12px 0;">
        <p style="white-space:normal;margin:0px;padding:0px;box-sizing:border-box;text-align:justify;">
          正文段落排版效果，字阶设置为 14px，行高 1.75。通过对目标文章的 CSS 提取，主色与装饰均已对齐。
        </p>
      </section>

      <section style="padding:14px 22px 6px;box-sizing:border-box;">
        <p style="font-size:16px;font-weight:700;line-height:1.4;color:{p_col};margin:0;letter-spacing:0.5px;">
          子小标题演示
          <span style="background:#FFF0E6;color:{a_col};padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;margin-left:8px;vertical-align:middle;display:inline-block;">重点标记</span>
        </p>
      </section>

      <section style="font-size:14px;font-family:PingFangSC-light;padding:3px 22px 3px 36px;line-height:1.75;box-sizing:border-box;position:relative;">
        <p style="white-space:normal;margin:0px;padding:0px;box-sizing:border-box;text-align:justify;">
          <span style="position:absolute;left:22px;color:{p_col};font-weight:bold;">•</span>列表项点缀颜色自动匹配主色调；
        </p>
      </section>
      <section style="font-size:14px;font-family:PingFangSC-light;padding:3px 22px 3px 36px;line-height:1.75;box-sizing:border-box;position:relative;">
        <p style="white-space:normal;margin:0px;padding:0px;box-sizing:border-box;text-align:justify;">
          <span style="position:absolute;left:22px;color:{p_col};font-weight:bold;">•</span>结构清晰，便于随时调用。
        </p>
      </section>
    </section>
  </div>
</body>
</html>"""
    out_file = Path(out_preview_path).resolve()
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    return out_file

def clone_style(input_source, style_name=None, display_name=None, export_to_typesetter=True):
    raw_html = fetch_wechat_article_html(input_source)
    print("2. 正在进行视觉 DNA 逆向分析...")
    visual_dna = analyze_visual_dna(raw_html)

    if not style_name:
        # 生成默认英文名
        style_name = "cloned_" + re.sub(r'[^a-zA-Z0-9]', '_', visual_dna["primary_color"].replace("#", "").lower())[:8]
    if not display_name:
        display_name = f"复刻风格_{visual_dna['article_title'][:8]}"

    print(f"  ✓ 提取到主色调: {visual_dna['primary_color']}")
    print(f"  ✓ 提取到点缀色: {visual_dna['accent_color']}")
    print(f"  ✓ 提取到引言卡: 背景 {visual_dna['callout_bg']}, 边框 {visual_dna['callout_border']}")

    # 1. 导出到 sqsl-article-to-wechat/styles/（如果存在）
    typesetter_styles_dirs = [
        Path(__file__).resolve().parent.parent.parent / "sqsl-article-to-wechat" / "styles",
        Path.home() / ".gemini" / "config" / "skills" / "sqsl-article-to-wechat" / "styles"
    ]
    
    exported_files = []
    if export_to_typesetter:
        for t_dir in typesetter_styles_dirs:
            if t_dir.parent.exists():
                t_dir.mkdir(parents=True, exist_ok=True)
                target_py = t_dir / f"style_{style_name}.py"
                generate_style_module(style_name, display_name, visual_dna, target_py)
                exported_files.append(target_py)
                print(f"3. 成功注册到排版引擎风格池: {target_py}")

    # 2. 生成当前目录的展示模块与预览页
    local_output_dir = Path.cwd() / "output" if not Path("styles").exists() else Path.cwd() / "styles"
    local_output_dir.mkdir(parents=True, exist_ok=True)
    local_py = local_output_dir / f"style_{style_name}.py"
    generate_style_module(style_name, display_name, visual_dna, local_py)

    preview_html = local_output_dir / f"{style_name}_风格预览.html"
    generate_style_spec_preview(style_name, display_name, visual_dna, preview_html)
    print(f"4. 生成风格视觉预览页: {preview_html}")

    return {
        "style_name": style_name,
        "display_name": display_name,
        "visual_dna": visual_dna,
        "style_py": local_py,
        "preview_html": preview_html,
        "exported_files": exported_files
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clone WeChat Official Account article typesetting style")
    parser.add_argument("input_source", help="WeChat article URL or local HTML file path")
    parser.add_argument("--name", help="Style identifier slug (e.g. tech_blue)")
    parser.add_argument("--display-name", help="Display name for human (e.g. 极客蓝调大刊)")
    args = parser.parse_args()

    try:
        clone_style(args.input_source, style_name=args.name, display_name=args.display_name)
    except Exception as e:
        print(f"❌ 克隆失败: {e}", file=sys.stderr)
        sys.exit(1)
