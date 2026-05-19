# /seo-research — Perplexity Deep Research Phase (API-powered)

You are the research coordinator for the Content SEO pipeline.

**Argument:** `$ARGUMENTS` (the blog post slug)

## What to Do

### Step 1: Load Context
All paths below are relative to the repo root (current working directory).

1. Read `./pipeline.yaml` — find the post matching the slug
2. Read `./config/seo-settings.yaml` — load brand + settings. If a `paths.planning_brief` key is set, it points to an external doc with per-post Perplexity prompts.
3. Read the planning brief at `paths.planning_brief` (if set) — find the exact Perplexity prompt for this post. If unset, derive a prompt from the post's `title`, `primary_keyword`, and `content_angle`.
4. Read `./templates/research-brief.md` — load the output template.

If the slug doesn't match any post in pipeline.yaml, show available slugs.
If research is already done for this slug, warn the user and ask if they want to overwrite.

### Step 2: Show Research Plan
1. Show the user the post metadata (title, keyword, KD, content angle)
2. Show the research prompt that will be sent to Perplexity
3. Show estimated API cost (~$0.40-0.50 per deep research query)
4. Ask: "Ready to run? (Y/n)"

### Step 3: Call Perplexity Deep Research API
Run the Perplexity API call via bash using curl:

```bash
curl -s https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-deep-research",
    "messages": [
      {
        "role": "system",
        "content": "You are a thorough SEO and content research assistant. Provide detailed, data-backed research with specific statistics, sources, and URLs. Always cite your sources."
      },
      {
        "role": "user",
        "content": "{{PERPLEXITY_RESEARCH_PROMPT}}"
      }
    ],
    "search_recency_filter": "month"
  }'
```

**Environment variable:** `PERPLEXITY_API_KEY` must be set (starts with `pplx-`). See `.env.example`.
If not set, fall back to manual mode: present the prompt and ask user to paste results.

**Fallback mode (if API fails or no key):**
1. Present the research prompt formatted for copy-paste
2. Tell user: "API unavailable. Copy this prompt, run it in Perplexity, and paste the full response back."
3. Continue from Step 4 with pasted results

### Step 4: Process Research Output
1. Take the API response (or user-pasted response)
2. Structure it into the research brief template with these sections:
   - **Market Context** — synthesize the landscape, current state of knowledge, gaps
   - **Key Statistics & Data Points** — extract EVERY stat with source attribution into a table
   - **Competitor Content Analysis** — identify top 5 ranking URLs, their strengths, their gaps
   - **Expert Opinions & Quotes** — pull any named sources/quotes with attribution
   - **Unique Angles Not Yet Covered** — identify 3+ fresh takes the brand can own
   - **Internal Linking Opportunities** — cross-reference `pipeline.yaml` for sibling posts/pages
   - **Raw Research Output** — preserve full Perplexity response verbatim
   - **API Metadata** — model used, tokens consumed, citations returned, cost estimate

3. Save the structured research to: `./output/{{SLUG}}/research.md`
4. (Optional) Save raw API JSON to: `./output/{{SLUG}}/research-raw.json`

### Step 5: Update Pipeline
1. Update `./pipeline.yaml` — set this post's `status.research: done`
2. Show cost summary: "Research cost: ~$X.XX (sonar-deep-research)"
3. Confirm to user: "Research saved. Next step: `/seo-brief {{SLUG}}`"

## API Configuration

**Endpoint:** `https://api.perplexity.ai/chat/completions`
**Model:** `sonar-deep-research` (best for comprehensive research queries)
**Auth:** Bearer token — `PERPLEXITY_API_KEY` environment variable
**Cost:** ~$0.40-0.50 per deep research query (input: $2/M, output: $8/M, citations: $2/M, reasoning: $3/M, search: $5/1K)
**Rate limit:** 50 RPM
**Recency filter:** "month" (latest data)

## Fallback Modes
1. **No API key** → Manual mode (copy/paste from Perplexity browser)
2. **API error/rate limit** → Retry once, then fall back to manual mode
3. **sonar-deep-research unavailable** → Try `sonar-pro` ($3/$15 per M tokens, ~$0.15/query)

## Rules
- NEVER fabricate research — only structure what the API or user provides
- ALWAYS preserve the raw output in full
- ALWAYS show cost estimate before and after the API call
- Log API usage for cost tracking
