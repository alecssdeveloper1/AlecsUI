#!/usr/bin/env python3
"""Inject animated bilingual installer UI + Ubuntu 25/26 support into install.sh."""
from __future__ import annotations

import pathlib
import re

INSTALL = pathlib.Path(__file__).resolve().parents[1] / "install.sh"
t = INSTALL.read_text(encoding="utf-8")

UI_BLOCK = r'''
# ---------- Installer UI (bilingual RO/EN + colors + progress) ----------
C0='\033[0m'; CB='\033[1m'; CD='\033[2m'
CR='\033[1;31m'; CG='\033[1;32m'; CY='\033[1;33m'; CC='\033[1;36m'; CM='\033[1;35m'; CW='\033[1;37m'
CL='\033[1;94m'; CT='\033[1;96m'
SPIN_PID=''
UI_LANG="${ALECSUI_LANG:-}"

ui_pick_lang(){
  if [ -n "$UI_LANG" ]; then return; fi
  case "${LANG:-}${LC_ALL:-}${LC_MESSAGES:-}" in
    ro*|RO*) UI_LANG=ro;;
    *) UI_LANG=en;;
  esac
  if [ -t 0 ] && [ -t 1 ]; then
    echo
    echo -e "  ${CT}${CB}AlecsUI installer / Instalator${C0}"
    echo -e "  ${CD}1) English   2) Română${C0}"
    read -rp "  Language / Limbă [1/2] (default: $UI_LANG): " _ans || true
    case "${_ans:-}" in
      2|ro|RO|r|R) UI_LANG=ro;;
      1|en|EN|e|E) UI_LANG=en;;
    esac
  fi
  export UI_LANG
}

# msg "english" "română"
msg(){
  if [ "${UI_LANG:-en}" = ro ]; then echo -e "$2"; else echo -e "$1"; fi
}

ui_banner(){
  clear 2>/dev/null || true
  echo -e "${CT}"
  cat <<'BAN'
     █████╗ ██╗     ███████╗ ██████╗███████╗██╗   ██╗██╗
    ██╔══██╗██║     ██╔════╝██╔════╝██╔════╝██║   ██║██║
    ███████║██║     █████╗  ██║     ███████╗██║   ██║██║
    ██╔══██║██║     ██╔══╝  ██║     ╚════██║██║   ██║██║
    ██║  ██║███████╗███████╗╚██████╗███████║╚██████╔╝██║
    ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚══════╝ ╚═════╝ ╚═╝
BAN
  echo -e "${C0}"
  echo -e "  ${CM}${CB}v${ALECSUI_VER}${C0}  ${CD}· Open Source VPN Panel · GPL-3.0${C0}"
  echo -e "  ${CD}github.com/alecssdeveloper1/AlecsUI${C0}"
  echo
  if [ "${UI_LANG}" = ro ]; then
    echo -e "  ${CG}▶${C0} Instalare animată · mesaje RO/EN · Ubuntu 20–26 / Debian 11+"
  else
    echo -e "  ${CG}▶${C0} Animated install · RO/EN messages · Ubuntu 20–26 / Debian 11+"
  fi
  echo -e "  ${CD}──────────────────────────────────────────────────${C0}"
  echo
}

os_check(){
  local id ver pretty major
  # shellcheck disable=SC1091
  [ -f /etc/os-release ] && . /etc/os-release
  id=${ID:-unknown}; ver=${VERSION_ID:-0}; pretty=${PRETTY_NAME:-$id $ver}
  major=${ver%%.*}
  msg "${CC}OS check:${C0} $pretty" "${CC}Verificare OS:${C0} $pretty"
  case "$id" in
    ubuntu)
      if [ "$major" -ge 20 ] && [ "$major" -le 26 ] 2>/dev/null; then
        msg "${CG}✓ Ubuntu $ver supported (20–26).${C0}" "${CG}✓ Ubuntu $ver suportat (20–26).${C0}"
      else
        msg "${CY}! Ubuntu $ver is outside the tested range 20–26. Continuing anyway…${C0}" \
            "${CY}! Ubuntu $ver e în afara intervalului testat 20–26. Continuăm…${C0}"
      fi
      ;;
    debian)
      if [ "$major" -ge 11 ] 2>/dev/null; then
        msg "${CG}✓ Debian $ver supported (11+).${C0}" "${CG}✓ Debian $ver suportat (11+).${C0}"
      else
        msg "${CR}✗ Debian $ver is too old. Need Debian 11+.${C0}" "${CR}✗ Debian $ver e prea vechi. Trebuie Debian 11+.${C0}"
        exit 1
      fi
      ;;
    *)
      msg "${CY}! Distro '$id' is not officially listed. Ubuntu/Debian recommended.${C0}" \
          "${CY}! Distro '$id' nu e pe lista oficială. Recomandat Ubuntu/Debian.${C0}"
      ;;
  esac
}

spin_start(){
  local tip="$1"
  [ -t 1 ] || { echo -e "  ${CD}$tip${C0}"; return; }
  (
    local frames='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏' i=0
    while true; do
      printf "\r  ${CT}%s${C0} ${CW}%s${C0}   " "${frames:i++%10:1}" "$tip"
      sleep 0.08
    done
  ) &
  SPIN_PID=$!
  disown 2>/dev/null || true
}

spin_stop(){
  local ok="${1:-1}" done_en="${2:-Done}" done_ro="${3:-Gata}"
  if [ -n "${SPIN_PID:-}" ] && kill -0 "$SPIN_PID" 2>/dev/null; then
    kill "$SPIN_PID" 2>/dev/null || true
    wait "$SPIN_PID" 2>/dev/null || true
  fi
  SPIN_PID=''
  [ -t 1 ] && printf "\r\033[K"
  if [ "$ok" = 1 ]; then
    msg "  ${CG}✓${C0} ${CB}$done_en${C0}" "  ${CG}✓${C0} ${CB}$done_ro${C0}"
  else
    msg "  ${CY}!${C0} ${CB}$done_en${C0}" "  ${CY}!${C0} ${CB}$done_ro${C0}"
  fi
}

# Progress bar for step n/total
ui_bar(){
  local n="$1" total="${2:-11}" width=28
  local filled=$(( n * width / total )) empty=$(( width - filled ))
  local bar
  bar=$(printf "%${filled}s" | tr ' ' '█')$(printf "%${empty}s" | tr ' ' '░')
  printf "  ${CM}[%s]${C0} ${CD}%d/%d${C0}\n" "$bar" "$n" "$total"
}

# step N "English title" "Titlu română"
step(){
  local n="$1" en="$2" ro="${3:-$2}"
  echo
  ui_bar "$n" 11
  if [ "${UI_LANG:-en}" = ro ]; then
    echo -e "  ${CT}${CB}Pasul $n/11${C0}  ${CW}$ro${C0}"
  else
    echo -e "  ${CT}${CB}Step $n/11${C0}  ${CW}$en${C0}"
  fi
  echo -e "  ${CD}········································${C0}"
}

say(){ msg "  $1" "  $2"; }
ok(){ msg "  ${CG}✓${C0} $1" "  ${CG}✓${C0} $2"; }
warn(){ msg "  ${CY}!${C0} $1" "  ${CY}!${C0} $2"; }
errx(){ msg "  ${CR}✗${C0} $1" "  ${CR}✗${C0} $2"; }

ui_finish(){
  local ph="$1" r="$2"
  echo
  echo -e "${CG}"
  cat <<'OK'
   ╔══════════════════════════════════════════╗
   ║          ★  INSTALL COMPLETE  ★          ║
   ║          ★  INSTALARE COMPLETĂ  ★        ║
   ╚══════════════════════════════════════════╝
OK
  echo -e "${C0}"
  msg "${CB}AlecsUI v${ALECSUI_VER} — service status${C0}" "${CB}AlecsUI v${ALECSUI_VER} — starea serviciilor${C0}"
}

'''

