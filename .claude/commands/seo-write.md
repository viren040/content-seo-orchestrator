# /seo-write — Blog Post Content Writer

You are the content writer for the Content SEO pipeline.

**Argument:** `$ARGUMENTS` (the blog post slug)

## What to Do

### Step 1: Load All Context
All paths below are relative to the repo root.

1. Read `./pipeline.yaml` — find the post
2. Read `./output/{{SLUG}}/brief.md` — the approved content brief
3. Read `./output/{{SLUG}}/research.md` — the raw research
4. Read `./templates/blog-post.md` — the post template
5. Read `./config/seo-settings.yaml` — SEO rules & brand voice
6. (Optional) If `paths.brand_bible` is set in `seo-settings.yaml`, read that file for deeper brand voice context

If brief.md doesn't exist, tell user: "Brief not done yet. Run `/seo-brief {{SLUG}}` first."

### Step 2: Write the Full Blog Post
Follow the approved content brief outline exactly. Write the complete post:

**Frontmatter:**
- Fill all metadata fields from brief (title, slug, meta title, meta description, etc.)
- Set `publishedAt` to today's date
- Set `status: "Draft"`
- Set `image_path` to `./blog-images/{{SLUG}}/blog-hero.png`
- Set `author` to `brand.author_default` (or `brand.author_personal` for personal-voice posts)

**Content Body:**
1. **Introduction** (150-200 words)
   - Hook that creates urgency or curiosity
   - State the problem clearly
   - Promise what the reader will learn
   - Naturally include primary keyword in first 100 words

2. **H2 Sections** (as outlined in brief)
   - Follow the exact H2/H3 structure from the brief
   - 200-400 words per H2 section
   - Include data points with sources where specified
   - Weave in secondary keywords naturally (don't force)
   - Place internal links at natural anchor points

3. **Conclusion + CTA** (100-150 words)
   - Summarize 3 key takeaways
   - Natural CTA — pull URL from `brand.cta_url` in `seo-settings.yaml`

4. **FAQs** (3-6 pairs)
   - Answer questions from research that weren't fully covered in main content
   - Each answer: 2-3 sentences, direct and useful
   - Include primary keyword in at least 1 FAQ answer

5. **Internal Links** (as HTML comments at bottom)
   - List all internal links used, formatted for the CMS `internalLinks` array

### Step 3: Save & Update
1. Save the full post to: `./output/{{SLUG}}/draft.md`
2. Update `./pipeline.yaml` — set `status.content: done`
3. Tell user: "Draft saved. Review it, then run `/seo-optimize {{SLUG}}` for SEO scoring."

## Writing Rules — Non-Negotiable

### Voice & Tone
- Pull voice and tone from `config/seo-settings.yaml → content_rules.voice` and `content_rules.tone_guidelines`
- No fluff paragraphs. No throat-clearing introductions.
- Never start sections with "In today's digital landscape..." or similar cliches

### SEO Rules
- Primary keyword in: H1, first 100 words, at least 1 H2, meta title, meta description, 1 FAQ answer
- Secondary keywords: use each at least once, naturally
- Keyword density: 1-2% for primary keyword (or whatever `seo_defaults.keyword_density_target` says)
- Every H2 should be a potential featured snippet answer
- Internal links: minimum 3 (or `seo_defaults.min_internal_links`), placed at natural anchor points

### Content Quality
- Every claim must be backed by data or a specific example
- Use real customers/case studies — not hypotheticals
- Tables and bullet points for scannable content
- Short paragraphs (3-4 sentences max)
- No padding — if a section doesn't add value, cut it

### What NOT to Do
- Don't write "As an AI..." or any AI self-references
- Don't use marketing buzzwords without substance
- Don't pad word count with repetition
- Don't make up statistics or sources
- Don't write introductions longer than 200 words
