# Session Log — 2026-03-15

## What Was Done

### 1. Supabase → Sanity Image Migration (COMPLETE)
- Uploaded all 17 blog post images to Sanity as native assets
- Set `image` field with proper asset references on all 17 posts
- Removed `legacyImageUrl` from all 17 posts
- Zero Supabase dependency for blog images

### 2. Cover Image Fixes (COMPLETE)
- Generated branded covers (1200x630) for 4 pipeline posts that had infographic diagrams as covers
- Infographics moved inside blog content at contextually appropriate spots:
  - **LLM Audit**: 5-step process diagram after intro section
  - **Brands Invisible**: Problem/solution framework after "5 Structural Reasons" header
  - **AI Visibility Score**: Component breakdown after weights table
  - **Playbook**: 5-tool workflow after tools table
- Generated covers for all 9 new draft posts

### 3. Canonical URLs Fixed (COMPLETE)
- Set `canonicalUrl` on all 13 posts that were missing it
- Pattern: `https://www.asvaai.com/blogs/{slug}`
- All 17 posts now have canonical URLs

### 4. 9 Draft Posts Created in Sanity (COMPLETE)
- Created all 9 remaining pipeline posts as drafts in Sanity
- Each has: title, slug, pillar, primaryKeyword, metaTitle, metaDescription, excerpt, tags, internalLinks
- Status: `draft`, Hidden: `true` (won't show on blog listing until published)

### 5. Publishing Schedule Created
- `PUBLISHING-SCHEDULE.md` — 5-day schedule (2 posts/day, Mar 16-20)
- Per-post checklist: research → brief → write → optimize → cover → publish

### 6. Repo Cleanup
- Flattened `covers/remaining/` into `covers/`
- Removed duplicate `generate_pipeline_covers.py`
- Updated `generate_covers.py` to include all 23 posts
- Updated `pipeline.yaml` last_updated date
- Updated README architecture diagram

### 7. Memory Files Updated
- `project_blog_pipeline.md` — full rewrite reflecting current state
- `MEMORY.md` — updated index with new reference files
- `reference_sanity_assets.md` — new file with all Sanity asset IDs
- `reference_figma_diagrams.md` — unchanged (still valid)

---

## Codebase Audit Findings

### Blog URL Structure
- **Pattern**: `/blogs/:slug` (plural) — consistent across all routes
- **Canonical**: `https://asvaai.com/blogs/{slug}`
- **No duplicate content** between /blogs/ and /learn/

### Supabase Cleanup Needed (Website Codebase)
The website still has legacy Supabase integration:
- `useBlogPosts.ts` — Supabase as fallback data source (Sanity takes priority)
- `server.js` — Supabase used for sitemap blog slug fetching
- **Note**: Supabase is also used for auth, forms, tools, admin — cannot fully remove

**Blog-specific cleanup tasks** (for website repo):
- [ ] Remove `fetchSupabasePosts()` from `useBlogPosts.ts`
- [ ] Update `server.js` sitemap to fetch slugs from Sanity instead
- [ ] Remove `legacyImageUrl` from GROQ coalesce query (`queries.ts` line 30)
- [ ] Move Supabase credentials in `server.js` to env vars

### Image Resolution
- GROQ query: `coalesce(image.asset->url, legacyImageUrl)` — works correctly
- After cleanup: can simplify to just `image.asset->url`

---

## Current State Summary

| Category | Count | Status |
|----------|-------|--------|
| Published blog posts | 17 | All have native Sanity images + canonical URLs |
| Pipeline posts (published) | 4 | Full pipeline complete (research → publish) |
| Pipeline posts (draft) | 9 | Created in Sanity, need content pipeline |
| Cover images generated | 23 | All in `/covers/` directory |
| Infographics embedded | 4 | In published post content |
| Slash commands | 7 | All functional |
| Templates | 4 | Ready for use |

---

## Next Steps

1. **Start daily pipeline** — Run `/seo-daily` to begin research for `ai-seo-agency-guide` (KD 15)
2. **Upload 9 draft covers** to Sanity as native assets
3. **Website code cleanup** — Remove Supabase blog fallback in website repo
4. **Deploy** — Push website code changes to Netlify
5. **IndexNow** — Add to /seo-publish workflow
