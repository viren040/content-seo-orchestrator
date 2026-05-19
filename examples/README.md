# Example Pipelines

Starter `pipeline.yaml` files for four common content-SEO patterns. Copy the closest fit into your repo root as `pipeline.yaml`, then edit slugs/keywords/CTAs to match your brand.

| Vertical | File | What it covers |
|---|---|---|
| B2B SaaS | [`b2b-saas.pipeline.yaml`](./b2b-saas.pipeline.yaml) | Product-led content, comparison pages, feature explainers, AEO/category education |
| D2C ecommerce | [`d2c-ecommerce.pipeline.yaml`](./d2c-ecommerce.pipeline.yaml) | Buying guides, product comparisons, sizing/usage content, AI search visibility for shopping queries |
| Local business | [`local-business.pipeline.yaml`](./local-business.pipeline.yaml) | "[Service] in [city]", pricing/timeline FAQs, neighborhood guides, local AEO |
| Agency / consultancy | [`agency.pipeline.yaml`](./agency.pipeline.yaml) | Thought-leadership, case studies, methodology posts, /vs/ pages for tool comparisons |

## How to use

```bash
# 1. Copy the closest fit
cp examples/b2b-saas.pipeline.yaml pipeline.yaml

# 2. Edit slugs, keywords, internal links to match your brand
# 3. Update config/seo-settings.yaml with your brand, voice, CTAs
# 4. Run
/seo-status
```

## What's in each example

Each starter file ships with **8-10 posts** in `publish_order`, lowest KD first (quick wins early). Every post includes:
- `primary_keyword` + `secondary_keywords` (representative volumes/KDs — verify with your own keyword research tool)
- `content_angle` — what makes the post distinct
- `schema_type` — `BlogPosting`, `HowTo`, or `FAQPage` depending on shape
- `internal_links` — example anchor + URL pairs (rewire to your site)
- `status` — all `pending` so the orchestrator picks them up in order

## Want a vertical we don't ship?

Open a [Discussion](https://github.com/viren040/content-seo-orchestrator/discussions) — patterns we'd like to add: marketplace, fintech, healthcare, edtech, real estate, restaurants.