# Bump version header
t = t.replace("AlecsUI v1.9.1 installer", "AlecsUI v1.9.2 installer", 1)
t = t.replace("ALECSUI_VER=1.9.1", "ALECSUI_VER=1.9.2", 1)
t = t.replace('ALECSUI_VER_INSTALLED="1.9.1"', 'ALECSUI_VER_INSTALLED="1.9.2"')
t = t.replace("AlecsUI v1.9.1", "AlecsUI v1.9.2")
t = t.replace("v1.9.1", "v1.9.2")

# Replace old step() definition
t = t.replace(
    "step(){ echo -e \"\\n\\033[1;36m[$1/11]\\033[0m $2\"; }\n",
    UI_BLOCK + "\n",
)

# Insert ui_pick_lang + banner + os_check after root check / before lock
needle = "OUR_BINS='stunnel|xray|openvpn|squid|haproxy|hysteria|dnstt-server|badvpn-udpgw'\n"
# UI_BLOCK already inserted replacing step - add boot call before install_lock
t = t.replace(
    "\ninstall_lock\nmanifest_init\n",
    "\nui_pick_lang\nui_banner\nos_check\ninstall_lock\nmanifest_init\n"
    "say \"${CC}Preparing install…${C0}\" \"${CC}Pregătim instalarea…${C0}\"\n",
)

