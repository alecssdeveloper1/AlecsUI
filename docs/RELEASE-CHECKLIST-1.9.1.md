# Release checklist — AlecsUI v1.9.1

- [ ] `bash -n install.sh` PASS
- [ ] `python3 tests/extract_and_check.py` PASS
- [ ] `bash tests/installer_static_checks.sh` PASS
- [ ] CI green on PR
- [ ] SECURITY-REPORT reviewed
- [ ] CHANGELOG.md has 1.9.1 section
- [ ] README version badges 1.9.1
- [ ] `scripts/make-release-checksum.sh` → `install.sh.sha256`
- [ ] VM: Ubuntu 22.04 fresh install + Server check
- [ ] VM: Debian 12 fresh install
- [ ] VM: foreign stunnel on 443 (SSL port reassigned, foreign left running)
- [ ] VM: upgrade from 1.9.0 with users kept
- [ ] VM: uninstall restores SSH drop-in / foreign stunnel; reinstall OK
- [ ] Manual: SSH user login, VLESS/Reality connect, Hysteria2 UDP (where supported)
- [ ] Maintainer approval for commit
- [ ] Maintainer approval for tag `v1.9.1` + GitHub Release assets
- [ ] **Do not** claim Production Ready until VM matrix primary rows PASS
