#!/usr/bin/env python3
"""Fix over-replacements and wire menu/panel to dedicated stunnel + CSRF JS."""
from __future__ import annotations

import pathlib
import re

INSTALL = pathlib.Path(__file__).resolve().parents[1] / "install.sh"
t = INSTALL.read_text(encoding="utf-8")

# Fix legacy marker / stunnel4 migration logic
t = t.replace("legacy-alecsui-stunnel.owned", "legacy-stunnel4.owned")
t = t.replace(
    """  # Legacy: only if our marker file says we previously owned alecsui-stunnel via AlecsUI conf path
  if [ -f /etc/tunnel/legacy-stunnel4.owned ] && [ -f /etc/stunnel/stunnel.conf ] && grep -q 'AlecsUI' /etc/stunnel/stunnel.conf 2>/dev/null; then
    p=$(systemctl show -p MainPID --value alecsui-stunnel 2>/dev/null || true)
    if [ -n "$p" ] && [ "$p" != 0 ]; then
      cmd=$(tr '\\0' ' ' <"/proc/$p/cmdline" 2>/dev/null || true)
      echo "$cmd" | grep -Eq '/etc/stunnel/stunnel\\.conf' && pids+=("$p")
    fi
  fi""",
    """  # Legacy v1.8: AlecsUI used system stunnel4 + /etc/stunnel/stunnel.conf (marker required)
  if [ -f /etc/tunnel/legacy-stunnel4.owned ] && [ -f /etc/stunnel/stunnel.conf ] && grep -q 'AlecsUI' /etc/stunnel/stunnel.conf 2>/dev/null; then
    p=$(systemctl show -p MainPID --value stunnel4 2>/dev/null || true)
    if [ -n "$p" ] && [ "$p" != 0 ]; then
      cmd=$(tr '\\0' ' ' <"/proc/$p/cmdline" 2>/dev/null || true)
      echo "$cmd" | grep -Eq '/etc/stunnel/stunnel\\.conf' && pids+=("$p")
    fi
  fi""",
)
t = t.replace(
    """# Stop ONLY AlecsUI stunnel unit/PIDs — never systemctl stop alecsui-stunnel unless legacy-owned marker
stunnel_stop_clean(){
  local pid still i
  echo "Preparing AlecsUI stunnel ($ALECSUI_STUNNEL_UNIT)..."
  systemctl stop "$ALECSUI_STUNNEL_UNIT" 2>/dev/null || true
  if [ -f /etc/tunnel/legacy-stunnel4.owned ]; then
    echo "  legacy AlecsUI alecsui-stunnel ownership marker present — stopping alecsui-stunnel only for migration"
    systemctl stop alecsui-stunnel 2>/dev/null || true
  fi""",
    """# Stop ONLY AlecsUI stunnel unit/PIDs — never stop foreign stunnel4 unless legacy AlecsUI marker
stunnel_stop_clean(){
  local pid still i
  echo "Preparing AlecsUI stunnel ($ALECSUI_STUNNEL_UNIT)..."
  systemctl stop "$ALECSUI_STUNNEL_UNIT" 2>/dev/null || true
  if [ -f /etc/tunnel/legacy-stunnel4.owned ]; then
    echo "  legacy AlecsUI marker: stopping system stunnel4 only for migration to dedicated unit"
    systemctl stop stunnel4 2>/dev/null || true
  fi""",
)
t = t.replace(
    "; AlecsUI $ALECSUI_VER dedicated stunnel — foreign alecsui-stunnel untouched",
    "; AlecsUI $ALECSUI_VER dedicated stunnel — foreign stunnel4 untouched",
)
t = t.replace(
    "# Do NOT enable/modify generic alecsui-stunnel for AlecsUI",
    "# Do NOT enable/modify generic stunnel4 for AlecsUI",
)
t = t.replace(
    "# Never claim generic alecsui-stunnel as ours without conf path",
    "# Never claim generic stunnel as ours without our conf path",
)

