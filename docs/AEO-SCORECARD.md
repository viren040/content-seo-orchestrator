# The AEO Scorecard

A 10-check rubric for scoring whether a blog post is shaped to get cited by ChatGPT, Perplexity, Google AI Overviews, and other LLM answer engines.

> This is the methodology behind the `/seo-optimize` slash command in [content-seo-orchestrator](https://github.com/viren040/content-seo-orchestrator). Shared as a standalone doc so you can apply it manually if you don't want to clone the repo.

## Why a separate scorecard for AEO

Classic SEO scorecards (Yoast, Surfer, Clearscope) score for *ranking* — keyword placement, density, internal link count, meta length. They miss what makes content *citable* by LLMs.

LLMs preferentially cite content with:
1. **FAQ-shaped sub-headings** they can lift Q&A pairs from verbatim
2. **Named entities** (real customers, real products, real numbers) over generic claims
3. **Source attribution** on every stat — LLMs trained on factual content prefer to surface citations that themselves cite sources
4. **Clear schema markup** (FAQPage, HowTo) when the post is question-shaped
5. **Specific over abstract** — "average asphalt driveway in Glendale costs $4,200" beats "driveway costs vary"

The scorecard below scores for both: classic SEO rank signals and AEO citation signals.

## The 10 checks (10 points each = 100)

### 1. Keyword placement (10 pts)
- [ ] Primary keyword in H1
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in ≥1 H2
- [ ] Primary keyword in meta title
- [ ] Primary keyword in meta description

Each box = 2 points.

### 2. Keyword density (10 pts)
- Primary keyword density: target 1-2%
- Under 0.5%: too thin (deduct 5)
- 1-2%: full marks
- Over 3%: stuffing (deduct 5)
- Secondary keywords: each must appear at least once (deduct 1 each)

### 3. Meta title (10 pts)
- Length 50-60 chars = full marks
- 60-70 chars = 7 pts
- Over 70 = 5 pts (truncated in SERP)
- Contains primary keyword (deduct 3 if missing)
- Compelling — would you click it? (subjective, deduct 2 if generic)

### 4. Meta description (10 pts)
- Length 150-160 chars = full marks
- Contains primary keyword (deduct 3 if missing)
- Contains CTA or value prop (deduct 2 if missing)
- Not truncated awkwardly mid-sentence (deduct 2 if so)

### 5. Heading structure (10 pts)
- Single H1 (the title) — deduct 3 if more than one H1
- Logical H2 → H3 hierarchy (no skipping levels) — deduct 2
- At least 4 H2 sections — deduct 2 if under
- H2s descriptive and keyword-relevant — deduct 3 if generic

### 6. Content length (10 pts)
- Within 80-120% of target word count = full marks
- Under 80% = thin content flag, deduct 5
- Over 120% = padding flag, deduct 2

### 7. Internal links (10 pts)
- Minimum 3 internal links = full marks (4+ ideal)
- Links to a CTA / money page = +2
- Anchor text is descriptive (not "click here") — deduct 3 if generic

### 8. FAQ quality (10 pts) — *the AEO-specific check*
- 3-6 FAQ pairs present = full marks
- Questions are genuine search queries (not made-up) — deduct 5 if generic
- Answers are direct (2-3 sentences) — deduct 2 if long-winded
- At least 1 FAQ contains primary keyword — deduct 3 if not

**Why this matters for AEO**: an FAQ section gives LLMs discrete Q&A pairs they can lift directly into an answer. Posts without FAQ sections rarely get cited verbatim.

### 9. Readability (10 pts)
- Paragraphs max 4 sentences = full marks
- Uses bullet points and/or tables = full marks
- No wall-of-text sections = deduct 3 per wall
- Scannable with headers every 200-400 words = deduct 2 if not

### 10. Content quality (10 pts) — *the AEO-citation check*
- All claims backed by data or specific example = deduct 2 per unsourced claim (max -5)
- Real customer/product names used (not "leading brand") = deduct 5 if generic
- No fluff paragraphs = deduct 3 if filler
- CTA feels natural, not salesy = deduct 2 if pushy
- Excerpt is 150-200 chars = deduct 2 if not

**Why this matters for AEO**: LLMs preferentially cite content with named entities and sourced stats. "Salesforce grew CRM market share to 23.8% in 2025" beats "Salesforce is a leading CRM" by 10× in citation likelihood.

## Grading

| Score | Grade | Action |
|---|---|---|
| 90-100 | A | Publish-ready |
| 80-89 | B | Minor tweaks; publish after one revision |
| 70-79 | C | Needs work; revise sections that scored < 7 |
| 60-69 | D | Significant issues; rewrite weak sections |
| < 60 | F | Rewrite from outline |

## Real example (one of the Asva AI blog posts)

| Check | Score | Notes |
|---|---|---|
| Keyword placement | 10/10 | "audit brand visibility llms" in H1, intro, 2 H2s, meta title + desc |
| Keyword density | 9/10 | 1.4% — within range |
| Meta title | 10/10 | 58 chars, KW included |
| Meta description | 8/10 | 155 chars, KW + CTA, slightly truncated |
| Heading structure | 10/10 | 1 H1, 6 H2s, logical H3s |
| Content length | 10/10 | 1,623 words / 1,600 target |
| Internal links | 9/10 | 4 internal links, descriptive anchors |
| FAQ quality | 10/10 | 5 FAQs, primary KW in 2 |
| Readability | 8/10 | Mostly short paragraphs; one 6-sentence block in section 3 |
| Content quality | 9/10 | All claims sourced; 2 named brands (Salesforce, HubSpot) used |
| **Total** | **93/100 (A)** | Publish-ready |

## How to apply this manually

1. Print or copy the 10 checks above into your editor
2. Score each section out of 10
3. Sum to 100
4. If under 80, identify the lowest-scoring checks and revise

## Or use the tool

The `/seo-optimize <slug>` command in [content-seo-orchestrator](https://github.com/viren040/content-seo-orchestrator) runs this scorecard automatically and outputs a report with specific fix suggestions. Free, MIT, runs in Claude Code.

---

Last updated: 2026-05-19. PRs welcome to refine the rubric — we treat it as a living doc.
