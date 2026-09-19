#!/usr/bin/env python3
"""Writes help/errors/<kind>/index.md for every NFSError.kind the app can
produce. The kinds must match NFSKit/Sources/NFSKit/NFSError.swift in the
app repo (see ErrorKindTests there); a kind with no page 404s to the site's
generic troubleshooting page, which is survivable but wastes a tap.

Run from the site root: python3 scripts/gen_error_pages.py
"""
import os, textwrap

PAGES = {}

def page(kind, title, summary, body):
    PAGES[kind] = (title, summary, textwrap.dedent(body).strip() + "\n")

# ---------------------------------------------------------------- connecting

page("timeout", "The server didn't respond in time",
"The app sent its request and nothing came back. Usually the NAS is off, asleep, on a different network, or a firewall is silently dropping the packets.",
"""
## What this means

NFS Files opened a connection to the address you entered and waited about eight seconds. Nothing answered — not even a refusal. A silent non-answer is different from a "connection refused": refused means a machine is there and said no; a timeout means the packets went nowhere.

## Check these, in order

1. **Is the server on?** Look at the dot on the server card in NFS Files. Grey means the app couldn't ping it either. A sleeping NAS (hibernation, HDD spin-down with network standby) often won't wake for NFS.
2. **Same network?** Your phone or Mac has to be on the same LAN as the NAS. Turn off any VPN (Tailscale, WireGuard, a corporate VPN) and make sure you're not on a guest Wi-Fi network — most routers isolate guest devices from the rest of the house.
3. **Right address?** A typo in the IP is the most common cause of all. Use **Scan My Network** in the add-server form: it sweeps your subnet for anything speaking RPC and lists what it finds.
4. **The NAS's own firewall.** Synology, QNAP and TrueNAS all ship a firewall that, once enabled, blocks NFS unless you add a rule. NFS needs port **111** (portmapper), **2049** (NFS) and the MOUNT service port (random unless you pin it) open to your subnet. See the [setup guide for your NAS](/guides/).
5. **Router firewall / VLANs.** If the NAS is on a different VLAN (pfSense, UniFi, OPNsense), the firewall between VLANs must allow those same ports. NFSv3 is particularly awkward across firewalls because MOUNT uses a random port — pin it on the server, or pick **NFSv4** in the app's Advanced settings (NFSv4 uses port 2049 only).
6. **Local Network permission.** On iPhone and iPad, a denied Local Network permission can look like a timeout. See [Local Network permission](/help/local-network/).

## On a Mac

The same checks apply. Additionally, on macOS 15 and later, the first time an app talks to the local network macOS asks for permission — if that dialog was dismissed, you'll see either this error or "host unreachable". [How to turn it on](/help/local-network/).
""")

page("connection_closed", "The server closed the connection",
"A machine answered, then hung up before finishing. Usually the NFS service is restarting, a TCP wrapper rule rejected you, or the NAS went to sleep mid-conversation.",
"""
## What this means

The TCP connection was established — so the address and port are right — but the server ended it without replying. That's different from a refusal (nothing listening) or a timeout (nothing answering).

## Common causes

- **The NFS service is restarting** on the NAS (after a settings change, an update, or a nightly task). Wait thirty seconds and try again.
- **TCP wrappers** — on Linux servers, `/etc/hosts.deny` with a line like `rpcbind: ALL` or `mountd: ALL` makes the server accept the connection and immediately close it. Add your subnet to `/etc/hosts.allow`, or remove the deny rule.
- **The NAS went to sleep** partway through. Disable HDD hibernation for testing, or turn on wake-on-LAN and wake it first.
- **A proxy or "smart" firewall** in the path is terminating idle connections. Rare on a home network, common on a corporate one.
- **A userspace NFS server** (Docker images, small Go/Rust servers) that crashed on the request. Check its log.

## What to try

Tap **Inspect Server** on the server card. If the RPC table loads but the export list doesn't, the problem is with `mountd`; if nothing loads, the whole RPC stack on the server is refusing you.
""")

page("dns", "Couldn't find a server with that name",
"The name you typed didn't resolve to an address. `.local` names only work on the same network segment, and short names like `nas` usually don't work on iOS at all.",
"""
## What this means

Before NFS Files can connect it has to turn the name into an IP address. That lookup failed.

## The usual reasons

- **A `.local` name across VLANs or Wi-Fi bands.** `mynas.local` is a Bonjour (mDNS) name. It resolves only on the same broadcast domain — a NAS on a different VLAN, a wired NAS with Wi-Fi client isolation on, or a mesh network with mDNS reflection off will not answer.
- **A bare short name.** `nas`, `synology`, `truenas` — these depend on a DNS search domain that iOS and iPadOS generally don't apply. Use `nas.local`, the full name your router gives it (`nas.lan`, `nas.home.arpa`), or the IP.
- **A typo.**
- **Pi-hole / custom DNS** that doesn't know the name.

## The reliable fix

Use the IP address. Find it in your router's client list, on the NAS's own status page, or with **Scan My Network** in NFS Files, which sweeps your subnet and shows what's answering. Give the NAS a fixed IP (DHCP reservation on the router) so it doesn't change.
""")

