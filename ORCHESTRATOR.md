# Content SEO Orchestrator — Agent Flow

## Overview
3-agent pipeline to go from content brief → published blog post with images.
This document describes the underlying architecture. For day-to-day use, see [README.md](./README.md) and the `/seo-*` slash commands.

---

## Agent 1: Image Agent

### Local PNG Generator (cover + social cards)
```bash
# 1200x630 branded cover for the post
python generate_covers.py \
  --slug your-blog-slug \
  --title "Your Blog Title" \
  --output ./covers/

# Per-post social cards (OG / Twitter / LinkedIn / hero)
python generate-blog-images.py \
  --title "Your Blog Title" \
  --tag "Playbook" \
  --subtitle "One-line description" \
  --date "March 2026" \
  --output ./blog-images/your-blog-slug/
```
**Outputs per post:** `blog-hero.png`, `social-og.png`, `twitter-card.png`, `linkedin-card.png`

### Figma / FigJam Diagrams
- Tool: Figma MCP → `generate_diagram` (Mermaid.js → FigJam)
- Supports: flowcharts, sequence diagrams, state diagrams, gantt charts
- Export: `get_screenshot` to PNG, or use FigJam claim URLs

---

## Agent 2: Content Generation Agent

### Input
- `./pipeline.yaml` — post registry
- `./config/seo-settings.yaml → paths.planning_brief` — optional doc with per-post Perplexity research prompts
- `./output/<slug>/research.md` — research output from `/seo-research`
- `./output/<slug>/brief.md` — content brief from `/seo-brief`

### Process
1. Run Perplexity prompts (via API or copy-paste) → gather research data
2. Generate content brief from research (`/seo-brief`)
3. Write full blog post markdown from brief (`/seo-write`)
4. Follow brand voice from `config/seo-settings.yaml → content_rules`
5. Include SEO metadata: title tag, meta description, slug, primary KW, secondary KWs
6. Reference infographic diagrams at appropriate sections
7. Output: CMS-ready markdown with image references

### Output Location
```
./output/<slug>/draft.md
```

---

## Agent 3: CMS Publishing Agent

### Process
1. Read draft markdown + frontmatter
2. Upload images to your CMS asset pipeline (or reference existing assets)
3. Build the CMS document JSON (see `templates/sanity-document.json` for shape)
4. Publish via your CMS API/MCP
5. Submit to IndexNow (Bing/Yandex) for instant indexing

### Sanity (reference implementation)
Direct HTTP API (recommended over MCP for deterministic `_id`):
```bash
curl -X POST "https://${SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07/data/mutate/${SANITY_DATASET}" \
  -H "Authorization: Bearer $SANITY_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "mutations": [{ "createOrReplace": <PAYLOAD_WITH_DETERMINISTIC_ID> }] }'
```

### Swapping CMS
Edit `.claude/commands/seo-publish.md` — replace the Sanity curl/MCP calls with your CMS's API. The rest of the pipeline is CMS-agnostic.

---

## Orchestrator Flow

```
Content Brief (pipeline.yaml + planning_brief)
    |
    v
+-------------------------+
|  /seo-research          | <- Perplexity Deep Research API
|  /seo-brief             |
|  /seo-write             |
|  Output: blog markdown  |
+-----------+-------------+
            |
    +-------+-------+
    v               v
+----------+  +----------------+
| Covers   |  | Figma Diagrams |
| Hero PNG |  | (Mermaid→FigJam)|
+----+-----+  +-------+--------+
     |                |
     +--------+-------+
              v
+-------------------------+
|  /seo-optimize          | <- SEO score (10 checks × 10 pts)
|  /seo-publish           | <- CMS publish + IndexNow ping
+-------------------------+
```

---

## How to Continue in Future Sessions
The pipeline is stateless — every command re-reads `pipeline.yaml` and `output/<slug>/*` to figure out where you left off. Just run `/seo-status` or `/seo-daily` to pick up.

### Quick Commands
- Generate covers: `python generate_covers.py --slug <slug>`
- Generate social images: `python generate-blog-images.py --output ./blog-images/<slug>/`
- Generate Figma diagram: use `generate_diagram` via Figma MCP
- Check status: `/seo-status`
