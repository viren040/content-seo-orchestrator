# Content SEO Orchestrator

> A Claude Code–native content SEO pipeline. **Research → Brief → Write → SEO Score → Publish → IndexNow** in **15 min/day** at **~$0.45/post**. MIT-licensed. Fork it, adapt it, ship it.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-D97757)](https://claude.com/claude-code)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

---

## Real-world result

One brand we run this pipeline for went from **131 → 964 avg impressions/day** in 12 months — **a 7.3× lift**. Monthly impressions went from **2,142 → 39,240 (18× growth)**. Blog content produced by this orchestrator accounted for **51.8% of all impressions** (126,829 of 244,861) across 119 posts.

Honest caveat: clicks didn't grow proportionally over this window — CTR dropped because new content ranked but the title/meta layer hadn't been tuned yet. That's the *next* iteration of the pipeline (a `/seo-refresh` command for re-optimizing live posts), shipping soon. The pipeline gets you to "ranking"; closing the gap to "clicking" is the obvious next step.

Top posts produced by the pipeline (real, live):

| Post | Impressions | Avg position |
|---|---|---|
| `best-hr-ai-tools-2025` | 24,297 | 11.1 |
| `ai-agents-2025-state-of-ai` | 13,699 | 7.7 |
| `voice-ai-recruitment` | 7,189 | 17.6 |
| `top-10-ai-recruiting-tools-in-2026` | 5,943 | 7.5 |
| `babblebots-vs-paradox-ai-olivia` | 5,367 | 6.3 |

This is the Asva AI blog content (12 posts on AEO / AI visibility) shipped as the working example in `/output/` and `pipeline.yaml`. Browse those to see real input → real output.

---

## What this is

A 6-step content SEO pipeline that runs as Claude Code slash commands, with 4 human gates so you stay in control of the high-judgment calls.

```
Research → Brief → Write → SEO Score → Cover/Diagrams → Publish → IndexNow
   GATE     GATE    GATE                                  GATE
```

You handle: research angle, brief approval, copy voice, publish decision.
The pipeline handles: structure, templates, SEO scoring, image generation, CMS publishing, instant indexing.

## Why this exists

Most SEO/AEO content stacks fail one of two ways:

1. **Fully automated** — thin, generic posts you wouldn't put your name on. Google's March 2026 core update gutted exactly this kind of content.
2. **Fully manual** — 80% of your day is research, formatting, and CMS clicking. You don't scale.

This pipeline keeps the *boring* stuff automated (templates, scoring, CMS payloads, image generation, indexing) and the *interesting* stuff human (research angle, brief approval, copy voice, publish decision).

---

## Commands

| Command | What It Does | Human Gate |
|---------|-------------|------------|
| `/seo-status` | Pipeline dashboard — all posts, completion %, next task | No |
| `/seo-research <slug>` | Perplexity Deep Research API (with manual paste fallback) | Yes — review prompt + cost |
| `/seo-brief <slug>` | Generates content brief from research | Yes — approve brief |
| `/seo-write <slug>` | Writes full blog post from brief, in brand voice | Yes — review draft |
| `/seo-optimize <slug>` | 10-check SEO quality score (0-100) with fix suggestions | No |
| `/seo-publish <slug>` | Pushes to CMS as draft or live, pings IndexNow | Yes — confirm publish |
| `/seo-daily` | Daily 15-min workflow — auto-picks next task | Runs the appropriate step |

---

## Cost per post

| Step | Service | Cost |
|------|---------|------|
| Research | Perplexity `sonar-deep-research` | ~$0.45 |
| Brief, write, SEO review | Claude Code | included |
| Publish | Sanity Content Lake API | $0.00 (250K req/mo free) |
| Indexing | IndexNow (Bing/Yandex/Seznam/Naver) | $0.00 |
| Images | Pillow / headless Chrome (local) | $0.00 |
| **Total** | | **~$0.45/post** |

| Approach | Cost per post | Time per post |
|---|---|---|
| **This pipeline** | **~$0.45** | **15-20 min (human review)** |
| Freelance writer | $100-500 | 3-5 days |
| SEO agency | $200-1,000 | 1-2 weeks |
| Pure AI generation (no review, no research) | ~$0.05 | 5 min, generic output |

Full breakdown in [config/api-setup.md](./config/api-setup.md).

---

## How this compares to AI visibility tools

This is a content **production** pipeline. It's complementary to AI **tracking** tools, not a replacement.

| Tool | Category | What it does |
|---|---|---|
| **content-seo-orchestrator** (this) | Production | Produces SEO/AEO-shaped posts and ships them |
| Profound / Peec / Promptwatch | Tracking | Tracks where you appear in LLM answers |
| AI Peekaboo | Tracking | Query AI visibility data via MCP |
| Purple Leaf | Readiness audit | Audits whether your existing pages are AI-ready |
| Asva AI | Production + tracking + agent visibility | Enterprise platform |

If you want to know whether you show up in ChatGPT, use a tracker. If you want to *make* the posts that get you cited, use this.

---

## SEO scoring (10 checks × 10 points = 100)

Keyword placement · keyword density · meta title · meta description · heading structure · content length · internal links · FAQ quality · readability · content quality.

A (90+) = publish-ready · B (80-89) = minor tweaks · C (70-79) = needs work · F (<60) = rewrite.

---

## Features at a glance

### Research
- Perplexity Deep Research API integration (`sonar-deep-research`, ~$0.45/post)
- Manual paste fallback if no API key
- Source URLs preserved on every stat extracted
- Cost tracking on every call

### Content
- Brand voice + tone driven by `config/seo-settings.yaml` — no hardcoded brand
- Brief-first writing (no draft until brief is approved)
- Multi-brand: keep one repo, swap settings per project (`config/seo-settings.example.yaml` ships with the Asva AI reference brand)
- Real examples enforced; hypotheticals banned

### Images
- `generate_covers.py` — branded 1200×630 covers via Pillow
- `generate-blog-images.py` — HTML→PNG via headless Chrome (hero + OG + Twitter + LinkedIn cards per post)
- Figma/FigJam infographics via Figma MCP (Mermaid → FigJam)

### Publishing (Sanity reference implementation)
- **Direct HTTP API**, not the Sanity MCP. Why: the MCP's `create_documents_from_json` overwrites your custom `_id` with a random UUID, breaking deterministic frontends. Direct curl preserves `_id` like `blogPost-<slug>`.
- IndexNow ping for Bing/Yandex/Seznam/Naver after live publish
- Pre-flight checks: SEO score gate, required-field validation, human confirmation

### Pluggable CMS
Sanity ships as the reference. Swap in WordPress / Contentful / Strapi / Webflow / Ghost by editing `.claude/commands/seo-publish.md`. Pipeline, briefs, writing, scoring, images stay CMS-agnostic.

---

## Architecture

```
your-project/
├── pipeline.yaml                  # All posts + status (single source of truth)
├── .env                           # API keys (gitignored)
├── config/
│   ├── seo-settings.yaml          # Your brand, CMS, SEO rules
│   ├── seo-settings.example.yaml  # Reference brand (Asva AI)
│   └── api-setup.md
├── templates/                     # Research brief, content brief, blog post, CMS payload
├── output/<slug>/                 # Per-post working dir (research → brief → draft → review → payload)
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

```bash
# 1. Clone
git clone https://github.com/viren040/content-seo-orchestrator.git
cd content-seo-orchestrator

# 2. Configure
cp .env.example .env
# Edit .env — at minimum: PERPLEXITY_API_KEY, SANITY_AUTH_TOKEN

# 3. Edit your brand
# config/seo-settings.yaml — brand.name, brand.website, sanity.project_id, voice, content_pillars

# 4. Add your posts to pipeline.yaml (see existing entries for shape)

# 5. (Optional Python deps for image generation)
python -m venv .venv && source .venv/bin/activate
pip install pyyaml pillow requests

# 6. In Claude Code:
/seo-status      # dashboard
/seo-daily       # auto-picks next post, runs next step, pauses at human gates
```

---

## Roadmap

Shipped:
- Perplexity Deep Research API
- Direct Sanity HTTP publishing (with the MCP `_id` workaround)
- IndexNow ping
- Cover + social image generators
- Multi-brand config

Confirmed next:
- `/seo-refresh` command — re-optimize live posts (close the impressions → clicks gap)
- DataForSEO MCP integration — automated keyword opportunity detection
- GSC API integration — impressions/CTR tracking inside the pipeline
- Cannibalization audit script
- Multi-language content (one source draft → localized variants)

Likely:
- WordPress / Contentful / Webflow publishers
- Rank tracking dashboard
- AI citation tracking (which LLMs cite the post)

Want one of these sooner? [Open a Discussion](https://github.com/viren040/content-seo-orchestrator/discussions) or send a PR. See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## License

MIT. See [LICENSE](./LICENSE). Use it, fork it, ship it. Stars and PRs appreciated.

---

Built with Claude Code by [Viren Inaniyan](https://linkedin.com/in/vireninaniyan) at [Asva AI](https://asvaai.com) / [Tru Commerce](https://trucommerce.ai).
