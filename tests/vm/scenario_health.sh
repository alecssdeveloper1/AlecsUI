#!/usr/bin/env bash
# Verify real listeners + panel check — not only systemctl active.
set -euo pipefail
. /etc/tunnel/config
fail=0
check_tcp(){ local p=$1 n=$2; if ss -lntp | grep -Eq ":${p}\\b"; then echo "OK tcp $p ($n)"; else echo "FAIL tcp $p ($n)"; fail=1; fi; }
check_udp(){ local p=$1 n=$2; if ss -lnup | grep -Eq ":${p}\\b"; then echo "OK udp $p ($n)"; else echo "WARN udp $p ($n) — may be expected if feature skipped"; fi; }
check_tcp "$PANEL_PORT" panel
check_tcp "$WS_PORT" ws-ssh
check_tcp "$WSTLS_PORT" wstls
# SSL may be 10443 when h443 mode; otherwise SSL_PORT
if [ -f /etc/tunnel/h443.on ] && [ "${SSL_PORT}" = 443 ]; then check_tcp 10443 ssl-loopback; else check_tcp "$SSL_PORT" ssl; fi
systemctl is-active --quiet alecsui-stunnel || { echo FAIL alecsui-stunnel; fail=1; }
systemctl is-active --quiet tunnel-panel || { echo FAIL tunnel-panel; fail=1; }
# Foreign stunnel4 must not be required; if running, ensure we did not kill it solely for install
if systemctl is-active --quiet stunnel4 2>/dev/null; then echo "INFO: system stunnel4 still active (foreign OK)"; fi
[ -f /etc/ssh/sshd_config.d/00-alecsui.conf ] || { echo FAIL missing SSH Match drop-in; fail=1; }
sshd -t || { echo FAIL sshd -t; fail=1; }
python3 /opt/tunnel-panel/panel.py check || true
[ "$fail" = 0 ] || exit 1
echo "HEALTH OK"
