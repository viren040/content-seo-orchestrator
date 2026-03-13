"""
Local blog image generator for ASVA AI
Uses HTML templates + html2image (Chrome) to render branded PNGs
Run: python generate-blog-images.py --title "Your Blog Title" --output ./output/

Brand Bible v1.0 colors applied.
"""
import argparse
import os
from html2image import Html2Image

# ── Asva AI Brand Bible v1.0 ──────────────────────────────────────
BRAND = {
    "bg":             "#0A0F1E",   # Deep Space Navy
    "accent":         "#6C63FF",   # Electric Violet
    "teal":           "#00C9B1",   # Agentic Teal
    "amber":          "#F5A623",   # Signal Amber
    "dark_slate":     "#2A2D3E",   # Dark Slate
    "soft_violet":    "#8B83FF",   # Soft Violet
    "text":           "#FFFFFF",   # Pure White
    "ghost":          "#F8F8FF",   # Ghost White
    "muted":          "#9B99B5",   # Stellar Grey
    "deep_text":      "#1A1D2E",   # Deep Text
    "font_headline":  "Space Grotesk",
    "font_body":      "Inter",
    "font_data":      "JetBrains Mono",
}

# ── 1. Hero / Header Image (1200×630) ─────────────────────────────
HERO_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1200px; height: 630px;
    background: {bg};
    display: flex; align-items: center; justify-content: center;
    position: relative; overflow: hidden;
    font-family: 'Inter', sans-serif;
}}
.grid {{
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(108,99,255,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(108,99,255,0.08) 1px, transparent 1px);
    background-size: 60px 60px;
}}
.glow {{
    position: absolute; top: -100px; right: -100px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(108,99,255,0.15), transparent 70%);
    border-radius: 50%;
}}
.glow-teal {{
    position: absolute; bottom: -80px; left: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(0,201,177,0.10), transparent 70%);
    border-radius: 50%;
}}
.content {{
    position: relative; z-index: 2;
    max-width: 900px; padding: 60px;
    text-align: center;
}}
h1 {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700; font-size: 48px;
    color: {text}; line-height: 1.2;
    margin-bottom: 20px;
}}
.accent-line {{
    width: 80px; height: 4px;
    background: {accent}; margin: 0 auto 20px;
    border-radius: 2px;
}}
.meta {{
    font-size: 16px; color: {muted};
    font-weight: 500;
}}
.footer {{
    position: absolute; bottom: 24px; right: 40px;
    font-size: 14px; color: {muted};
    opacity: 0.6;
}}
</style>
</head>
<body>
<div class="grid"></div>
<div class="glow"></div>
<div class="glow-teal"></div>
<div class="content">
    <div class="accent-line"></div>
    <h1>{title}</h1>
    <p class="meta">ASVA AI &middot; {date}</p>
</div>
<div class="footer">asvaai.com</div>
</body>
</html>
"""

# ── 2. OG / Social Card (1200×675) ────────────────────────────────
OG_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1200px; height: 675px;
    background: {bg};
    display: flex; align-items: center;
    position: relative; overflow: hidden;
    font-family: 'Inter', sans-serif;
}}
.left {{
    flex: 1; padding: 60px;
    display: flex; flex-direction: column; justify-content: center;
}}
.right {{
    width: 350px; height: 100%;
    background: linear-gradient(135deg, {accent}22, {accent}08);
    display: flex; align-items: center; justify-content: center;
    position: relative;
}}
.right::before {{
    content: ''; position: absolute;
    width: 200px; height: 200px;
    border: 2px solid {accent}44;
    border-radius: 50%; opacity: 0.3;
}}
.right::after {{
    content: ''; position: absolute;
    width: 120px; height: 120px;
    border: 2px solid {teal}44;
    border-radius: 50%; opacity: 0.4;
}}
.tag {{
    display: inline-block; padding: 6px 16px;
    background: {accent}22; border: 1px solid {accent}44;
    border-radius: 20px; font-size: 13px;
    color: {accent}; font-weight: 500;
    margin-bottom: 24px; text-transform: uppercase;
    letter-spacing: 1px;
}}
h1 {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700; font-size: 40px;
    color: {text}; line-height: 1.25;
    margin-bottom: 16px;
}}
.meta {{
    font-size: 15px; color: {muted};
}}
.footer {{
    position: absolute; bottom: 20px; left: 60px;
    font-size: 13px; color: {muted}; opacity: 0.5;
}}
</style>
</head>
<body>
<div class="left">
    <span class="tag">{tag}</span>
    <h1>{title}</h1>
    <p class="meta">By Viren Inaniyan &middot; {date}</p>
</div>
<div class="right"></div>
<div class="footer">asvaai.com</div>
</body>
</html>
"""

