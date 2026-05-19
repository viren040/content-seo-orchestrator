# /seo-refresh — Refresh a Live Post for CTR

You are the refresh agent for the Content SEO pipeline. This command runs on **already-published** posts and proposes title/meta/intro updates to close the gap between impressions and clicks.

**Argument:** `$ARGUMENTS` (the blog post slug)

## When to use this

After a post has been live for **≥30 days**. By then GSC has enough data to know:
- Which queries the post is ranking for
- Which queries get impressions but no clicks (the refresh opportunity)
- Whether the post's existing meta title/desc match user intent

Most pipelines ship content but never refresh it. The original `/seo-write` step optimizes for *being relevant to the query*; this command optimizes for *winning the click* once you're already ranking.

## What to Do

### Step 1: Load Context
All paths below are relative to the repo root.

1. Read `./pipeline.yaml` — find the post matching the slug. Confirm `status.published: done`.
2. Read `./output/{{SLUG}}/draft.md` — the current live content + frontmatter
3. Read `./output/{{SLUG}}/published.json` — confirm canonical URL + publish date
4. Read `./config/seo-settings.yaml` — load brand voice + CTA URL

If `status.published` is not `done`, stop and tell the user: "Post not published yet. Use `/seo-publish {{SLUG}}` first."

### Step 2: Pull GSC data (if configured)

If `GSC_SERVICE_ACCOUNT` env var is set and points to a valid service-account JSON, fetch last 28 days of query/page data for this post's canonical URL:

```bash
# Pseudocode — real implementation in scripts/fetch_gsc.py (TODO)
python scripts/fetch_gsc.py \
  --service-account "$GSC_SERVICE_ACCOUNT" \
  --site "$GSC_SITE_URL" \
  --page "https://yourdomain.com/blog/{{SLUG}}" \
  --days 28
```

If GSC isn't configured, fall back to manual mode: ask the user to paste the GSC export for this URL's queries (CSV or table).

The data you need per query:
- Query text
- Impressions
- Clicks
- CTR
- Avg position

### Step 3: Diagnose

Score the post on three failure modes:

#### A. Title mismatch (high impressions, low CTR)
Look for queries where impressions are high (top 10 of this post's queries) but CTR is < 1.5%. If found, the title likely doesn't match what users expect when they see this query in search results.

**Fix candidates**: rewrite the meta title to incorporate the highest-impression query verbatim (or close to it), test 2-3 variants.

#### B. Intent drift (ranking for queries you didn't target)
Look for queries you weren't optimizing for that have meaningful impressions (> 50/month). If found, the post is being pulled in for adjacent intent — and your meta description / intro may not address that intent.

**Fix candidates**: rewrite meta description to acknowledge both the original target keyword AND the drifted-into query. Possibly add an intro paragraph or H2 that addresses the drifted query.

#### C. Position 6-15 floor (good rank, no clicks)
Look for queries where avg position is 6-15 (page 1 bottom or top of page 2) with clicks under 5% of impressions. Page 2 traffic is famously zero; positions 6-10 should yield more clicks than they are.

**Fix candidates**: title is competing against pages above you on the same terms. Test a more specific or more emotive title.

### Step 4: Generate refresh recommendations

Output a report with three sections:

```markdown
# Refresh Report — {{TITLE}}

**Live URL:** {{CANONICAL_URL}}
**Published:** {{PUBLISH_DATE}}
**Days live:** XXX
**Last 28 days:** XXX impressions / XXX clicks / X.X% CTR / avg pos X.X

## Diagnosis

[A/B/C from above, with specific query examples]

## Proposed changes

### Current meta title (XX chars)
"{{current_title}}"

### Proposed meta title (XX chars)
"{{proposed_title}}"

Why: [1-2 sentence reasoning tied to the GSC data above]

### Current meta description (XX chars)
"{{current_desc}}"

### Proposed meta description (XX chars)
"{{proposed_desc}}"

Why: [reasoning]

### Intro paragraph changes (if any)
[Specific text changes, diff format]

### Other H2/H3 changes (if any)
[Specific text changes]

## Expected lift

Honest estimate based on the diagnosis:
- If title-mismatch (A): expect CTR lift 2-4x within 14 days
- If intent-drift (B): expect impressions stay flat, clicks lift 50-100%
- If position-floor (C): may not move CTR; consider whether to keep the post or sunset
```

### Step 5: Human gate

Show the report. Ask: **"Apply these changes to the live post? (Y/n)"**

If yes:
1. Update `./output/{{SLUG}}/draft.md` with the new title/meta/intro
2. Re-run `/seo-publish {{SLUG}}` to push to CMS (publishes as an update; same `_id` so the URL stays)
3. Tag `./output/{{SLUG}}/refresh-{{DATE}}.md` with a record of what was changed and why
4. Update `pipeline.yaml`:
   ```yaml
   refreshes:
     - date: YYYY-MM-DD
       diagnosis: A/B/C
       title_change: true/false
       expected_lift: "2-4x CTR"
   ```

If no, save the report to `./output/{{SLUG}}/refresh-proposed-{{DATE}}.md` and exit. User can apply manually.

### Step 6: Schedule a follow-up check

Remind the user to re-check this slug in 21 days to validate the refresh moved CTR:

```
Refresh applied. Re-check on {{DATE+21}} with `/seo-refresh {{SLUG}}` to see if the change worked.
```

## What this does NOT do

- Doesn't rewrite the full post (that's a different command — call `/seo-write` again with a force flag if needed)
- Doesn't change the canonical URL (that breaks backlinks)
- Doesn't change the slug
- Doesn't refresh cover images (use `generate_covers.py` separately if needed)

## Rules

- Only run on posts where `status.published: done`
- Always show the GSC data summary before proposing changes
- Always ask for confirmation before pushing changes to CMS
- Preserve the canonical URL — never change the slug on a refresh
- Log every refresh in `pipeline.yaml` so the history is auditable
