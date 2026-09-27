#!/usr/bin/env bash
# Publish this site to allgemselect.com too.
#
#   scripts/sync-allgemselect.sh
#
# The canonical site is https://jbaker00.github.io/nfsfiles-site/ — the app
# and the App Store listing link there directly (James, 2026-09-26: no
# redirecting people to allgemselect.com). allgemselect.com stays up only
# for the pending AdSense review, so it's a mirror: the separate GitHub
# Pages repo jbaker00/allgemselect-site, holding this same tree with
#   url: https://allgemselect.com · baseurl: "" · adsense: true · CNAME
# GitHub Pages lets one custom domain belong to one repo, and a repo with a
# custom domain redirects its github.io address to it — hence two repos.
#
# Run after pushing a site change. If AdSense approves and the site moves to
# allgemselect.com for good, retire the mirror instead: put the CNAME back
# here and point the app/ASC links at the domain in the next release.
set -euo pipefail
cd "$(dirname "$0")/.."
MIRROR=${MIRROR_DIR:-$HOME/code/allgemselect-site}
[[ -z $(git status --porcelain) ]] || { echo "commit (and push) the site first"; exit 1; }
[[ -d $MIRROR/.git ]] || git clone -q https://github.com/jbaker00/allgemselect-site.git "$MIRROR"
git -C "$MIRROR" pull -q --ff-only || true
SRC=$(git rev-parse --short HEAD)

rsync -a --delete --exclude .git ./ "$MIRROR/"
cd "$MIRROR"
sed -i '' -e 's#^url: .*#url: https://allgemselect.com#' \
          -e 's#^baseurl: .*#baseurl: ""#' \
          -e 's#^adsense: .*#adsense: true#' _config.yml
grep -q '^adsense: true' _config.yml || { echo "override failed — check _config.yml keys"; exit 1; }
echo allgemselect.com > CNAME

git add -A
if git diff --cached --quiet; then
  echo "mirror already matches nfsfiles-site $SRC"
else
  git commit -q -m "Mirror nfsfiles-site $SRC"
  git push -q origin HEAD:main
  echo "mirror updated to nfsfiles-site $SRC"
fi
