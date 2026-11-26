# Changelog

All notable changes to AlecsUI are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/). Versioning follows SemVer.

AlecsUI is a **modified** fork of ReXUI (Ali / chaliraza777), GPL-3.0.

## [1.9.7] — 2026-11-26

### Fixed
- Panel URL: warn when port is not Cloudflare HTTPS (46026 etc. fails behind orange cloud); show IP fallback
- New installs prefer panel ports **2053/8443/2083…** (CF-compatible) instead of random high ports
- Server check + menu + Settings show Cloudflare port guidance after domain cert

## [1.9.6] — 2026-11-26

### Fixed
- Let's Encrypt: stop installing acme.sh with `admin@localhost` (LE `invalidContact`); prompt for real email / default `ssl@domain`
- ACME: auto-fix bad ACCOUNT_EMAIL; use webroot when HAProxy/443 mode holds port 80

## [1.9.5] — 2026-11-26

### Fixed
- Installer UI: ASCII-only progress bar/spinner/banner (Termius showed `?` for UTF-8 block/braille; `tr`+multi-byte was broken)

## [1.9.4] — 2026-11-26

### Fixed
- Server check false **"Not installed"** / **Xray · Stopped**: panel routed all `systemctl` via helper, which rejected `show` and `is-active --quiet`
- Port conflict false positive: AlecsUI stunnel binary named `stunnel4` is now treated as ours
- Helper allowlist: flags before unit (`--quiet`); larger stdout for status reads

## [1.9.3] — 2026-11-26

### Fixed
- Stunnel: re-check + auto-reassign SSL/WS-TLS **immediately before bind** (WHM/cPanel often holds 443/2083)
- Stunnel conf: `foreground = yes`, bind `0.0.0.0:PORT` (clearer failures under systemd Type=simple)
- Retry once with alternate ports on Address-already-in-use; persist new ports to `/etc/tunnel/config`
- Disable stock `stunnel4` unit after apt when its config has no `accept=` (avoids racing AlecsUI)

## [1.9.2] — 2026-03-26

### Added
- Animated bilingual installer (RO/EN): banner, spinner, progress bar, colored status
- Language prompt (or `ALECSUI_LANG=ro|en`)
- Official OS range: Ubuntu **20–26**, Debian **11+**

## [1.9.1] — 2026-03-26

### Security
- Dedicated `alecsui-stunnel` unit + `/etc/alecsui/*` — never `systemctl stop stunnel4` unless legacy AlecsUI marker
- SSH: `Match Group alecsui-ssh` for password auth; global PasswordAuthentication not forced on; `sshd -t` rollback
- Uninstall: manifest-aware, restores foreign stunnel/SSH drop-ins; explicit `DELETE-USERS` for purge
- Digests only from `github.com` (`dl_official_digest`); Hysteria hashes official-only
- BadVPN pinned to commit of tag `1.999.130`
- acme.sh via versioned GitHub archive (no `curl|sh`)
- Dedicated CSRF token (`csrf` / `X-CSRF`) for mutating API
- Port checks IPv4+IPv6; auto-reassign SSL if foreign stunnel holds 443
- Privileged helper socket (`alecsui-helper`) allowlist for systemctl/user/firewall ops

### Docs / tests
- `docs/SECURITY-REPORT-1.9.1.md`, compatibility matrix, release checklist, `tests/vm/`

### Known
- Panel still runs as root (helper prepared for future drop)
- VM matrix not executed in this workspace — not Production Ready

## [1.9.0] — 2026-03-26

### Security
- Stunnel stop targets **only AlecsUI PIDs** (unit / pidfile / our config); no mass `pkill` of foreign stunnel.
- Port conflict detection uses **PID + systemd unit**, not bare process names (`python3`/`stunnel` alone no longer “own” foreign ports).
- TCP vs UDP ports treated separately (Hysteria2 UDP 443 ≠ TLS TCP 443).
- Xray install requires **pinned version + SHA256**; missing/mismatched digest aborts (no “install anyway”).
- Self-signed stunnel CN no longer uses `www.google.com`; misleading existing certs are replaced with `AlecsUI-selfsigned`.
- Initial panel password is **not** written to `/etc/tunnel/panel-login.txt`.
- Logout clears the session cookie (`Max-Age=0`).
- Soft CSRF: mutating `/api/*` rejects cross-origin `Origin`/`Referer`.
- SSH tuning still enables password auth for tunnel users but **does not** enable root password login; warns if `PermitRootLogin yes`.
- `/etc/tunnel` permissions tightened; UFW changes preceded by a rules backup.
- Safe update prefers **GitHub Releases + SHA256**; `main` only with `ALECSUI_ALLOW_MAIN=1`.

### Added
- Install flock lock (`/run/alecsui-install.lock`).
- Pre-install/upgrade backup under `/root/alecsui-preinstall-*`.
- Capability probe → `/etc/tunnel/capabilities` (virt, TUN, WG, BBR, systemd).
- OpenVPN package/service skipped when TUN missing; WireGuard skipped without kernel support.
- Server check reports virt/capabilities and stunnel CN issues.
- CI workflow, SECURITY.md, CONTRIBUTING.md, NOTICE, issue templates, extract tests.

### Changed
- Version branding → AlecsUI v1.9.0.
- Documented production-readiness gaps that remain (see SECURITY.md / release notes).

## [1.8.0] — prior

- Stunnel 443 reinstall conflict mitigation (v1.7 leftover).
- OpenVZ-friendlier install notes.
- Download mirrors for Xray/Hysteria.
- Panel password printed early during install.
