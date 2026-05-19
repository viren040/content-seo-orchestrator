# API Setup & Cost Guide

## Required API Keys

### 1. Perplexity API (Research)
**What:** Powers the `/seo-research` step with Deep Research queries.
**Cost:** ~$0.40-0.50 per blog post research query.

**Setup:**
1. Go to https://console.perplexity.ai
2. Navigate to API Settings
3. Generate an API key (starts with `pplx-`)
4. Set environment variable:
   ```bash
   export PERPLEXITY_API_KEY="pplx-your-key-here"
   ```
5. Or add to `~/.zshrc` / `~/.bashrc` for persistence:
   ```bash
   echo 'export PERPLEXITY_API_KEY="pplx-your-key-here"' >> ~/.zshrc
   ```

**Models available:**
| Model | Use Case | Input/M | Output/M | Search/1K | Avg. Cost/Query |
|-------|----------|---------|----------|-----------|-----------------|
| `sonar-deep-research` | Full research (recommended) | $2 | $8 | $5 | ~$0.40-0.50 |
| `sonar-pro` | Quick research (fallback) | $3 | $15 | $8 | ~$0.10-0.15 |
| `sonar` | Basic search (budget) | $1 | $1 | $5 | ~$0.02-0.05 |

**Rate limits:** 50 requests/minute. No issue for blog pipeline.

---

### 2. Sanity CMS (Publishing)
**What:** Powers the `/seo-publish` step to push blog posts to CMS.
**Cost:** Free tier = 250K API requests/month. More than enough.

**Setup:** Two options.

**Option A — Direct HTTP API (recommended).** Set in `.env`:
```bash
SANITY_AUTH_TOKEN=sk...          # write-scope token
SANITY_PROJECT_ID=your-project-id
SANITY_DATASET=production
```
The orchestrator uses HTTP directly for publish operations (see `.claude/commands/seo-publish.md` for why — the MCP overwrites custom `_id` values).

**Option B — Sanity MCP** (useful for queries, asset uploads, etc.):
1. Install Sanity MCP: https://www.sanity.io/docs/mcp
2. Authenticate via `sanity login`
3. Set `sanity.project_id` and `sanity.dataset` in `config/seo-settings.yaml`

---

### 3. Figma API (Diagrams) — Already Connected
**What:** Fetches FigJam diagrams for blog post infographics.
**Cost:** Free with Starter plan (rate-limited).
**Setup:** Already connected via Figma MCP.

---

### 4. Canva API (Images) — Already Connected
**What:** Generates branded blog images via Canva MCP.
**Cost:** Free API. Requires Canva Pro subscription ($15/mo) for full features.
**Setup:** Already connected via Canva MCP. Brand Kit ID: `kAGYIU1mVv8`

---

## Cost Per Blog Post

### Full Pipeline Cost Breakdown

| Step | Service | API Model | Cost | Notes |
|------|---------|-----------|------|-------|
| **Research** | Perplexity | sonar-deep-research | ~$0.45 | 1 deep query per post |
| **Brief** | Claude Code | (included) | $0.00 | Runs locally in Claude Code |
| **Write** | Claude Code | (included) | $0.00 | Runs locally in Claude Code |
| **SEO Review** | Claude Code | (included) | $0.00 | Runs locally in Claude Code |
| **Publish** | Sanity MCP | Content Lake API | $0.00 | Free tier (250K/mo) |
| **Images** | Already done | N/A | $0.00 | Pre-generated |
| **Diagrams** | Already done | N/A | $0.00 | Pre-generated |

### Per Blog Post Total: ~$0.45

### Full 12-Post Pipeline Total: ~$5.40

### Monthly Recurring (if running weekly batches): ~$2-5/month

---

## Cost Comparison

| Approach | Cost per Blog | Time per Blog | Quality |
|----------|--------------|---------------|---------|
| **This pipeline (Claude + Perplexity API)** | ~$0.45 | 15-20 min | High (human-reviewed) |
| Manual writing (freelancer) | $100-500 | 3-5 days | Variable |
| SEO agency (per post) | $200-1,000 | 1-2 weeks | Variable |
| AI-only (no research, no review) | ~$0.05 | 5 min | Low (generic) |

---

## Environment Variables Summary

```bash
# Required
export PERPLEXITY_API_KEY="pplx-your-key-here"

# Optional (for future integrations)
# export AHREFS_API_KEY="your-key"
# export DATAFORSEO_LOGIN="your-login"
# export DATAFORSEO_PASSWORD="your-password"
# export GSC_SERVICE_ACCOUNT="/path/to/service-account.json"
```

---

## API Health Check

Run this to verify all APIs are working:

```bash
# Test Perplexity API
curl -s https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "sonar", "messages": [{"role": "user", "content": "ping"}]}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin); print('✅ Perplexity API: OK' if 'choices' in r else '❌ Perplexity API: Error')"
```

Sanity and Figma MCPs are verified by Claude Code automatically when you use `/seo-publish` or reference diagrams.

---

## Future API Integrations (not needed today)

| Service | What For | When | Est. Cost |
|---------|----------|------|-----------|
| **Ahrefs API** | Automated keyword tracking, rank monitoring | Phase 2 | $99/mo (Lite plan) |
| **DataForSEO** | SERP data, AI mention tracking | Phase 2 | Pay-as-you-go (~$0.04/query) |
| **Google Search Console API** | Impressions, clicks, CTR tracking | Phase 2 | Free |
| **Google Analytics API** | Traffic attribution | Phase 3 | Free |
