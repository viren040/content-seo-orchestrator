# /seo-research — Perplexity Deep Research Phase (API-powered)

You are the research coordinator for Asva AI's Content SEO pipeline.

**Argument:** `$ARGUMENTS` (the blog post slug)

## What to Do

### Step 1: Load Context
1. Read `/Users/viren/SEO - Asva Main Website/pipeline.yaml` — find the post matching the slug
2. Read `/Users/viren/Desktop/Asva AI — Docs & Strategy/Feature-Page-Blog-Planning-Brief.md` — find the exact Perplexity research prompt for this post
3. Read `/Users/viren/SEO - Asva Main Website/templates/research-brief.md` — load the output template
4. Read `/Users/viren/SEO - Asva Main Website/config/seo-settings.yaml` — load settings

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
        "content": "{{PERPLEXITY_RESEARCH_PROMPT_FROM_PLANNING_BRIEF}}"
      }
    ],
    "search_recency_filter": "month"
  }'
```

**Environment variable:** `PERPLEXITY_API_KEY` must be set (starts with `pplx-`).
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
   - **Unique Angles Not Yet Covered** — identify 3+ fresh takes we can own
   - **Internal Linking Opportunities** — cross-reference pipeline.yaml for all Asva AI posts/pages
   - **Raw Research Output** — preserve full Perplexity response verbatim
   - **API Metadata** — model used, tokens consumed, citations returned, cost estimate

3. Save the structured research to: `/Users/viren/SEO - Asva Main Website/output/{{SLUG}}/research.md`

### Step 5: Update Pipeline
1. Update `pipeline.yaml` — set this post's `status.research: done`
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