page("refused", "The server refused the connection",
"A machine is at that address, but nothing is listening on the port. The NFS service is probably switched off, or the app is pointed at the wrong port.",
"""
## What this means

The server answered — with a TCP reset. That's what an operating system says when nothing is listening on a port. So the address is right; the service isn't there.

## If you're using the normal (portmapper) mode

The app first asks the **portmapper on port 111**. A refusal here means `rpcbind` isn't running. Two very different explanations:

1. **NFS is switched off on the NAS.** Every NAS ships with NFS disabled.
   - **Synology:** Control Panel → File Services → NFS → *Enable NFS service*.
   - **QNAP:** Control Panel → Network & File Services → Win/Mac/NFS/WebDAV → NFS Service → enable.
   - **TrueNAS:** System → Services → NFS → running (and *Start automatically*).
   - **Unraid:** Settings → NFS → *Enable NFS: Yes*.
   - **Linux / Raspberry Pi:** `sudo apt install nfs-kernel-server` and `sudo systemctl enable --now nfs-server`.
2. **The server is NFSv4-only and doesn't run a portmapper.** Some servers (TrueNAS with NFSv3 disabled, hardened Linux boxes, some Docker images) only speak NFSv4 on port 2049 and never start `rpcbind`. In NFS Files, open the server's Advanced settings, set **NFS Version → NFSv4**, turn on **Custom Port** and enter **2049**. The app then skips the portmapper entirely.

## If you're using Custom Port

Then the port you typed is closed. Check the server's configuration for the port it actually uses. Userspace servers commonly use 2049 or a high port like 20490; check their log line on startup.

## A firewall can also "refuse"

Most firewalls silently drop (which gives a [timeout](/help/errors/timeout/)), but some are configured to reject, which looks like this. If the NAS firewall is on, add a rule allowing 111 and 2049 (and mountd) from your subnet.
""")

page("host_unreachable", "No route to the server",
"Your device couldn't find a path to that address. On iPhone, iPad and Mac the most common cause is the Local Network permission being off.",
"""
## What this means

The operating system reported *host unreachable*. It didn't even get as far as sending the request — it couldn't work out how to reach that address. On a local network that almost always means one of three things.

## 1. Local Network permission (most likely)

iOS, iPadOS and macOS 15+ ask, the first time an app talks to your LAN, whether to allow it. If that was answered *Don't Allow* — or dismissed — every local connection fails with exactly this error, and the app is never asked again.

- **iPhone / iPad:** Settings → Privacy & Security → **Local Network** → turn on **NFS Files**.
- **Mac (macOS 15 Sequoia and later):** System Settings → Privacy & Security → **Local Network** → turn on **NFS Files**.

Full walkthrough with screenshots: [Local Network permission](/help/local-network/).

## 2. Different subnet

Your device is on `192.168.1.x` but the NAS is on `192.168.2.x` (a second router, a guest network, a VLAN) with no route between them. Check the IP your device has (Settings → Wi-Fi → ⓘ) against the NAS's IP. Same first three numbers, or a router that routes between them, is required.

## 3. The NAS is off, or the IP is wrong

On a LAN, an address that no device answers ARP for can produce this error rather than a timeout. Check the dot on the server card and try **Scan My Network**.
""")

page("network_unreachable", "No network for that address",
"Your device has no usable network interface for that address — Wi-Fi is off, you're on cellular only, or (on a Mac) the Local Network permission is denied.",
"""
## What this means

The operating system said *network unreachable*: there's no interface that could carry a packet to that address at all.

## Check

- **Wi-Fi is on** and connected to your home network. Cellular can't reach a NAS on your LAN (unless you've set up a VPN to home — in which case check that the VPN is connected).
- **Airplane mode** is off.
- **On a Mac with macOS 15 or later:** a denied **Local Network** permission produces this error. System Settings → Privacy & Security → Local Network → turn on NFS Files. [Details](/help/local-network/).
- **IPv6 address?** If you typed an IPv6 literal and your Wi-Fi has no IPv6, use the IPv4 address instead.
- **Ethernet adapter on iPad or Mac:** make sure it has an address (Settings → Ethernet), not just a link.
""")

page("connection_reset", "The server dropped the connection",
"The connection was open and working, then the server reset it. Almost always transient: the NAS rebooted, the NFS service restarted, or a firewall timed out an idle session.",
"""
## What this means

*Connection reset by peer*. Something on the server end tore down an established connection.

## What to do

1. **Try again.** If the NAS was restarting, the second attempt usually works.
2. **Was it idle for a long time?** Some routers and firewalls expire idle TCP sessions after a few minutes and reset them when traffic resumes. Reconnecting fixes it; if it keeps happening, look for an "idle timeout" setting on the firewall.
3. **Check the NAS log** if it recurs — a crashing NFS daemon or a storage error underneath will show there.
4. **On Linux servers:** TCP wrappers (`/etc/hosts.deny`) can reset connections from addresses that aren't allowed. Make sure your subnet is in `/etc/hosts.allow`.
""")

page("connection_failed", "Couldn't reach the server",
"A network error the app couldn't classify further. The system's own description is in the message; the basics below cover most of them.",
"""
## What this means

The connection failed with an error the app doesn't have a specific page for. The text after "Couldn't reach the server" in the alert is the operating system's description — it's worth reading.

## The basics

- Same Wi-Fi network as the NAS, VPN off, guest network off.
- The NAS is on and the IP is right (**Scan My Network** finds it).
- Local Network permission is on for NFS Files ([how](/help/local-network/)).
- NFS is enabled on the NAS ([setup guides](/guides/)).

## If it persists

Email the exact message — **Settings → Contact Support** in the app starts the email with it filled in. Unclassified errors are how new pages get added here.
""")

