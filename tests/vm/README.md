# VM test suite (staging only)

Do **not** run against production VPS.

## Scenarios

| ID | Script / manual | Goal |
|----|-----------------|------|
| V1 | `scenario_fresh.sh` | Fresh Ubuntu/Debian install |
| V2 | manual | Foreign stunnel on 443 before install |
| V3 | manual | Occupied TCP/UDP ports |
| V4 | manual | OpenVZ/LXC without TUN |
| V5 | manual | Upgrade with existing users |
| V6 | manual | Uninstall + reinstall |
| V7 | `scenario_health.sh` | Post-install health (not just systemctl) |

## V2 foreign stunnel (manual)

On a clean VM as root:

```bash
apt-get install -y stunnel4
# configure /etc/stunnel/stunnel.conf accept=443 for an unrelated service
systemctl enable --now stunnel4
# then run AlecsUI install.sh
# EXPECT: AlecsUI picks alternate SSL_PORT; system stunnel4 still active; alecsui-stunnel uses other port
```

## Success criteria

- Listener sockets exist for claimed ports (`ss -lntp` / `ss -lnup`)
- `python3 /opt/tunnel-panel/panel.py check` has zero unexpected FAIL for installed features
- Foreign services still running after install/uninstall
- SSH: root password auth not newly enabled globally; `alecsui-ssh` group users can password-auth
