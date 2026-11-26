---
name: Bug report
about: Something broken in install, panel, or protocols
labels: bug
---

**AlecsUI version**
- [ ] 1.9.x
- [ ] 1.8.x
- [ ] other:

**VPS**
- OS (Ubuntu/Debian + version):
- Virt (KVM / OpenVZ / LXC / unknown):
- Arch (x86_64 / arm64):

**What happened**
Steps to reproduce:

**Expected**

**Logs** (sanitize secrets)
```
journalctl -u tunnel-panel -n 50 --no-pager
systemctl status stunnel4 --no-pager
menu → Server check
```

**Do not paste** panel passwords, Telegram tokens, private keys, or backup JSON.