page("malformed_reply", "The server sent a reply the app couldn't understand",
"Whatever is on that port isn't speaking NFS. Usually a Custom Port pointed at the wrong service, or a proxy in the way.",
"""
## What this means

NFS Files got a response, but it didn't parse as an ONC RPC / NFS message. The most likely explanation: the port belongs to something else.

## Check

- **Custom Port on?** Make sure the port is the NFS/MOUNT port, not SMB (445), the web UI (5000/5001 on Synology, 8080 on QNAP), or SSH (22).
- **A proxy or load balancer** in the path is unlikely at home, but if this is a corporate network, ask whether NFS traffic is inspected.
- **A broken or very old userspace server.** Some NFS implementations in Docker images or embedded devices send non-standard replies. Try forcing **NFSv3** in the server's Advanced settings; if that doesn't help, check for an updated image.
- **Inspect Server** on the server card shows the server's RPC table — if that loads, the portmapper is fine and the problem is specific to NFS or MOUNT.
""")

page("auth_rejected", "The server rejected the app's credentials",
"The server won't accept plain AUTH_SYS (uid/gid) authentication. Either the export requires Kerberos, or the security list for the share doesn't include `sys`.",
"""
## What this means

NFS has no passwords. Ordinary NFS (what NFS Files speaks) identifies you with a numeric user and group ID — the `sys` security flavour, also called AUTH_UNIX. The server refused that flavour outright at the RPC layer. That happens when the share is configured for **Kerberos only**.

## Fix it on the server

Add `sys` to the share's security options. Kerberos can stay enabled alongside it.

<div id="nas-synology"></div>

- **Synology:** Control Panel → Shared Folder → select the folder → Edit → **NFS Permissions** → edit the rule → **Security**: tick **sys** (you can leave krb5 ticked too).

<div id="nas-truenas"></div>

- **TrueNAS:** Sharing → Unix (NFS) Shares → edit → Advanced Options → **Security**: make sure **SYS** is in the list (it must be first if you want it used by default). Also System → Services → NFS → *Require Kerberos for NFSv4* must be **off**.

<div id="nas-pi"></div>

- **Linux / Raspberry Pi:** in `/etc/exports`, an option like `sec=krb5` restricts the export. Change it to `sec=sys:krb5` (or remove `sec=` — `sys` is the default), then `sudo exportfs -ra`.

- **QNAP, Unraid, UGREEN:** don't offer Kerberos-only NFS from their UIs; if you see this error there, the server is probably restricting by client address instead — see [access denied](/help/errors/mount_access_denied/).

## NFS Files does not support Kerberos

That's deliberate: Kerberos needs a KDC, keytabs, and a domain, none of which exist on a home network. If your workplace NAS is Kerberos-only, ask the administrator for a `sys`-secured export for your subnet, or use their VPN and a different client.
""")

page("rpc_rejected", "The server rejected the request at the RPC layer",
"The program version the app asked for isn't what the server offers. Usually a server that speaks only NFSv4 reached through the NFSv3 path, or Custom Port pointing at a different RPC service.",
"""
## What this means

The server answered, but said the RPC program or version doesn't match. NFS Files speaks **NFSv3** (with the separate MOUNT v3 protocol) and **NFSv4.0**. This error means the server doesn't offer the one the app tried.

## Most likely: a version mismatch

- **The server is NFSv4-only** (TrueNAS with NFSv3 disabled, many hardened Linux setups, some Docker images). With *NFS Version: Auto* the app tries v4 first, then v3 — if the v4 attempt failed for some *other* reason, the error you see is from the v3 attempt and can be misleading. Set **NFS Version → NFSv4** in the server's Advanced settings so you see the real v4 error.
- **The server is NFSv2-only.** Very old devices and some routers with USB storage. NFS Files doesn't support NFSv2; there's no fix short of a newer server.
- **NFSv4.1+ only.** A server configured to *require* 4.1 or 4.2 will reject 4.0. On Linux, `/etc/nfs.conf` `[nfsd] vers4.0=y` re-enables it; on TrueNAS, check the NFS service's protocol options.

## Custom Port pointing at the wrong RPC service

If **Custom Port** is on, the port must be the NFS server (and for v3, also the MOUNT server). Pointing it at the portmapper (111) or another RPC program gives this error.

## See what the server offers

**Inspect Server** on the server card shows the RPC table — every program and version registered on the server. Look for `nfs` versions 3 and 4 and `mountd` version 3.
""")

page("program_unavailable", "NFS isn't registered on this server",
"The portmapper answered but has no NFS or MOUNT service registered for the version the app asked for. NFS is probably enabled but not running, or the server is NFSv4-only.",
"""
## What this means

The portmapper on port 111 is running — so the server is up and RPC works — but when NFS Files asked "where is NFS version 3 / MOUNT version 3?", the portmapper said *no such program*.

## Causes and fixes

1. **NFS service enabled but not started.** On Linux, `sudo systemctl status nfs-server` and `rpcinfo -p` on the server; on a NAS, toggle the NFS service off and on.
2. **NFSv4-only server.** NFSv4 doesn't use the MOUNT protocol, so a server with NFSv3 disabled registers no `mountd`. Set **NFS Version → NFSv4** in the app's Advanced settings.
   - **TrueNAS:** System → Services → NFS → Advanced → *Enabled Protocols*. If only NFSv4 is ticked, either tick NFSv3 as well or use NFSv4 in the app.
   - **Linux:** `/etc/nfs.conf` `[nfsd] vers3=n` means v3 is off.
3. **A stale portmapper.** After reconfiguring NFS, `rpcbind` can hold an out-of-date table. Restart the NFS service (or the NAS).

## See for yourself

**Inspect Server** on the server card shows the RPC table — the same output as `rpcinfo -p`. If `nfs` is there but `mountd` isn't, that's case 2.
""")

