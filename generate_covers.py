#!/usr/bin/env python3
"""Generate branded blog cover images (1200x630) for Asva AI blog posts."""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Brand colors
PRIMARY_PURPLE = "#7C3AED"
DARK = "#1F2937"
EMERALD = "#10B981"
WHITE = "#FFFFFF"

# Image dimensions
WIDTH = 1200
HEIGHT = 630

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "covers")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Blog posts: (title, filename)
# All 17 blog posts — legacy + pipeline
POSTS = [
    # Legacy posts (pre-pipeline)
    ("Business Agent + Direct Offers: Google's New Merchant Growth Stack", "business-agent-direct-offers.png"),
    ("From Conversation to Conversion: How UCP Enables Checkout in AI Mode", "ucp-checkout-ai-mode.png"),
    ("How MyMuse Became ChatGPT's #1 Sexual Wellness Brand in 60 Days", "mymuse-chatgpt-brand.png"),
    ("The Ultimate Guide to AEO 2026: How to Get ChatGPT to Recommend Your Product", "ultimate-guide-aeo-2026.png"),
    ("UCP Technical Architecture: Capabilities, Extensions & Transport Bindings", "ucp-technical-architecture.png"),
    ("UCP: What Google Launched on Jan 11, 2026 and Why It Matters", "ucp-google-launch.png"),
    ("AI Visibility Trends 2025 — Master ChatGPT Optimization", "ai-visibility-trends-2025.png"),
    ("How to Get Your Brand Mentioned by ChatGPT & AI Search", "chatgpt-brand-mentions.png"),
    ("The Ultimate Guide to AI Training Data Control", "ai-training-data-control.png"),
    ("Why AEO is Critical for Business Success in 2025", "why-aeo-critical-2025.png"),
    # Pipeline posts (4 published + 9 draft)
    ("How to Audit Your Brand's Visibility on LLMs (Free DIY Guide)", "audit-brand-visibility-llms.png"),
    ("Why Brands Are Invisible in AI Search — And How to Fix It", "brands-invisible-ai-search.png"),
    ("What Is an AI Visibility Score — And How Is It Calculated?", "what-is-ai-visibility-score.png"),
    ("How We Automated Organic Growth Using Claude + 4 Tools", "claude-seo-automation-stack.png"),
    ("The AI SEO Agency Guide: What to Look for When Hiring", "ai-seo-agency-guide.png"),
    ("What Strategies Improve Brand Visibility in AI Search?", "strategies-brand-visibility-ai.png"),
    ("Best AI Search Monitoring Platforms Compared (2026)", "best-ai-monitoring-platforms-2026.png"),
    ("How to Track Brand Mentions in AI Search", "track-brand-mentions-ai-search.png"),
    ("How AI Search Citation Sources Work", "ai-citation-sources.png"),
    ("How Agencies Can Add AEO to Their Service Stack", "agencies-add-aeo.png"),
    ("Why You Need AI Search Monitoring Tools (Not Just GA)", "why-ai-monitoring-tools.png"),
    ("Agency Rank Tracking Across AI Platforms", "agency-rank-tracking-ai.png"),
    ("AI Search Competitive Analysis: See What Competitors Win", "ai-competitive-analysis.png"),
]


def get_font(size, bold=False):
    """Try to load a clean system font, fall back to default."""
    font_paths = [
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                if path.endswith(".ttc"):
                    # For .ttc files, index 0 is regular, index 1 is often bold
                    idx = 1 if bold else 0
                    return ImageFont.truetype(path, size, index=idx)
                else:
                    return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def wrap_title(title, font, draw, max_width):
    """Word-wrap title text to fit within max_width pixels."""
    words = title.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def generate_cover(title, filename):
    """Generate a single blog cover image."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DARK)
    draw = ImageDraw.Draw(img)

    # --- Purple accent: left bar + top gradient strip ---
    # Left vertical bar
    bar_width = 8
    draw.rectangle([0, 0, bar_width, HEIGHT], fill=PRIMARY_PURPLE)

    # Top accent strip with gradient effect
    strip_height = 6
    draw.rectangle([0, 0, WIDTH, strip_height], fill=PRIMARY_PURPLE)

    # Subtle decorative elements - diagonal accent line
    for i in range(3):
        y_offset = 80 + i * 4
        draw.line(
            [(bar_width + 40, y_offset), (bar_width + 120, y_offset)],
            fill=PRIMARY_PURPLE,
            width=2,
        )

    # Bottom-right decorative corner dots
    for i in range(5):
        x = WIDTH - 60 + i * 8
        y = HEIGHT - 60
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=PRIMARY_PURPLE)

    # --- Title text ---
    title_font = get_font(46, bold=True)
    max_text_width = WIDTH - 160  # margins: left 80, right 80
    lines = wrap_title(title, title_font, draw, max_text_width)

    # Calculate vertical positioning (center the text block vertically, shifted up slightly)
    line_height = 58
    total_text_height = len(lines) * line_height
    start_y = (HEIGHT - total_text_height) // 2 - 30

    # Ensure we don't go too high
    start_y = max(start_y, 60)

    for i, line in enumerate(lines):
        y = start_y + i * line_height
        draw.text((80, y), line, fill=WHITE, font=title_font)

    # --- Separator line ---
    sep_y = start_y + total_text_height + 24
    draw.line([(80, sep_y), (280, sep_y)], fill=EMERALD, width=3)

    # --- "ASVA AI" branding ---
    brand_font = get_font(22, bold=True)
    brand_y = HEIGHT - 70
    draw.text((80, brand_y), "ASVA AI", fill=EMERALD, font=brand_font)

    # Small tagline
    tag_font = get_font(14, bold=False)
    draw.text((80, brand_y + 30), "asva.ai", fill="#9CA3AF", font=tag_font)

    # --- Save ---
    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path, "PNG", quality=95)
    print(f"  Created: {filename}")


def main():
    print(f"Generating {len(POSTS)} blog cover images...")
    print(f"Output: {OUTPUT_DIR}\n")
    for title, filename in POSTS:
        generate_cover(title, filename)
    print(f"\nDone! {len(POSTS)} covers generated.")


if __name__ == "__main__":
    main()
