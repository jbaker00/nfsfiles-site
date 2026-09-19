---
title: "Setup guides"
kicker: NFS Files
summary: "The server-side half of connecting: enable NFS, allow non-privileged ports, let your device's address in, and pick a squash mode — for each NAS."
description: "NFS server setup guides for Synology, QNAP, TrueNAS, Unraid, UGREEN and Linux/Raspberry Pi, for use with NFS Files."
---

Every NAS calls the same three settings something different. Pick yours — each guide ends with the export path to type in NFS Files and how to check your work with Inspect Server.

<ul class="cards">
<li><a href="/guides/synology/"><strong>Synology (DSM 7)</strong><span>The most common NAS — NFS service, per-share rules, non-privileged ports</span></a></li>
<li><a href="/guides/qnap/"><strong>QNAP (QTS / QuTS hero)</strong><span>NFS service, NFS host access, squash options</span></a></li>
<li><a href="/guides/truenas/"><strong>TrueNAS</strong><span>CORE and SCALE — service, shares, Mapall, non-root mount</span></a></li>
<li><a href="/guides/unraid/"><strong>Unraid</strong><span>NFS enable, rules, and the nobody:users ownership gotcha</span></a></li>
<li><a href="/guides/ugreen/"><strong>UGREEN (UGOS)</strong><span>Shared-folder NFS rules</span></a></li>
<li><a href="/guides/pi/"><strong>Linux / Raspberry Pi</strong><span>nfs-kernel-server and /etc/exports from scratch</span></a></li>
</ul>

Background that applies to all of them: [exports, the insecure option, and ports](/help/exports/) and [user IDs, groups and squash](/help/identity/).
