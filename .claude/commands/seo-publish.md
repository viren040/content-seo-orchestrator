# /seo-publish — Sanity CMS Publisher

You are the publishing agent for Asva AI's Content SEO pipeline.

**Argument:** `$ARGUMENTS` (the blog post slug)

## What to Do

### Step 1: Load & Validate
1. Read `/Users/viren/SEO - Asva Main Website/pipeline.yaml` — find the post
2. Read `/Users/viren/SEO - Asva Main Website/output/{{SLUG}}/draft.md` — the final draft
3. Read `/Users/viren/SEO - Asva Main Website/output/{{SLUG}}/seo-review.md` — check SEO score
4. Read `/Users/viren/SEO - Asva Main Website/templates/sanity-document.json` — Sanity template
5. Read `/Users/viren/SEO - Asva Main Website/config/seo-settings.yaml` — Sanity config

**Pre-flight checks:**
- Confirm draft.md exists
- Confirm SEO score is 70+ (warn if lower, ask user to confirm)
- Confirm all required Sanity fields can be populated

### Step 2: Build Sanity Payload
Convert the draft.md into a Sanity-ready JSON document:

1. **Parse frontmatter** from draft.md to extract:
   - title, slug, author, publishedAt, updatedAt
   - metaTitle, metaDescription, primaryKeyword
   - schemaType, pillar, cluster, tags
   - excerpt, ctaUrl, status

2. **Extract content body** (everything between frontmatter and FAQs)

3. **Extract FAQs** into structured array:
   ```json
   [{"_type": "faq", "_key": "faq1", "question": "...", "answer": "..."}]
   ```

4. **Extract internal links** into structured array:
   ```json
   [{"_type": "internalLink", "_key": "link1", "anchor": "...", "url": "..."}]
   ```

5. **Build final JSON** matching the Sanity blogPost schema

### Step 3: Preview & Confirm
1. Show the user the complete JSON payload (formatted)
2. Show a summary:
   ```
   Title: {{TITLE}}
   Slug: {{SLUG}}
   Word Count: XXXX
   FAQs: X
   Internal Links: X
   Schema Type: {{SCHEMA_TYPE}}
   ```
3. Ask: **"Publish as Draft or Publish Live?"**
   - **Draft**: Creates document in Sanity but doesn't make it public
   - **Live**: Creates and publishes immediately

### Step 4: Push to Sanity
Use the Sanity MCP tools:

**For Draft:**
```
Use mcp tool: create_documents_from_json
- projectId: en9d2pb2
- dataset: production
- documents: [the JSON payload]
```

**For Live (after draft):**
```
Use mcp tool: publish_documents
- projectId: en9d2pb2
- dataset: production
- documentIds: [the created document ID]
```

### Step 5: Verify & Save
1. Use `query_documents` to verify the document exists in Sanity:
   ```
   *[_type == "blogPost" && slug.current == "{{SLUG}}"][0]{title, slug, status, publishedAt}
   ```
2. Save confirmation to: `/Users/viren/SEO - Asva Main Website/output/{{SLUG}}/published.json`
   ```json
   {
     "slug": "{{SLUG}}",
     "sanity_id": "{{DOCUMENT_ID}}",
     "published_at": "{{TIMESTAMP}}",
     "status": "draft|published",
     "url": "https://asvaai.com/blog/{{SLUG}}"
   }
   ```
3. Update `pipeline.yaml`:
   - If draft: set `status.sanity_draft: done`
   - If live: set both `status.sanity_draft: done` and `status.published: done`
4. Confirm to user with the live URL

## Important Notes
- **Image handling**: The blog-hero.png already exists in `/blog-images/{{SLUG}}/`. Reference it in the image field. If the Sanity schema requires an uploaded asset, note this for the user to upload manually via Sanity Studio.
- **Never publish without user confirmation** — this is a hard human gate
- If any required field is missing, list what's missing and how to fix it
