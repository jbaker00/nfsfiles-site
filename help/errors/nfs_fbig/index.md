---
title: "The file is too large for this server"
kind: nfs_fbig
summary: "The server can't hold a file this size — usually a 4 GB limit on an exFAT/FAT32 volume (USB drives), or a per-file quota."
description: "NFS Files error nfs_fbig: The server can't hold a file this size — usually a 4 GB limit on an exFAT/FAT32 volume (USB drives), or a per-file quota."
---

## What this means

NFS status 27, *EFBIG*. The write would exceed the maximum file size the filesystem allows.

## Causes

- **FAT32** (4 GB max) or **exFAT** volumes on USB drives attached to the NAS. Reformat the drive as ext4, btrfs or APFS-on-Mac, or copy to the NAS's main volume.
- **A file-size limit** in a user quota or a userspace server's configuration.
- Very old NFSv2-era servers with 2 GB limits — NFS Files doesn't support those anyway.
