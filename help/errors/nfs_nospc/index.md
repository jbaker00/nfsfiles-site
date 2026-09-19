---
title: "The server is out of space"
kind: nfs_nospc
summary: "The volume the share lives on is full. Free some space on the NAS, or check whether snapshots or a recycle bin are holding it."
description: "NFS Files error nfs_nospc: The volume the share lives on is full. Free some space on the NAS, or check whether snapshots or a recycle bin are holding it."
---

## What this means

NFS status 28, *ENOSPC*. The server tried to allocate space and there was none.

## Where the space went

- **Recycle bins** — Synology and QNAP keep deleted files in `#recycle` / `@Recycle`; empty them.
- **Snapshots** — Synology Snapshot Replication, TrueNAS ZFS snapshots and QNAP snapshots all hold space until they're deleted.
- **Another share** on the same volume filled it up. The free-space figure NFS Files shows on the server card is for the volume, not the share.
- **Inodes** — a volume with millions of tiny files can be "full" with space left. `df -i` on Linux.
