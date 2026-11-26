# AlecsUI v1.9.1 — Security Report

**Status:** Hardening applied in code. **Not Production Ready** until VM matrix tests pass.  
**Date:** 2026-03-26  
**Scope:** install.sh monolith (panel, menu, services)

## Fixed in 1.9.1

| ID | Severity | Finding | Fix |
|----|----------|---------|-----|
| S1 | P0 | Generic `stunnel4` stopped without ownership check | Dedicated `alecsui-stunnel` + `/etc/alecsui/stunnel.conf`; foreign stunnel untouched |
| S2 | P0 | Mass/ambiguous stunnel PID kill | Only PIDs with our unit/cmdline; KILL after TERM timeout |
| S3 | P0 | Global `PasswordAuthentication yes` | `Match Group alecsui-ssh` only; drop-in rollback on `sshd -t` fail |
| S4 | P0 | Uninstall disabled foreign stunnel / wiped broadly | Manifest + restore originals; no `stunnel4` disable |
| S5 | P0 | Digest from same mirror as binary | `dl_official_digest` only from `github.com` |
| S6 | P1 | BadVPN floating tag | Pinned commit `752c6b49…` (tag 1.999.130) |
| S7 | P1 | `curl \| sh` acme.sh | Versioned GitHub tarball `acme.sh@3.1.0` |
| S8 | P1 | CSRF only Origin header | Dedicated CSRF token in session + `X-CSRF` / body |
| S9 | P1 | Port steal / IPv6 ignored | `busy` checks `-4`/`-6`; auto-reassign SSL if foreign |

## Residual risks (not Production Ready blockers alone, but must be tracked)

| ID | Severity | Residual | Plan |
|----|----------|----------|------|
| R1 | High | Panel still runs as **root** | Helper allowlist exists; full `User=` drop after soak |
| R2 | High | SSH user passwords in `users.json` for share UI | Encrypt at rest / optional omit from disk |
| R3 | Medium | Encrypted backup needs `python3-cryptography` | Document; default still plaintext JSON with 0600 |
| R4 | Medium | Helper allowlist incomplete vs all panel ops | Expand after VM tests |
| R5 | Medium | Go/dnstt integrity depends on go.dev JSON SHA | Keep; consider vendoring |
| R6 | Low | Session in memory only | Acceptable; document |

## Explicit non-claims

- No VM install/connection tests executed in this pass.
- No declaration of Production Ready.
- No GitHub publish/tag/commit without maintainer approval.
