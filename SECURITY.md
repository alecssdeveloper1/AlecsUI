# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.9.x   | Yes       |
| 1.8.x   | Best-effort |
| < 1.8   | No        |

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security problems that can be exploited remotely (auth bypass, RCE, path traversal, secret leak).

Email or contact the maintainer privately via GitHub Security Advisories:
https://github.com/alecssdeveloper1/AlecsUI/security/advisories/new

Include:
- Affected version / commit
- Reproduction steps
- Impact (who can exploit, what is gained)

You should receive an acknowledgement within a few days.

## Hardening expectations (operators)

- Run only on a dedicated VPS you control.
- Prefer **KVM**; OpenVZ/LXC may lack TUN/WireGuard/BBR.
- Change the panel password immediately; enable **2FA**.
- Do not leave the initial password in chat logs or tickets.
- Use **Let's Encrypt** (menu → SSL) for a real domain; self-signed certs are for testing only.
- Open only required ports in the **provider** firewall (TCP/UDP differ — e.g. Hysteria2 UDP 443 ≠ TLS TCP 443).
- Keep backups offline; backup JSON contains user secrets.
- Update only from **GitHub Releases** with SHA256 (do not set `ALECSUI_ALLOW_MAIN=1` unless you accept the risk).

## Known residual risks

See the latest release notes / audit notes. Critical findings must be fixed before calling a build Production Ready.