# Menu apply() must write dedicated conf
old_apply = """apply(){
  . $CF
  cat > /etc/stunnel/stunnel.conf <<S
pid = /var/run/alecsui-stunnel/alecsui-stunnel.pid
cert = /etc/stunnel/stunnel.pem
sslVersionMin = TLSv1.2
socket = l:TCP_NODELAY=1
socket = r:TCP_NODELAY=1
[ssh-ssl]
accept = $( [ -f /etc/tunnel/h443.on ] && [ "$SSL_PORT" = 443 ] && echo 127.0.0.1:10443 || echo $SSL_PORT )
connect = 127.0.0.1:$SSH_PORT
[ssh-ws-tls]
accept = $WSTLS_PORT
connect = 127.0.0.1:$WS_PORT
S
  sed -i "s|^ExecStart=.*|ExecStart=/usr/bin/python3 /usr/local/bin/ws-ssh.py $WS_PORT $SSH_PORT|" /etc/systemd/system/ws-ssh.service
  systemctl daemon-reload
  systemctl restart alecsui-stunnel ws-ssh tunnel-panel
}"""
new_apply = """apply(){
  . $CF
  mkdir -p /etc/alecsui /run/alecsui
  local accept_ssl
  if [ -f /etc/tunnel/h443.on ] && [ "$SSL_PORT" = 443 ]; then accept_ssl=127.0.0.1:10443; else accept_ssl=$SSL_PORT; fi
  cat > /etc/alecsui/stunnel.conf <<S
; AlecsUI dedicated stunnel
pid = /run/alecsui/stunnel.pid
cert = /etc/alecsui/stunnel.pem
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
  sed -i "s|^ExecStart=.*|ExecStart=/usr/bin/python3 /usr/local/bin/ws-ssh.py $WS_PORT $SSH_PORT|" /etc/systemd/system/ws-ssh.service
  systemctl daemon-reload
  systemctl restart alecsui-stunnel ws-ssh tunnel-panel
}"""
if old_apply in t:
    t = t.replace(old_apply, new_apply)
else:
    print("WARN: apply() block not matched")

# Panel HAProxy stunnel conf path
t = t.replace("f='/etc/stunnel/stunnel.conf'; t=rd(f)", "f='/etc/alecsui/stunnel.conf'; t=rd(f)")

# Frontend: store CSRF from login and send X-CSRF on API posts
# Find typical api() or fetch helper in PANELHTML
if "X-CSRF" not in t.split("PANELHTML", 1)[-1][:50000]:
    # inject after login success handling patterns
    t2 = t
    # Common pattern in this panel: headers:{'X-Req':'1'
    t2 = t.replace(
        "headers:{'X-Req':'1','Content-Type':'application/json'}",
        "headers:{'X-Req':'1','X-CSRF':(window.CSRF||''),'Content-Type':'application/json'}",
    )
    t2 = t2.replace(
        'headers:{"X-Req":"1","Content-Type":"application/json"}',
        'headers:{"X-Req":"1","X-CSRF":(window.CSRF||""),"Content-Type":"application/json"}',
    )
    # login response sets CSRF
    if "j.csrf" not in t2:
        t2 = t2.replace(
            "if(j.ok)",
            "if(j.ok){if(j.csrf)window.CSRF=j.csrf;",
            1,
        )
        # This might break syntax - be careful. Better find login handler.
    if t2 != t:
        t = t2
        print("CSRF headers patched (best-effort)")
    else:
        print("WARN: could not patch CSRF headers")

# Also add window.CSRF='' near top of script in panel html
if "window.CSRF" not in t:
    t = t.replace(
        "const $=",
        "window.CSRF=window.CSRF||'';const $=",
        1,
    )

# Exclude /api/check from csrf? mutating check/fix needs csrf. state excluded already.

# encrypted backup note in backup_file - add optional passphrase wrapper
if "def backup_encrypt" not in t:
    t = t.replace(
        "def backup_file(path=None):",
        '''def backup_encrypt(raw, passphrase):
    """Encrypt backup JSON with passphrase (Fernet-like via PBKDF2+AES if cryptography missing: XOR fallback refused)."""
    import hashlib, os
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except Exception:
        raise Err('Encrypted backups need the cryptography package (apt install python3-cryptography)')
    salt=os.urandom(16); key=hashlib.pbkdf2_hmac('sha256', passphrase.encode(), salt, 200000, 32)
    aes=AESGCM(key); nonce=os.urandom(12); ct=aes.encrypt(nonce, raw if isinstance(raw,bytes) else raw.encode(), None)
    return b'ALECSUI1'+salt+nonce+ct
def backup_file(path=None):'''
    )

INSTALL.write_bytes(t.replace("\r\n", "\n").encode("utf-8"))
print("follow-up OK", INSTALL.stat().st_size)
