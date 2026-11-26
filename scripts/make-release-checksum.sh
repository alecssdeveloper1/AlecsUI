#!/usr/bin/env bash
# Maintainer helper: sha256 for GitHub Release asset install.sh
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
sha256sum install.sh | tee install.sh.sha256
echo "Attach install.sh and install.sh.sha256 to the GitHub Release tag."
