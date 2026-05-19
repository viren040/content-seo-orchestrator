#!/usr/bin/env bash
# ============================================================
# content-seo-orchestrator — one-shot bootstrap
# Usage: ./setup.sh
# ============================================================

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() {
  echo ""
  echo -e "${GREEN}==>${NC} $1"
}

print_warn() {
  echo -e "${YELLOW}!${NC}  $1"
}

print_err() {
  echo -e "${RED}x${NC}  $1"
}

# ---- 1. Sanity checks ----
print_step "Checking prerequisites"

if ! command -v python3 &> /dev/null; then
  print_err "python3 not found. Install Python 3.10+ first."
  exit 1
fi
echo "    python3: $(python3 --version)"

if ! command -v git &> /dev/null; then
  print_err "git not found. Install git first."
  exit 1
fi
echo "    git: $(git --version)"

if [ ! -f "config/seo-settings.yaml" ]; then
  print_err "config/seo-settings.yaml not found. Are you in the repo root?"
  exit 1
fi
echo "    repo root: yes"

# ---- 2. Python venv + deps ----
print_step "Setting up Python environment"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  echo "    created .venv"
else
  echo "    .venv exists, skipping"
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet pyyaml pillow requests
echo "    installed pyyaml, pillow, requests"

# ---- 3. .env setup ----
print_step "Setting up .env"

if [ ! -f ".env" ]; then
  cp .env.example .env
  print_warn ".env created from .env.example. Edit it to add your real API keys."
  print_warn "Minimum required:"
  echo "      - PERPLEXITY_API_KEY (or run /seo-research in manual paste mode)"
  echo "      - SANITY_AUTH_TOKEN, SANITY_PROJECT_ID (if publishing to Sanity)"
else
  echo "    .env already exists, skipping"
fi

# ---- 4. Config check ----
print_step "Verifying config/seo-settings.yaml"

if grep -q "your-project-id\|Your Brand\|example.com" config/seo-settings.yaml; then
  print_warn "config/seo-settings.yaml has placeholder values."
  print_warn "Edit these before running /seo-status:"
  echo "      - brand.name, brand.website, brand.cta_url"
  echo "      - sanity.project_id (or set in .env)"
  echo "      - content_rules.voice + tone_guidelines"
else
  echo "    seo-settings.yaml looks customized"
fi

# ---- 5. Pipeline check ----
print_step "Verifying pipeline.yaml"

post_count=$(python3 -c "
import yaml
with open('pipeline.yaml') as f:
    p = yaml.safe_load(f)
print(len(p.get('posts', [])))
" 2>/dev/null || echo "0")

if [ "$post_count" -eq 0 ]; then
  print_warn "pipeline.yaml has no posts."
  print_warn "Copy a starter from examples/ or add your own posts:"
  echo "      cp examples/b2b-saas.pipeline.yaml pipeline.yaml"
  echo "      cp examples/d2c-ecommerce.pipeline.yaml pipeline.yaml"
  echo "      cp examples/local-business.pipeline.yaml pipeline.yaml"
  echo "      cp examples/agency.pipeline.yaml pipeline.yaml"
else
  echo "    pipeline.yaml has $post_count posts"
fi

# ---- 6. Claude Code check ----
print_step "Checking Claude Code setup"

if [ ! -d ".claude/commands" ]; then
  print_err ".claude/commands/ not found. The orchestrator depends on these."
  exit 1
fi

cmd_count=$(ls .claude/commands/seo-*.md 2>/dev/null | wc -l | tr -d ' ')
echo "    found $cmd_count /seo-* commands"

# ---- 7. Done ----
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup complete.${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "  1. Edit .env (add PERPLEXITY_API_KEY, SANITY_AUTH_TOKEN at minimum)"
echo "  2. Edit config/seo-settings.yaml (your brand, voice, CTAs)"
echo "  3. Make sure pipeline.yaml has your posts (copy from examples/ if needed)"
echo "  4. Open this folder in Claude Code"
echo "  5. Run: /seo-status"
echo ""
echo "Docs:"
echo "  - README:        ./README.md"
echo "  - Architecture:  ./docs/ARCHITECTURE.md"
echo "  - FAQ:           ./docs/FAQ.md"
echo "  - AEO scorecard: ./docs/AEO-SCORECARD.md"
echo "  - Comparison:    ./docs/COMPARISON.md"
echo ""
