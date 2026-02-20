#!/bin/bash
# Run this from the root of your null-void repo
# Usage: bash create-pr.sh

set -e

BRANCH="fix/consistency-ch1-ch4"
PATCH_FILE="consistency-fixes.patch"

# Check we're in the right repo
if [ ! -d "World-Bible" ]; then
    echo "ERROR: Run this from the root of the null-void repo"
    exit 1
fi

# Make sure we're on main and up to date
git checkout main
git pull origin main

# Create branch and apply patch
git checkout -b "$BRANCH"
git apply "$PATCH_FILE"
git add -A
git commit -m "fix: consistency fixes for Ch1-Ch4 (Nix, Sai, Standoff, Paladins)

## Changes

### Fix 1: Nix species/gender (Ch1)
- Changed Nix from cat/female to rabbit/male matching characters/Nix.md

### Fix 2: Sai gravity cycle foreshadowing (Ch1 + Ch2)
- Ch1: sensory seed during repair scene
- Ch2: Kito times heist for Sai's heavy phase

### Fix 3: Ch3 structural revision — Mexican Standoff + Paladins
- NEW Part III (Pasca): Vlk betrayal, 22 Inkvizícia guards
- NEW Part IV (Opice): Rau + Kira, massacre, Hard Light reveal, collapse
- Maks screams BEŽ! ZACHRÁŇ ICH! (only time in the book)
- Renumbered Kobky from Part IV → Part V

### Fix 4: Ch4 opening adjustment
- Maks follows Paladins from Ch3 instead of discovering them fresh
- Trimmed redundant description, updated cross-references"

# Push
git push origin "$BRANCH"

# Create PR via GitHub CLI (if available)
if command -v gh &> /dev/null; then
    gh pr create \
        --title "fix: Consistency fixes Ch1–Ch4 (Nix, Sai, Standoff, Paladins)" \
        --body "## Summary

Fixes 4 consistency issues identified during a review of Prologue → Ch3 leading into Ch4.

### Fix 1: Nix Species/Gender (Ch1)
Nix was described as a cat (Felis/female) on line 37 but as a rabbit (Usagi/male) on line 93 and in \`characters/Nix.md\`. Fixed to Usagi/male throughout.

### Fix 2: Sai Gravity Cycle — Early Introduction (Ch1 + Ch2)
The Sai 20-hour gravity cycle appeared for the first time in Ch3 as a key tactical element with zero prior setup. Added two seeds:
- **Ch1:** Sensory mention during repair scene (light phase)
- **Ch2:** Kito explicitly times the heist for Sai's heavy phase

### Fix 3: Ch3 Structural Revision (Major — +142 lines)
Replaced the old artillery-based collapse with the full planned sequence from \`planning/01-prach-nevriss.md\`:
- **Part III (Pasca):** Mexican Standoff — Vlk's betrayal pays off, 22 Inkvizícia guards surround the group
- **Part IV (Opice):** Rau + Kira enter through the wall, massacre all guards, Hard Light shields revealed, Rau's axe collapses the tunnel, Maks screams \"BEŽ! ZACHRÁŇ ICH!\"
- Kobky section renumbered to Part V

### Fix 4: Ch4 Opening Adjustment
Maks now follows the Paladins from Ch3 rather than encountering them for the first time. Trimmed redundant armor description, reframed shooting as a known-futile second attempt.

---

**Files changed:** 4 | **+142 / -26**" \
        --base main
    echo "PR created!"
else
    echo ""
    echo "==========================================="
    echo "Branch pushed! Create the PR manually at:"
    echo "https://github.com/BranLang/null-void/compare/main...$BRANCH"
    echo "==========================================="
fi