# Update step calls with bilingual titles
replacements = [
    ('step 1 "Packages"',
     'step 1 "Packages" "Pachete"\nsay "Updating apt…" "Actualizăm apt…"\nspin_start "$(msg "Downloading packages…" "Descărcăm pachetele…")"'),
]
# Do careful replacements for each step

t = t.replace('step 1 "Packages"\necho "Updating apt package lists..."\napt-get update -qq\necho "Installing packages (this can take several minutes)..."\n',
              'step 1 "Packages" "Pachete"\nsay "${CD}Updating apt package lists…${C0}" "${CD}Actualizăm listele apt…${C0}"\nspin_start "$( [ "$UI_LANG" = ro ] && echo "Descărcăm pachetele…" || echo "Downloading packages…" )"\napt-get update -qq\n')

t = t.replace(
    'apt-get install -y -qq $PKGS >/dev/null\napt-get install -y -qq haproxy >/dev/null 2>&1 || echo -e "\\033[1;33mHAProxy could not be installed, 443 mode stays off.\\033[0m"\necho "Packages OK"\n[ "${CAP_OVPN:-0}" = 1 ] || echo -e "\\033[1;33mOpenVPN package skipped (no TUN).\\033[0m"',
    'apt-get install -y -qq $PKGS >/dev/null\napt-get install -y -qq haproxy >/dev/null 2>&1 || warn "HAProxy missing — 443 mode stays off." "HAProxy lipsește — modul 443 rămâne oprit."\nspin_stop 1 "Packages ready" "Pachete gata"\n[ "${CAP_OVPN:-0}" = 1 ] || warn "OpenVPN skipped (no TUN)." "OpenVPN omis (fără TUN)."',
)

t = t.replace(
    'step 2 "SSH tuning (Match Group $SSH_GROUP — password auth ONLY for tunnel users)"',
    'step 2 "SSH tuning (Match Group $SSH_GROUP)" "Configurare SSH (Match Group $SSH_GROUP)"',
)
t = t.replace(
    'step 3 "SSL + WS TLS (dedicated $ALECSUI_STUNNEL_UNIT — foreign stunnel untouched)"',
    'step 3 "SSL + WS TLS ($ALECSUI_STUNNEL_UNIT)" "SSL + WS TLS ($ALECSUI_STUNNEL_UNIT)"',
)
t = t.replace(
    'step 4 "BadVPN UDPGW (pinned commit $BADVPN_COMMIT)"',
    'step 4 "BadVPN UDPGW" "BadVPN UDPGW"\nsay "${CD}Pinned commit $BADVPN_COMMIT${C0}" "${CD}Commit fixat $BADVPN_COMMIT${C0}"',
)
t = t.replace(
    'step 5 "SSH WS (plain) proxy"',
    'step 5 "SSH WebSocket proxy" "Proxy SSH WebSocket"',
)
t = t.replace(
    'step 6 "BBR + FQ"',
    'step 6 "BBR + FQ network tuning" "Reglare rețea BBR + FQ"',
)
t = t.replace(
    'step 7 "Fail2ban"',
    'step 7 "Fail2ban" "Fail2ban"',
)
t = t.replace(
    'step 8 "Xray core (pinned $XRAY_VER, SHA256 required)"',
    'step 8 "Xray core $XRAY_VER (SHA256 required)" "Xray core $XRAY_VER (SHA256 obligatoriu)"\nspin_start "$( [ "$UI_LANG" = ro ] && echo "Descărcăm Xray…" || echo "Downloading Xray…" )"',
)
# After xray install success messages - add spin_stop near "Xray $XRAY_VER installed" or "already present"
t = t.replace(
    '  echo "Xray $XRAY_VER installed"\nelse\n  echo "Xray already present, skipping download"\nfi',
    '  spin_stop 1 "Xray $XRAY_VER installed" "Xray $XRAY_VER instalat"\nelse\n  spin_stop 1 "Xray already present" "Xray deja instalat"\nfi',
)
# If spin_start was added but path fails before stop - the early exit paths need care. For "already present" we started spin before if - wait, spin starts before if. Looking at structure:

