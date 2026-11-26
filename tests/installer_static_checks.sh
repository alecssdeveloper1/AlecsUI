#!/usr/bin/env bash
# Static checks for install.sh — does NOT run the installer on a live VPS.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== bash -n install.sh =="
bash -n install.sh

echo "== required markers =="
grep -q 'ALECSUI_VER=1.9.4' install.sh
grep -q 'ui_banner' install.sh
grep -q 'ui_pick_lang' install.sh
grep -q 'os_check' install.sh
grep -q 'install_lock' install.sh
grep -q 'stunnel_ours_pids' install.sh
grep -q 'pre_upgrade_backup' install.sh
grep -q 'AlecsUI-selfsigned' install.sh
grep -q 'SHA256 missing or mismatched' install.sh
grep -q 'alecsui-stunnel' install.sh
grep -qE 'Match Group (\$SSH_GROUP|alecsui-ssh)' install.sh
grep -q 'dl_official_digest' install.sh
grep -q 'BADVPN_COMMIT=752c6b49' install.sh
! grep -q 'pkill -KILL -x stunnel4' install.sh
! grep -q 'subj "/CN=www.google.com"' install.sh
! grep -q 'curl -fsSL https://get.acme.sh | sh' install.sh

echo "== python extract =="
python3 tests/extract_and_check.py

if command -v shellcheck >/dev/null 2>&1; then
  echo "== shellcheck (advisory) =="
  # Full file is huge/embedded; focus on early functions by disabling some noise
  shellcheck -e SC2034,SC2086,SC2155,SC2164,SC2181,SC1091,SC2002,SC2016 install.sh || true
else
  echo "shellcheck not installed — skipped"
fi

echo "OK: installer static checks passed"
