#!/usr/bin/env python3
"""Apply AlecsUI v1.9.1 hardening patches to install.sh (local only)."""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.sh"

NEW_HEADER = r'''#!/bin/bash
# AlecsUI v1.9.1 installer
# Self-hosted SSH + Xray panel: SSH, SSL, SSH WebSocket (+TLS), UDPGW, Xray (VLESS XHTTP TLS / TCP TLS / Reality / XHTTP, Trojan), OpenVPN (TCP + HTTP proxy), Hysteria2 (UDP), WireGuard, DNS tunnel (dnstt) + V2Ray,
# web panel with users, subscriptions, data and device limits, Telegram alerts, backups, 2FA, and a terminal menu.
# Run as root on Ubuntu or Debian:  bash install.sh   (running it again updates AlecsUI and keeps users and settings)
# https://github.com/alecssdeveloper1/AlecsUI · License: GPL-3.0 · fork of ReXUI by Ali (chaliraza777) · maintained by Alecs (alecssdeveloper1)
# Modified from ReXUI — see CHANGELOG.md and NOTICE.
set -e
trap 'echo -e "\n\033[1;31mERROR: failed at line $LINENO\033[0m"' ERR
[ "${EUID:-$(id -u)}" -ne 0 ] && { echo "Please run as root"; exit 1; }

ALECSUI_VER=1.9.1
SSH_PORT_DEF=22
SSL_PORT=443; WS_PORT=8880; WSTLS_PORT=2083; UDPGW_PORT=7300; VWSTLS_PORT=8443; VTCP_PORT=2053; VWS_PORT=8080; REALITY_PORT=8444; TROJAN_PORT=2096; OVPN1_PORT=1194; OVPN2_PORT=110; SQUID_PORT=3128; HY_PORT=443; HY_HOP=20000-30000; WG_PORT=51820; HYV=2.13.0; DNSTTV=v1.20240513.0
# BadVPN tag 1.999.130 resolved commit (pinned; clone must match)
BADVPN_COMMIT=48bc05d4b052e7dccc3cfa5ed4dadbe35d20d0c0
ACME_VER=3.1.0
LIB=/usr/local/lib/tunnel
XRAY_VER=v26.11.9
LOCKF=/run/alecsui-install.lock
CAPF=/etc/tunnel/capabilities
MANIFEST=/etc/tunnel/manifest.json
ORIGD=/etc/tunnel/originals
ALECSUI_STUNNEL_CONF=/etc/alecsui/stunnel.conf
ALECSUI_STUNNEL_PEM=/etc/alecsui/stunnel.pem
ALECSUI_STUNNEL_UNIT=alecsui-stunnel
SSH_GROUP=alecsui-ssh
OUR_UNITS='alecsui-stunnel|xray|ws-ssh|badudp|tunnel-panel|alecsui-helper|haproxy|squid|alecsui-ovpn@|alecsui-hy2|alecsui-wg|alecsui-dns|fail2ban'
OUR_BINS='stunnel|xray|openvpn|squid|haproxy|hysteria|dnstt-server|badvpn-udpgw'

step(){ echo -e "\n\033[1;36m[$1/11]\033[0m $2"; }

install_lock(){
  mkdir -p "$(dirname "$LOCKF")"
  exec 9>"$LOCKF"
  if ! flock -n 9; then
    echo -e "\033[1;31mERROR: another AlecsUI install/update is already running (lock $LOCKF).\033[0m"
    exit 1
  fi
  echo "$$ $(date -Is) AlecsUI $ALECSUI_VER" >&9
}

manifest_init(){
  mkdir -p /etc/tunnel "$ORIGD"
  [ -f "$MANIFEST" ] || echo '{"version":"'"$ALECSUI_VER"'","files":[],"units":[],"dirs":[],"sysctl":[],"cron":[],"ufw":[],"groups":[],"users_sys":[]}' > "$MANIFEST"
  chmod 600 "$MANIFEST"
}
manifest_add(){
  local kind="$1" path="$2"
  python3 - "$MANIFEST" "$kind" "$path" <<'PY'
import json,sys
p,k,v=sys.argv[1],sys.argv[2],sys.argv[3]
try: o=json.load(open(p))
except Exception: o={"files":[],"units":[],"dirs":[],"sysctl":[],"cron":[],"ufw":[],"groups":[],"users_sys":[]}
o.setdefault(k,[]);
if v not in o[k]: o[k].append(v)
o["version"]=o.get("version") or ""
json.dump(o, open(p,"w"), indent=1)
PY
}

pre_upgrade_backup(){
  [ -d /etc/tunnel ] || return 0
  local bdir=/root/alecsui-preinstall-$(date +%F-%H%M%S)
  mkdir -p "$bdir"
  cp -a /etc/tunnel "$bdir/" 2>/dev/null || true
  [ -d /etc/alecsui ] && cp -a /etc/alecsui "$bdir/" 2>/dev/null || true
  [ -f /etc/stunnel/stunnel.conf ] && cp -a /etc/stunnel/stunnel.conf "$bdir/foreign-or-legacy-stunnel.conf" 2>/dev/null || true
  if [ -x /opt/tunnel-panel/panel.py ]; then
    python3 /opt/tunnel-panel/panel.py backup "$bdir/users-settings.json" >/dev/null 2>&1 || true
    chmod 600 "$bdir/users-settings.json" 2>/dev/null || true
  fi
  chmod -R go-rwx "$bdir" 2>/dev/null || true
  echo "Pre-install backup: $bdir"
}

pid_unit(){
  local pid="$1" u=""
  [ -n "$pid" ] && [ "$pid" -gt 1 ] 2>/dev/null || { echo ""; return; }
  u=$(systemctl status "$pid" 2>/dev/null | awk -F'[● ]+' '/\.service/{print $2; exit}')
  [ -n "$u" ] || u=$(tr '\0' ' ' <"/proc/$pid/cgroup" 2>/dev/null | grep -oE '[^/]+\.service' | tail -1 || true)
  echo "${u:-}"
}

# AlecsUI stunnel only: dedicated unit OR cmdline with our conf path
is_alecsui_stunnel_pid(){
  local pid="$1" unit cmd
  [ -n "$pid" ] && [ "$pid" -gt 1 ] 2>/dev/null || return 1
  unit=$(pid_unit "$pid")
  [ "$unit" = "${ALECSUI_STUNNEL_UNIT}.service" ] && return 0
  cmd=$(tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null || true)
  echo "$cmd" | grep -Fq "$ALECSUI_STUNNEL_CONF" && return 0
  return 1
}

ours_listener(){
  local pid="$1" unit bin
  unit=$(pid_unit "$pid")
  if [ -n "$unit" ] && echo "$unit" | grep -Eqi "$OUR_UNITS"; then return 0; fi
  if is_alecsui_stunnel_pid "$pid"; then return 0; fi
  bin=$(tr '\0' ' ' <"/proc/$pid/comm" 2>/dev/null || true)
  [ -z "$bin" ] && bin=$(ps -p "$pid" -o comm= 2>/dev/null || true)
  if echo "$bin" | grep -Eqi 'python'; then
    tr '\0' ' ' <"/proc/$pid/cmdline" 2>/dev/null | grep -Eq 'tunnel-panel|ws-ssh\.py|alecsui-helper' && return 0
    return 1
  fi
  if echo "$bin" | grep -Eqi "^($OUR_BINS)$"; then
    # Never claim generic stunnel4 as ours without conf path
    if echo "$bin" | grep -Eqi 'stunnel'; then
      is_alecsui_stunnel_pid "$pid" && return 0
      return 1
    fi
    return 0
  fi
  return 1
}

# busy PORT proto  — checks IPv4 and IPv6; does not steal foreign ports
busy(){
  local port="$1" proto="${2:-tcp}" line pid rest foreign=0 fam
  for fam in -4 -6; do
    local ss_args=(-ln "$fam")
    [ "$proto" = udp ] && ss_args+=(-u) || ss_args+=(-t)
    while IFS= read -r line; do
      echo "$line" | grep -Eq ":${port}([^0-9]|$)" || continue
      pid=$(echo "$line" | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2)
      if [ -z "$pid" ]; then
        echo "Port $port/$proto ($fam) in use (owner unknown):"; echo "  $line"; foreign=1; continue
      fi
      if ours_listener "$pid"; then continue; fi
      rest=$(ps -p "$pid" -o user=,pid=,comm=,args= 2>/dev/null || echo "pid=$pid")
      echo "Port $port/$proto ($fam) is already in use by another program:"
      echo "  $rest"; echo "  $line"; foreign=1
    done < <(ss "${ss_args[@]}" -p 2>/dev/null || true)
  done
  if [ "$foreign" = 1 ]; then
    echo "AlecsUI will not take over foreign ports."
    return 1
  fi
  return 0
}

# If preferred port is foreign-busy, pick next free from candidates (never steal)
pick_free_tcp(){
  local var="$1"; shift
  local cur="${!var}" c
  if busy "$cur" tcp; then return 0; fi
  echo -e "\033[1;33mPort $cur/tcp is taken by a foreign process — selecting an alternate for $var.\033[0m"
  for c in "$@"; do
    [ "$c" = "$cur" ] && continue
    if busy "$c" tcp; then
      eval "$var=$c"
      echo "  -> $var=$c"
      return 0
    fi
  done
  echo -e "\033[1;31mERROR: no free TCP port for $var among candidates.\033[0m"
  exit 1
}

stunnel_ours_pids(){
  local pids=() p line pid
  p=$(systemctl show -p MainPID --value "${ALECSUI_STUNNEL_UNIT}" 2>/dev/null || true)
  if [ -n "$p" ] && [ "$p" != 0 ] && is_alecsui_stunnel_pid "$p"; then pids+=("$p"); fi
  for f in /run/alecsui/stunnel.pid /var/run/alecsui/stunnel.pid; do
    [ -f "$f" ] || continue
    p=$(tr -dc '0-9' <"$f" 2>/dev/null || true)
    [ -n "$p" ] && is_alecsui_stunnel_pid "$p" && pids+=("$p")
  done
  while IFS= read -r line; do
    pid=$(echo "$line" | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2)
    [ -n "$pid" ] || continue
    is_alecsui_stunnel_pid "$pid" && pids+=("$pid")
  done < <(ss -lntp 2>/dev/null | grep -E "stunnel" || true)
  # Legacy: only if our marker file says we previously owned stunnel4 via AlecsUI conf path
  if [ -f /etc/tunnel/legacy-stunnel4.owned ] && [ -f /etc/stunnel/stunnel.conf ] && grep -q 'AlecsUI' /etc/stunnel/stunnel.conf 2>/dev/null; then
    p=$(systemctl show -p MainPID --value stunnel4 2>/dev/null || true)
    if [ -n "$p" ] && [ "$p" != 0 ]; then
      cmd=$(tr '\0' ' ' <"/proc/$p/cmdline" 2>/dev/null || true)
      echo "$cmd" | grep -Eq '/etc/stunnel/stunnel\.conf' && pids+=("$p")
    fi
  fi
  printf '%s\n' "${pids[@]}" | awk 'NF && !seen[$0]++'
}

# Stop ONLY AlecsUI stunnel unit/PIDs — never systemctl stop stunnel4 unless legacy-owned marker
stunnel_stop_clean(){
  local pid still i
  echo "Preparing AlecsUI stunnel ($ALECSUI_STUNNEL_UNIT)..."
  systemctl stop "$ALECSUI_STUNNEL_UNIT" 2>/dev/null || true
  if [ -f /etc/tunnel/legacy-stunnel4.owned ]; then
    echo "  legacy AlecsUI stunnel4 ownership marker present — stopping stunnel4 only for migration"
    systemctl stop stunnel4 2>/dev/null || true
  fi
  for pid in $(stunnel_ours_pids); do
    if kill -0 "$pid" 2>/dev/null; then
      echo "  TERM AlecsUI stunnel pid $pid"
      kill -TERM "$pid" 2>/dev/null || true
    fi
  done
  for i in 1 2 3 4 5; do
    still=0
    for pid in $(stunnel_ours_pids); do kill -0 "$pid" 2>/dev/null && still=1; done
    [ "$still" = 0 ] && break
    sleep 1
  done
  for pid in $(stunnel_ours_pids); do
    if kill -0 "$pid" 2>/dev/null; then
      echo "  KILL AlecsUI stunnel pid $pid (after TERM timeout)"
      kill -KILL "$pid" 2>/dev/null || true
    fi
  done
  mkdir -p /run/alecsui /var/run/alecsui /etc/alecsui
  chmod 755 /run/alecsui /etc/alecsui
}

stunnel_write_conf(){
  mkdir -p /etc/alecsui
  local accept_ssl
  if [ -f /etc/tunnel/h443.on ] && [ "$SSL_PORT" = 443 ]; then accept_ssl=127.0.0.1:10443; else accept_ssl=$SSL_PORT; fi
  cat > "$ALECSUI_STUNNEL_CONF" <<S
; AlecsUI $ALECSUI_VER dedicated stunnel — foreign stunnel4 untouched
pid = /run/alecsui/stunnel.pid
cert = $ALECSUI_STUNNEL_PEM
sslVersionMin = TLSv1.2
socket = l:TCP_NODELAY=1
socket = r:TCP_NODELAY=1
[ssh-ssl]
accept = $accept_ssl
connect = 127.0.0.1:$SSH_PORT
[ssh-ws-tls]
accept = $WSTLS_PORT
connect = 127.0.0.1:$WS_PORT
S
  chmod 644 "$ALECSUI_STUNNEL_CONF"
  manifest_add files "$ALECSUI_STUNNEL_CONF"
  cat > /etc/systemd/system/${ALECSUI_STUNNEL_UNIT}.service <<S
[Unit]
Description=AlecsUI stunnel (SSH SSL / WS-TLS)
After=network.target
[Service]
Type=simple
ExecStart=/usr/bin/stunnel4 $ALECSUI_STUNNEL_CONF
ExecReload=/bin/kill -HUP \$MAINPID
Restart=on-failure
RestartSec=3
PrivateTmp=true
[Install]
WantedBy=multi-user.target
S
  manifest_add units "${ALECSUI_STUNNEL_UNIT}.service"
}

stunnel_start_ok(){
  stunnel_stop_clean
  stunnel_write_conf
  systemctl daemon-reload
  systemctl enable "$ALECSUI_STUNNEL_UNIT" >/dev/null 2>&1 || true
  if ! systemctl start "$ALECSUI_STUNNEL_UNIT"; then
    echo -e "\033[1;31mERROR: $ALECSUI_STUNNEL_UNIT failed to start\033[0m"
    journalctl -u "$ALECSUI_STUNNEL_UNIT" -n 20 --no-pager 2>/dev/null || true
    return 1
  fi
  sleep 1
  if systemctl is-active --quiet "$ALECSUI_STUNNEL_UNIT" && ss -lntp 2>/dev/null | grep -E ":($SSL_PORT|$WSTLS_PORT|10443)\\b" | grep -qi stunnel; then
    echo "$ALECSUI_STUNNEL_UNIT is active and listening"
    return 0
  fi
  echo -e "\033[1;31mERROR: $ALECSUI_STUNNEL_UNIT not listening after start\033[0m"
  systemctl status "$ALECSUI_STUNNEL_UNIT" --no-pager -l 2>/dev/null || true
  return 1
}

vps_probe(){
  local virt=unknown kern arch
  kern=$(uname -r); arch=$(uname -m)
  echo "VPS capability check (AlecsUI $ALECSUI_VER)..."
  echo "  Kernel: $kern  Arch: $arch"
  if [ -f /proc/vz/version ] || uname -r | grep -Eqi 'vz|virtuozzo|openvz'; then virt=openvz
  elif grep -qiE 'container|lxc' /proc/1/environ 2>/dev/null || [ -f /.dockerenv ] || uname -r | grep -Eqi 'lxc|container'; then virt=lxc
  elif systemd-detect-virt >/dev/null 2>&1; then virt=$(systemd-detect-virt 2>/dev/null || echo kvm)
  elif [ -d /proc/xen ]; then virt=xen
  else virt=kvm; fi
  echo "  Virt: $virt"
  CAP_TUN=0; CAP_WG=0; CAP_BBR=0; CAP_SYSTEMD=0; CAP_OVPN=0
  command -v systemctl >/dev/null && systemctl list-units >/dev/null 2>&1 && CAP_SYSTEMD=1
  [ "$CAP_SYSTEMD" = 1 ] || { echo -e "\033[1;31mERROR: systemd is required.\033[0m"; exit 1; }
  if [ -c /dev/net/tun ]; then CAP_TUN=1; CAP_OVPN=1; echo "  TUN: OK"; else
    echo -e "\033[1;33m  TUN: MISSING — OpenVPN NOT SUPPORTED.\033[0m"
  fi
  if modprobe tcp_bbr 2>/dev/null || grep -qw bbr /proc/sys/net/ipv4/tcp_available_congestion_control 2>/dev/null; then
    CAP_BBR=1; echo "  BBR: OK"
  else echo -e "\033[1;33m  BBR: NOT SUPPORTED.\033[0m"; fi
  if modprobe wireguard 2>/dev/null && ip link add rxwg-probe type wireguard 2>/dev/null; then
    ip link del rxwg-probe 2>/dev/null || true; CAP_WG=1; echo "  WireGuard: OK"
  else
    ip link del rxwg-probe 2>/dev/null || true
    echo -e "\033[1;33m  WireGuard: NOT SUPPORTED.\033[0m"
  fi
  case "$virt" in openvz|lxc) echo -e "\033[1;33mNOTE: $virt detected. Prefer KVM for OpenVPN/WireGuard/BBR.\033[0m";; esac
  mkdir -p /etc/tunnel
  cat > "$CAPF" <<C
ALECSUI_VER=$ALECSUI_VER
VIRT=$virt
ARCH=$arch
KERNEL=$kern
CAP_TUN=$CAP_TUN
CAP_OVPN=$CAP_OVPN
CAP_WG=$CAP_WG
CAP_BBR=$CAP_BBR
CAP_SYSTEMD=$CAP_SYSTEMD
C
  chmod 644 "$CAPF"
  WG_KERNEL_OK=$CAP_WG
  export WG_KERNEL_OK CAP_TUN CAP_OVPN CAP_WG CAP_BBR
}

# Official digest ONLY from github.com (never from mirror). Binary may use mirror but must match official digest.
dl_official_digest(){
  local out="$1" url="$2"
  [[ "$url" == https://github.com/* ]] || { echo "ERROR: digest URL must be github.com"; return 1; }
  rm -f "$out"
  curl -fL --connect-timeout 10 --max-time 60 -o "$out" "$url" || return 1
  [ -s "$out" ] || return 1
}

dl(){
  local out="$1" url="$2" min="${3:-0}" expect="${4:-}" u ok=0 got
  local mirrors=("" "https://ghfast.top/" "https://ghproxy.net/" "https://mirror.ghproxy.com/" "https://github.moeyy.xyz/")
  for m in "${mirrors[@]}"; do
    if [[ "$url" == https://github.com/* ]]; then u="${m}${url}"; else u="$url"; [ -n "$m" ] && continue; fi
    echo "  -> $u"
    rm -f "$out"
    if command -v curl >/dev/null 2>&1; then
      curl -fL --connect-timeout 8 --max-time 90 --retry 1 --retry-delay 1 -o "$out" "$u" && ok=1 || ok=0
    elif command -v wget >/dev/null 2>&1; then
      wget -q --timeout=8 --tries=2 -O "$out" "$u" && ok=1 || ok=0
    else echo "ERROR: curl/wget missing"; return 1; fi
    if [ "$ok" = 1 ] && [ -f "$out" ] && [ "$(stat -c%s "$out" 2>/dev/null || echo 0)" -ge "$min" ]; then
      if [ -n "$expect" ]; then
        got=$(sha256sum "$out" | awk '{print $1}')
        if [ "$got" != "$expect" ]; then echo "  SHA256 mismatch — rejecting"; rm -f "$out"; continue; fi
        echo "  OK + SHA256 verified"
      else echo "  OK ($(du -h "$out" | awk '{print $1}'))"; fi
      return 0
    fi
    rm -f "$out"
  done
  return 1
}

install_lock
manifest_init
[ -f /etc/tunnel/config ] && . /etc/tunnel/config
[ -f "$CAPF" ] && . "$CAPF" 2>/dev/null || true
if [ -z "${PANEL_PORT:-}" ]; then
  PANEL_PORT=$(shuf -i 20000-59999 -n1)
  while ! busy "$PANEL_PORT" tcp; do PANEL_PORT=$(shuf -i 20000-59999 -n1); done
fi
[ -n "${WEB_PATH:-}" ] || WEB_PATH=$(tr -dc a-z0-9 </dev/urandom | head -c 10)
pre_upgrade_backup
vps_probe

# Port plan: never steal; reassign SSL if foreign stunnel holds 443
stunnel_stop_clean
pick_free_tcp SSL_PORT 443 444 10443 8443 9443
pick_free_tcp WS_PORT 8880 8881 8081 9080
pick_free_tcp WSTLS_PORT 2083 2084 2087 2096
busy "$PANEL_PORT" tcp || { echo "PANEL_PORT busy"; exit 1; }
if [ -c /dev/net/tun ]; then
  pick_free_tcp OVPN1_PORT 1194 1195 1196
  pick_free_tcp OVPN2_PORT 110 111 112
  pick_free_tcp SQUID_PORT 3128 3129 8080
fi
busy "$HY_PORT" udp || { echo -e "\033[1;33mUDP $HY_PORT busy — set HY_PORT in /etc/tunnel/config after install if needed.\033[0m"; }
if [ "${CAP_WG:-0}" = 1 ]; then
  busy "$WG_PORT" udp || echo -e "\033[1;33mUDP $WG_PORT (WireGuard) busy — WG may fail until free.\033[0m"
fi

export DEBIAN_FRONTEND=noninteractive
mkdir -p /etc/tunnel/cert $LIB /etc/alecsui "$ORIGD"

step 1 "Packages"
echo "Updating apt package lists..."
apt-get update -qq
echo "Installing packages (this can take several minutes)..."
PKGS="openssh-server stunnel4 fail2ban cmake build-essential git openssl curl cron python3 socat unzip iptables squid"
[ "${CAP_OVPN:-0}" = 1 ] && PKGS="$PKGS openvpn"
# shellcheck disable=SC2086
apt-get install -y -qq $PKGS >/dev/null
apt-get install -y -qq haproxy >/dev/null 2>&1 || echo -e "\033[1;33mHAProxy could not be installed, 443 mode stays off.\033[0m"
echo "Packages OK"
[ "${CAP_OVPN:-0}" = 1 ] || echo -e "\033[1;33mOpenVPN package skipped (no TUN).\033[0m"

step 2 "SSH tuning (Match Group $SSH_GROUP — password auth ONLY for tunnel users)"
mkdir -p /etc/ssh/sshd_config.d
grep -q '^Include' /etc/ssh/sshd_config || sed -i '1i Include /etc/ssh/sshd_config.d/*.conf' /etc/ssh/sshd_config
# Backup existing drop-in / effective snippets we replace
if [ -f /etc/ssh/sshd_config.d/00-tunnel.conf ]; then
  cp -a /etc/ssh/sshd_config.d/00-tunnel.conf "$ORIGD/00-tunnel.conf.bak.$(date +%s)"
fi
getent group "$SSH_GROUP" >/dev/null || groupadd --system "$SSH_GROUP"
manifest_add groups "$SSH_GROUP"
ROOT_LOGIN=$(sshd -T 2>/dev/null | awk '/^permitrootlogin /{print $2; exit}')
# Global: do NOT enable PasswordAuthentication for everyone. Only Match Group.
cat > /etc/ssh/sshd_config.d/00-alecsui.conf <<S
# Managed by AlecsUI $ALECSUI_VER
# PasswordAuthentication is NOT enabled globally.
# Tunnel VPN/SSH clients are in group $SSH_GROUP and matched below.
UseDNS no
TCPKeepAlive yes
ClientAliveInterval 15
ClientAliveCountMax 2
AllowTcpForwarding yes
Compression no
Match Group $SSH_GROUP
    PasswordAuthentication yes
    AllowTcpForwarding yes
S
manifest_add files /etc/ssh/sshd_config.d/00-alecsui.conf
rm -f /etc/ssh/sshd_config.d/00-tunnel.conf
if ! sshd -t; then
  echo -e "\033[1;31mERROR: sshd -t failed — rolling back AlecsUI SSH drop-in.\033[0m"
  rm -f /etc/ssh/sshd_config.d/00-alecsui.conf
  exit 1
fi
systemctl restart ssh 2>/dev/null || systemctl restart sshd
# Verify: root must not gain password auth from our drop-in; group match must allow passwords
echo "SSH effective checks:"
echo "  PermitRootLogin: $(sshd -T | awk '/^permitrootlogin /{print $2; exit}')"
echo "  PasswordAuthentication (global default): $(sshd -T | awk '/^passwordauthentication /{print $2; exit}')"
if command -v sshd >/dev/null; then
  # Match user simulation if supported
  if sshd -T -C user=root,host=localhost,addr=127.0.0.1 2>/dev/null | awk '/^passwordauthentication /{print $2; exit}' | grep -qi yes; then
    case "${ROOT_LOGIN:-}" in
      yes) echo -e "\033[1;33mNOTE: root password auth is enabled by existing server policy (not introduced as global yes by AlecsUI Match).\033[0m";;
    esac
  fi
fi
case "${ROOT_LOGIN:-}" in
  yes|Yes) echo -e "\033[1;33mSECURITY: PermitRootLogin is 'yes'. Prefer prohibit-password + SSH keys for root.\033[0m";;
esac
SSH_PORT=$(sshd -T | awk '/^port /{print $2; exit}'); SSH_PORT=${SSH_PORT:-$SSH_PORT_DEF}
cat > /etc/tunnel/config <<S
SSH_PORT=$SSH_PORT
SSL_PORT=$SSL_PORT
UDPGW_PORT=$UDPGW_PORT
WS_PORT=$WS_PORT
WSTLS_PORT=$WSTLS_PORT
PANEL_PORT=$PANEL_PORT
WEB_PATH=$WEB_PATH
VWSTLS_PORT=$VWSTLS_PORT
VTCP_PORT=$VTCP_PORT
VWS_PORT=$VWS_PORT
REALITY_PORT=$REALITY_PORT
TROJAN_PORT=$TROJAN_PORT
OVPN1_PORT=$OVPN1_PORT
OVPN2_PORT=$OVPN2_PORT
SQUID_PORT=$SQUID_PORT
HY_PORT=$HY_PORT
HY_HOP=$HY_HOP
WG_PORT=$WG_PORT
S
chmod 600 /etc/tunnel/config
manifest_add files /etc/tunnel/config

step 3 "SSL + WS TLS (dedicated $ALECSUI_STUNNEL_UNIT — foreign stunnel untouched)"
stunnel_stop_clean
# Migrate legacy AlecsUI pem out of /etc/stunnel without destroying foreign certs
if [ ! -f "$ALECSUI_STUNNEL_PEM" ]; then
  if [ -f /etc/stunnel/stunnel.pem ] && [ -f /etc/tunnel/legacy-stunnel4.owned ]; then
    cp -a /etc/stunnel/stunnel.pem "$ALECSUI_STUNNEL_PEM"
  elif [ -f /etc/stunnel/stunnel.pem ] && grep -q 'AlecsUI\|ssh-ws-tls' /etc/stunnel/stunnel.conf 2>/dev/null; then
    cp -a /etc/stunnel/stunnel.pem "$ALECSUI_STUNNEL_PEM"
    # Restore foreign stunnel.conf if we have original; else leave a note
    if [ -f "$ORIGD/stunnel.conf.pre-alecsui" ]; then
      cp -a "$ORIGD/stunnel.conf.pre-alecsui" /etc/stunnel/stunnel.conf
    fi
    touch /etc/tunnel/legacy-stunnel4.owned
  else
    # First install: if /etc/stunnel/stunnel.conf exists and is NOT ours, back it up and do not overwrite
    if [ -f /etc/stunnel/stunnel.conf ] && ! grep -q 'AlecsUI' /etc/stunnel/stunnel.conf 2>/dev/null; then
      cp -a /etc/stunnel/stunnel.conf "$ORIGD/stunnel.conf.pre-alecsui"
      echo "Preserved foreign /etc/stunnel/stunnel.conf -> $ORIGD/stunnel.conf.pre-alecsui"
    fi
    openssl req -new -x509 -days 3650 -nodes -subj "/CN=AlecsUI-selfsigned" -out "$ALECSUI_STUNNEL_PEM" -keyout "$ALECSUI_STUNNEL_PEM" 2>/dev/null
  fi
fi
if openssl x509 -in "$ALECSUI_STUNNEL_PEM" -noout -subject 2>/dev/null | grep -qi 'www\.google\.com'; then
  echo -e "\033[1;33mReplacing misleading stunnel CN www.google.com with AlecsUI-selfsigned.\033[0m"
  cp -a "$ALECSUI_STUNNEL_PEM" "$ALECSUI_STUNNEL_PEM.bak.$(date +%s)"
  openssl req -new -x509 -days 3650 -nodes -subj "/CN=AlecsUI-selfsigned" -out "$ALECSUI_STUNNEL_PEM" -keyout "$ALECSUI_STUNNEL_PEM" 2>/dev/null
fi
chmod 600 "$ALECSUI_STUNNEL_PEM"
manifest_add files "$ALECSUI_STUNNEL_PEM"
# Do NOT enable/modify generic stunnel4 for AlecsUI
stunnel_start_ok || echo -e "\033[1;33mWARNING: $ALECSUI_STUNNEL_UNIT not running yet; will retry at the end.\033[0m"

step 4 "BadVPN UDPGW (pinned commit $BADVPN_COMMIT)"
if [ ! -x /usr/local/bin/badvpn-udpgw ]; then
  cd /tmp && rm -rf badvpn
  git -c advice.detachedHead=false clone -q https://github.com/ambrop72/badvpn.git
  cd badvpn
  git checkout -q "$BADVPN_COMMIT"
  GOT=$(git rev-parse HEAD)
  [ "$GOT" = "$BADVPN_COMMIT" ] || { echo "ERROR: BadVPN commit mismatch ($GOT != $BADVPN_COMMIT)"; exit 1; }
  mkdir build && cd build
  cmake .. -Wno-dev -DBUILD_NOTHING_BY_DEFAULT=1 -DBUILD_UDPGW=1 >/tmp/badvpn-build.log 2>&1 || { echo "BadVPN cmake failed, see /tmp/badvpn-build.log"; exit 1; }
  { make -j$(nproc) && make install; } >>/tmp/badvpn-build.log 2>&1 || { echo "BadVPN build failed, see /tmp/badvpn-build.log"; exit 1; }
  cd /
  manifest_add files /usr/local/bin/badvpn-udpgw
fi
cat > /etc/systemd/system/badudp.service <<S
[Unit]
Description=AlecsUI BadVPN UDPGW
After=network.target
[Service]
ExecStart=/usr/local/bin/badvpn-udpgw --listen-addr 127.0.0.1:$UDPGW_PORT --max-clients 1000 --max-connections-for-client 100
Restart=always
LimitNOFILE=1048576
PrivateTmp=true
[Install]
WantedBy=multi-user.target
S
manifest_add units badudp.service

step 5 "SSH WS (plain) proxy"
'''

