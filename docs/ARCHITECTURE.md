# Architecture

How the pipeline actually works. Useful if you want to fork, extend, or debug.

## The mental model

The orchestrator is a **stateless chain of slash commands** with **file-based state**. There's no daemon, no database, no API server. Every command:

1. Reads `pipeline.yaml` + the relevant files in `output/<slug>/`
2. Performs one step
3. Writes its output to `output/<slug>/`
4. Updates the post's `status` field in `pipeline.yaml`
5. Exits

Because all state lives in files, you can interrupt at any point and resume with no loss. You can also work on different posts in parallel — each lives in its own `output/<slug>/` directory.

## Directory layout (state)

```
your-repo/
├── pipeline.yaml                  # Post registry + status (the orchestrator's database)
├── config/seo-settings.yaml       # Brand + voice + SEO rules
├── output/
│   └── <slug>/                    # Per-post state
│       ├── research.md            # /seo-research output
│       ├── research-raw.json      # raw Perplexity API response
│       ├── brief.md               # /seo-brief output
│       ├── draft.md               # /seo-write output
│       ├── seo-review.md          # /seo-optimize output
│       ├── sanity-payload.json    # /seo-publish staged payload
│       └── published.json         # /seo-publish confirmation
└── .claude/commands/              # The slash commands themselves
    ├── seo-status.md
    ├── seo-research.md
    ├── seo-brief.md
    ├── seo-write.md
    ├── seo-optimize.md
    ├── seo-publish.md
    ├── seo-refresh.md             # CTR/title/meta refresh on live posts
    └── seo-daily.md               # Orchestrator (picks next task)
```

## The chain

```
pipeline.yaml                        config/seo-settings.yaml
       │                                       │
       └──────────────┬────────────────────────┘
                      │
                      ▼
              /seo-status        ◀── dashboard, read-only
                      │
                      ▼
              /seo-daily         ◀── picks the next pending step
                      │
        ┌─────────────┴──────────────────────────┐
        ▼                                        ▼
  /seo-research                          (if research already done)
  Perplexity API                         /seo-brief
  $0.45 cost                             reads research → brief
  human gate ◀── review prompt           human gate ◀── approve brief
        │                                        │
        ▼                                        ▼
  output/<slug>/research.md             output/<slug>/brief.md
        │                                        │
        └─────────────────┬──────────────────────┘
                          ▼
                    /seo-write
                    reads brief + research → draft
                    human gate ◀── review draft
                          │
                          ▼
                  output/<slug>/draft.md
                          │
                          ▼
                   /seo-optimize
                   10-check scorecard, no gate
                          │
                          ▼
                output/<slug>/seo-review.md
                          │
                          ▼
                   /seo-publish
                   builds CMS payload
                   human gate ◀── confirm publish
                          │
                          ▼
                   Sanity HTTP API + IndexNow ping
                          │
                          ▼
                output/<slug>/published.json
                          │
                          ▼
                  (optional, weeks later)
                   /seo-refresh
                   reads GSC → refreshes title/meta on live posts
```

## Slash commands in detail

Each command is a markdown file in `.claude/commands/` with three sections:

1. **What to do** — step-by-step instructions for Claude
2. **Input files** — what to read
3. **Output files** — what to write + how to update pipeline.yaml

### Why slash commands instead of a Python orchestrator

Three reasons:

1. **The LLM is the orchestrator**, not a wrapper around it. The slash command files are prompts; Claude reads them and acts. Adding a feature = editing markdown, not writing Python.
2. **Human gates are baked in**. After each step, the command pauses and asks the user. A Python script would either skip gates (bad output) or fake them (worse output).
3. **Stateless re-entry**. Because all state is files, you can stop mid-pipeline and pick up tomorrow with `/seo-daily`. Python orchestrators tend to have in-memory state that complicates this.

## How brand voice is injected

`config/seo-settings.yaml` has a `content_rules` block:

```yaml
content_rules:
  voice: "Precise, Confident, Useful"
  brand_pillars:
    - "Pillar 1 — short descriptor"
    - "..."
  tone_guidelines:
    - "No fluff — every sentence earns its place"
    - "..."
```

Every command that produces content (`/seo-brief`, `/seo-write`) reads this YAML and applies it. No hardcoded brand voice in any command. Forking the repo + editing this YAML = running your brand.

## Pluggable CMS

The default `/seo-publish` ships with a Sanity HTTP implementation. To swap CMS:

1. Open `.claude/commands/seo-publish.md`
2. Replace the curl block with your CMS's API call
3. Adjust the JSON payload to match your CMS schema
4. Update `templates/sanity-document.json` to your CMS shape (and rename it)

Other commands are CMS-agnostic.

## The Sanity `_id` workaround

If you use Sanity, note: the Sanity MCP's `create_documents_from_json` ignores your custom `_id` and generates a random UUID. Most frontends query by deterministic IDs (e.g. `blogPost-<slug>`), so MCP-published documents show "Post not found".

The fix is in `.claude/commands/seo-publish.md`: we use Sanity's direct HTTP mutation endpoint (`POST /v2021-06-07/data/mutate/<dataset>`) which preserves the `_id` field. Documented inline.

## Cost model

| Cost | When | How much |
|---|---|---|
| Perplexity Deep Research | `/seo-research` | ~$0.45 per post |
| Claude Code | `/seo-brief`, `/seo-write`, `/seo-optimize` | included in your Claude Code plan |
| Sanity Content Lake | `/seo-publish` | free tier (250K reqs/mo) |
| IndexNow | `/seo-publish` | free |
| Total | per post | ~$0.45 |

If you don't want to pay the Perplexity API cost, `/seo-research` falls back to manual paste mode — you run the prompt in Perplexity yourself and paste the response. Same end result, just slower.

## Extending the pipeline

Common extensions and where to plug them in:

| Want to add | Edit |
|---|---|
| New CMS | `.claude/commands/seo-publish.md` |
| Different research source (Tavily, Exa, etc.) | `.claude/commands/seo-research.md` |
| Extra SEO check | `.claude/commands/seo-optimize.md` |
| New image style | `generate_covers.py` |
| New language voice | `config/seo-settings.yaml` (clone the file per language) |
| Pre-publish review step | New `.claude/commands/seo-review.md`, called from `/seo-daily` |

## What's NOT in here

We deliberately don't ship:

- A web UI (the pipeline runs in Claude Code; that's the UI)
- A cloud-hosted version (defeats the local-first design)
- A database (filesystem is the database)
- Multi-user / multi-tenant logic (one repo = one brand; fork per brand)
- Realtime sync (filesystem + git is the sync mechanism)

If you want any of these, fork it — there's no "platform" you'd be working against.

## Questions

Open a [Discussion](https://github.com/viren040/content-seo-orchestrator/discussions) — happy to talk through architecture decisions, alternative designs, or specific extensions.
