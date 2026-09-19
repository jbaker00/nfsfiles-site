---
title: "The share is read-only"
kind: nfs_rofs
summary: "The export is shared read-only, or the volume under it went read-only after an error."
description: "NFS Files error nfs_rofs: The export is shared read-only, or the volume under it went read-only after an error."
---

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
