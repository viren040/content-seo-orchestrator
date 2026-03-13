# Content SEO Orchestrator

A Claude Code-native content SEO pipeline that takes blog posts from research to published — with human-in-the-loop at every decision point.

Built for [Asva AI](https://asvaai.com) by [Viren Inaniyan](https://linkedin.com/in/vireninaniyan). Open source for anyone to fork and adapt.

---

## What This Does

```
Research → Brief → Write → SEO Score → Publish
   🔒        🔒      🔒                   🔒
```

6-step pipeline with 4 human gates (🔒). You stay in control of research quality, content angle, final copy, and publish decision. The system handles structure, templates, SEO scoring, and CMS publishing.

**Daily time commitment: 15-20 minutes.**

---

## Architecture

```
your-project/
├── pipeline.yaml                  # Single source of truth — all posts + status
├── config/
│   └── seo-settings.yaml          # Brand, CMS, SEO rules
├── templates/
│   ├── research-brief.md          # Research output structure
│   ├── content-brief.md           # Writing brief structure
│   ├── blog-post.md               # Post template (CMS-ready)
│   └── sanity-document.json       # CMS payload template
├── output/
│   └── <slug>/                    # Per-post working directory
│       ├── research.md            # Step 1 output
│       ├── brief.md               # Step 2 output
│       ├── draft.md               # Step 3 output
│       ├── seo-review.md          # Step 4 output
│       ├── sanity-payload.json    # Step 5 output
│       └── published.json         # Step 6 confirmation
├── .claude/commands/              # Claude Code slash commands
│   ├── seo-status.md
│   ├── seo-research.md
│   ├── seo-brief.md
│   ├── seo-write.md
│   ├── seo-optimize.md
│   ├── seo-publish.md
│   └── seo-daily.md
└── README.md
```

---

## Commands

| Command | What It Does | Human Gate |
|---------|-------------|------------|
| `/seo-status` | Pipeline dashboard — see all posts, completion %, next task | No |
| `/seo-research <slug>` | Presents research prompt, structures Perplexity output | Yes — paste research |
| `/seo-brief <slug>` | Generates content brief from research | Yes — approve brief |
| `/seo-write <slug>` | Writes full blog post from brief | Yes — review draft |
| `/seo-optimize <slug>` | SEO quality score (0-100) with fix suggestions | No |
| `/seo-publish <slug>` | Pushes to CMS as draft or live | Yes — confirm publish |
| `/seo-daily` | Daily 15-min workflow — auto-picks next task | Runs appropriate step |

---

## Quick Start

### 1. Fork & Configure

```bash
# Clone
git clone https://github.com/your-org/content-seo-orchestrator.git
cd content-seo-orchestrator

# Edit pipeline.yaml — add your blog posts
# Edit config/seo-settings.yaml — set your brand, CMS, SEO rules
```

### 2. Add Your Posts to `pipeline.yaml`

```yaml
posts:
  - id: "1.1"
    title: "Your Blog Post Title"
    slug: "your-blog-post-slug"
    primary_keyword: "target keyword"
    keyword_volume: 1000
    keyword_difficulty: 15
    word_count_target: 1800
    publish_order: 1
    status:
      research: pending
      brief: pending
      content: pending
      seo_review: pending
      published: pending
```

### 3. Run Daily

```
/seo-daily
```

The orchestrator picks the next post, runs the next step, and pauses at human gates.

---

## Adapting for Your CMS

This system ships with Sanity CMS integration. To use a different CMS:

1. **Edit `templates/sanity-document.json`** → rename and restructure for your CMS schema
2. **Edit `.claude/commands/seo-publish.md`** → replace Sanity MCP calls with your CMS API/MCP
3. **Keep everything else** — the pipeline, templates, and other commands are CMS-agnostic

### Supported CMS integrations (via MCP):
- **Sanity** — built-in
- **WordPress** — use WordPress MCP
- **Contentful** — use Contentful MCP
- **Strapi** — use Strapi MCP
- **Headless** — any CMS with an API

---

## Pipeline Flow

```
Step 1: /seo-research        Step 2: /seo-brief         Step 3: /seo-write
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Run Perplexity   │    │ Search intent    │    │ Full blog post   │
│ research prompt  │───▶│ SEO metadata     │───▶│ Brand voice      │
│ Structure output │    │ Content outline  │    │ FAQs + links     │
│ 🔒 Human: paste  │    │ 🔒 Human: approve│    │ 🔒 Human: review │
└──────────────────┘    └──────────────────┘    └──────────────────┘
                                                         │
Step 6: /seo-publish      Step 5: (optional)      Step 4: /seo-optimize
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Build CMS payload│    │ Edit based on    │    │ 10-point SEO     │
│ Push to CMS      │◀───│ SEO feedback     │◀───│ quality audit    │
│ Verify published │    │                  │    │ Score 0-100      │
│ 🔒 Human: confirm│    └──────────────────┘    │ Auto — no gate   │
└──────────────────┘                            └──────────────────┘
```

---

## SEO Scoring (10 checks × 10 points = 100)

| Check | What It Measures |
|-------|-----------------|
| Keyword Placement | Primary KW in H1, intro, H2, meta title, meta desc |
| Keyword Density | 1-2% target, flag stuffing or thin |
| Meta Title | Length (50-60 chars), includes KW, click-worthy |
| Meta Description | Length (150-160 chars), includes KW + CTA |
| Heading Structure | H1 → H2 → H3 hierarchy, min 4 H2s |
| Content Length | Actual vs. target word count |
| Internal Links | Min 3, descriptive anchors, CTA link |
| FAQ Quality | 3-6 pairs, genuine queries, KW inclusion |
| Readability | Short paragraphs, bullets/tables, scannable |
| Content Quality | Data-backed, real examples, no fluff |

**Grading**: A (90+) = publish-ready | B (80-89) = minor tweaks | C (70-79) = needs work | F (<60) = rewrite

---

## Tech Stack

- **Orchestration**: Claude Code (slash commands)
- **Research**: Perplexity AI (manual, pasted in)
- **Content**: Claude (writes from brief)
- **SEO Data**: Ahrefs / DataForSEO (keyword research)
- **CMS**: Sanity (via MCP)
- **Images**: Python script (HTML → PNG via Chrome)
- **Diagrams**: Figma/FigJam (via MCP)

---

## Contributing

1. Fork this repo
2. Add your improvements (new commands, CMS integrations, scoring checks)
3. Submit a PR

Ideas for contribution:
- WordPress/Contentful/Strapi publish commands
- Automated keyword research via DataForSEO MCP
- AI search visibility tracking integration
- Multi-language content pipeline
- Client/project isolation for agencies

---

## License

MIT — use it, fork it, sell it, whatever. Credit appreciated.

---

Built with Claude Code by [Asva AI](https://asvaai.com)
