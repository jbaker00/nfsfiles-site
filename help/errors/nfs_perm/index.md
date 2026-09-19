---
title: "Operation not permitted"
kind: nfs_perm
summary: "The server allows you into the folder but refused this particular change. Almost always: changing an owner or group needs root, and the export squashes root."
description: "NFS Files error nfs_perm: The server allows you into the folder but refused this particular change. Almost always: changing an owner or group needs root, and the export squashes root."
---

## What this means

NFS status 1, *EPERM*: not *access denied* to the folder, but *this operation* isn't permitted for who you are. It's distinct from [access denied](/help/errors/nfs_access/).

## When you'll see it

- **Changing owner or group** in the permission editor. On every Unix server, only root can give a file to another user, and nearly every export maps root to nobody (`root_squash`). Even presenting UID 0 doesn't help. Change ownership on the NAS itself (SSH `sudo chown`, or the NAS's file manager).
- **Changing permissions on a file you don't own.** Only the owner (or root) can `chmod`. Check *Inspect Server* → "Export owned by" against "You present".
- **Setting timestamps** or other attributes on read-only or immutable files.

## What helps

Match the UID/GID you present to the file's owner (the permission editor shows the current owner), or do the change on the server side. See [User IDs and squash](/help/identity/).
