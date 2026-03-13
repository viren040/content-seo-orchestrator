# Asva AI Blog Pipeline — Orchestrator

## Overview
3-agent pipeline to go from content brief → published blog post with images.

---

## Agent 1: Image Agent (DONE)

### Local PNG Generator
```bash
cd "/Users/viren/SEO - Asva Main Website"
source .venv/bin/activate
python generate-blog-images.py \
  --title "Your Blog Title" \
  --tag "Playbook" \
  --subtitle "One-line description" \
  --date "March 2026" \
  --output ./blog-images/<slug>/
```
**Outputs per post:** `blog-hero.png`, `social-og.png`, `twitter-card.png`, `linkedin-card.png`

### Figma Infographics
- Tool: Figma MCP → `generate_diagram` (Mermaid.js → FigJam)
- Supports: flowcharts, sequence diagrams, state diagrams, gantt charts
- Export: `get_screenshot` to PNG, or use FigJam claim URLs

### Status: 13/13 posts — all images generated

---

## Agent 2: Content Generation Agent (NEXT)

### Input
- `/Users/viren/Desktop/Asva AI — Docs & Strategy/Feature-Page-Blog-Planning-Brief.md`
- Contains Perplexity research prompts per post

### Process
1. Run Perplexity prompts → gather research data
2. Generate full blog post markdown per content brief
3. Follow Asva AI voice: Precise, Confident, Useful
4. Include SEO metadata: title tag, meta description, slug, primary KW, secondary KWs
5. Reference infographic diagrams at appropriate sections
6. Output: Sanity-ready markdown with image references

### Output Location
```
/Users/viren/SEO - Asva Main Website/blog-content/<slug>.md
```

---

## Agent 3: Sanity Publishing Agent (EXISTS — separate session)

### Process
1. Read blog content markdown
2. Upload images to Sanity asset pipeline
3. Create `blogPost` document with:
   - Portable text blocks
   - SEO metadata
   - Image references (hero, OG, inline infographics)
   - Author: Viren Inaniyan
   - Category/tags
4. Publish or schedule

### Sanity MCP Tools
- `create_documents_from_markdown` — push markdown as Sanity doc
- `patch_document_from_markdown` — update existing post
- `publish_documents` — go live

---

## Orchestrator Flow

```
Content Brief (planning doc)
    │
    ▼
┌─────────────────────────┐
│  Agent 2: Content Gen   │ ← Perplexity research
│  Output: blog markdown  │
└────────────┬────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌──────────┐  ┌──────────────┐
│ Agent 1  │  │ Agent 1      │
│ Local PNG│  │ Figma Diagrams│
└────┬─────┘  └──────┬───────┘
     │               │
     └───────┬───────┘
             ▼
┌─────────────────────────┐
│  Agent 3: Sanity Publish│
│  Images + Content → CMS │
└─────────────────────────┘
```

---

## Publish Order (lowest KD first)
1. `audit-brand-visibility-llms` (KD 2)
2. `brands-invisible-ai-search-how-to-fix` (KD 12)
3. `what-is-ai-visibility-score` (KD 13)
4. `ai-seo-agency-guide` (KD 15)
5. `strategies-improve-brand-visibility-ai-search` (KD 17)
6. `best-ai-search-monitoring-platforms-2026` (KD 18)
7. `how-to-track-brand-mentions-ai-search` (KD 19)
8. `how-ai-search-citation-sources-work` (KD 20)
9. `agencies-add-aeo-service-offering` (KD 20)
10. `why-use-ai-search-monitoring-tools` (KD 22)
11. `agency-rank-tracking-ai-platforms` (KD 26)
12. `ai-search-competitive-analysis` (KD 33)

---

## How to Continue in Future Sessions
Say: **"continue blog pipeline"** — Claude will load memory and pick up where we left off.

### Quick Commands
- Generate images for new post: `python generate-blog-images.py --title "..." --output ./blog-images/<slug>/`
- Generate Figma diagram: use `generate_diagram` via Figma MCP
- Check status: read `project_blog_pipeline.md` in memory