page("export_not_found", "That folder isn't shared",
"The server has NFS running but doesn't export the path you typed. The path has to match the server's export list exactly — and every NAS spells it differently.",
"""
## What this means

The MOUNT request came back *no such folder*. The server is fine; the **export path** doesn't match anything it shares.

## The fix: ask the server

In the add-server form, tap **Find Shared Folders**. The app asks the server for its export list and lets you pick from it. That removes the guesswork entirely.

## Why paths trip people up

Each NAS uses its own layout, and the export path is the server's *internal* path, not the share name:

<div id="nas-synology"></div>

| NAS | Export path looks like |
|---|---|
| Synology | `/volume1/photos` (not `/photos`) |
| QNAP | `/share/CACHEDEV1_DATA/Public` (QNAP also accepts `/Public` on many models) |
| Unraid | `/mnt/user/media` |
| TrueNAS | `/mnt/tank/media` (pool, then dataset) |
| UGREEN | `/volume1/media` |
| Linux / Raspberry Pi | whatever is in `/etc/exports`, e.g. `/srv/nfs/media` |
| macOS | whatever is in `/etc/exports`, e.g. `/Users/Shared/media` |

Case matters. Trailing slashes don't.

## NFSv4 and subfolders

With **NFSv4**, some Linux servers export a *pseudo-root* (`fsid=0`): the path you mount is relative to that root, so `/` or `/media` may be right where NFSv3 needed `/srv/nfs/media`. If Find Shared Folders shows a path that doesn't work on v4, try the shorter form — or set NFS Version to NFSv3.

Synology only lets you mount a *subfolder* of a share if the NFS rule has **Allow users to access mounted subfolders** ticked.
""")

page("mount_access_denied", "The server refused this device",
"The most common NFS error there is. Two causes look identical from the client: the share requires privileged ports (add `insecure`), or your device's address isn't in the share's allowed-client list.",
"""
## What this means

The server's MOUNT service answered *access denied* (EACCES). Annoyingly, Linux-based servers — which is nearly every NAS — return exactly the same answer for two different problems:

1. **The export requires privileged ports.** Traditionally, NFS servers only trusted clients connecting from ports below 1024, because only root could open them. iPhone, iPad and Mac apps can't use those ports at all. The export needs the `insecure` option (called *non-privileged ports* on Synology).
2. **Your device's address doesn't match the export's client rule.** Exports are granted to hosts or subnets. If the rule says `192.168.1.0/24` and your phone has `192.168.2.37` (a different Wi-Fi network, a VLAN, a VPN address), you're refused.

## Tell them apart

Tap **Inspect Server** on the server card in NFS Files. The **Shared Folders** section lists every export with the client rules the server reports for it. If your subnet is listed (or the rule is `*`), the problem is #1. If it isn't, it's #2.

## Fix #1 — allow non-privileged ports

<div id="nas-synology"></div>

**Synology (DSM 7):** Control Panel → Shared Folder → select the folder → Edit → **NFS Permissions** tab → select the rule → Edit → tick **Allow connections from non-privileged ports (ports higher than 1024)** → OK → Save. Also tick **Allow users to access mounted subfolders** if you connect to subfolders.

<div id="nas-ugreen"></div>

**UGREEN (UGOS Pro):** Control Panel → Shared Folder → the folder → NFS → edit the rule. The layout mirrors Synology's; look for the non-privileged-ports option in the rule. If you don't see it, check the IP rule first (Fix #2). *I don't own a UGREEN — if the screens have moved, email a screenshot and I'll fix this page.*

<div id="nas-truenas"></div>

**TrueNAS (CORE and SCALE):** System → Services → NFS → edit (⚙) → tick **Allow non-root mount** → Save. This is TrueNAS's name for `insecure`, and it's global rather than per share.

<div id="nas-unraid"></div>

**Unraid:** the default rule already includes `insecure`. Shares → the share → NFS Security Settings → **Rule** — make sure `insecure` is in the option list, e.g. `192.168.1.0/24(sec=sys,rw,insecure,anongid=100,anonuid=99,all_squash)`.

<div id="nas-qnap"></div>

**QNAP (QTS / QuTS hero):** QNAP's NFS server allows non-privileged ports by default; if you see this error on a QNAP it's almost always Fix #2.

<div id="nas-pi"></div>

**Linux / Raspberry Pi / OpenMediaVault:** add `insecure` to the export's options in `/etc/exports`, then `sudo exportfs -ra`:

```
/srv/nfs/media  192.168.1.0/24(rw,sync,insecure,no_subtree_check,all_squash,anonuid=1000,anongid=1000)
```

OMV: Services → NFS → Shares → edit → *Extra options* → add `insecure`.

**macOS as a server:** in `/etc/nfs.conf` add `nfs.server.mount.require_resv_port = 0`, then `sudo nfsd restart`.

## Fix #2 — allow your device's address

Find your device's IP (iPhone: Settings → Wi-Fi → ⓘ; Mac: System Settings → Wi-Fi → Details). Then make sure the export's client rule covers it. A subnet like `192.168.1.0/24` covers every address starting `192.168.1.`; a single IP only covers that device (and phones change IP unless the router reserves one).

- **Synology:** the NFS rule's **Hostname or IP** field. `*` allows everyone on any network the NAS can see; a subnet is safer.
- **QNAP:** Control Panel → Privilege → Shared Folders → Edit Shared Folder Permission → *NFS host access* → add the IP or network and tick it.
- **TrueNAS:** the share's *Authorized Networks* / *Authorized Hosts*. Empty means everyone.
- **Unraid:** the rule's leading host/subnet, and *Security* set to Public or Secure/Private with your network listed.
- **Linux:** the host pattern before the parentheses in `/etc/exports`.

Hostname rules (rather than IP) need the server to reverse-resolve your device's IP to that name — unreliable for phones. Use IPs or subnets.

## Still refused after both?

- The share may be exported to a **different interface**. A NAS with two networks (LAN + Docker bridge, or LAN + Thunderbolt) can bind rules to one of them.
- **`subtree_check`** on Linux can refuse subfolder mounts; use `no_subtree_check`.
- Send the output of Inspect Server with your email — it includes the exact rule the server reports.
""")

