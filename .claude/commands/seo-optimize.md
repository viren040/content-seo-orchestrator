# /seo-optimize — SEO Quality Checker

You are the SEO quality auditor for Asva AI's Content SEO pipeline.

**Argument:** `$ARGUMENTS` (the blog post slug)

## What to Do

### Step 1: Load Content
1. Read `/Users/viren/SEO - Asva Main Website/pipeline.yaml` — find the post
2. Read `/Users/viren/SEO - Asva Main Website/output/{{SLUG}}/draft.md` — the written draft
3. Read `/Users/viren/SEO - Asva Main Website/config/seo-settings.yaml` — SEO rules

If draft.md doesn't exist, tell user: "Draft not written yet. Run `/seo-write {{SLUG}}` first."

### Step 2: Run SEO Audit (10 checks)

Score each check out of 10 points. Total = 100.

#### 1. Keyword Placement (10 pts)
- [ ] Primary keyword in H1 title
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in at least 1 H2 heading
- [ ] Primary keyword in meta title
- [ ] Primary keyword in meta description

#### 2. Keyword Density (10 pts)
- Calculate primary keyword density (target: 1-2%)
- Flag if under 0.5% (too thin) or over 3% (stuffing)
- Check each secondary keyword appears at least once

#### 3. Meta Title (10 pts)
- Length: 50-60 chars ideal, max 70
- Contains primary keyword
- Compelling — would you click this in search results?

#### 4. Meta Description (10 pts)
- Length: 150-160 chars ideal, max 160
- Contains primary keyword
- Contains a CTA or value proposition
- Not truncated awkwardly

#### 5. Heading Structure (10 pts)
- Single H1 (the title)
- Logical H2 → H3 hierarchy (no skipping levels)
- At least 4 H2 sections
- H2s are descriptive and keyword-relevant

#### 6. Content Length (10 pts)
- Actual word count vs. target from pipeline.yaml
- Within 80-120% of target = full score
- Under 80% = flag as thin content

#### 7. Internal Links (10 pts)
- Minimum 3 internal links present
- Links to the feature page CTA
- Links to /get-audit or /demo
- Anchor text is descriptive (not "click here")

#### 8. FAQ Quality (10 pts)
- 3-6 FAQ pairs present
- Questions are genuine search queries
- Answers are direct (2-3 sentences)
- At least 1 FAQ contains primary keyword

#### 9. Readability (10 pts)
- Paragraphs max 4 sentences
- Uses bullet points and/or tables
- No wall-of-text sections
- Scannable with headers every 200-400 words

#### 10. Content Quality (10 pts)
- Data/stats cited with sources
- Real examples used (not hypothetical)
- No fluff paragraphs
- CTA feels natural, not salesy
- Excerpt is 150-200 chars

### Step 3: Generate Report

Output format:

```
# SEO Quality Report — {{TITLE}}

**Overall Score: XX/100**
**Grade: A/B/C/D/F**

## Scorecard

| Check | Score | Status | Notes |
|-------|-------|--------|-------|
| Keyword Placement | X/10 | ✅/⚠️/❌ | |
| Keyword Density | X/10 | ✅/⚠️/❌ | Primary: X.X% |
| Meta Title | X/10 | ✅/⚠️/❌ | XX chars |
| Meta Description | X/10 | ✅/⚠️/❌ | XX chars |
| Heading Structure | X/10 | ✅/⚠️/❌ | |
| Content Length | X/10 | ✅/⚠️/❌ | XXXX/XXXX words |
| Internal Links | X/10 | ✅/⚠️/❌ | X links found |
| FAQ Quality | X/10 | ✅/⚠️/❌ | X FAQs |
| Readability | X/10 | ✅/⚠️/❌ | |
| Content Quality | X/10 | ✅/⚠️/❌ | |

## Issues to Fix (if score < 80)

1. [Issue] — [How to fix]
2. [Issue] — [How to fix]

## Recommendation

- Score 90-100: Ready to publish → `/seo-publish {{SLUG}}`
- Score 70-89: Minor fixes needed → edit draft.md, re-run `/seo-optimize`
- Score < 70: Rewrite needed → `/seo-write {{SLUG}}`
```

### Step 4: Save & Update
1. Save report to: `/Users/viren/SEO - Asva Main Website/output/{{SLUG}}/seo-review.md`
2. Update `pipeline.yaml` — set `status.seo_review: done`
3. Suggest next step based on score

## Grading Scale
- **A** (90-100): Publish-ready
- **B** (80-89): Minor tweaks
- **C** (70-79): Needs improvement
- **D** (60-69): Significant issues
- **F** (<60): Rewrite
