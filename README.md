# Content SEO Orchestrator

> A Claude Code–native content SEO pipeline. **Research → Brief → Write → SEO Score → Publish → IndexNow** in **15 min/day** at **~$0.45/post**. MIT-licensed. Fork it, adapt it, ship it.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-D97757)](https://claude.com/claude-code)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![Discussions](https://img.shields.io/badge/Discussions-open-blue)](https://github.com/viren040/content-seo-orchestrator/discussions)
[![Release](https://img.shields.io/badge/release-v1.0.0-success)](./CHANGELOG.md)

**What's new in v1.0.0 (2026-05-19)**: 4 vertical starter pipelines (B2B SaaS, D2C, local biz, agency) · `/seo-refresh` command · standalone [AEO Scorecard](./docs/AEO-SCORECARD.md) · [feature comparison](./docs/COMPARISON.md) vs Profound/Peec/AI Peekaboo · one-shot `setup.sh` · full [CHANGELOG](./CHANGELOG.md).

## Table of contents

- [Real-world result](#real-world-result)
- [What this is](#what-this-is)
- [Why this exists](#why-this-exists)
- [Commands](#commands)
- [Cost per post](#cost-per-post)
- [How this compares to alternatives](#how-this-compares-to-ai-visibility-tools)
- [Features at a glance](#features-at-a-glance)
- [Architecture](#architecture)
- [Quick start](#quick-start)
- [Starter pipelines by vertical](#starter-pipelines-by-vertical)
- [Roadmap](#roadmap)
- [Docs deep-dives](#docs-deep-dives)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

---

## Real-world result

One brand we run this pipeline for went from **131 → 964 avg impressions/day** in 12 months — **a 7.3× lift**. Monthly impressions went from **2,142 → 39,240 (18× growth)**. Blog content produced by this orchestrator accounted for **51.8% of all impressions** (126,829 of 244,861) across 119 posts.

Honest caveat: clicks didn't grow proportionally over this window — CTR dropped because new content ranked but the title/meta layer hadn't been tuned yet. That gap is now closed by the new [`/seo-refresh` command](./.claude/commands/seo-refresh.md) which re-optimizes live posts using GSC data.

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

A 7-step content SEO pipeline that runs as Claude Code slash commands, with 4 human gates so you stay in control of the high-judgment calls.

```
Research → Brief → Write → SEO Score → Cover/Diagrams → Publish → IndexNow → Refresh
   GATE     GATE    GATE                                  GATE                 GATE
```

You handle: research angle, brief approval, copy voice, publish decision, refresh decision.
The pipeline handles: structure, templates, SEO scoring, image generation, CMS publishing, instant indexing, CTR optimization.

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
| `/seo-research <slug>` | Perplexity Deep Research API (with manual paste fallback) | Yes |
| `/seo-brief <slug>` | Generates content brief from research | Yes |
| `/seo-write <slug>` | Writes full blog post from brief, in brand voice | Yes |
| `/seo-optimize <slug>` | 10-check SEO quality score (0-100) with fix suggestions | No |
| `/seo-publish <slug>` | Pushes to CMS as draft or live, pings IndexNow | Yes |
| `/seo-refresh <slug>` | Re-optimizes title/meta/intro on live posts using GSC data | Yes |
| `/seo-daily` | Daily 15-min workflow — auto-picks next task | Runs appropriate step |

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
| AI Peekaboo | Tracking + MCP/API | Query AI visibility data via MCP |
| Purple Leaf | Readiness audit | Audits whether your existing pages are AI-ready |
| Asva AI | Production + tracking + agent visibility | Enterprise platform |

If you want to know whether you show up in ChatGPT, use a tracker. If you want to *make* the posts that get you cited, use this. **Full feature matrix**: [docs/COMPARISON.md](./docs/COMPARISON.md).

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

### SEO + AEO scoring
- 10-check rubric (see [docs/AEO-SCORECARD.md](./docs/AEO-SCORECARD.md))
- Scores for both SERP rank and LLM citation likelihood
- Specific fix suggestions when score < 80

### Images
- `generate_covers.py` — branded 1200×630 covers via Pillow
- `generate-blog-images.py` — HTML→PNG via headless Chrome (hero + OG + Twitter + LinkedIn cards per post)
- Figma/FigJam infographics via Figma MCP (Mermaid → FigJam)

### Publishing (Sanity reference implementation)
- **Direct HTTP API**, not the Sanity MCP. Why: the MCP's `create_documents_from_json` overwrites your custom `_id` with a random UUID, breaking deterministic frontends. Direct curl preserves `_id` like `blogPost-<slug>`.
- IndexNow ping for Bing/Yandex/Seznam/Naver after live publish
- Pre-flight checks: SEO score gate, required-field validation, human confirmation

### Refresh / CTR optimization
- `/seo-refresh` reads GSC data, diagnoses high-impressions/low-CTR pages, proposes title/meta/intro changes
- Categorizes the problem (title mismatch vs intent drift vs position-floor) so you know what kind of fix to apply

### Pluggable CMS
Sanity ships as the reference. Swap in WordPress / Contentful / Strapi / Webflow / Ghost by editing `.claude/commands/seo-publish.md`. Pipeline, briefs, writing, scoring, images stay CMS-agnostic.

---

## Architecture

Full deep-dive: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md).

```
your-project/
├── pipeline.yaml                  # All posts + status (single source of truth)
├── .env                           # API keys (gitignored)
├── config/
│   ├── seo-settings.yaml          # Your brand, CMS, SEO rules
│   ├── seo-settings.example.yaml  # Reference brand (Asva AI)
│   └── api-setup.md
├── templates/                     # Research brief, content brief, blog post, CMS payload
├── examples/                      # Starter pipelines by vertical
│   ├── b2b-saas.pipeline.yaml
│   ├── d2c-ecommerce.pipeline.yaml
│   ├── local-business.pipeline.yaml
│   └── agency.pipeline.yaml
├── docs/                          # Deep-dive references
│   ├── ARCHITECTURE.md
│   ├── COMPARISON.md
│   ├── AEO-SCORECARD.md
│   └── FAQ.md
├── output/<slug>/                 # Per-post working dir
├── covers/                        # 1200x630 branded covers
├── blog-images/<slug>/            # Per-post social images
├── infographics/                  # FigJam diagram exports
├── generate_covers.py             # Pillow cover generator
├── generate-blog-images.py        # HTML→PNG social card generator
├── setup.sh                       # One-shot bootstrap
└── .claude/commands/              # The /seo-* slash commands
```

---

## Quick start

**Fastest path** (~3 minutes):

```bash
git clone https://github.com/viren040/content-seo-orchestrator.git
cd content-seo-orchestrator
./setup.sh
```

The bootstrap script creates a venv, installs deps, copies `.env.example → .env`, and walks you through what to edit next.

**Manual path** (if you'd rather):

```bash
# 1. Clone
git clone https://github.com/viren040/content-seo-orchestrator.git
cd content-seo-orchestrator

# 2. Configure
cp .env.example .env
# Edit .env — at minimum: PERPLEXITY_API_KEY, SANITY_AUTH_TOKEN

# 3. Edit your brand
# config/seo-settings.yaml — brand.name, brand.website, sanity.project_id, voice, content_pillars

# 4. Pick a starter pipeline
cp examples/b2b-saas.pipeline.yaml pipeline.yaml
# (or d2c-ecommerce / local-business / agency)

# 5. (Optional Python deps for image generation)
python -m venv .venv && source .venv/bin/activate
pip install pyyaml pillow requests

# 6. In Claude Code:
/seo-status      # dashboard
/seo-daily       # auto-picks next post, runs next step, pauses at human gates
```

---

## Starter pipelines by vertical

Four pre-built `pipeline.yaml` files in [`examples/`](./examples/), each with 8 starter posts:

| Vertical | File | What it covers |
|---|---|---|
| **B2B SaaS** | [`b2b-saas.pipeline.yaml`](./examples/b2b-saas.pipeline.yaml) | Product-led content, comparisons, feature explainers, category education |
| **D2C ecommerce** | [`d2c-ecommerce.pipeline.yaml`](./examples/d2c-ecommerce.pipeline.yaml) | Buying guides, product comparisons, sizing/usage, AI shopping visibility |
| **Local business** | [`local-business.pipeline.yaml`](./examples/local-business.pipeline.yaml) | "[Service] in [city]", pricing/timeline FAQs, neighborhood guides |
| **Agency / consultancy** | [`agency.pipeline.yaml`](./examples/agency.pipeline.yaml) | Methodology, case studies, tool comparisons, founder-voice contrarian |

Copy the closest fit to `./pipeline.yaml`, edit slugs/keywords/internal links, run `/seo-status`.

---

## Roadmap

Shipped in v1.0.0:
- Perplexity Deep Research API
- Direct Sanity HTTP publishing (with the MCP `_id` workaround)
- IndexNow ping
- Cover + social image generators
- Multi-brand config
- `/seo-refresh` for CTR re-optimization
- 4 starter pipelines by vertical
- AEO Scorecard (10-check rubric)

Confirmed next:
- DataForSEO MCP integration — automated keyword opportunity detection
- GSC API integration — automatic data fetch for `/seo-refresh`
- Cannibalization audit script
- Multi-language content (one source draft → localized variants)

Likely:
- WordPress / Contentful / Webflow publishers (PRs welcome)
- Rank tracking dashboard
- AI citation tracking (which LLMs cite the post)

Want one of these sooner? [Open a Discussion](https://github.com/viren040/content-seo-orchestrator/discussions) or send a PR. See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Docs deep-dives

| Doc | What it covers |
|---|---|
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | How the slash commands chain; why slash-commands instead of a Python orchestrator; how to extend |
| [docs/COMPARISON.md](./docs/COMPARISON.md) | Feature matrix vs Profound, Peec, Promptwatch, AI Peekaboo, Purple Leaf |
| [docs/AEO-SCORECARD.md](./docs/AEO-SCORECARD.md) | The 10-check rubric, shareable as a standalone doc |
| [docs/FAQ.md](./docs/FAQ.md) | Common setup + usage questions |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | How to contribute (especially looking for: WordPress publisher, DataForSEO integration) |

---

## FAQ

A few quick answers; full FAQ in [docs/FAQ.md](./docs/FAQ.md).

**Is it really $0.45/post?** Yes — that's the marginal API cost per post (one Perplexity Deep Research call). You also need a Claude Code subscription, which you presumably have if you're reading this. CMS publishing is free tier. IndexNow is free.

**Do I need to use Claude Code?** Yes — the slash commands run inside Claude Code. Porting to another LLM client would be straightforward (each command is just a markdown prompt), but we don't ship one.

**Do I need Sanity?** No — Sanity is the reference CMS. Edit one file (`.claude/commands/seo-publish.md`) to swap to WordPress / Contentful / Strapi / Webflow / Ghost.

**Can I run this for multiple clients?** Yes — fork the repo per client. Each gets its own `config/seo-settings.yaml` + `pipeline.yaml`. See FAQ for details.

**What if I don't want to pay the Perplexity API cost?** `/seo-research` has a manual paste fallback. Print the prompt → copy into Perplexity web UI → paste response back. Same end result, just slower.

---

## Contributing

PRs welcome. Highest-value contributions right now:
- WordPress publisher (`.claude/commands/seo-publish.md` port to WP REST API)
- Contentful / Webflow / Ghost publishers
- DataForSEO MCP integration in `/seo-research`
- Localization workflow (one source draft → multi-language)

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines. Open a [Discussion](https://github.com/viren040/content-seo-orchestrator/discussions) before large changes.

---

## License

MIT. See [LICENSE](./LICENSE). Use it, fork it, ship it. Stars and PRs appreciated.

---

Built with Claude Code by [Viren Inaniyan](https://linkedin.com/in/vireninaniyan) at [Asva AI](https://asvaai.com) / [Tru Commerce](https://trucommerce.ai).
