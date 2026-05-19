# /seo-publish — Sanity CMS Publisher

You are the publishing agent for the Content SEO pipeline.

**Argument:** `$ARGUMENTS` (the blog post slug)

This command ships with Sanity CMS as the reference implementation. To target a different CMS (WordPress, Contentful, Strapi, etc.), edit this file and swap the API/MCP calls — the rest of the pipeline is CMS-agnostic.

## What to Do

### Step 1: Load & Validate
All paths below are relative to the repo root.

1. Read `./pipeline.yaml` — find the post
2. Read `./output/{{SLUG}}/draft.md` — the final draft
3. Read `./output/{{SLUG}}/seo-review.md` — check SEO score (if exists)
4. Read `./templates/sanity-document.json` — Sanity template
5. Read `./config/seo-settings.yaml` — Sanity config + brand URLs

**Required env vars** (see `.env.example`):
- `SANITY_AUTH_TOKEN` — write-scope token from sanity.io → Project → API → Tokens
- `SANITY_PROJECT_ID` — overrides `sanity.project_id` from settings if set
- `INDEXNOW_KEY` + `INDEXNOW_HOST` — for instant indexing on Bing/Yandex (optional)

**Pre-flight checks:**
- Confirm draft.md exists
- If SEO review exists, confirm score is 70+ (warn if lower, ask user to confirm)
- Confirm all required Sanity fields can be populated
- Confirm `$SANITY_AUTH_TOKEN` is set

### Step 2: Build Sanity Payload

Convert the draft.md into a Sanity-ready JSON document following the schema used by your live posts (see `templates/sanity-document.json` for the reference shape).

**CRITICAL — Document ID format:** `<schema_type>-<SLUG>` (e.g. `blogPost-my-slug`).
**CRITICAL — Slug format:** `{"_type": "slug", "current": "<SLUG>"}`

1. **Parse frontmatter** from draft.md to extract all metadata fields

2. **Extract content body** — everything between frontmatter `---` markers and the FAQ section. This goes into `content` as a markdown string.

3. **Extract FAQs** into structured array — NO `_type` field on FAQ items:
   ```json
   [{"_key": "faq1", "question": "...", "answer": "..."}]
   ```

4. **Extract internal links** into structured array — NO `_type` field on link items:
   ```json
   [{"_key": "il1", "anchor": "...", "url": "..."}]
   ```

5. **Build final JSON** with these exact fields (matching live posts — adjust to your schema):
   ```json
   {
     "_type": "<sanity.schema_type from settings>",
     "_id": "<schema_type>-<SLUG>",
     "title": "",
     "slug": {"_type": "slug", "current": ""},
     "author": "<brand.author_default or brand.author_personal>",
     "publishedAt": "YYYY-MM-DD",
     "updatedAt": "YYYY-MM-DDTHH:MM:SS.000Z",
     "excerpt": "",
     "content": "",
     "pillar": "",
     "cluster": "",
     "tags": [],
     "primaryKeyword": "",
     "metaTitle": "",
     "metaDescription": "",
     "schemaType": "BlogPosting",
     "canonicalUrl": "<brand.website>/blogs/<SLUG>",
     "ctaUrl": "<brand.website><brand.cta_url>",
     "status": "published",
     "hidden": false,
     "faqs": [],
     "internalLinks": []
   }
   ```

### Step 3: Preview & Confirm
1. Show a summary table:
   ```
   Title:          {{TITLE}}
   Slug:           {{SLUG}}
   Document ID:    <schema_type>-{{SLUG}}
   Word Count:     XXXX
   FAQs:           X items
   Internal Links: X items
   Schema Type:    {{SCHEMA_TYPE}}
   Author:         {{AUTHOR}}
   Pillar:         {{PILLAR}}
   ```
2. Ask: **"Publish as Draft or Publish Live?"**

### Step 4: Push to Sanity

**Important:** The Sanity MCP `create_documents_from_json` ignores custom `_id` values and generates random UUIDs. Most frontends query by a deterministic `_id` (e.g. `blogPost-<slug>`), so documents with UUID IDs will show "Post not found".

**Use the Sanity HTTP API directly via curl instead:**

```bash
PROJECT_ID="${SANITY_PROJECT_ID:-$(yq -r '.sanity.project_id' config/seo-settings.yaml)}"
DATASET="${SANITY_DATASET:-$(yq -r '.sanity.dataset' config/seo-settings.yaml)}"

curl -s -X POST "https://${PROJECT_ID}.api.sanity.io/v2021-06-07/data/mutate/${DATASET}" \
  -H "Authorization: Bearer $SANITY_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mutations": [
      { "createOrReplace": <THE_FULL_JSON_PAYLOAD_WITH_CORRECT_ID> }
    ]
  }'
```

The JSON payload MUST include:
- `"_type": "<schema_type>"`
- `"_id": "<schema_type>-<SLUG>"` (this is what the frontend uses to find the post)

**For Live (after creating):**
Use Sanity MCP `publish_documents` with the project from settings:
- resource: `{"projectId": "<sanity.project_id>", "dataset": "<sanity.dataset>"}`
- documentIds: `["<schema_type>-<SLUG>"]`

### Step 5: Submit to IndexNow (instant indexing)
After publishing live, submit the URL to IndexNow for instant crawling by Bing, Yandex, Seznam, and Naver:

```bash
if [ -n "$INDEXNOW_KEY" ] && [ -n "$INDEXNOW_HOST" ]; then
  curl -s -X POST "https://api.indexnow.org/indexnow" \
    -H "Content-Type: application/json" \
    -d "{
      \"host\": \"$INDEXNOW_HOST\",
      \"key\": \"$INDEXNOW_KEY\",
      \"urlList\": [\"https://${INDEXNOW_HOST}/blogs/{{SLUG}}\"]
    }"
fi
```

**Setup:** Host `{INDEXNOW_KEY}.txt` at `https://<your-domain>/{INDEXNOW_KEY}.txt` containing just the key. Expected response: HTTP 202.
**Coverage:** Bing, Yandex, Seznam, Naver. Google uses its own indexing API.

Only submit to IndexNow when publishing **live** (not drafts).

### Step 6: Verify & Save
1. Query Sanity to verify:
   ```
   *[_type == "<schema_type>" && slug.current == "{{SLUG}}"][0]{title, slug, status, _id, publishedAt}
   ```
2. Save confirmation to: `./output/{{SLUG}}/published.json` (include IndexNow status)
3. Update `pipeline.yaml`:
   - Draft: set `status.sanity_draft: done`
   - Live: set both `status.sanity_draft: done` and `status.published: done`
4. Show the user: "Published! URL: <brand.website>/blogs/{{SLUG}} | IndexNow: submitted"

## Schema Notes (Sanity-specific gotchas)

- `_id` should use a deterministic format like `<schema_type>-<SLUG>`
- `publishedAt` typically uses date format `YYYY-MM-DD`
- `canonicalUrl` should be the full public URL
- FAQ + internal-link items need `_key` only (no `_type`)
- Pick author from `brand.author_default` or `brand.author_personal` in settings

## Rules
- **Never publish without user confirmation** — hard human gate
- If any required field is missing, list what's missing and how to fix
- Image handling: cover images live in `./blog-images/<SLUG>/`. Upload them to Sanity assets first (see `generate-blog-images.py` and `generate_covers.py`).
