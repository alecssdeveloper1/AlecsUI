# Contributing to AlecsUI

Thanks for helping. AlecsUI is GPL-3.0 and a modified fork of ReXUI — keep attribution intact.

## Development model

Almost all runtime code ships inside the single-file installer `install.sh` (panel Python, HTML/JS, systemd units, menu). Prefer small, reviewable patches.

1. Fork and create a branch: `fix/…` or `feat/…`
2. Edit `install.sh` (and docs/CI as needed)
3. Run local checks (see below)
4. Open a PR against `main` — **do not publish a release without maintainer approval**

## Local checks

```bash
# Bash syntax
bash -n install.sh

# Extract and syntax-check embedded panel
python3 tests/extract_and_check.py

# ShellCheck (optional but recommended)
shellcheck -x install.sh || true
```

CI runs the same checks on every PR.

## Rules

- Do not remove features to make tests pass.
- Do not commit secrets, tokens, or live VPS configs.
- Do not install unverified third-party binaries (SHA256 required).
- Preserve users, passwords, certs, and settings on upgrade.
- Never `pkill -KILL` unrelated processes (especially foreign stunnel).
- Document user-facing changes in `CHANGELOG.md`.
- Keep GPL-3.0 and ReXUI attribution.

## Releases (maintainers)

1. Bump `ALECSUI_VER` in `install.sh` and UI strings
2. Update `CHANGELOG.md`
3. Tag `vX.Y.Z`
4. Attach `install.sh` + `install.sh.sha256` to the GitHub Release
5. Do not force-push release tags