page("mount_denied", "The server refused to share that folder",
"The MOUNT request failed with an error other than access denied or not found — the path is a file, is too long, or the server hit an internal error.",
"""
## What this means

The MOUNT service on the server answered with an unusual status. The alert names it: *not a folder*, *name too long*, *not supported*, or a server fault.

## Check

- **Is the path a folder?** An export path that points at a file returns *not a folder*. Use **Find Shared Folders** to pick from what the server actually exports.
- **Very long paths** — over 255 characters per component — are refused.
- **Server fault** means the server's `mountd` hit an internal error: a disk that isn't mounted, a dataset that's locked (encrypted TrueNAS datasets after a reboot), or a corrupt exports table. Check the NAS's storage page and its NFS log.
- **Not supported** from MOUNT is rare and usually means a minimal userspace server. Try **NFS Version → NFSv4** (no MOUNT protocol at all).
""")

page("unsupported", "The server doesn't support something the app needs",
"The server answered, but lacks an operation NFS Files relies on. Try pinning the other NFS version; if that doesn't help, email the message.",
"""
## What this means

NFS Files asked for an operation the server says it doesn't implement. Full servers (Linux `nfsd`, every major NAS) implement everything the app uses; the ones that don't are usually small userspace servers.

## Try

1. In the server's Advanced settings, set **NFS Version** explicitly — **NFSv3** if it was Auto or v4, **NFSv4** if it was v3. The two versions have different required operations.
2. If the server is a Docker image or a small Go/Rust/Python NFS server, check for an updated version; several gained missing operations recently.
3. Email the exact message from the alert (**Settings → Contact Support** fills it in). Knowing which operation and which server lets me either work around it or document it here.
""")

# ------------------------------------------------------------- nfs statuses

page("nfs_perm", "Operation not permitted",
"The server allows you into the folder but refused this particular change. Almost always: changing an owner or group needs root, and the export squashes root.",
"""
## What this means

NFS status 1, *EPERM*: not *access denied* to the folder, but *this operation* isn't permitted for who you are. It's distinct from [access denied](/help/errors/nfs_access/).

## When you'll see it

- **Changing owner or group** in the permission editor. On every Unix server, only root can give a file to another user, and nearly every export maps root to nobody (`root_squash`). Even presenting UID 0 doesn't help. Change ownership on the NAS itself (SSH `sudo chown`, or the NAS's file manager).
- **Changing permissions on a file you don't own.** Only the owner (or root) can `chmod`. Check *Inspect Server* → "Export owned by" against "You present".
- **Setting timestamps** or other attributes on read-only or immutable files.

## What helps

Match the UID/GID you present to the file's owner (the permission editor shows the current owner), or do the change on the server side. See [User IDs and squash](/help/identity/).
""")

page("nfs_noent", "No such file or folder",
"The item isn't there any more — renamed, moved or deleted by someone else since the listing was loaded — or, on NFSv4, the export path doesn't exist under the server's pseudo-root.",
"""
## What this means

NFS status 2, *ENOENT*. The server was asked about a name that doesn't exist in that folder.

## Usually

Someone (or something — a sync job, a media server tidying up) changed the folder after NFS Files listed it. Pull to refresh, or go back and re-open the folder.

## On NFSv4, at connect time

If this happened while *connecting*, the export path doesn't exist under the NFSv4 pseudo-filesystem. Linux servers with `fsid=0` present a different root to NFSv4 clients than to NFSv3 ones — `/srv/nfs/media` on v3 may be `/media` on v4. Use **Find Shared Folders**, try the shorter path, or set **NFS Version → NFSv3**. Details on the [not shared](/help/errors/export_not_found/) page.

## Case sensitivity

NFS servers are case-sensitive. `Photos` and `photos` are different folders.
""")