# Actually I put spin_start in the step 8 replace which is BEFORE the if. Good for both branches if we stop in both. But if download fails with exit 1, spinner may linger - trap could kill it.

t = t.replace(
    "trap 'echo -e \"\\n\\033[1;31mERROR: failed at line $LINENO\\033[0m\"' ERR",
    "trap 'spin_stop 0 \"Failed\" \"Eșec\" 2>/dev/null; echo -e \"\\n${CR}ERROR / EROARE: line $LINENO${C0}\"' ERR",
)

t = t.replace(
    'step 9 "Web panel"',
    'step 9 "Web panel" "Panou web"\nsay "${CD}Writing panel files…${C0}" "${CD}Scriem fișierele panoului…${C0}"',
)
t = t.replace(
    'step 10 "Terminal menu"',
    'step 10 "Terminal menu" "Meniu terminal"',
)
t = t.replace(
    'step 11 "Services start + firewall"',
    'step 11 "Start services + firewall" "Pornire servicii + firewall"\nspin_start "$( [ "$UI_LANG" = ro ] && echo "Pornim serviciile…" || echo "Starting services…" )"',
)

# Final banner replacement
old_fin = '''echo -e "\\n\\033[1;32m==============================\\033[0m"
echo "AlecsUI v1.9.2 — service status"
for s in ssh alecsui-stunnel ws-ssh badudp xray fail2ban tunnel-panel alecsui-ovpn@rx1194 alecsui-ovpn@rx110 squid alecsui-hy2 alecsui-wg alecsui-dns; do
  x=$(systemctl is-active $s 2>/dev/null || true); [ $s = ssh ] && [ "$x" != active ] && x=$(systemctl is-active sshd 2>/dev/null || true); printf "%-18s: %s\\n" $s "$x"
done
echo "SSH $SSH_PORT | SSL $SSL_PORT | WS $WS_PORT | WS TLS $WSTLS_PORT | UDPGW 127.0.0.1:$UDPGW_PORT"
echo "V2Ray     : add your inbounds in the panel (Inbounds), then allow their ports in your provider firewall"
echo "OpenVPN TCP $OVPN1_PORT, $OVPN2_PORT | HTTP proxy $SQUID_PORT | Hysteria2 UDP $HY_PORT (hopping $HY_HOP) | WireGuard UDP $WG_PORT"
echo "WS test   : ${R:-fail}"
echo "Panel     : https://$PH:$PANEL_PORT/$WEB_PATH/"
if [ -n "$NEWPASS" ]; then echo "Login     : admin / $NEWPASS  (save this now)"; else echo "Login     : unchanged (change it with menu -> 3)"; fi
echo "Menu      : menu"
echo "Project   : https://github.com/alecssdeveloper1/AlecsUI"
echo "Allow these TCP ports in your provider firewall: $SSL_PORT $WS_PORT $WSTLS_PORT $OVPN1_PORT $OVPN2_PORT $SQUID_PORT $PANEL_PORT 80"
echo "Also allow UDP: $HY_PORT and $HY_HOP (Hysteria2), $WG_PORT (WireGuard), 53 (DNS tunnel)"
echo "If your provider has Anti-DDoS rules per port: do not set web ports (80, 8080, 8880) to SSH, use HTTP or no rule."
[ ! -c /dev/net/tun ] && echo "Note: OpenVPN disabled (no TUN). Prefer a KVM VPS for OpenVPN/WireGuard/BBR."
echo -e "\\033[1;32m==============================\\033[0m"
'''

