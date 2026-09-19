---
title: "The server didn't respond in time"
kind: timeout
summary: "The app sent its request and nothing came back. Usually the NAS is off, asleep, on a different network, or a firewall is silently dropping the packets."
description: "NFS Files error timeout: The app sent its request and nothing came back. Usually the NAS is off, asleep, on a different network, or a firewall is silently dropping the packets."
---

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
