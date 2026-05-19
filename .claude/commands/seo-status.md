# /seo-status — Content SEO Pipeline Dashboard

You are the pipeline dashboard for the Content SEO system.

## What to Do

1. **Read** the pipeline registry at `./pipeline.yaml`

2. **Display a status table** showing all posts with their pipeline progress:

```
| # | Post Title (truncated) | Slug | KD | IMG | DIA | RES | BRF | WRT | OPT | DFT | PUB |
|---|----------------------|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
```

Where columns are:
- IMG = Images | DIA = Diagrams | RES = Research | BRF = Brief | WRT = Content | OPT = SEO Review | DFT = CMS Draft | PUB = Published
- Use "done" for done, "pending" for pending, "in-progress" for in-progress

3. **Show summary stats:**
   - Total posts: X
   - Fully published: X
   - Next up: [Post title] (KD X) — next step: [step name]
   - Pipeline completion: X%

4. **Auto-suggest the next action:**
   - Find the post with the lowest `publish_order` that has incomplete steps
   - Identify which step is next (first `pending` step after all `done` steps)
   - Suggest the exact command: `/seo-research <slug>` or `/seo-brief <slug>` etc.

5. **Sort by publish_order** (lowest KD first = fastest wins)

## Output Format

Present as a clean, scannable dashboard. The user should know in 5 seconds:
- Where the pipeline stands overall
- What to do next
- How much is left

## Rules
- Read-only — never modify pipeline.yaml
- If all posts are published, congratulate and suggest next phase (technical SEO, rank tracking, content refresh)
