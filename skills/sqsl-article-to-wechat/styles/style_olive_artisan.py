# -*- coding: utf-8 -*-
"""
style_olive_artisan.py - 阿芋·草木山野手作与生活大刊风 (Voicer Lifestyle Style)
基于《重访阿芋：是制帽师，也是山野里的自在风》官方排版系统 100% 深度复刻：
1. 章节序号图片化：01/02/03 采用 Bodoni/Didot 艺术高反差斜体数字与极简柔光椭圆背景；
2. 章节大标题：居中黄色高亮胶带底衬（#E0DEA8）+ Optima/苹方粗体（#000000），两端带 2px 字间距；
3. 引言/重点卡：温润燕麦米灰（#F7F6F3）浅色大卡片，呼吸留白；
4. 调色板：纯正草木橄榄绿（#A7A56D）用于徽章与圆点，柔和炭黑（#3E3E3E）正文，杜绝一切无关生硬蓝色！
"""

import re
import html
import subprocess
import tempfile
from pathlib import Path

STYLE_NAME = "olive_artisan"
STYLE_DISPLAY_NAME = "阿芋·草木山野生活风"

B64_NUM_CACHE = {
    1: "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",
    2: "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",
    3: "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"
}

def get_chapter_number_b64(idx):
    """获取或动态渲染章节艺术数字图片（512x359 Retina 居中椭圆底衬图）"""
    if idx in B64_NUM_CACHE:
        return "data:image/png;base64," + B64_NUM_CACHE[idx]
    
    # 动态渲染 04 及以上数字
    try:
        num_str = f"{idx:02d}"
        html_tpl = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 512px; height: 359px; background: transparent;
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
}}
.oval {{
  position: absolute; width: 490px; height: 330px;
  background: #F7F6F3;
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  transform: rotate(-10deg);
}}
.text {{
  position: relative; z-index: 2;
  font-family: "Bodoni 72", "Didot", "Playfair Display", Georgia, serif;
  font-size: 270px; font-weight: 900; color: #000;
  letter-spacing: -12px; line-height: 1;
  display: flex; align-items: center; justify-content: center;
  margin-top: -15px;
}}
.d0 {{
  transform: rotate(-18deg) scaleX(0.88);
  display: inline-block; margin-right: 12px;
}}
.dn {{
  display: inline-block;
}}
</style></head>
<body>
<div class="oval"></div>
<div class="text"><span class="d0">{num_str[0]}</span><span class="dn">{num_str[1]}</span></div>
</body></html>"""
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(html_tpl)
            tmp_h = f.name
        tmp_png = tmp_h + ".png"
        chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        cmd = [
            chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
            "--window-size=512,359",
            f"--screenshot={tmp_png}",
            "--default-background-color=00000000",
            tmp_h
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(tmp_png, "rb") as pf:
            b64_val = base64.b64encode(pf.read()).decode("utf-8")
        B64_NUM_CACHE[idx] = b64_val
        Path(tmp_h).unlink(missing_ok=True)
        Path(tmp_png).unlink(missing_ok=True)
        return "data:image/png;base64," + b64_val
    except Exception:
        # 兜底返回 01
        return "data:image/png;base64," + B64_NUM_CACHE[1]


class ClonedStyle_Olive_artisan:
    name = "olive_artisan"
    display_name = "阿芋·草木山野生活风"
    
    def render_doc_start(self):
        return """<section style="max-width:677px;margin:0 auto;background:#FFFFFF;font-family:Optima-Regular,PingFangTC-light,PingFangSC-light,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#3E3E3E;line-height:1.8;letter-spacing:1.5px;box-sizing:border-box;">"""

    def render_h1(self, title, tag=""):
        tag_html = f'<p style="font-size:12px;font-weight:700;color:#A7A56D;letter-spacing:3px;margin:0 0 12px;text-transform:uppercase;text-align:center;"><span leaf="">{tag}</span></p>' if tag else ""
        return f"""
  <!-- 主标题 -->
  <section style="padding:36px 20px 14px;text-align:center;box-sizing:border-box;">
    {tag_html}
    <p style="font-size:22px;font-weight:bold;line-height:1.45;color:#2B2B2B;margin:0 0 16px;letter-spacing:1.5px;"><span leaf="">{title}</span></p>
  </section>
  <section style="text-align:center;margin:6px 0 28px;line-height:0;box-sizing:border-box;">
    <section style="display:inline-block;width:32px;height:1px;background:#D5D3C8;"><span leaf=""><br/></span></section>
  </section>"""

    def render_h2(self, idx, text):
        num_b64 = get_chapter_number_b64(idx)
        return f"""
  <!-- H2 章节标题（艺术序号图片 + 胶带高亮居中标题） -->
  <section style="margin:44px 0 20px;text-align:center;box-sizing:border-box;">
    <p style="margin:0 auto 12px;text-align:center;line-height:normal;">
      <img src="{num_b64}" style="width:134px;height:auto !important;display:inline-block;" alt="{idx:02d}" />
    </p>
    <p style="white-space:normal;text-align:center;margin:0 auto 16px;line-height:normal;">
      <span style="background-color:#E0DEA8;color:#000000;font-family:Optima-Regular,PingFangTC-light,-apple-system,sans-serif;font-size:18px;font-weight:bold;letter-spacing:2px;padding:3px 12px;display:inline-block;"><span leaf="">&nbsp;{text}&nbsp;</span></span>
    </p>
  </section>"""

    def render_h3(self, text, is_highlight=False):
        badge = f'<span style="background:#E0DEA8;color:#000000;padding:2px 8px;border-radius:3px;font-size:11px;font-weight:700;margin-left:8px;vertical-align:middle;display:inline-block;"><span leaf="">重点</span></span>' if is_highlight else ''
        return f"""
  <!-- H3 小标题 -->
  <section style="padding:18px 20px 8px;box-sizing:border-box;">
    <p style="font-size:16px;font-weight:bold;line-height:1.5;color:#2E2E2E;margin:0;letter-spacing:1.5px;">
      <span style="color:#A7A56D;margin-right:6px;">●</span><span leaf="">{text}</span>{badge}
    </p>
  </section>"""

    def render_callout(self, content):
        return f"""
  <!-- 燕麦暖灰引言大卡片 (Voicer Lifestyle Style) -->
  <section style="background:#F7F6F3;padding:22px 24px;margin:24px 18px;border-radius:4px;box-sizing:border-box;">
    <p style="margin:0;font-size:14.5px;color:#3B3B3B;line-height:1.85;letter-spacing:1.5px;text-align:justify;"><span leaf="">{content}</span></p>
  </section>"""

    def render_paragraph(self, content):
        return f"""
  <!-- 段落正文 -->
  <section style="font-size:15px;font-family:PingFangSC-light,PingFangTC-light;padding:0 20px;line-height:1.85;letter-spacing:1.5px;box-sizing:border-box;margin:16px 0;">
    <p style="white-space:normal;margin:0;padding:0;box-sizing:border-box;text-align:justify;"><span leaf="">{content}</span></p>
  </section>"""

    def render_list_item(self, content, is_ordered=False, num=1):
        bullet = f"{num}." if is_ordered else "●"
        bullet_color = "#3E3E3E" if is_ordered else "#A7A56D"
        return f"""
  <!-- 列表项 -->
  <section style="font-size:15px;font-family:PingFangSC-light,PingFangTC-light;padding:4px 20px 4px 38px;line-height:1.8;letter-spacing:1.2px;box-sizing:border-box;position:relative;">
    <p style="white-space:normal;margin:0;padding:0;box-sizing:border-box;text-align:justify;">
      <span style="position:absolute;left:20px;color:{bullet_color};font-weight:bold;">{bullet}</span><span leaf="">{content}</span>
    </p>
  </section>"""

    def render_image(self, b64_or_src, caption=""):
        caption_html = f"""
  <section style="text-align:center;margin:0 0 24px;line-height:1.5;box-sizing:border-box;padding:0 20px;">
    <p style="margin:6px 0 0;font-size:13px;color:#888888;font-family:PingFangSC-light;letter-spacing:1px;"><span style="color:#3E3E3E;margin-right:4px;">●</span><span leaf="">{caption}</span></p>
  </section>""" if caption else '<section style="margin-bottom:16px;"></section>'
        
        return f"""
  <!-- 插图卡片 -->
  <section style="text-align:center;margin:22px 0 8px;line-height:0;width:100%;box-sizing:border-box;">
    <section style="max-width:100%;vertical-align:middle;display:inline-block;width:92%;height:auto;box-sizing:border-box;">
      <img src="{b64_or_src}" style="vertical-align:middle;max-width:100%;width:100%;box-sizing:border-box;display:block;border-radius:4px;box-shadow:0 2px 12px rgba(0,0,0,0.04);" alt="{caption}"/>
    </section>
  </section>{caption_html}"""

    def render_code_block(self, code_text, lang=""):
        escaped_code = html.escape(code_text)
        return f"""
  <!-- 代码块 (柔和暖深炭灰，无生硬蓝) -->
  <section style="margin:18px 20px;border-radius:6px;background:#2B2B2B;padding:16px;box-sizing:border-box;overflow-x:auto;">
    <p style="margin:0 0 8px;font-size:11px;color:#A7A56D;font-family:ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:1px;">{lang or 'CODE'}</p>
    <pre style="margin:0;font-family:ui-monospace,Menlo,Monaco,Consolas,monospace;font-size:12.5px;color:#EDECE6;line-height:1.6;white-space:pre-wrap;word-break:break-all;"><code>{escaped_code}</code></pre>
  </section>"""

    def render_table(self, headers, rows):
        th_cells = "".join([f'<th style="border:1px solid #E5E3D8;background:#F7F6F3;color:#2B2B2B;font-size:13px;font-weight:600;padding:8px 12px;text-align:left;">{h}</th>' for h in headers])
        tr_rows = []
        for r in rows:
            td_cells = "".join([f'<td style="border:1px solid #E5E3D8;font-size:13px;color:#3E3E3E;padding:8px 12px;">{cell}</td>' for cell in r])
            tr_rows.append(f'<tr>{td_cells}</tr>')
        tbody_html = "".join(tr_rows)
        return f"""
  <!-- 表格 -->
  <section style="margin:18px 20px;overflow-x:auto;box-sizing:border-box;">
    <table style="width:100%;border-collapse:collapse;border:1px solid #E5E3D8;text-align:left;">
      <thead><tr>{th_cells}</tr></thead>
      <tbody>{tbody_html}</tbody>
    </table>
  </section>"""

    def render_hr(self):
        return f"""
  <section style="text-align:center;margin:36px 0;line-height:0;box-sizing:border-box;">
    <section style="display:inline-block;width:32px;height:1px;background:#D5D3C8;"><span leaf=""><br/></span></section>
  </section>"""

    def render_footer(self, author="", note=""):
        return f"""
  <section style="text-align:center;margin:40px 0 20px;line-height:0;box-sizing:border-box;">
    <section style="display:inline-block;width:32px;height:1px;background:#D5D3C8;"><span leaf=""><br/></span></section>
  </section>
  <section style="text-align:center;color:#888888;font-size:12px;font-family:PingFangSC-light;padding:0 20px;line-height:1.75;margin:16px 0 32px;letter-spacing:1.5px;box-sizing:border-box;">
    <p style="margin:0;padding:0;color:#A7A56D;box-sizing:border-box;"><span leaf="">● 漫游生活手作排版 ●</span></p>
  </section>"""

STYLE_INSTANCE = ClonedStyle_Olive_artisan()
