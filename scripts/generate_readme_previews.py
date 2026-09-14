#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/liguiyu/Documents/myCreation/skills/sqsl-wechat-skill")
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

STYLES_INFO = [
    {
        "id": "editorial",
        "title": "Editorial · 先锋大刊风",
        "badge": "官方核心风格",
        "badge_color": "#93C5FD",
        "badge_bg": "rgba(37, 99, 235, 0.25)",
        "badge_border": "rgba(147, 197, 253, 0.4)",
        "header_bg": "linear-gradient(135deg, #08285E 0%, #153E7E 100%)",
        "wrapper_bg": "#EEF2F7",
        "desc": "Didot 艺术大水印 · 宋体高对比中文 · 88% 黄金留白 · 经典墨蓝先锋调性",
        "card_bg": "#FFFFFF",
        "height": 1380
    },
    {
        "id": "olive_artisan",
        "title": "阿芋 · 草木山野生活风",
        "badge": "生活美学大刊",
        "badge_color": "#E5E3B3",
        "badge_bg": "rgba(176, 172, 114, 0.25)",
        "badge_border": "rgba(229, 227, 179, 0.4)",
        "header_bg": "linear-gradient(135deg, #2B2F23 0%, #3C4232 100%)",
        "wrapper_bg": "#F4F3EE",
        "desc": "Bodoni 粗斜体艺术大数字 · 黄绿胶带高亮大标题 · 燕麦米灰软卡片 · 1.8 呼吸行高",
        "card_bg": "#FFFFFF",
        "height": 1420
    }
]

def main():
    assets_dir = BASE_DIR / "assets"
    assets_dir.mkdir(exist_ok=True)
    tmp_dir = Path("/tmp/sqsl_readme_previews")
    tmp_dir.mkdir(exist_ok=True)

    sample_md = BASE_DIR / "skills/sqsl-article-to-wechat/examples/sample_editorial_article.md"
    render_script = BASE_DIR / "skills/sqsl-article-to-wechat/scripts/render_wechat_html.py"

    for style_cfg in STYLES_INFO:
        s_id = style_cfg["id"]
        out_html = tmp_dir / f"article_{s_id}.html"
        out_preview = tmp_dir / f"preview_{s_id}.html"
        
        print(f"--> 渲染 [{s_id}] 风格 HTML...")
        render_cmd = [
            "python3",
            str(render_script),
            str(sample_md),
            "--style", s_id,
            "--output-html", str(out_html),
            "--output-preview", str(out_preview)
        ]
        subprocess.run(render_cmd, check=True)

        with open(out_html, "r", encoding="utf-8") as f:
            article_body = f.read()

        # 生成精美展示容器
        showcase_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: {style_cfg["wrapper_bg"]};
    padding: 30px;
    display: flex;
    justify-content: center;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", sans-serif;
  }}
  .preview-wrapper {{
    width: 680px;
    background: {style_cfg["card_bg"]};
    border-radius: 18px;
    box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.12), 0 0 0 1px rgba(15, 23, 42, 0.05);
    overflow: hidden;
  }}
  .preview-header {{
    background: {style_cfg["header_bg"]};
    padding: 16px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }}
  .window-dots {{
    display: flex;
    gap: 7px;
    width: 50px;
  }}
  .dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }}
  .dot-red {{ background: #EF4444; }}
  .dot-yellow {{ background: #F59E0B; }}
  .dot-green {{ background: #10B981; }}
  .header-badge {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .badge-title {{
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}
  .badge-tag {{
    background: {style_cfg["badge_bg"]};
    color: {style_cfg["badge_color"]};
    border: 1px solid {style_cfg["badge_border"]};
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
  }}
  .header-meta {{
    font-size: 11.5px;
    color: rgba(255,255,255,0.6);
    font-weight: 500;
  }}
  .preview-content {{
    padding: 22px 14px 40px;
    background: {style_cfg["card_bg"]};
  }}
</style>
</head>
<body>
  <div class="preview-wrapper">
    <div class="preview-header">
      <div class="window-dots">
        <div class="dot dot-red"></div>
        <div class="dot dot-yellow"></div>
        <div class="dot dot-green"></div>
      </div>
      <div class="header-badge">
        <span class="badge-title">{style_cfg["title"]}</span>
        <span class="badge-tag">{style_cfg["badge"]}</span>
      </div>
      <div class="header-meta">WeChat Render</div>
    </div>
    <div class="preview-content">
      {article_body}
    </div>
  </div>
</body>
</html>"""

        showcase_file = tmp_dir / f"showcase_{s_id}.html"
        with open(showcase_file, "w", encoding="utf-8") as f:
            f.write(showcase_html)

        out_png = assets_dir / f"preview_{s_id}.png"
        print(f"--> 正在截图生成: {out_png.name}...")
        shot_cmd = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            f"--window-size=740,{style_cfg['height']}",
            "--device-scale-factor=2",
            f"--screenshot={out_png}",
            str(showcase_file)
        ]
        subprocess.run(shot_cmd, check=True)
        print(f"✅ 生成成功: {out_png} ({os.path.getsize(out_png):,} bytes)")

if __name__ == "__main__":
    main()
