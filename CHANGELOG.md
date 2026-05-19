# Changelog

All notable changes to this project will be documented here. Format roughly follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] — 2026-05-19

First stable, publicly-shipped release. The pipeline is feature-complete for B2B SaaS, D2C ecommerce, local business, and agency content workflows.

### Added
- **`/seo-refresh` command** — re-optimize titles/meta/intro on already-published posts using GSC query data. Closes the impressions-to-clicks gap.
- **`examples/` directory** with 4 vertical starter pipelines:
  - `b2b-saas.pipeline.yaml`
  - `d2c-ecommerce.pipeline.yaml`
  - `local-business.pipeline.yaml`
  - `agency.pipeline.yaml`
- **`docs/` directory** with four deep-dive references:
  - `ARCHITECTURE.md` — how the slash commands chain, why slash-commands instead of a Python orchestrator
  - `COMPARISON.md` — feature matrix vs Profound, Peec, Promptwatch, AI Peekaboo, Purple Leaf
  - `AEO-SCORECARD.md` — the 10-check rubric, shareable as a standalone doc
  - `FAQ.md` — common setup and usage questions
- **`setup.sh`** one-shot bootstrap — cuts time-to-first-`/seo-status` to ~3 minutes
- **`CHANGELOG.md`** (this file)

### Changed
- README rewritten to lead with real GSC proof from a brand running this pipeline (131 → 964 impressions/day in 12 months, 7.3×; 18× monthly impressions; 51.8% of total impressions from blog content). Honest caveat on click growth.
- README now includes a comparison matrix vs alternatives so visitors place the tool correctly (production, not tracking).
- All `.claude/commands/*.md` use repo-relative paths — previously had hardcoded user paths.

## [0.3.0] — 2026-05-19

Public-template prep.

### Added
- `LICENSE` (MIT) as a proper file
- `CONTRIBUTING.md` + GitHub issue templates (bug, feature)
- `.github/social-card.png` — 1200×630 OG image for shares
- `.env.example` with all env vars documented (Perplexity, Sanity, IndexNow, DataForSEO, GSC)
- `config/seo-settings.example.yaml` — Asva AI reference brand kept as an example

### Changed
- Strip hardcoded user paths from `.claude/commands/*.md` — commands now read everything relative to repo root
- Move brand specifics (project_id, IndexNow key, CTA URLs, author name) out of code into `config/seo-settings.yaml` and `.env`
- Tighten `.gitignore` to block `SESSION-MEMORY.md`, brand-specific configs, GSC exports, credential files

### Repo metadata
- Description, topics (seo / aeo / geo / ai-seo / claude-code / etc.), homepage URL set on GitHub
- GitHub Discussions enabled

## [0.2.0] — 2026-03-26

Real-world usage iteration (Babblebots client work).

### Added
- Cover image generator (`generate_covers.py`) — branded 1200×630 PNGs via Pillow
- Per-post social image generator (`generate-blog-images.py`) — hero + OG + Twitter + LinkedIn cards via headless Chrome
- Direct Sanity HTTP API publishing (workaround for the Sanity MCP `_id` overwrite bug)
- IndexNow ping after live publish (Bing / Yandex / Seznam / Naver)
- 10-check SEO scorecard in `/seo-optimize`

## [0.1.0] — 2026-03-15

Initial commit.

### Added
- 7 slash commands: `/seo-status`, `/seo-research`, `/seo-brief`, `/seo-write`, `/seo-optimize`, `/seo-publish`, `/seo-daily`
- `pipeline.yaml` registry pattern
- `config/seo-settings.yaml` brand config pattern
- Templates: research brief, content brief, blog post, Sanity document
- Perplexity Deep Research API integration with manual paste fallback

---

[Unreleased]: https://github.com/viren040/content-seo-orchestrator/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/viren040/content-seo-orchestrator/releases/tag/v1.0.0
[0.3.0]: https://github.com/viren040/content-seo-orchestrator/compare/15b8e86...7ea5179
[0.2.0]: https://github.com/viren040/content-seo-orchestrator/compare/11282ff...15b8e86
[0.1.0]: https://github.com/viren040/content-seo-orchestrator/commit/11282ff
