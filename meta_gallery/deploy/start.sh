#!/usr/bin/env bash
# Start the dashboard on a host such as Render, in team mode.
# Files people create (made images, notes, usage) live on the persistent disk when there is one,
# so a redeploy does not wipe them. Data files from git (sales, ads, health) always come from the repo.
set -euo pipefail
cd "$(dirname "$0")/../.."
D=data/meta-gallery
P="${PERSIST_DIR:-/var/data}"
# Only on the host (Render sets RENDER=true), never on a laptop copy of the repo.
if { [ "${RENDER:-}" = "true" ] || [ -n "${PERSIST_DIR:-}" ]; } && [ -d "$P" ] && [ -w "$P" ]; then
  for x in variants product_ads product_story catalog_refresh products images breakdowns.json notes.json settings.json packs.json playbook.json tests.json catalog_prompt.json client_orders.json; do
    if [ ! -e "$P/$x" ] && [ -e "$D/$x" ]; then cp -a "$D/$x" "$P/$x"; fi
    if [ -e "$P/$x" ]; then rm -rf "${D:?}/$x"; ln -s "$P/$x" "$D/$x"; fi
  done
  export TEAM_STATE="${TEAM_STATE:-$P/team}"
else
  echo "No persistent disk at $P: made images and usage counts reset on each deploy."
fi
export TEAM_MODE=1
exec python -m meta_gallery.server