page("nfs_io", "The server reported an I/O error",
"The server tried to read or write the disk and failed. That's a storage problem on the NAS, not a network one — check its storage health.",
"""
## What this means

NFS status 5, *EIO*. The NFS layer is fine; the disk underneath returned an error. Treat this seriously — it's often the first visible sign of a failing drive.

## Check on the NAS

- **Storage manager / pool health:** Synology Storage Manager, QNAP Storage & Snapshots, TrueNAS Storage → pool status, Unraid Main → array. A degraded or errored volume explains this.
- **USB drives** that were unplugged or spun down. Re-plug and re-export.
- **Encrypted datasets** that are locked after a reboot (TrueNAS) — unlock them.
- **Overlay or FUSE mounts** (mergerfs, rclone mounts, Docker volumes) exported over NFS can return EIO when the backend is unavailable.
- **Linux:** `dmesg | tail` on the server shows the actual disk error.

## From the app's side

Nothing to fix. Reconnect after the storage is healthy.
""")

page("nfs_access", "Access denied by the server",
"You're connected, but the server won't let the user you present read or write here. NFS has no passwords — the numeric User ID is your identity, and the export may squash it.",
"""
## What this means

NFS status 13, *EACCES*. The server checked the numeric **User ID / Group ID** the app presents against the folder's owner, group and permissions — and said no.

## Why NFS works this way

NFS (the `sys` flavour every home NAS uses) has no login. The client simply *states* a UID and GID, and the server takes it at face value — then applies normal Unix permissions, possibly after **squashing** (remapping) that identity:

- `root_squash` — UID 0 becomes `nobody`. On by default everywhere.
- `all_squash` — *every* UID becomes one designated user (`anonuid`/`anongid`). Then the UID you present doesn't matter at all; the folder has to be accessible to that designated user.
- No squash — the UID you present is used as-is.

## Find out what the server sees

Tap **Inspect Server** on the server card. It shows **You present** (your UID/GID), **Export owned by** (the folder's owner), the folder's permission bits, and whether **Read** and **Write** actually work — plus a plain-language read on which squash mode you're hitting. Free, no Pro needed.

## Fix it

**Option A — present the right UID.** On the server, run `id yourname` to find your numeric UID and GID (the first user on Synology is usually `1026`, on most Linux boxes `1000`). Put those in the server's **Advanced → User ID / Group ID** in NFS Files.

<div id="nas-synology"></div>

**Option B — squash everyone to one user (simplest).** Make the export map all clients to a user that owns the folder:

- **Synology:** NFS rule → **Squash: Map all users to admin** (or to guest for read-only folders). Then the UID in the app is irrelevant.
- **QNAP:** NFS host access → *Squash option: all_squash*, *Anonymous UID/GID* set to the share's owner.
- **TrueNAS:** share → Advanced → **Mapall User / Mapall Group** set to the owner.
- **Unraid:** the default rule already does this (`all_squash,anonuid=99,anongid=100` = `nobody:users`); make sure the share's files are owned by `nobody:users` (Tools → New Permissions).
- **Linux:** `all_squash,anonuid=1000,anongid=1000` in `/etc/exports`.

**Option C — fix the folder's permissions** on the server so your UID (or group) has access: `chmod`, `chown`, or the NAS's file manager.

## Group-owned folders

NFS Files currently sends one group ID. If access depends on a *secondary* group membership on the server, use Option B or make the folder readable by the primary group. (Extra group IDs are on the roadmap.)

Full background: [User IDs and squash](/help/identity/).
""")

page("nfs_exist", "An item with that name already exists",
"The server already has something with that name in this folder — possibly one you can't see because it differs only by case, or is a hidden file.",
"""
## What this means

NFS status 17, *EEXIST*. You tried to create, rename or move something to a name that's taken.

## Check

- **Refresh the folder.** Another device may have created it since you loaded the list.
- **Hidden files.** NFS Files shows dotfiles (`.DS_Store`, `._name` AppleDouble files) so you can see them, but Files.app and the Finder hide them — the conflicting item may be one of those.
- **Case.** The server is case-sensitive, but if it's a share on a case-insensitive volume (some Synology btrfs shares configured for Windows, macOS APFS exports), `Photo.jpg` and `photo.jpg` collide.

Pick a different name.
""")

page("nfs_notdir", "That item isn't a folder",
"The app tried to open or list something that's a file (or a link to a file), not a folder.",
"""
## What this means

NFS status 20, *ENOTDIR*. A path component that should be a folder is a file.

## Usually

- **The export path** points at a file. Use **Find Shared Folders** and pick a folder.
- **A symbolic link** on the server that points at a file (or a dangling one). NFS Files follows links where the server allows; a link to a file can't be opened as a folder. Fix or remove the link on the server.
""")

page("nfs_isdir", "That item is a folder",
"A file operation was attempted on a folder. Refresh — the item may have changed type on the server since it was listed.",
"""
## What this means

NFS status 21, *EISDIR*. The name refers to a folder, and the operation (download, overwrite, delete-as-file) only works on files.

## Usually

The listing was stale: a file was deleted and a folder created with the same name, or a symbolic link now points at a folder. Pull to refresh and try again. If it persists for one specific item, look at it on the server itself.
""")

page("nfs_fbig", "The file is too large for this server",
"The server can't hold a file this size — usually a 4 GB limit on an exFAT/FAT32 volume (USB drives), or a per-file quota.",
"""
## What this means

NFS status 27, *EFBIG*. The write would exceed the maximum file size the filesystem allows.

## Causes

- **FAT32** (4 GB max) or **exFAT** volumes on USB drives attached to the NAS. Reformat the drive as ext4, btrfs or APFS-on-Mac, or copy to the NAS's main volume.
- **A file-size limit** in a user quota or a userspace server's configuration.
- Very old NFSv2-era servers with 2 GB limits — NFS Files doesn't support those anyway.
""")