def main() -> int:
    raw = INSTALL.read_text(encoding="utf-8", errors="replace")
    # Cut from start through "step 5 \"SSH WS" line inclusive start of old step5 - we replace through BadVPN and reconnect at step 5
    m = re.search(r'^step 5 "SSH WS \(plain\) proxy"\s*$', raw, re.M)
    if not m:
        print("step 5 marker not found", file=sys.stderr)
        return 1
    rest = raw[m.start():]
    # Skip old step 5 header line — NEW_HEADER already ends with step 5 header
    rest_body = rest.split("\n", 1)[1]
    new = NEW_HEADER + rest_body

    # Version bumps
    new = new.replace("AlecsUI v1.9.0", "AlecsUI v1.9.1")
    new = new.replace("ALECSUI_VER_INSTALLED=\"1.9.0\"", "ALECSUI_VER_INSTALLED=\"1.9.1\"")
    new = new.replace("Protected panel · AlecsUI v1.9.0", "Protected panel · AlecsUI v1.9.1")
    new = new.replace("Powered by <b>AlecsUI</b> v1.9.0", "Powered by <b>AlecsUI</b> v1.9.1")
    new = new.replace("Powered by AlecsUI v1.9.0", "Powered by AlecsUI v1.9.1")
    new = new.replace('<span class="ver">AlecsUI v1.9.0</span>', '<span class="ver">AlecsUI v1.9.1</span>')

    # Xray: digest only from github.com
    new = new.replace(
        """  if ! dl /tmp/xr/x.dgst "$XR_DGST" 20; then
    echo -e "\\033[1;31mERROR: Xray digest file missing — refusing to install unverified binary.\\033[0m"
    rm -rf /tmp/xr; exit 1
  fi""",
        """  if ! dl_official_digest /tmp/xr/x.dgst "$XR_DGST"; then
    echo -e "\\033[1;31mERROR: Xray digest missing from github.com — refusing unverified binary.\\033[0m"
    rm -rf /tmp/xr; exit 1
  fi""",
    )

    # Hysteria: official hashes from github.com only
    old_hy = """  if dl $HT/hy "$HU/hysteria-linux-$HA" 1000000 && dl $HT/hashes.txt "$HU/hashes.txt" 20; then
    HW=$(grep -E "[ /*]hysteria-linux-$HA\\$" $HT/hashes.txt | awk '{print $1}' | head -1); HG=$(sha256sum $HT/hy | awk '{print $1}')
    if [ -n "$HW" ] && [ "$HW" = "$HG" ]; then install -m 755 $HT/hy /usr/local/bin/hysteria; echo "Hysteria2 installed (checksum OK)"
    else echo "WARNING: Hysteria2 checksum did not match, it was NOT installed"; fi
  else echo "WARNING: Hysteria2 download failed, UDP users will not work until you run the installer again"; fi"""
    new_hy = """  if ! dl_official_digest $HT/hashes.txt "$HU/hashes.txt"; then
    echo "WARNING: Hysteria2 official hashes.txt from github.com unavailable — NOT installed"
  else
    HW=$(grep -E "[ /*]hysteria-linux-$HA\\$" $HT/hashes.txt | awk '{print $1}' | head -1)
    if [ -z "$HW" ]; then echo "WARNING: hash for hysteria-linux-$HA missing — NOT installed"
    elif dl $HT/hy "$HU/hysteria-linux-$HA" 1000000 "$HW"; then
      install -m 755 $HT/hy /usr/local/bin/hysteria; echo "Hysteria2 installed (official SHA256 OK)"
      # manifest added later if present
    else echo "WARNING: Hysteria2 binary failed SHA256 — NOT installed"; fi
  fi"""
    if old_hy in new:
        new = new.replace(old_hy, new_hy)
    else:
        print("WARN: Hysteria block not exact-matched")

    # acme.sh: pin version tarball instead of curl|sh
    old_acme = """need(){
  [ -x $A ] || curl -fsSL https://get.acme.sh | sh >/dev/null 2>&1
  [ -x $A ] || { echo "acme.sh could not be installed (check internet)"; return 1; }
  $A --set-default-ca --server letsencrypt >/dev/null 2>&1
}"""
    new_acme = """need(){
  if [ ! -x $A ]; then
    local TD Z SUM URL
    TD=$(mktemp -d); URL="https://github.com/acmesh-official/acme.sh/archive/refs/tags/$ACME_VER.tar.gz"
    # ACME_VER may be unset in menu subshell — default
    ACME_VER=${ACME_VER:-3.1.0}
    URL="https://github.com/acmesh-official/acme.sh/archive/refs/tags/${ACME_VER}.tar.gz"
    echo "Installing acme.sh ${ACME_VER} from GitHub (no curl|sh)..."
    if curl -fsSL --max-time 120 -o "$TD/acme.tgz" "$URL"; then
      tar -C "$TD" -xzf "$TD/acme.tgz"
      ( cd "$TD/acme.sh-${ACME_VER}" && bash acme.sh --install -m admin@localhost --nocron >/dev/null 2>&1 ) || true
    fi
    rm -rf "$TD"
  fi
  [ -x $A ] || { echo "acme.sh could not be installed (check internet)"; return 1; }
  $A --set-default-ca --server letsencrypt >/dev/null 2>&1
}"""
    if old_acme in new:
        new = new.replace(old_acme, new_acme)
    else:
        print("WARN: acme need() block not exact-matched")

    # mkuser: add to SSH_GROUP
    new = new.replace(
        "if run('chpasswd',inp='%s:%s\\n'%(n,p)).returncode:",
        "run('usermod','-aG','alecsui-ssh',n)\n    if run('chpasswd',inp='%s:%s\\n'%(n,p)).returncode:",
        1,
    )

    # CSRF + logout already partly there — strengthen SESS with csrf
    if "def csrf_tok" not in new:
        new = new.replace(
            "SESS={}; FAIL={}\n",
            "SESS={}; FAIL={}\n"
            "def csrf_new(): return secrets.token_hex(32)\n"
            "def csrf_ok(tok, got):\n"
            "    s=SESS.get(tok) if tok else None\n"
            "    return bool(s) and hmac.compare_digest(str(s.get('csrf','')), str(got or ''))\n",
        )
        # on login set csrf
        new = new.replace(
            "SESS[t]={'exp':now+43200,'ip':ip,'ua':self.headers.get('User-Agent','')[:160],'t':int(now)}; login_log(ip,curuser(),'OK',self.headers.get('User-Agent',''))\n"
            "                return self.out(200,{'ok':1},ck='sid=%s; HttpOnly; Secure; SameSite=Strict; Path=%s; Max-Age=43200'%(t,BASE))",
            "ct=csrf_new(); SESS[t]={'exp':now+43200,'ip':ip,'ua':self.headers.get('User-Agent','')[:160],'t':int(now),'csrf':ct}; login_log(ip,curuser(),'OK',self.headers.get('User-Agent',''))\n"
            "                return self.out(200,{'ok':1,'csrf':ct},ck='sid=%s; HttpOnly; Secure; SameSite=Strict; Path=%s; Max-Age=43200'%(t,BASE))",
        )
        # require csrf on mutating API after auth
        new = new.replace(
            "if not self.authed(): return self.out(401,{'e':'login'})\n"
            "            if r=='/api/logout':",
            "if not self.authed(): return self.out(401,{'e':'login'})\n"
            "            if r not in ('/api/logout','/api/state','/api/hist','/api/brand','/api/captcha') and r.startswith('/api/'):\n"
            "                if not csrf_ok(self.tok(), d.get('csrf') or self.headers.get('X-CSRF')): return self.out(403,{'e':'bad csrf'})\n"
            "            if r=='/api/logout':",
        )

    # Fix stunnel references in panel restart lists and final status
    new = new.replace("'stunnel4'", "'alecsui-stunnel'")
    new = new.replace("stunnel4", "alecsui-stunnel")  # careful - may over-replace
    # Undo over-replace in comments about foreign stunnel / package name
    new = new.replace("/usr/bin/alecsui-stunnel", "/usr/bin/stunnel4")
    new = new.replace("openssh-server alecsui-stunnel fail2ban", "openssh-server stunnel4 fail2ban")
    new = new.replace("PKGS=\"openssh-server alecsui-stunnel", "PKGS=\"openssh-server stunnel4")
    new = new.replace("apt-get install -y -qq openssh-server alecsui-stunnel", "apt-get install -y -qq openssh-server stunnel4")

    # Uninstall replacement
    old_un = None
    m2 = re.search(r"^uninst\(\)\{.*?^\}", new, re.M | re.S)
    if m2:
        new_un = r'''uninst(){
  echo -e "${Y}This removes ONLY AlecsUI resources listed in $MANIFEST (or the known set). External stunnel4/SSH/firewall policies are restored when originals exist.${N}"
  read -rp "Type DELETE-USERS to also remove tunnel Linux users (or keep to preserve users): " yu
  read -rp "Type yes to confirm uninstall: " y; [ "$y" = yes ] || { echo "Cancelled"; return; }
  f=/root/alecsui-backup-before-uninstall-$(date +%F-%H%M).json
  python3 $PY backup "$f" >/dev/null 2>&1 && chmod 600 "$f" && echo "External backup saved: $f"
  # Stop only AlecsUI units
  systemctl disable --now tunnel-panel alecsui-helper xray ws-ssh badudp alecsui-stunnel >/dev/null 2>&1 || true
  for u in $(systemctl list-units --all --plain --no-legend 'alecsui-ovpn@*' 2>/dev/null | awk '{print $1}') alecsui-ovpn@rx1194 alecsui-ovpn@rx110; do systemctl disable --now "$u" >/dev/null 2>&1 || true; done
  systemctl disable --now alecsui-hy2 alecsui-wg alecsui-dns >/dev/null 2>&1 || true
  # Do NOT disable foreign stunnel4 / ssh / fail2ban
  if [ -f /etc/tunnel/h443.on ]; then
    systemctl disable --now haproxy >/dev/null 2>&1 || true
    [ -f /etc/haproxy/haproxy.cfg.orig ] && mv -f /etc/haproxy/haproxy.cfg.orig /etc/haproxy/haproxy.cfg
    rm -f /etc/haproxy/alecsui.pem
  fi
  if [ "$yu" = DELETE-USERS ]; then python3 $PY purge 2>/dev/null || true
  else echo "Tunnel Linux users preserved (no purge)."; fi
  if [ -f /etc/squid/squid.conf.orig ]; then mv -f /etc/squid/squid.conf.orig /etc/squid/squid.conf; fi
  # Restore SSH drop-in
  rm -f /etc/ssh/sshd_config.d/00-alecsui.conf /etc/ssh/sshd_config.d/00-tunnel.conf
  if sshd -t 2>/dev/null; then systemctl reload ssh 2>/dev/null || systemctl reload sshd 2>/dev/null || true; fi
  # Restore foreign stunnel if we preserved it
  if [ -f /etc/tunnel/originals/stunnel.conf.pre-alecsui ]; then
    cp -a /etc/tunnel/originals/stunnel.conf.pre-alecsui /etc/stunnel/stunnel.conf
    echo "Restored foreign /etc/stunnel/stunnel.conf"
  fi
  # Remove AlecsUI-owned paths
  rm -f /etc/systemd/system/alecsui-ovpn@.service /etc/systemd/system/alecsui-hy2.service /etc/systemd/system/alecsui-stunnel.service /etc/systemd/system/alecsui-helper.service
  rm -f /etc/systemd/system/alecsui-wg.service /etc/systemd/system/alecsui-dns.service /etc/systemd/system/{tunnel-panel,xray,ws-ssh,badudp}.service
  rm -f /etc/sysctl.d/99-alecsui-wg.conf /etc/sysctl.d/99-alecsui-ovpn.conf /etc/sysctl.d/99-zz-alecsui-perf.conf
  rm -f /etc/cron.d/alecsui-reboot /etc/cron.d/tunnel-expire
  rm -rf /opt/tunnel-panel /etc/alecsui /run/alecsui /usr/local/etc/xray /var/log/xray $LIB
  rm -f /usr/local/bin/xray /usr/local/bin/ws-ssh.py /usr/local/bin/badvpn-udpgw /usr/local/bin/geoip.dat /usr/local/bin/geosite.dat /usr/local/bin/hysteria /usr/local/bin/dnstt-server
  # Keep /etc/tunnel backup copy outside; remove live tree last
  rm -rf /etc/tunnel /etc/tunnel-users
  systemctl daemon-reload
  rm -f /usr/local/bin/menu
  echo -e "${G}AlecsUI uninstalled.${N} External stunnel4/SSH/fail2ban left alone. Backup: $f"
  exit 0
}'''
        new = new[: m2.start()] + new_un + new[m2.end() :]
    else:
        print("WARN: uninst() not found")

    # Final status line uses alecsui-stunnel
    new = new.replace(
        "for s in ssh alecsui-stunnel ws-ssh badudp xray fail2ban tunnel-panel",
        "for s in ssh alecsui-stunnel ws-ssh badudp xray fail2ban tunnel-panel",
    )
    new = new.replace(
        "stunnel_start_ok || echo -e \"\\033[1;33mWARNING: alecsui-stunnel still failed",
        "stunnel_start_ok || echo -e \"\\033[1;33mWARNING: alecsui-stunnel still failed",
    )
    # Fix menu srv restart that might say alecsui-stunnel incorrectly for package
    new = new.replace("systemctl restart alecsui-stunnel ws-ssh", "systemctl restart alecsui-stunnel ws-ssh")

    # Ensure ACME_VER exported in menu cert script - inject near LIB=
    if "ACME_VER=" not in new.split("cat > $LIB/cert.sh", 1)[-1][:500]:
        new = new.replace(
            "C=/etc/tunnel/cert; LIB=/usr/local/lib/tunnel; A=/root/.acme.sh/acme.sh",
            "C=/etc/tunnel/cert; LIB=/usr/local/lib/tunnel; A=/root/.acme.sh/acme.sh; ACME_VER=3.1.0",
        )

    INSTALL.write_bytes(new.replace("\r\n", "\n").encode("utf-8"))
    print("Patched", INSTALL, "bytes", INSTALL.stat().st_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