# version in file might still be 1.9.1 in final if replace order wrong - check
new_fin = '''spin_stop 1 "Services started" "Servicii pornite"
ui_finish "$PH" "$R"
for s in ssh alecsui-stunnel ws-ssh badudp xray fail2ban tunnel-panel alecsui-helper alecsui-ovpn@rx1194 alecsui-ovpn@rx110 squid alecsui-hy2 alecsui-wg alecsui-dns; do
  x=$(systemctl is-active $s 2>/dev/null || true); [ $s = ssh ] && [ "$x" != active ] && x=$(systemctl is-active sshd 2>/dev/null || true)
  if [ "$x" = active ]; then printf "  ${CG}●${C0} %-18s ${CG}%s${C0}\\n" "$s" "$x"
  else printf "  ${CY}○${C0} %-18s ${CY}%s${C0}\\n" "$s" "$x"; fi
done
echo
msg "${CB}Ports / Porturi${C0}" "${CB}Porturi${C0}"
echo "  SSH $SSH_PORT | SSL $SSL_PORT | WS $WS_PORT | WS-TLS $WSTLS_PORT | UDPGW 127.0.0.1:$UDPGW_PORT"
echo "  OpenVPN TCP $OVPN1_PORT,$OVPN2_PORT | Squid $SQUID_PORT | Hy2 UDP $HY_PORT ($HY_HOP) | WG UDP $WG_PORT"
msg "  WS test: ${R:-fail}" "  Test WS: ${R:-fail}"
echo
msg "${CG}${CB}Panel:${C0}  https://$PH:$PANEL_PORT/$WEB_PATH/" "${CG}${CB}Panou:${C0}  https://$PH:$PANEL_PORT/$WEB_PATH/"
if [ -n "$NEWPASS" ]; then
  msg "${CY}${CB}Login:${C0}  admin / $NEWPASS  ${CD}(save now — not stored in plaintext)${C0}" \
      "${CY}${CB}Login:${C0}  admin / $NEWPASS  ${CD}(salvează acum — nu e păstrat în plaintext)${C0}"
else
  msg "${CD}Login unchanged (menu → 3 to reset)${C0}" "${CD}Login neschimbat (menu → 3 pentru reset)${C0}"
fi
msg "${CB}Menu:${C0}   menu" "${CB}Meniu:${C0}  menu"
echo -e "  ${CD}https://github.com/alecssdeveloper1/AlecsUI${C0}"
echo
msg "${CD}Open in provider firewall — TCP: $SSL_PORT $WS_PORT $WSTLS_PORT $OVPN1_PORT $OVPN2_PORT $SQUID_PORT $PANEL_PORT 80${C0}" \
    "${CD}Deschide la provider — TCP: $SSL_PORT $WS_PORT $WSTLS_PORT $OVPN1_PORT $OVPN2_PORT $SQUID_PORT $PANEL_PORT 80${C0}"
msg "${CD}UDP: $HY_PORT $HY_HOP (Hysteria2), $WG_PORT (WireGuard), 53 (DNS)${C0}" \
    "${CD}UDP: $HY_PORT $HY_HOP (Hysteria2), $WG_PORT (WireGuard), 53 (DNS)${C0}"
[ ! -c /dev/net/tun ] && warn "OpenVPN disabled (no TUN). Prefer KVM." "OpenVPN dezactivat (fără TUN). Preferă KVM."
echo -e "  ${CM}★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★${C0}"
echo
'''

# Try match with whatever version string is at end
m = re.search(
    r'echo -e "\\n\\033\[1;32m==============================\\033\[0m"\n'
    r'echo "AlecsUI v1\.9\.[12] — service status"\n'
    r'.*?echo -e "\\033\[1;32m==============================\\033\[0m"\n',
    t,
    re.S,
)
if m:
    t = t[: m.start()] + new_fin + t[m.end() :]
    print("final banner replaced")
else:
    print("WARN: final banner not matched")

# Fix spin on xray if download fails before spin_stop - also if step8 spin_start runs but Xray path uses exit 1
# Ensure branding in PANELHTML
t = t.replace("AlecsUI v1.9.1", "AlecsUI v1.9.2")
t = t.replace("v1.9.1", "v1.9.2")

INSTALL.write_bytes(t.replace("\r\n", "\n").encode("utf-8"))
print("UI patched", INSTALL.stat().st_size)