page("nfs_nospc", "The server is out of space",
"The volume the share lives on is full. Free some space on the NAS, or check whether snapshots or a recycle bin are holding it.",
"""
## What this means

NFS status 28, *ENOSPC*. The server tried to allocate space and there was none.

## Where the space went

- **Recycle bins** — Synology and QNAP keep deleted files in `#recycle` / `@Recycle`; empty them.
- **Snapshots** — Synology Snapshot Replication, TrueNAS ZFS snapshots and QNAP snapshots all hold space until they're deleted.
- **Another share** on the same volume filled it up. The free-space figure NFS Files shows on the server card is for the volume, not the share.
- **Inodes** — a volume with millions of tiny files can be "full" with space left. `df -i` on Linux.
""")

page("nfs_rofs", "The share is read-only",
"The export is shared read-only, or the volume under it went read-only after an error.",
"""
## What this means

NFS status 30, *EROFS*. Writes are refused because the filesystem — as seen by this client — is read-only.

## Two possibilities

**1. The export rule is read-only.**

<div id="nas-synology"></div>

- **Synology:** NFS rule → **Privilege: Read/Write**.
- **QNAP:** NFS host access → *Access right: read/write*.
- **TrueNAS:** share → untick **Read Only**.
- **Unraid:** NFS Security Settings → *Security* rule with `rw`.
- **Linux:** `rw` instead of `ro` in `/etc/exports`, then `sudo exportfs -ra`.

**2. The volume itself is read-only.** Synology puts a volume into read-only mode after a filesystem error (Storage Manager shows a warning); Linux remounts a volume read-only on disk errors (`dmesg` shows it). Fix the storage; the export rule is fine.
""")

page("nfs_nametoolong", "The name is too long",
"Server filesystems cap each name at 255 bytes — and accented or non-Latin characters take two to four bytes each.",
"""
## What this means

NFS status 63, *ENAMETOOLONG*. The file or folder name exceeds the server's limit.

## The limit is in bytes, not characters

Linux filesystems allow 255 **bytes** per name. In UTF-8, ASCII letters are one byte, accented Latin letters two, and most CJK characters three — so a 100-character Japanese filename is already 300 bytes. Some NAS models with encrypted shares (Synology eCryptfs) drop the limit to about **143 characters**.

Shorten the name.
""")

page("nfs_notempty", "The folder isn't empty",
"The server won't delete a folder that still has something in it — sometimes a hidden file you can't see in Files.app or the Finder.",
"""
## What this means

NFS status 66, *ENOTEMPTY*. Deleting a folder over NFS only works when it's empty.

## Check inside it in NFS Files

The app shows hidden files (`.DS_Store`, `._something` AppleDouble files, `@eaDir` on Synology, `.Trash` folders) that Files.app and the Finder hide. Delete those first, then the folder.

If you're deleting from the Finder or Files.app through the NFS Files location, the system asks the app to delete items one at a time; a folder whose contents failed to delete will show this. Open the folder in NFS Files to see what's left.
""")

page("nfs_dquot", "Storage quota exceeded",
"The user you present (or the user the export squashes you to) has hit their quota on the NAS.",
"""
## What this means

NFS status 69, *EDQUOT*. There's free space on the volume, but the *user* the write is charged to has reached their quota.

## Who gets charged

Whatever user the server maps you to — the UID you present, or with `all_squash` the anonymous user (`anonuid`). Check **Inspect Server** to see which.

## Raise or remove it

- **Synology:** Control Panel → User & Group → the user → Quota; or Shared Folder → the folder → Edit → *Advanced* → shared-folder quota.
- **QNAP:** Control Panel → Privilege → Quota.
- **TrueNAS:** the dataset's *Quota / Refquota*, and per-user quotas under the dataset's *User Quotas*.
- **Linux:** `quota -u username` and `edquota`.
""")

page("nfs_stale", "Stale file handle",
"The server no longer recognises the handle the app holds for this item — it was moved or deleted server-side, or the export was restarted. Reconnect from the server list.",
"""
## What this means

NFS status 70, *ESTALE*. NFS identifies files by an opaque *handle* rather than a path. The server says the handle the app holds doesn't point at anything any more.

## Causes

- **The item was deleted or moved** on the server (by another device, a script, a media manager) while NFS Files still had it open.
- **The export was re-exported** — the NAS rebooted, the NFS service restarted, or the volume was remounted — and the server's handle numbering changed. Common with **USB drives** that were unplugged and re-plugged.
- **The export options changed** (`fsid=`, or the share was recreated).

## Fix

Go back to the server list and reconnect; the app fetches fresh handles. If it keeps happening after every server restart on Linux, add a fixed `fsid=<number>` to the export in `/etc/exports` so handles survive reboots.
""")

page("nfs_badhandle", "The file handle is no longer valid",
"An NFSv4 server rejected the handle the app holds. Same cure as a stale handle: reconnect from the server list.",
"""
## What this means

NFSv4 status 10001, *BADHANDLE*. The server considers the file handle malformed or from a different generation — typically after the NFS service restarted, the export was re-created, or the volume was remounted.

## Fix

Reconnect from the server list. If it recurs on one specific item, look at that item on the server; if it recurs after every NAS restart, the export needs a stable `fsid`. See [stale file handle](/help/errors/nfs_stale/).
""")

