# FAQ

## General

### What is this exactly?
A 7-slash-command pipeline that runs in Claude Code. It takes a blog post from research idea to live publication, with 4 human review gates. The output is markdown drafts plus auto-published CMS documents. See [README](../README.md) for the full overview.

### Who is this for?
Solo founders, small marketing teams, agencies running content for clients, and SEO/AEO practitioners who want a systematic pipeline they own and can fork. If you'd rather use a hosted tool, see the [comparison](./COMPARISON.md) — Profound / Peec / Promptwatch / AI Peekaboo are decent.

### Is it really $0.45/post?
That's the per-post API cost (one Perplexity Deep Research call). You also need a Claude Code subscription. CMS publishing is on Sanity's free tier. IndexNow is free. Cover images run locally with Pillow. So: ~$0.45 in marginal API cost per post, plus your Claude Code subscription.

### Do I need to use Claude Code?
Yes — the orchestrator is a set of `.claude/commands/*.md` slash commands. They run inside Claude Code. If you want to run this outside Claude Code, you'd need to port the commands to your LLM client of choice (it's not hard; each command is a prompt).

### What does "AEO" mean?
Answer Engine Optimization — optimizing content for inclusion in answers from ChatGPT, Perplexity, Google AI Overviews, etc. Distinct from SEO (optimizing for SERP rank). See the [AEO Scorecard](./AEO-SCORECARD.md) for the specific differences.

---

## Setup

### How long does first-time setup take?
~15 minutes if you already have Claude Code + a Sanity project. ~30-45 minutes if you also need to spin up Sanity from scratch.

### Do I need Sanity?
No — Sanity is the reference CMS implementation. You can swap to WordPress, Contentful, Strapi, Webflow, or any other CMS by editing one file (`.claude/commands/seo-publish.md`). PRs for additional CMS publishers welcome.

### Do I need the Perplexity API?
No — `/seo-research` has a manual paste fallback. If `PERPLEXITY_API_KEY` is unset, it prints the research prompt for you to copy into Perplexity's web UI, then accepts the pasted response. Same end result, just slower.

### Can I run this without a CMS?
Yes — skip `/seo-publish` and you'll get markdown drafts in `output/<slug>/draft.md`. Use them however you want.

### What permissions does my Sanity API token need?
The publish command needs write scope. Either `Editor` role (recommended) or `Deploy Studio Administrator` works. Generate at sanity.io/manage → your project → API → Tokens.

---

## Usage

### What's the daily workflow?
`/seo-daily` picks the next pending step from `pipeline.yaml` and runs it. Default mode is "one step per day" — research today, brief tomorrow, write the day after, etc. If you want to batch multiple steps, say "let's batch" or "sprint" and the orchestrator keeps going.

### Can I work on multiple posts in parallel?
Yes. Each post has its own `output/<slug>/` directory. You can have post A in `/seo-write` while post B is in `/seo-research`.

### What if I want to override Claude's output?
The 4 human gates are exactly for this. After each step, the orchestrator pauses and asks you to confirm or revise. Edit the output file (`brief.md`, `draft.md`, etc.) directly, then say "continue" and the next step picks up your edits.

### How do I update an already-published post?
Use `/seo-refresh <slug>`. It reads the live post, fetches recent GSC data (if `GSC_SERVICE_ACCOUNT` is configured), and proposes title/meta/intro changes to improve CTR. Then `/seo-publish` again to push the update.

### What's the human gate cadence?
- `/seo-research` — review the research prompt + cost before the API call
- `/seo-brief` — approve the brief before writing
- `/seo-write` — review the draft before SEO scoring
- `/seo-publish` — confirm draft-vs-live and confirm the final payload

Gates take ~30 seconds each. Don't skip them — the output quality drops noticeably if you do.

---

## Multi-brand / agency use

### Can I run this for multiple clients?
Yes. Two patterns:

1. **One repo per client** (recommended) — clone the orchestrator for each client; each has its own `config/seo-settings.yaml` + `pipeline.yaml`.
2. **One repo with branching** — keep one fork, swap `config/seo-settings.yaml` per client. Use git branches per client.

Pattern 1 is cleaner because each client's output history stays in their repo.

### Does it work for non-English content?
The pipeline is language-agnostic. The voice / tone / examples in `config/seo-settings.yaml` drive the language. You can run it for German, Hindi, Portuguese, etc. — the Perplexity research step also supports multiple languages via the `search_recency_filter` and prompt language.

### Can I white-label this for clients?
Yes — MIT license. Strip references, rebrand, charge whatever you want. Credit appreciated but not required.

---

## Cost / pricing

### Why $0.45/post?
That's roughly the cost of one Perplexity `sonar-deep-research` call: input + output + citations + reasoning + search. We've seen it range $0.30-$0.65 depending on the depth of research.

### Can I lower the cost further?
Yes — switch the research model in `.claude/commands/seo-research.md` to `sonar-pro` (~$0.10-0.15/query) or `sonar` (~$0.02-0.05/query). Quality drops noticeably with `sonar`. `sonar-pro` is the cheap-but-decent middle ground.

### What's the cost compared to a freelance writer?
Per post: ~$0.45 vs $100-500 for a freelancer or $200-1,000 for an agency. Per-month at 10 posts: ~$4.50 vs ~$1,000-$5,000. The catch is your time — you still spend 15-20 min/post on review gates. If your time is worth more than freelance rates, this tilts in favor of hiring.

---

## Troubleshooting

### Why does my Sanity doc show "Post not found"?
The Sanity MCP's `create_documents_from_json` overwrites your custom `_id` with a UUID, but most frontends query by deterministic IDs like `blogPost-<slug>`. Use the direct HTTP curl pattern in `.claude/commands/seo-publish.md` instead — it preserves `_id`. This is the most common gotcha.

### Why are my SEO scores low?
Common causes:
- Brief skipped step (no clear keyword strategy)
- Draft is too short (under 80% of `word_count_target`)
- Missing FAQ section (this is now AEO-required, not optional)
- Generic anchor text on internal links

Run `/seo-optimize` and the report tells you exactly what's missing.

### Why aren't my IndexNow pings working?
Three checks:
1. Is `INDEXNOW_KEY` set in `.env`?
2. Is the file `{INDEXNOW_KEY}.txt` hosted at `https://yourdomain.com/{INDEXNOW_KEY}.txt`?
3. Does it return HTTP 200 when you curl it? If 404, the publisher can't verify the key.

### My Perplexity calls are returning empty
Three checks:
1. `PERPLEXITY_API_KEY` set?
2. Account has credits? (Check console.perplexity.ai → Usage)
3. Are you hitting rate limit? (50 RPM)

If all yes, try switching to `sonar-pro` temporarily to confirm the issue is `sonar-deep-research` specific (which has been flaky in early 2026).

---

## Roadmap / contributions

### When will WordPress be supported?
Looking for a PR. Should be a ~2-hour port of `.claude/commands/seo-publish.md` to use the WP REST API instead of Sanity. See [CONTRIBUTING.md](../CONTRIBUTING.md).

### Will you build a hosted/SaaS version?
No. The local-first, Claude-Code-native design is the value proposition. A hosted version would defeat the point — you'd be locked into our infrastructure instead of owning your pipeline.

### How can I contribute?
Open a Discussion first if it's > 30 min of work. PRs welcome for: new CMS publishers, keyword research integrations (DataForSEO, Ahrefs), additional language packs, alternative research sources, bug fixes, doc improvements.

---

Last updated: 2026-05-19. Missing a question? [Open a Discussion](https://github.com/viren040/content-seo-orchestrator/discussions) and we'll add it.