# ── 3. Twitter Card (1200×628) ─────────────────────────────────────
TWITTER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1200px; height: 628px;
    background: linear-gradient(135deg, {bg} 0%, {dark_slate} 100%);
    display: flex; align-items: center;
    position: relative; overflow: hidden;
    font-family: 'Inter', sans-serif;
}}
.bar {{
    position: absolute; top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, {accent}, {teal});
}}
.content {{
    padding: 60px 80px;
    max-width: 850px;
}}
h1 {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700; font-size: 44px;
    color: {text}; line-height: 1.2;
    margin-bottom: 20px;
}}
.meta {{
    font-size: 16px; color: {muted};
    font-weight: 500;
}}
.brand {{
    position: absolute; bottom: 30px; right: 40px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700; font-size: 20px;
    color: {accent};
}}
</style>
</head>
<body>
<div class="bar"></div>
<div class="content">
    <h1>{title}</h1>
    <p class="meta">{date} &middot; asvaai.com</p>
</div>
<div class="brand">Asva AI</div>
</body>
</html>
"""


# ── 4. LinkedIn Card (1200×627) ────────────────────────────────────
LINKEDIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1200px; height: 627px;
    background: {bg};
    display: flex;
    position: relative; overflow: hidden;
    font-family: 'Inter', sans-serif;
}}
.accent-bar {{
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 6px;
    background: linear-gradient(180deg, {accent}, {teal});
}}
.grid {{
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(108,99,255,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(108,99,255,0.05) 1px, transparent 1px);
    background-size: 80px 80px;
}}
.glow-tr {{
    position: absolute; top: -120px; right: -120px;
    width: 450px; height: 450px;
    background: radial-gradient(circle, rgba(108,99,255,0.12), transparent 70%);
    border-radius: 50%;
}}
.glow-bl {{
    position: absolute; bottom: -100px; left: 200px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(0,201,177,0.08), transparent 70%);
    border-radius: 50%;
}}
.content {{
    position: relative; z-index: 2;
    flex: 1; padding: 56px 64px;
    display: flex; flex-direction: column; justify-content: center;
}}
.tag-row {{
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 28px;
}}
.tag {{
    display: inline-block; padding: 6px 18px;
    background: {accent}18; border: 1px solid {accent}40;
    border-radius: 20px; font-size: 12px;
    color: {soft_violet}; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1.5px;
}}
.dot {{
    width: 4px; height: 4px;
    background: {muted}; border-radius: 50%;
}}
.read-time {{
    font-size: 12px; color: {muted};
    font-weight: 500; text-transform: uppercase;
    letter-spacing: 1px;
}}
h1 {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700; font-size: 42px;
    color: {text}; line-height: 1.22;
    margin-bottom: 20px;
    max-width: 750px;
}}
.subtitle {{
    font-size: 17px; color: {muted};
    line-height: 1.5; max-width: 600px;
    font-weight: 400;
}}
.bottom-bar {{
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 56px; padding: 0 64px;
    background: {dark_slate}cc;
    display: flex; align-items: center; justify-content: space-between;
    backdrop-filter: blur(8px);
}}
.author {{
    display: flex; align-items: center; gap: 12px;
}}
.avatar {{
    width: 32px; height: 32px;
    background: linear-gradient(135deg, {accent}, {teal});
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700; font-size: 14px; color: {text};
}}
.author-info {{
    display: flex; flex-direction: column;
}}
.author-name {{
    font-size: 13px; color: {text};
    font-weight: 600;
}}
.author-role {{
    font-size: 11px; color: {muted};
    font-weight: 400;
}}
.brand-mark {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700; font-size: 16px;
    color: {accent};
    display: flex; align-items: center; gap: 8px;
}}
.brand-dot {{
    width: 8px; height: 8px;
    background: {teal}; border-radius: 50%;
}}
</style>
</head>
<body>
<div class="accent-bar"></div>
<div class="grid"></div>
<div class="glow-tr"></div>
<div class="glow-bl"></div>
<div class="content">
    <div class="tag-row">
        <span class="tag">{tag}</span>
        <span class="dot"></span>
        <span class="read-time">{date}</span>
    </div>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
</div>
<div class="bottom-bar">
    <div class="author">
        <div class="avatar">VI</div>
        <div class="author-info">
            <span class="author-name">Viren Inaniyan</span>
            <span class="author-role">Founder, Asva AI</span>
        </div>
    </div>
    <div class="brand-mark">
        <span class="brand-dot"></span>
        asvaai.com
    </div>
</div>
</body>
</html>
"""


