<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,6,20,24&height=220&section=header&text=AlecsUI&fontSize=78&fontColor=ffffff&fontAlignY=38&desc=All-in-one%20VPN%20Panel%20·%20SSH%20·%20V2Ray%20·%20OpenVPN%20·%20WireGuard&descAlignY=58&descSize=14" width="100%" alt="AlecsUI banner"/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=26&duration=2800&pause=900&color=14B8A6&center=true&vCenter=true&multiline=true&width=720&height=90&lines=One+panel.+All+tunnels.;Port+443+%26+80+ready.;Install+in+one+command.)](https://github.com/alecssdeveloper1/AlecsUI)

<br/>

![version](https://img.shields.io/badge/version-1.7-0d9488?style=for-the-badge&logo=v&logoColor=white)
![license](https://img.shields.io/badge/license-GPL--3.0-16a34a?style=for-the-badge&logo=gnu&logoColor=white)
![os](https://img.shields.io/badge/Ubuntu%20%7C%20Debian-x86__64%20%7C%20arm64-0ea5e9?style=for-the-badge&logo=linux&logoColor=white)
![stars](https://img.shields.io/github/stars/alecssdeveloper1/AlecsUI?style=for-the-badge&color=f59e0b&logo=github)
![forks](https://img.shields.io/github/forks/alecssdeveloper1/AlecsUI?style=for-the-badge&color=ec4899&logo=github)

<br/>

![SSH](https://img.shields.io/badge/SSH-22%2F443-ef4444?style=flat-square&logo=ssh&logoColor=white)
![SSL](https://img.shields.io/badge/SSL-TLS-f97316?style=flat-square&logo=letsencrypt&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-80%2F443-eab308?style=flat-square&logo=socketdotio&logoColor=black)
![V2Ray](https://img.shields.io/badge/V2Ray-VLESS%20%7C%20Trojan-22c55e?style=flat-square&logo=v&logoColor=white)
![Reality](https://img.shields.io/badge/Reality-TLS-14b8a6?style=flat-square)
![OpenVPN](https://img.shields.io/badge/OpenVPN-TCP-06b6d4?style=flat-square&logo=openvpn&logoColor=white)
![Hysteria2](https://img.shields.io/badge/Hysteria2-UDP-3b82f6?style=flat-square)
![WireGuard](https://img.shields.io/badge/WireGuard-51820-8b5cf6?style=flat-square&logo=wireguard&logoColor=white)
![DNS](https://img.shields.io/badge/DNS%20Tunnel-53-d946ef?style=flat-square&logo=cloudflare&logoColor=white)
![HAProxy](https://img.shields.io/badge/443%20mode-HAProxy-f43f5e?style=flat-square&logo=nginx&logoColor=white)

<br/>

**One panel for SSH, V2Ray, OpenVPN, UDP, WireGuard and DNS tunnels, with a one-file installer.**  
Everything on port **443** and **80**.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="700">

</div>

<p align="center"><img src="screenshots/dashboard-dark.png" alt="AlecsUI dashboard (dark)" width="100%"></p>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12,6,20&height=4" width="100%"/>

## ✨ What's new in 1.7

![New](https://img.shields.io/badge/NEW-v1.7-14b8a6?style=for-the-badge)
![Inbounds](https://img.shields.io/badge/Inbounds-3X--UI%20style-8b5cf6?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Hardened-ef4444?style=for-the-badge)

- **Inbounds page (like 3X-UI):** make your own V2Ray configs. Pick **VLESS or Trojan**, the port, the transport (**TCP, XHTTP, WS, XHTTP CDN, WS CDN**) and the security (**None, TLS or Reality**). Address, Host, Path and SNI are set on the inbound
- Fresh installs start with **no inbounds**, you make exactly the ones you want
- Each V2Ray user gets only the inbounds you **attach** to them. A new inbound is never added to old users by itself
- Inbounds can **share a port** when they fit together, and a used port is shown before you save
- **WebSocket** for VLESS and Trojan, also through Cloudflare CDN. On 443 mode, WS TLS works on 443 and WS without TLS on 80
- **Compact tables:** inbounds and users in thin rows with a small on/off switch. Tap a user to see details and edit
- **Teal** is the new default colour (the others are still in Settings → Appearance)
- The browser **Back button** now goes back inside the panel

**🔐 Security**
- Xray now runs as its own user (`alecsui-xray`), other services cannot read its keys or config
- Xray downloads (installer, menu and panel update) are checked against the official checksum. If the check fails, nothing is changed
- **Restore** checks every user in the backup file and skips broken ones (it tells you how many)
- A user is not created if its password could not be set
- Old failed-login records are cleaned up every minute, so memory stays small

<details>
<summary><b>🕒 What was new in 1.6 and 1.5</b></summary>

- **1.6:** WireGuard users (own keys, QR, .conf), payload generator on SSH users, real IP for SSH users, CDN address kept on restore
- **1.5:** 443 mode (HAProxy) with self test and rollback, real client IP behind HAProxy, CDN mode, payload builder, server check with Fix buttons, Ports page, Performance mode, Settings in 6 tabs, "No expiry" from Edit

</details>

<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4e04-b05e-b6f0c4555a7f.gif" width="100%">

## 📸 Screenshots

<p align="center">
  <img src="https://img.shields.io/badge/Desktop-UI-0ea5e9?style=for-the-badge&logo=googlechrome&logoColor=white"/>
  <img src="https://img.shields.io/badge/Mobile-PWA-ec4899?style=for-the-badge&logo=pwa&logoColor=white"/>
  <img src="https://img.shields.io/badge/Dark%20%7C%20Light-Themes-8b5cf6?style=for-the-badge&logo=palette&logoColor=white"/>
</p>

| Inbounds | Add inbound |
|---|---|
| <img src="screenshots/inbounds.png" alt="Inbounds"> | <img src="screenshots/add-inbound.png" alt="Add inbound"> |
| **V2Ray users** | **Add V2Ray user (attach inbounds)** |
| <img src="screenshots/users.png" alt="V2Ray users"> | <img src="screenshots/add-v2ray-user.png" alt="Add V2Ray user"> |
| **User details** | **Dashboard (light)** |
| <img src="screenshots/user-details.png" alt="User details"> | <img src="screenshots/dashboard-light.png" alt="Dashboard light"> |
| **SSH users** | **UDP users (Hysteria2)** |
| <img src="screenshots/ssh-users.png" alt="SSH users"> | <img src="screenshots/udp-users.png" alt="UDP users"> |
| **OpenVPN user (.ovpn + bug host)** | **WireGuard user (QR + .conf)** |
| <img src="screenshots/openvpn-user.png" alt="OpenVPN user"> | <img src="screenshots/wireguard-user.png" alt="WireGuard user"> |
| **Who is online** | **Settings: General** |
| <img src="screenshots/online.png" alt="Online users"> | <img src="screenshots/settings-general.png" alt="Settings general"> |
| **DNS tunnel settings** | **CDN mode (Cloudflare)** |
| <img src="screenshots/dns-settings.png" alt="DNS settings"> | <img src="screenshots/cdn.png" alt="CDN mode"> |
| **Payload builder** | **Server check** |
| <img src="screenshots/payloads.png" alt="Payload builder"> | <img src="screenshots/server-check.png" alt="Server check"> |
| **Ports and 443 mode** | **Login** |
| <img src="screenshots/ports.png" alt="Port manager"> | <img src="screenshots/login.jpg" alt="Login page"> |

| Phone: dashboard | Phone: users | Phone: inbounds | User's own page |
|---|---|---|---|
| <img src="screenshots/mobile-dashboard.png" alt="Phone dashboard"> | <img src="screenshots/mobile-users.png" alt="Phone users"> | <img src="screenshots/mobile-inbounds.png" alt="Phone inbounds"> | <img src="screenshots/mobile-user-page.png" alt="User page"> |

<sub>Screenshots use demo data.</sub>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=6,12,24&height=4" width="100%"/>

## 🚀 Install

<p align="center">
  <img src="https://img.shields.io/badge/1_command-install-22c55e?style=for-the-badge&logo=gnubash&logoColor=white"/>
  <img src="https://img.shields.io/badge/root-required-ef4444?style=for-the-badge&logo=linux&logoColor=white"/>
  <img src="https://img.shields.io/badge/Ubuntu_20.04%2B_%7C_Debian_11%2B-supported-0ea5e9?style=for-the-badge"/>
</p>

Run as **root** on a fresh Ubuntu 20.04+ or Debian 11+ VPS (KVM recommended):

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/alecssdeveloper1/AlecsUI/main/install.sh)
```

At the end you get the **panel address** and the **login**. Save them.  
Then type `menu` on the server for the terminal menu.

Running the installer again **updates AlecsUI** and keeps all users and settings.

After install, open **Inbounds** in the panel, make your V2Ray inbounds, then attach them to your V2Ray users.

<img src="https://user-images.githubusercontent.com/74038190/212284145-cbc325cf-53ce-4087-85ea-5c4b112e195d.gif" width="400">

## 🔥 Features

<p align="center">
  <img src="https://img.shields.io/badge/Users-multi%20protocol-f59e0b?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Inbounds-custom-8b5cf6?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/443%20mode-HAProxy-06b6d4?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/CDN-Cloudflare-f97316?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Panel-PWA-ec4899?style=for-the-badge"/>
</p>

**👥 Users, one tab per protocol**
- **V2Ray users:** every attached inbound in one subscription link
- **SSH users:** SSH, SSL, WebSocket, UDPGW, with ready payloads
- **OpenVPN users:** own certificate per user, .ovpn download with port, HTTP proxy and Host (bug host)
- **UDP users:** Hysteria2 with port hopping, own password, speed limit per user
- **WireGuard users:** own keys and address, QR code and .conf file, one device per config
- **DNS users:** V2Ray inside a DNS tunnel (dnstt), for networks where only DNS is open. *Needs your own domain.*
- Every type has its own add button and trial (1 day / 2 GB)
- Data limit, expiry, device limit (2 recommended), monthly reset, expiry from first use
- Disable with a reason, clone, notes, bulk actions (add days, device limit, reset, disable, delete), CSV export / import
- Share card image with QR for WhatsApp, new link / UUID / certificate in one tap

**🧩 Inbounds (V2Ray)**
- VLESS or Trojan on any port, TCP / XHTTP / WS, None / TLS / Reality, Cloudflare CDN for XHTTP and WS
- Address, Host, Path and SNI per inbound, on/off switch, edit and delete
- Attach inbounds to each user, select all / clear all

**🛡️ 443 mode (HAProxy)**
- TLS protocols on **443** (SSH SSL, WS TLS, V2Ray TLS inbounds, OpenVPN), plain WebSocket and V2Ray XHTTP / WS without TLS on **80**
- Works with any SNI, the old ports stay open as a second choice, users see both
- Checks itself on start, rolls back if a check fails, watchdog restarts it or turns it off and tells you on Telegram
- One button in **Settings → Network ports**, or `menu` → 443 mode

**☁️ CDN and payloads**
- **CDN mode:** XHTTP and WS inbounds through Cloudflare (orange cloud). Server IP stays hidden, Cloudflare hosts can be used as the address
- **CDN address per user:** give each user the Cloudflare IP or host that works on their network
- **Payload builder:** write payloads with ready variables ({bug}, {server}, {cdn}, ports, [crlf], [split]...), 11 presets, live preview
- Test a payload on the server in one tap (it checks that SSH really answers)
- Show your payloads to SSH users in their details and on their page, import / export as a file

**⚡ Built for many users**
- Add, edit or disable users without restarting Xray: nobody else gets disconnected
- OpenVPN runs one process per CPU core and spreads new connections between them
- Fair share per OpenVPN user (CAKE), speed limit per UDP user
- DNS cache in Xray, IPv4 first, bigger connection table, small logs, batched saves
- Fast panel with 1000+ users (paged list, compressed live updates)
- Watchdog restarts a service that stops working and tells you on Telegram
- **Performance mode:** Low ping, Balanced or Max speed, changed live without disconnecting anyone

**🖥️ Panel**
- Dashboard with live, 1 hour and 24 hour graphs, top users, usage per protocol, server traffic
- Online page for every protocol, kick, device limit, real IP of SSH users
- Light, dark and black themes, accent colours (teal by default), your own brand name
- Works great on phones, can be installed as an app (PWA)
- Search, logs, login history, activity log, logged-in devices
- 2FA, captcha after wrong logins, change the secret path in one tap

**👤 User page** (opens from the user's link)
- Usage, expiry, 30-day graph, configs with QR codes
- SSH details and payloads, OpenVPN file download, DNS tunnel details
- Announcements, renew warning, app links, change own password

**🧰 Server**
- Telegram alerts: logins, health, certificate, watchdog, daily report, daily backup file
- Backup and restore (OpenVPN certificates and DNS key included)
- **Server check:** services, Xray config, certificate, domains and DNS records (orange / grey cloud), OpenVPN network, firewall, time, disk, memory, with Fix buttons
- **Ports:** every port with its program and server firewall state (one tap to allow)
- Speed test, disk cleanup, swap, Xray auto update with rollback
- Let's Encrypt certificate, DuckDNS updater, fake website, BBR

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=20,12,6&height=4" width="100%"/>

## 🔌 Default ports

| Service | 443 mode | Own port (also works) |
|---|---|---|
| SSH | | 22 |
| SSH SSL / TLS | **443** | |
| SSH WebSocket | **80** | 8880 |
| SSH WebSocket TLS | **443** | 2083 |
| V2Ray inbounds with TLS | **443** | the port you choose |
| V2Ray XHTTP / WS without TLS | **80** | the port you choose |
| V2Ray Reality | | the port you choose |
| OpenVPN TCP | **443** | 1194, 110 |
| HTTP proxy for OpenVPN (Squid) | | 3128 |
| Hysteria2 (UDP) | | 443/udp + 20000-30000/udp (port hopping) |
| WireGuard (UDP) | | 51820/udp |
| DNS tunnel | | 53/udp |
| UDPGW | | 7300 (local) |
| Website | **80**, 443 | |
| Panel | | random (shown after install) |

Open these ports in your VPS provider's firewall (TCP and the UDP ones), plus the port of every inbound you make. Ports can be changed from `menu`.

On 443 mode an inbound also works on 443 / 80 when it uses the main path (`/vless` for XHTTP, `/vws` for WS).

> **Works on the server but not from outside?** Many providers have **Anti-DDoS rules per port**. A rule that expects **SSH** on a web port (80, 8080, 8880) lets only SSH through and silently drops WebSocket and XHTTP. Set those rules to **HTTP**, or delete them.

## 📱 Client apps

| Users | Apps |
|---|---|
| V2Ray | [v2rayNG](https://github.com/2dust/v2rayNG/releases/latest), [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases/latest), [Hiddify](https://github.com/hiddify/hiddify-app/releases/latest), NPV Tunnel |
| SSH | HTTP Custom, HTTP Injector, NPV Tunnel and other SSH / SSL / WebSocket apps |
| OpenVPN | [OpenVPN Connect](https://openvpn.net/client/), HTTP Custom |
| UDP (Hysteria2) | v2rayNG, NekoBox, Hiddify, NPV Tunnel |
| WireGuard | [WireGuard](https://www.wireguard.com/install/) (Android, iPhone, PC), Hiddify, NekoBox |
| DNS + V2Ray | HTTP Custom (SlowDNS, Type Auto), NPV Tunnel (DNSTT) |

## 🌐 DNS tunnel setup

DuckDNS cannot do this. Use your own domain (a cheap `.xyz` works) with DNS on Cloudflare (free) or any DNS host that has **NS** records:

| Type | Name | Value |
|---|---|---|
| A | `ns` | your server IP |
| NS | `t` | `ns.yourdomain.com` |

Then set `t.yourdomain.com` in **Settings → DNS** and open **UDP 53**.  
On Cloudflare keep the cloud **grey (DNS only)**.

## 🧡 CDN setup (Cloudflare)

Needs your own domain on Cloudflare:

| Type | Name | Value | Cloud |
|---|---|---|---|
| A | `cdn` | your server IP | **orange (Proxied)** |

Cloudflare → SSL/TLS → mode **Full**. Then type `cdn.yourdomain.com` in **Settings → CDN**.  
Keep the panel record and the DNS tunnel records **grey**.

## 💻 Terminal menu

```bash
menu
```

Uninstall, panel info, panel login reset (also turns off 2FA), port change (all protocols),
service restart, SSL certificate (Let's Encrypt or your own), backup and restore,
update AlecsUI, update Xray core and geo files, roll back Xray,
server check (find problems), performance mode, 443 mode on / off.

## 💡 Tips

- Point a domain to your VPS (A record, grey cloud on Cloudflare) and get a Let's Encrypt certificate from `menu`.
- Device limit 2 works best for most people (phone + one more, or Wi-Fi to mobile data).
- For lots of users pick a VPS with 2 or more CPU cores: OpenVPN uses every core.
- WireGuard needs a KVM VPS (most OpenVZ / LXC servers have no WireGuard in the kernel).
- Change the panel path in **Settings → General** if anyone else learns it.
- Something not working? Run **Settings → Server check** (or `menu` → Server check) first.

<img src="https://user-images.githubusercontent.com/74038190/212284087-bbe7e430-757e-4901-90bf-4cd2ce3e1852.gif" width="500">

## 👨‍💻 Made by

<div align="center">

### Alecs
[@alecssdeveloper1](https://github.com/alecssdeveloper1)

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=3000&pause=800&color=F59E0B&center=true&vCenter=true&width=520&lines=Thanks+for+using+AlecsUI!;Fork+of+ReXUI+%C2%B7+GPL-3.0" />

<br/>

*AlecsUI is a renamed fork of [ReXUI](https://github.com/chaliraza777/ReXUI) by Ali ([@chaliraza777](https://github.com/chaliraza777)), kept under GPL-3.0 with original credit.*

</div>

### ☕ Donează

<p align="center">
  <a href="https://wise.com/pay/me/alexandrup104"><img src="https://img.shields.io/badge/Wise-Donează-9FE870?style=for-the-badge&logo=wise&logoColor=black" alt="Wise"/></a>
  <a href="https://revolut.me/alecss12"><img src="https://img.shields.io/badge/Revolut-Donează-0075EB?style=for-the-badge&logo=revolut&logoColor=white" alt="Revolut"/></a>
</p>

### 📞 Contact

<p align="center">
  <a href="https://wa.me/40732159658"><img src="https://img.shields.io/badge/WhatsApp-+40_732_159_658-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp"/></a>
  <a href="https://t.me/alecss12"><img src="https://img.shields.io/badge/Telegram-@alecss12-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram"/></a>
</p>

---

## 📜 License

AlecsUI is free software under the **GNU General Public License v3.0**.  
You can use, study, share and change it. If you share a changed version, it must stay under GPL-3.0 with its source code public, and keep the credit to the original ReXUI project and this fork.

© 2026 Alecs ([alecssdeveloper1](https://github.com/alecssdeveloper1))  
Based on ReXUI © 2026 Ali ([chaliraza777](https://github.com/chaliraza777))

> Use AlecsUI only where it is legal, and follow your VPS provider's terms.

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,6,20,24&height=140&section=footer" width="100%"/>
