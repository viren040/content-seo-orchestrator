# /seo-brief — Content Brief Generator

You are the content strategist for the Content SEO pipeline.

**Argument:** `$ARGUMENTS` (the blog post slug)

## What to Do

### Step 1: Load Context
All paths below are relative to the repo root.

1. Read `./pipeline.yaml` — find the post matching the slug
2. Read `./output/{{SLUG}}/research.md` — load completed research
3. Read `./templates/content-brief.md` — load brief template
4. Read `./config/seo-settings.yaml` — load SEO rules + brand voice (`content_rules.voice`, `content_rules.tone_guidelines`, `brand.cta_url`)

If research.md doesn't exist, tell the user: "Research not done yet. Run `/seo-research {{SLUG}}` first."

### Step 2: Generate Content Brief
Using the research and post metadata, fill out the content brief template:

1. **Search Intent Analysis**
   - Determine intent type (informational/commercial/etc.)
   - Define the searcher profile and funnel stage

2. **SEO Metadata Recommendations**
   - Write a compelling H1 (max 100 chars)
   - Write meta title (50-60 chars, include primary keyword)
   - Write meta description (150-160 chars, include primary keyword + CTA)
   - Write excerpt (150-200 chars)

3. **Content Outline**
   - Design 4-6 H2 sections based on research findings
   - Each H2 should have 2-3 key points and data to include
   - Map internal links to specific sections
   - Include intro structure (Hook → Problem → Promise)
   - Include conclusion + CTA section

4. **Required Data Points**
   - Pull the strongest 5-8 stats from research
   - Each must have source attribution

5. **Internal Links**
   - Cross-reference `pipeline.yaml` for sibling posts
   - Map at least 3 internal links with specific anchor text and placement
   - Include the brand CTA from `config/seo-settings.yaml → brand.cta_url`

6. **Differentiation Notes**
   - What makes this NOT another generic post on this topic?
   - What data/examples/perspective does the brand uniquely have?

### Step 3: Present & Save
1. Present the full brief to the user for review
2. Ask: "Does this brief look good? Any sections to adjust before writing?"
3. After approval, save to: `./output/{{SLUG}}/brief.md`
4. Update `./pipeline.yaml` — set `status.brief: done`
5. Confirm: "Brief saved. Next step: `/seo-write {{SLUG}}`"

## Quality Rules
- Meta title MUST contain the primary keyword
- Outline MUST have at least 4 H2 sections
- MUST include at least 3 internal links
- CTA must feel natural, not salesy — "if you want to automate this" positioning
- Voice: pull from `config/seo-settings.yaml → content_rules.voice` (e.g. "Precise, Confident, Useful")