def generate(title: str, tag: str, date: str, output_dir: str, subtitle: str = ""):
    os.makedirs(output_dir, exist_ok=True)

    hti = Html2Image(
        output_path=output_dir,
        size=(1200, 630),
        browser_executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    )

    # ── Hero ──
    hero_html = HERO_TEMPLATE.format(title=title, date=date, **BRAND)
    hti.screenshot(html_str=hero_html, save_as="blog-hero.png")
    print(f"  Hero saved: {output_dir}/blog-hero.png")

    # ── OG Card ──
    hti.size = (1200, 675)
    og_html = OG_TEMPLATE.format(title=title, tag=tag, date=date, **BRAND)
    hti.screenshot(html_str=og_html, save_as="social-og.png")
    print(f"  OG Card saved: {output_dir}/social-og.png")

    # ── Twitter Card ──
    hti.size = (1200, 628)
    tw_html = TWITTER_TEMPLATE.format(title=title, date=date, **BRAND)
    hti.screenshot(html_str=tw_html, save_as="twitter-card.png")
    print(f"  Twitter Card saved: {output_dir}/twitter-card.png")

    # ── LinkedIn Card ──
    hti.size = (1200, 627)
    li_html = LINKEDIN_TEMPLATE.format(title=title, tag=tag, date=date, subtitle=subtitle, **BRAND)
    hti.screenshot(html_str=li_html, save_as="linkedin-card.png")
    print(f"  LinkedIn Card saved: {output_dir}/linkedin-card.png")

    # ── Compress (if pngquant available) ──
    for f in ["blog-hero.png", "social-og.png", "twitter-card.png", "linkedin-card.png"]:
        path = os.path.join(output_dir, f)
        os.system(f"pngquant --force --quality=80-95 --output {path} {path} 2>/dev/null")

    print(f"\n  All images in: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate on-brand blog images for Asva AI")
    parser.add_argument("--title", required=True, help="Blog post title")
    parser.add_argument("--tag", default="Playbook", help="Category tag (e.g. Playbook, Guide, Deep Dive)")
    parser.add_argument("--date", default="March 2026", help="Display date")
    parser.add_argument("--subtitle", default="", help="Short subtitle for LinkedIn card")
    parser.add_argument("--output", default="./blog-images", help="Output directory")
    args = parser.parse_args()
    generate(args.title, args.tag, args.date, args.output, args.subtitle)
