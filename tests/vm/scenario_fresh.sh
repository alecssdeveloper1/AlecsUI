#!/usr/bin/env bash
# Run ON a clean staging VM as root. Does not run on the developer Windows host.
set -euo pipefail
INSTALL_SH=${1:-./install.sh}
[ "$(id -u)" -eq 0 ] || { echo "root required"; exit 1; }
[ -f "$INSTALL_SH" ] || { echo "missing $INSTALL_SH"; exit 1; }
bash -n "$INSTALL_SH"
echo "=== Installing AlecsUI from $INSTALL_SH ==="
bash "$INSTALL_SH"
echo "=== Post checks ==="
bash "$(dirname "$0")/scenario_health.sh"
echo "FRESH INSTALL SCENARIO DONE"
