---
title: "Setup guides"
kicker: NFS Files
summary: "The server-side half of connecting: enable NFS, allow non-privileged ports, let your device's address in, and pick a squash mode — for each NAS."
description: "NFS server setup guides for Synology, QNAP, TrueNAS, Unraid, UGREEN and Linux/Raspberry Pi, for use with NFS Files."
---

Every NAS calls the same three settings something different. Pick yours — each guide ends with the export path to type in NFS Files and how to check your work with Inspect Server.

<ul class="cards" markdown="1">
- [Synology (DSM 7)](/guides/synology/) **The most common NAS — NFS service, per-share rules, non-privileged ports**
- [QNAP (QTS / QuTS hero)](/guides/qnap/) **NFS service, NFS host access, squash options**
- [TrueNAS](/guides/truenas/) **CORE and SCALE — service, shares, Mapall, non-root mount**
- [Unraid](/guides/unraid/) **NFS enable, rules, and the nobody:users ownership gotcha**
- [UGREEN (UGOS)](/guides/ugreen/) **Shared-folder NFS rules**
- [Linux / Raspberry Pi](/guides/pi/) **nfs-kernel-server and /etc/exports from scratch**
</ul>

Background that applies to all of them: [exports, the insecure option, and ports](/help/exports/) and [user IDs, groups and squash](/help/identity/).
