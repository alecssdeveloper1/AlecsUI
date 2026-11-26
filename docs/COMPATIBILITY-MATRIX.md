# AlecsUI VPS Compatibility Matrix (v1.9.1)

Legend: **OK** expected to work · **LIMITED** partial · **NO** not supported · **UNTESTED** no real VM result yet

| Environment | SSH/WS/SSL | V2Ray | Hysteria2 UDP | OpenVPN | WireGuard | BBR | Notes |
|-------------|-----------|-------|---------------|---------|-----------|-----|-------|
| Ubuntu 22.04 KVM x86_64 | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | Primary target |
| Ubuntu 24.04 KVM x86_64 | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | Primary target |
| Debian 12 KVM x86_64 | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | Primary target |
| Ubuntu arm64 KVM | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | UNTESTED | Xray/Hy2 arm64 builds |
| OpenVZ / LXC no TUN | LIMITED | UNTESTED | UNTESTED | **NO** | **NO** | LIMITED | Installer skips OVPN/WG |
| Foreign stunnel on TCP 443 | OK* | — | — | — | — | — | *SSL_PORT auto-reassigned |
| Foreign process on UDP 443 | — | — | LIMITED | — | — | — | Warn; configure HY_PORT |
| Kernel without WireGuard | OK | OK | OK | OK | **NO** | ? | Capability file marks CAP_WG=0 |
| Kernel without BBR | OK | OK | OK | OK | OK | **NO** | Default CC used |

Fill cells with PASS/FAIL after running `tests/vm/` scenarios. Do not mark Production Ready until Primary target rows are PASS.
