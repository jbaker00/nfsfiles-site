---
title: "The server reported an I/O error"
kind: nfs_io
summary: "The server tried to read or write the disk and failed. That's a storage problem on the NAS, not a network one — check its storage health."
description: "NFS Files error nfs_io: The server tried to read or write the disk and failed. That's a storage problem on the NAS, not a network one — check its storage health."
---

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
