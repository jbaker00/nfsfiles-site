---
title: "The server refused this device"
kind: mount_access_denied
summary: "The most common NFS error there is. Two causes look identical from the client: the share requires privileged ports (add `insecure`), or your device's address isn't in the share's allowed-client list."
description: "NFS Files error mount_access_denied: The most common NFS error there is. Two causes look identical from the client: the share requires privileged ports (add `insecure`), or your device's address isn't in the share's allowed-client list."
---

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
