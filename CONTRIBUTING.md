# Contributing

Thanks for considering a contribution. This project is small and opinionated — the goal is to keep the pipeline tight, not to be every-thing-to-every-CMS.

## What we'd love help with

- **New CMS publishers** — WordPress, Contentful, Strapi, Webflow, Ghost (mirror `.claude/commands/seo-publish.md`)
- **Keyword research integrations** — DataForSEO MCP, Ahrefs, Semrush (extend `/seo-research`)
- **Image generators** — Canva API, better Figma plugins, alternative cover styles
- **Rank/citation tracking** — post-publish dashboards that close the loop
- **Localization** — one source draft -> multiple language variants
- **Bug fixes + docs** — always welcome

## What we won't merge

- Cloud-hosted "platform" wrappers — the point is local-first, Claude Code-native
- Removal of the human gates — those are load-bearing on quality
- Hard dependencies on a specific brand/CMS in the core commands

## Workflow

1. Open an issue first if it's > 30 min of work — saves us both time aligning
2. Fork → branch → PR
3. Keep PRs small and focused. One feature/fix per PR.
4. Test on a clean fork — clone the repo into a new dir and walk through Quick Start
5. Update README if you're adding a new command, env var, or CMS

## Code style

- Python scripts use stdlib + a tiny set of deps (Pillow, requests, pyyaml). Don't add heavy frameworks.
- `.claude/commands/*.md` files should read paths relative to repo root (no `/Users/...`)
- Brand-specific values belong in `config/seo-settings.yaml`, never in command files

## Questions / proposals

Open a [Discussion](https://github.com/viren040/content-seo-orchestrator/discussions) for anything you want to talk through before opening a PR.
