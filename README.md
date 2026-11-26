<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,6,20,24&height=220&section=header&text=AlecsUI&fontSize=78&fontColor=ffffff&fontAlignY=38&desc=All-in-one%20VPN%20Panel%20·%20SSH%20·%20V2Ray%20·%20OpenVPN%20·%20WireGuard&descAlignY=58&descSize=14" width="100%" alt="AlecsUI banner"/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=2800&pause=900&color=14B8A6&center=true&vCenter=true&multiline=true&width=720&height=90&lines=Un+panou.+Toate+tunelurile.;One+panel.+All+tunnels.;Port+443+%26+80+ready.)](https://github.com/alecssdeveloper1/AlecsUI)

<br/>

### 🌐 Limbă / Language

[![Română](https://img.shields.io/badge/🇷🇴_Română-002B7F?style=for-the-badge)](#-română)
[![English](https://img.shields.io/badge/🇬🇧_English-CF142B?style=for-the-badge)](#-english)

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

**RO:** Un panou pentru SSH, V2Ray, OpenVPN, UDP, WireGuard și tuneluri DNS, cu instalator într-un singur fișier. Totul pe porturile **443** și **80**.  
**EN:** One panel for SSH, V2Ray, OpenVPN, UDP, WireGuard and DNS tunnels, with a one-file installer. Everything on port **443** and **80**.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="700">

</div>

<p align="center"><img src="screenshots/dashboard-dark.png" alt="AlecsUI dashboard (dark)" width="100%"></p>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=12,6,20&height=4" width="100%"/>

# 🇷🇴 Română

## ✨ Noutăți în 1.7

![New](https://img.shields.io/badge/NOU-v1.7-14b8a6?style=for-the-badge)
![Inbounds](https://img.shields.io/badge/Inbounds-stil_3X--UI-8b5cf6?style=for-the-badge)
![Security](https://img.shields.io/badge/Securitate-Întărită-ef4444?style=for-the-badge)

- **Pagină Inbounds (ca 3X-UI):** creezi propriile configuri V2Ray. Alegi **VLESS sau Trojan**, portul, transportul (**TCP, XHTTP, WS, XHTTP CDN, WS CDN**) și securitatea (**None, TLS sau Reality**). Address, Host, Path și SNI se setează pe inbound
- Instalările noi încep **fără inbounds** — faci exact ce ai nevoie
- Fiecare user V2Ray primește doar inbound-urile pe care i le **atașezi**. Un inbound nou nu se adaugă singur la userii vechi
- Inbound-urile pot **împărți un port** când se potrivesc, iar un port deja folosit e afișat înainte să salvezi
- **WebSocket** pentru VLESS și Trojan, inclusiv prin Cloudflare CDN. În modul 443, WS TLS pe 443 și WS fără TLS pe 80
- **Tabele compacte:** inbound-uri și useri pe rânduri subțiri, cu switch on/off. Atingi un user pentru detalii și editare
- **Teal** e culoarea implicită (restul în Settings → Appearance)
- Butonul **Back** din browser navighează înapoi în panou

**🔐 Securitate**
- Xray rulează ca user separat (`alecsui-xray`), celelalte servicii nu îi pot citi cheile sau configul
- Download-urile Xray (installer, meniu, update panou) sunt verificate cu checksum oficial. Dacă verificarea eșuează, nu se schimbă nimic
- **Restore** verifică fiecare user din backup și sare peste cei corupți (îți spune câți)
- Un user nu e creat dacă parola nu a putut fi setată
- Înregistrările vechi de login eșuat se curăță în fiecare minut

<details>
<summary><b>🕒 Ce era nou în 1.6 și 1.5</b></summary>

- **1.6:** useri WireGuard (chei proprii, QR, .conf), generator payload pe SSH, IP real pentru SSH, adresa CDN păstrată la restore
- **1.5:** modul 443 (HAProxy) cu self-test și rollback, IP client real în spatele HAProxy, CDN mode, payload builder, Server check cu butoane Fix, pagina Ports, Performance mode, Settings în 6 tab-uri, „No expiry” din Edit

</details>

## 🚀 Instalare

<p align="center">
  <img src="https://img.shields.io/badge/1_comandă-instalare-22c55e?style=for-the-badge&logo=gnubash&logoColor=white"/>
  <img src="https://img.shields.io/badge/root-obligatoriu-ef4444?style=for-the-badge&logo=linux&logoColor=white"/>
  <img src="https://img.shields.io/badge/Ubuntu_20.04%2B_%7C_Debian_11%2B-suportat-0ea5e9?style=for-the-badge"/>
</p>

Rulează ca **root** pe un VPS fresh Ubuntu 20.04+ sau Debian 11+ (recomandat KVM):

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/alecssdeveloper1/AlecsUI/main/install.sh)
```

La final primești **adresa panoului** și **login-ul**. Salvează-le.  
Apoi tastează `menu` pe server pentru meniul din terminal.

Dacă rulezi installer-ul din nou, **actualizează AlecsUI** și păstrează userii și setările.

După instalare, deschide **Inbounds** în panou, creează inbound-urile V2Ray, apoi atașează-le userilor V2Ray.

## 🔥 Funcții

**👥 Useri, câte un tab pe protocol**
- **V2Ray:** toate inbound-urile atașate într-un singur link de subscription
- **SSH:** SSH, SSL, WebSocket, UDPGW, cu payload-uri gata
- **OpenVPN:** certificat propriu per user, download `.ovpn` cu port, HTTP proxy și Host (bug host)
- **UDP:** Hysteria2 cu port hopping, parolă proprie, limită de viteză per user
- **WireGuard:** chei și adresă proprii, QR + `.conf`, un device per config
- **DNS:** V2Ray în tunel DNS (dnstt), pentru rețele unde e deschis doar DNS. *Ai nevoie de domeniu propriu.*
- Buton Add + trial (1 zi / 2 GB) pentru fiecare tip
- Limită date, expirare, limită device (recomandat 2), reset lunar, expirare de la prima folosire
- Disable cu motiv, clone, note, acțiuni bulk, export/import CSV
- Card share cu QR pentru WhatsApp, link / UUID / certificat nou dintr-un tap

**🧩 Inbounds (V2Ray)** · **🛡️ Modul 443 (HAProxy)** · **☁️ CDN și payload-uri** · **⚡ Optimizat pentru mulți useri** · **🖥️ Panou PWA** · **🧰 Server check, backup, Telegram**

## 🔌 Porturi implicite

| Serviciu | Modul 443 | Port propriu |
|---|---|---|
| SSH | | 22 |
| SSH SSL / TLS | **443** | |
| SSH WebSocket | **80** | 8880 |
| SSH WebSocket TLS | **443** | 2083 |
| V2Ray TLS | **443** | portul ales de tine |
| V2Ray XHTTP / WS fără TLS | **80** | portul ales de tine |
| V2Ray Reality | | portul ales de tine |
| OpenVPN TCP | **443** | 1194, 110 |
| HTTP proxy OpenVPN (Squid) | | 3128 |
| Hysteria2 (UDP) | | 443/udp + 20000-30000/udp |
| WireGuard (UDP) | | 51820/udp |
| Tunel DNS | | 53/udp |
| UDPGW | | 7300 (local) |
| Website | **80**, 443 | |
| Panou | | random (afișat după instalare) |

Deschide aceste porturi în firewall-ul providerului. Porturile se schimbă din `menu`.

> **Merge pe server, dar nu din exterior?** Mulți provideri au reguli Anti-DDoS pe port. O regulă care așteaptă **SSH** pe 80/8080/8880 lasă doar SSH și blochează WebSocket/XHTTP. Pune-le pe **HTTP** sau șterge-le.

## 📱 Aplicații client

| Useri | Aplicații |
|---|---|
| V2Ray | [v2rayNG](https://github.com/2dust/v2rayNG/releases/latest), [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases/latest), [Hiddify](https://github.com/hiddify/hiddify-app/releases/latest), NPV Tunnel |
| SSH | HTTP Custom, HTTP Injector, NPV Tunnel |
| OpenVPN | [OpenVPN Connect](https://openvpn.net/client/), HTTP Custom |
| UDP (Hysteria2) | v2rayNG, NekoBox, Hiddify, NPV Tunnel |
| WireGuard | [WireGuard](https://www.wireguard.com/install/), Hiddify, NekoBox |
| DNS + V2Ray | HTTP Custom (SlowDNS), NPV Tunnel (DNSTT) |

## 🌐 Setup tunel DNS

DuckDNS nu merge aici. Folosește un domeniu propriu cu DNS pe Cloudflare (sau orice host cu înregistrări **NS**):

| Tip | Nume | Valoare |
|---|---|---|
| A | `ns` | IP-ul serverului |
| NS | `t` | `ns.domeniultau.com` |

Apoi setează `t.domeniultau.com` în **Settings → DNS** și deschide **UDP 53**.  
Pe Cloudflare lasă norul **gri (DNS only)**.

## 🧡 Setup CDN (Cloudflare)

| Tip | Nume | Valoare | Nor |
|---|---|---|---|
| A | `cdn` | IP-ul serverului | **portocaliu (Proxied)** |

Cloudflare → SSL/TLS → modul **Full**. Apoi `cdn.domeniultau.com` în **Settings → CDN**.  
Panoul și înregistrările DNS tunnel rămân **gri**.

## 💻 Meniu terminal

```bash
menu
```

Dezinstalare, info panou, reset login (oprește și 2FA), schimbare porturi, restart servicii, certificat SSL, backup/restore, update AlecsUI / Xray, Server check, Performance mode, modul 443 on/off.

## 💡 Sfaturi

- Point un domeniu la VPS (A record, nor gri) și ia certificat Let's Encrypt din `menu`
- Limită device 2 e ideală pentru majoritatea (telefon + încă unul)
- Pentru mulți useri: VPS cu 2+ cores (OpenVPN folosește fiecare core)
- WireGuard are nevoie de VPS KVM
- Schimbă path-ul panoului din **Settings → General** dacă află altcineva
- Probleme? Rulează **Settings → Server check** (sau `menu` → Server check)

<p align="right"><a href="#-limbă--language">⬆️ Sus / Top</a></p>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=6,12,24&height=4" width="100%"/>

# 🇬🇧 English

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

<sub>Screenshots use demo data. / Screenshot-urile folosesc date demo.</sub>

<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4e04-b05e-b6f0c4555a7f.gif" width="100%">

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
- **CDN mode:** XHTTP and WS inbounds through Cloudflare (orange cloud). Server IP stays hidden
- **CDN address per user**, **Payload builder** with presets and live preview
- Test a payload on the server in one tap

**⚡ Built for many users** · **🖥️ Panel (PWA, themes, 2FA)** · **🧰 Server tools (Telegram, backup, Server check, Ports, BBR)**

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

Open these ports in your VPS provider's firewall. Ports can be changed from `menu`.

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

DuckDNS cannot do this. Use your own domain with DNS on Cloudflare (or any DNS host that has **NS** records):

| Type | Name | Value |
|---|---|---|
| A | `ns` | your server IP |
| NS | `t` | `ns.yourdomain.com` |

Then set `t.yourdomain.com` in **Settings → DNS** and open **UDP 53**.  
On Cloudflare keep the cloud **grey (DNS only)**.

## 🧡 CDN setup (Cloudflare)

| Type | Name | Value | Cloud |
|---|---|---|---|
| A | `cdn` | your server IP | **orange (Proxied)** |

Cloudflare → SSL/TLS → mode **Full**. Then type `cdn.yourdomain.com` in **Settings → CDN**.  
Keep the panel record and the DNS tunnel records **grey**.

## 💻 Terminal menu

```bash
menu
```

Uninstall, panel info, panel login reset (also turns off 2FA), port change, service restart, SSL certificate, backup and restore, update AlecsUI / Xray, server check, performance mode, 443 mode on / off.

## 💡 Tips

- Point a domain to your VPS (A record, grey cloud on Cloudflare) and get a Let's Encrypt certificate from `menu`
- Device limit 2 works best for most people
- For lots of users pick a VPS with 2+ CPU cores
- WireGuard needs a KVM VPS
- Change the panel path in **Settings → General** if anyone else learns it
- Something not working? Run **Settings → Server check** first

<p align="right"><a href="#-limbă--language">⬆️ Top / Sus</a></p>

<img src="https://user-images.githubusercontent.com/74038190/212284087-bbe7e430-757e-4901-90bf-4cd2ce3e1852.gif" width="500">

---

## 👨‍💻 Made by / Creat de

<div align="center">

### Alecs
[@alecssdeveloper1](https://github.com/alecssdeveloper1)

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=3000&pause=800&color=F59E0B&center=true&vCenter=true&width=560&lines=Mul%C8%9Bumim+c%C4%83+folose%C8%99ti+AlecsUI!;Thanks+for+using+AlecsUI!;Fork+of+ReXUI+%C2%B7+GPL-3.0" />

<br/>

**RO:** AlecsUI este un fork redenumit al [ReXUI](https://github.com/chaliraza777/ReXUI) de Ali ([@chaliraza777](https://github.com/chaliraza777)), păstrat sub GPL-3.0 cu credit original.  
**EN:** AlecsUI is a renamed fork of [ReXUI](https://github.com/chaliraza777/ReXUI) by Ali ([@chaliraza777](https://github.com/chaliraza777)), kept under GPL-3.0 with original credit.

</div>

### ☕ Donează / Donate

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

## 📜 License / Licență

**RO:** AlecsUI este software liber sub **GNU General Public License v3.0**. Poți folosi, studia, partaja și modifica. Dacă publici o versiune modificată, trebuie să rămână GPL-3.0, cu sursa publică, și să păstrezi creditul proiectului original ReXUI și al acestui fork.

**EN:** AlecsUI is free software under the **GNU General Public License v3.0**. You can use, study, share and change it. If you share a changed version, it must stay under GPL-3.0 with its source code public, and keep the credit to the original ReXUI project and this fork.

© 2026 Alecs ([alecssdeveloper1](https://github.com/alecssdeveloper1))  
Based on ReXUI © 2026 Ali ([chaliraza777](https://github.com/chaliraza777))

> **RO:** Folosește AlecsUI doar unde este legal și respectă termenii providerului VPS.  
> **EN:** Use AlecsUI only where it is legal, and follow your VPS provider's terms.

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,6,20,24&height=140&section=footer" width="100%"/>
