---
title: "Storage quota exceeded"
kind: nfs_dquot
summary: "The user you present (or the user the export squashes you to) has hit their quota on the NAS."
description: "NFS Files error nfs_dquot: The user you present (or the user the export squashes you to) has hit their quota on the NAS."
---

## What this means

NFS status 69, *EDQUOT*. There's free space on the volume, but the *user* the write is charged to has reached their quota.

## Who gets charged

Whatever user the server maps you to — the UID you present, or with `all_squash` the anonymous user (`anonuid`). Check **Inspect Server** to see which.

## Raise or remove it

- **Synology:** Control Panel → User & Group → the user → Quota; or Shared Folder → the folder → Edit → *Advanced* → shared-folder quota.
- **QNAP:** Control Panel → Privilege → Quota.
- **TrueNAS:** the dataset's *Quota / Refquota*, and per-user quotas under the dataset's *User Quotas*.
- **Linux:** `quota -u username` and `edquota`.
