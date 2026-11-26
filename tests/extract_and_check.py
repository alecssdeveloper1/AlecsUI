#!/usr/bin/env python3
"""Extract embedded panel.py / HTML / menu from install.sh and run syntax checks."""
from __future__ import annotations

import ast
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.sh"


def extract_heredoc(text: str, marker: str) -> str:
    # cat > path <<'MARKER' ... MARKER
    pat = re.compile(
        rf"<<['\"]?{re.escape(marker)}['\"]?\n(.*?\n){re.escape(marker)}\n",
        re.S,
    )
    m = pat.search(text)
    if not m:
        raise SystemExit(f"heredoc {marker} not found in install.sh")
    return m.group(1)


def main() -> int:
    raw = INSTALL.read_text(encoding="utf-8", errors="replace")
    errors: list[str] = []

    if "ALECSUI_VER=1.9.3" not in raw:
        errors.append("missing ALECSUI_VER=1.9.3")
    if re.search(r'subj "/CN=www\.google\.com"', raw):
        errors.append("P0: stunnel still generates CN=www.google.com")
    if "echo \"admin / $NEWPASS\" >" in raw:
        errors.append("P0: still writing plaintext panel-login.txt")
    if "pkill -KILL -x stunnel4" in raw or "pkill -TERM -x stunnel4" in raw:
        errors.append("P1: mass pkill stunnel4 still present")
    if re.search(r"systemctl stop stunnel4", raw) and "legacy-stunnel4.owned" not in raw:
        errors.append("P0: unconditional systemctl stop stunnel4")
    if "installing zip anyway" in raw.lower():
        errors.append("P0: Xray still installs without checksum")
    if "alecsui-stunnel" not in raw or "ALECSUI_STUNNEL_CONF" not in raw:
        errors.append("P0: dedicated alecsui-stunnel missing")
    if "Match Group $SSH_GROUP" not in raw and "Match Group alecsui-ssh" not in raw:
        errors.append("P0: SSH Match Group missing")
    if "dl_official_digest" not in raw:
        errors.append("P0: official digest helper missing")
    if "csrf_ok" not in raw:
        errors.append("P1: CSRF token check missing")
    if "curl -fsSL https://get.acme.sh | sh" in raw:
        errors.append("P0: acme.sh curl|sh still present")

    panel = extract_heredoc(raw, "PANELPY")
    try:
        ast.parse(panel)
        print("OK: PANELPY python syntax")
    except SyntaxError as e:
        errors.append(f"PANELPY syntax: {e}")

    if "Max-Age=0" not in panel or "/api/logout" not in panel:
        errors.append("logout should clear cookie (Max-Age=0)")
    if "bad origin" not in panel:
        errors.append("missing soft CSRF origin check")

    for name in ("ws-ssh.py",):
        # optional
        pass

    html = extract_heredoc(raw, "PANELHTML")
    if "v1.9.3" not in html:
        errors.append("UI branding not bumped to v1.9.3")
    if "X-CSRF" not in html and "csrf" not in html:
        errors.append("frontend CSRF wiring missing")

    # Write extracted panel for further tooling
    out = pathlib.Path(tempfile.gettempdir()) / "alecsui_panel_extract.py"
    out.write_text(panel, encoding="utf-8")
    print(f"Wrote {out}")

    if errors:
        print("FAIL:")
        for e in errors:
            print(" -", e)
        return 1
    print("All extract checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