page("nfs_notsupp", "The operation isn't supported by this server",
"The server doesn't implement this NFS operation. Small userspace servers skip things like SETATTR (used by the permission editor); do that action on the server instead.",
"""
## What this means

NFS status 10004, *NOTSUPP*. The server understood the request and declined to implement it. Full servers (Linux `nfsd`, every major NAS) support everything NFS Files uses; small userspace ones don't.

## Where you'll see it

- **Editing permissions** on a server without SETATTR. Some Go/Rust/Python NFS servers, some Docker "nfs-server" images, and a few embedded devices. Change permissions on the server itself.
- **Renaming across folders** on servers that don't implement RENAME between directories.
- **NFSv4 servers** that omit optional operations. Try **NFS Version → NFSv3** in the app.

## Which server is it?

If it's a NAS you'd expect to work, email me the model and the operation named in the alert.
""")

page("nfs_serverfault", "The server hit an internal error",
"The NFS server itself failed while handling the request. Usually transient; if it repeats, the NAS's own log says why.",
"""
## What this means

Status 10006, *SERVERFAULT*. Not a permissions or network problem — the server's NFS daemon encountered an error it couldn't classify.

## What to do

1. **Retry.** Often it's a momentary condition (a background scrub, a snapshot being taken).
2. **Check the NAS log** — Synology Log Center, QNAP System Logs, TrueNAS Alerts, `journalctl -u nfs-server` on Linux.
3. **Storage** — a dataset that's locked, unmounted or degraded produces this on some servers rather than an I/O error.
""")

page("nfs_delay", "The server asked to retry in a moment",
"The server is busy or the item is temporarily unavailable (a spun-down disk, a snapshot in progress). Wait a few seconds and try again.",
"""
## What this means

Status 10008, *DELAY* (called *JUKEBOX* in NFSv3, from the days of tape libraries). The request is valid; the server can't serve it right now.

## Usually

- **A spun-down disk** waking up. Give it 10–20 seconds.
- **A snapshot or scrub** running on that dataset.
- **Hierarchical storage** — a file archived to slower tiers (some enterprise NAS features).

Just try again.
""")

page("nfs_expired", "The connection to the server expired",
"The NFSv4 lease timed out — usually after the app was in the background a while or the NAS restarted. Reconnect from the server list.",
"""
## What this means

NFSv4 status 10011 / 10022 (*EXPIRED* / *STALE_CLIENTID*). NFSv4 servers give each client a lease that must be renewed. After a long pause — the app suspended in the background, the device asleep, the NAS restarted — the server forgets the client.

## Fix

Go back to the server list and reconnect. The app establishes a fresh client ID. Nothing on the server needs changing.
""")

page("nfs_grace", "The server is still starting up",
"The NFSv4 server just restarted and is in its grace period (typically 90 seconds) while old clients reclaim their state. Wait a minute and retry.",
"""
## What this means

NFSv4 status 10013, *GRACE*. After a restart, an NFSv4 server refuses new operations for a grace period so clients that were mid-write can recover. NFS Files has nothing to recover, but it still has to wait.

## Fix

Wait 60–90 seconds and try again. On Linux the period is `/proc/fs/nfsd/nfsv4gracetime` (default 90 s); on a NAS it isn't adjustable. If the server *always* reports grace, its NFS service is crash-looping — check the NAS log.
""")

page("cancelled", "Cancelled",
"You cancelled the operation. Nothing to fix.",
"""
Nothing went wrong on the server; the request was stopped from this end. If you didn't mean to cancel, just try again.
""")

def main():
    root = os.path.join(os.path.dirname(__file__), "..", "help", "errors")
    for kind, (title, summary, body) in PAGES.items():
        d = os.path.join(root, kind)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.md"), "w") as f:
            f.write("---\n")
            f.write(f"title: \"{title}\"\n")
            f.write(f"kind: {kind}\n")
            f.write(f"summary: \"{summary}\"\n")
            f.write(f"description: \"NFS Files error {kind}: {summary}\"\n")
            f.write("---\n\n")
            f.write(body)
    # Index page listing every error.
    with open(os.path.join(root, "index.md"), "w") as f:
        f.write("---\ntitle: \"Every error, explained\"\nkicker: Errors\nsummary: \"What each message NFS Files can show means, and what fixes it. Tap Learn More in the app to land on the right one.\"\n---\n\n")
        f.write("## Connecting\n\n<ul class=\"errlist\">\n")
        for kind in ["timeout", "refused", "host_unreachable", "network_unreachable", "dns", "connection_closed", "connection_reset", "connection_failed", "malformed_reply", "program_unavailable", "rpc_rejected", "auth_rejected", "export_not_found", "mount_access_denied", "mount_denied", "unsupported"]:
            t, s, _ = PAGES[kind]
            f.write(f"<li><a href=\"/help/errors/{kind}/\"><code>{kind}</code> {t}</a><br><span>{s}</span></li>\n")
        f.write("</ul>\n\n## While browsing and transferring\n\n<ul class=\"errlist\">\n")
        for kind in PAGES:
            if kind.startswith("nfs_"):
                t, s, _ = PAGES[kind]
                f.write(f"<li><a href=\"/help/errors/{kind}/\"><code>{kind}</code> {t}</a><br><span>{s}</span></li>\n")
        f.write("</ul>\n\nSomething not listed? The app shows codes like `nfs_status_123` for statuses it hasn't seen before — email the code and what you were doing.\n")
    print(f"wrote {len(PAGES)} error pages + index")

if __name__ == "__main__":
    main()
