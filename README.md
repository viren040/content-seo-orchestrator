# Content SEO Orchestrator

A Claude Code–native content SEO pipeline that takes blog posts from research to published — with a human in the loop at every decision point. Built by [Viren Inaniyan](https://linkedin.com/in/vireninaniyan) at [Asva AI](https://asvaai.com). MIT-licensed. Fork it, adapt it, ship it.

---

## What This Does

```
Research → Brief → Write → SEO Score → Cover/Diagrams → Publish → IndexNow
   GATE     GATE    GATE                                  GATE
```

A 6-step pipeline with 4 human gates. You keep judgment over research quality, content angle, final copy, and publish decision. The orchestrator handles structure, templates, SEO scoring, image generation, CMS publishing, and instant indexing.

**Daily time commitment: 15-20 minutes** with `/seo-daily`.

---

## Why this exists

Most SEO/AEO content stacks do one of two things badly:
1. **Fully automated**, producing thin, generic posts you wouldn't put your name on.
2. **Fully manual**, where 80% of your day is research, formatting, and CMS clicking.

This pipeline keeps the boring stuff automated (templates, scoring, CMS payloads, image generation, indexing) and the interesting stuff human (research angle, brief approval, copy voice, publish decision).

Cost per post: **~$0.45** (one Perplexity Deep Research call). Everything else runs locally in Claude Code.

---

## Commands

| Command | What It Does | Human Gate |
|---------|-------------|------------|
| `/seo-status` | Pipeline dashboard — all posts, completion %, next task | No |
| `/seo-research <slug>` | Perplexity Deep Research API (with fallback to manual paste) | Yes — review prompt + cost |
| `/seo-brief <slug>` | Generates content brief from research | Yes — approve brief |
| `/seo-write <slug>` | Writes full blog post from brief, in brand voice | Yes — review draft |
| `/seo-optimize <slug>` | 10-check SEO quality score (0-100) with fix suggestions | No |
| `/seo-publish <slug>` | Pushes to CMS as draft or live, then pings IndexNow | Yes — confirm publish |
| `/seo-daily` | Daily 15-min workflow — auto-picks next task | Runs appropriate step |

---

## Features

### Research
- **Perplexity Deep Research integration** — `sonar-deep-research` model via API, ~$0.45/post, with citations, sources, recency filter
- **Manual fallback** — if no API key, the command shows the prompt and accepts pasted Perplexity output
- **Cost tracking** — every research call shows estimated + actual cost
- **Source attribution** — every stat extracted with its source URL preserved in the research brief

### Content
- **Brand voice driven by config** — `config/seo-settings.yaml` controls voice, tone, content pillars, CTA URLs. No hardcoded brand assumptions.
- **Brief-first writing** — the brief is the contract. Drafts can't be written until a brief is approved.
- **Real examples enforced** — the writer is instructed to use real customers/case studies, never hypotheticals.
- **Multi-brand support** — keep one repo, swap `config/seo-settings.yaml` per project (Asva AI example included at `config/seo-settings.example.yaml`).

### SEO scoring (10 × 10 = 100)
Keyword placement · keyword density · meta title · meta description · heading structure · content length · internal links · FAQ quality · readability · content quality. Grades A–F with specific fix suggestions.

### Images
- **`generate-blog-images.py`** — HTML→PNG via headless Chrome. Outputs hero + OG + Twitter + LinkedIn cards per post.
- **`generate_covers.py`** — branded 1200×630 covers using Pillow. Drop in your logo, colors, and fonts via `config/seo-settings.yaml → design`.
- **Figma/FigJam infographics** — Mermaid → FigJam via Figma MCP. Auto-export to PNG.

### Publishing (Sanity reference implementation)
- **Direct HTTP API** — the orchestrator uses Sanity's HTTP mutation endpoint instead of the MCP. Why: Sanity MCP's `create_documents_from_json` overwrites your `_id` with a random UUID, breaking deterministic frontends. Direct curl preserves `_id` like `blogPost-<slug>`.
- **IndexNow ping** — after publishing live, the orchestrator pings IndexNow so Bing/Yandex/Seznam/Naver index within minutes. Google has its own indexing API (future integration).
- **Pre-flight checks** — SEO score gate, required-field validation, human confirmation before any write.

### Pluggable CMS
Sanity is the reference implementation. To use WordPress, Contentful, Strapi, Webflow, or any headless CMS:
1. Edit `.claude/commands/seo-publish.md` — replace Sanity API calls with your CMS's API/MCP
2. Edit `templates/sanity-document.json` — restructure for your schema
3. Everything else (pipeline, briefs, writing, scoring, images) is CMS-agnostic

---

## Architecture

```
your-project/
├── pipeline.yaml                  # Single source of truth — all posts + status
├── PUBLISHING-SCHEDULE.md         # Optional: publishing calendar + checklist
├── .env                           # API keys (gitignored — copy from .env.example)
├── config/
│   ├── seo-settings.yaml          # Your brand, CMS, SEO rules
│   ├── seo-settings.example.yaml  # Asva AI example
│   └── api-setup.md               # API keys + cost guide
├── templates/
│   ├── research-brief.md          # Research output structure
│   ├── content-brief.md           # Writing brief structure
│   ├── blog-post.md               # Post template (CMS-ready)
│   └── sanity-document.json       # CMS payload template
├── output/<slug>/                 # Per-post working dir
│   ├── research.md                # Step 1 output (structured)
│   ├── research-raw.json          # Raw Perplexity API response
│   ├── brief.md                   # Step 2 output
│   ├── draft.md                   # Step 3 output
│   ├── seo-review.md              # Step 4 output
│   ├── sanity-payload.json        # Step 6 payload
│   └── published.json             # Step 6 confirmation + IndexNow status
├── covers/                        # 1200x630 branded covers
├── blog-images/<slug>/            # Per-post social images
├── infographics/                  # FigJam diagram exports
├── generate_covers.py             # Pillow cover generator
├── generate-blog-images.py        # HTML→PNG social card generator
├── .claude/commands/              # The /seo-* slash commands
└── README.md
```

---

## Quick Start

### 1. Clone & install
```bash
git clone https://github.com/viren040/content-seo-orchestrator.git
cd content-seo-orchestrator

# Python deps for image generation (optional)
python -m venv .venv && source .venv/bin/activate
pip install pyyaml pillow requests
```

### 2. Configure
```bash
# Copy and edit env vars
cp .env.example .env
# Add at minimum: PERPLEXITY_API_KEY, SANITY_AUTH_TOKEN
```

Edit `config/seo-settings.yaml`:
- Set `brand.name`, `brand.website`, `brand.cta_url`
- Set `sanity.project_id` (or any CMS config)
- Tune `seo_defaults` (word count, keyword density, etc.)
- Customize `content_rules.voice` and `tone_guidelines`

### 3. Add your posts to `pipeline.yaml`
```yaml
posts:
  - id: "1.1"
    title: "Your Blog Post Title"
    slug: "your-blog-post-slug"
    primary_keyword: "target keyword"
    secondary_keywords: ["related kw 1", "related kw 2"]
    keyword_volume: 1000
    keyword_difficulty: 15
    word_count_target: 1800
    content_angle: "What makes this post distinct"
    publish_order: 1
    internal_links:
      - anchor: "Related concept"
        url: "/blog/related-post"
    status:
      research: pending
      brief: pending
      content: pending
      seo_review: pending
      sanity_draft: pending
      published: pending
```

### 4. Run daily
```bash
# Inside Claude Code:
/seo-daily
```
The orchestrator picks the next post, runs the next step, and pauses at human gates.

---

## API costs (per post)

| Step | Service | Cost | Notes |
|------|---------|------|-------|
| Research | Perplexity `sonar-deep-research` | ~$0.45 | One call per post |
| Brief | Claude Code | included | Runs locally |
| Write | Claude Code | included | Runs locally |
| SEO review | Claude Code | included | Runs locally |
| Publish | Sanity Content Lake API | $0.00 | 250K req/mo free tier |
| Indexing | IndexNow | $0.00 | Free |
| Images | Pillow / headless Chrome | $0.00 | Local |
| **Total** | | **~$0.45/post** | |

Compare to: $100-500/post freelancer, $200-1000/post agency, $0.05/post pure-AI generic slop.

Full breakdown in [config/api-setup.md](./config/api-setup.md).

---

## What's in this repo

The repo ships with a working example: Asva AI's blog content (12 posts on AEO/AI search visibility), all already published. Browse `output/`, `pipeline.yaml`, and `config/seo-settings.example.yaml` to see real input/output for the pipeline.

Want a different brand? Replace these three files and you're off:
1. `config/seo-settings.yaml`
2. `pipeline.yaml`
3. (Optional) `templates/sanity-document.json` if you're not using Sanity

---

## SEO scoring details

| Check | What It Measures | Threshold for full score |
|-------|------------------|--------------------------|
| Keyword Placement | Primary KW in H1, intro, ≥1 H2, meta title, meta desc | All 5 present |
| Keyword Density | Primary KW frequency vs. word count | 1-2% target |
| Meta Title | Length, KW inclusion, clickability | 50-60 chars, KW present |
| Meta Description | Length, KW + CTA | 150-160 chars, CTA present |
| Heading Structure | H1 → H2 → H3 hierarchy, ≥4 H2s | Logical hierarchy, no skips |
| Content Length | Word count vs. target | 80-120% of target |
| Internal Links | Count + anchor quality | ≥3, descriptive anchors |
| FAQ Quality | Count, query authenticity, KW | 3-6 FAQs, KW in ≥1 |
| Readability | Paragraph length, scannability | ≤4 sentences/para, bullets/tables |
| Content Quality | Sources, real examples, no fluff | All claims sourced |

**Grading**: A (90+) = publish-ready · B (80-89) = minor tweaks · C (70-79) = needs work · F (<60) = rewrite

---

## Roadmap

Confirmed:
- DataForSEO MCP integration for automated keyword opportunity detection
- GSC API integration for impression/CTR tracking on published posts
- Content cannibalization detector (audit script that flags overlapping posts in the CMS)
- Multi-language content pipeline (one source draft → localized variants)

Likely:
- WordPress publishing command
- Contentful publishing command
- Rank tracking dashboard (post → keyword → position → trend)
- AI citation tracking (which LLMs cite the post, with what query)

---

## Contributing

PRs welcome. Highest-value contributions:
- New CMS publishers (WordPress, Contentful, Strapi, Webflow, Ghost)
- Keyword research integrations (DataForSEO, Ahrefs, Semrush)
- Better cover/image generators (Canva API, Figma plugins)
- Rank tracking integrations
- Localization workflow

---

## License

MIT — use it, fork it, sell it, whatever. Credit appreciated.

---

Built with Claude Code by [Asva AI](https://asvaai.com).
