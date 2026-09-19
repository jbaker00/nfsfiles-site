---
title: "Access denied by the server"
kind: nfs_access
summary: "You're connected, but the server won't let the user you present read or write here. NFS has no passwords — the numeric User ID is your identity, and the export may squash it."
description: "NFS Files error nfs_access: You're connected, but the server won't let the user you present read or write here. NFS has no passwords — the numeric User ID is your identity, and the export may squash it."
---

## What this means

NFS status 13, *EACCES*. The server checked the numeric **User ID / Group ID** the app presents against the folder's owner, group and permissions — and said no.

## Why NFS works this way

NFS (the `sys` flavour every home NAS uses) has no login. The client simply *states* a UID and GID, and the server takes it at face value — then applies normal Unix permissions, possibly after **squashing** (remapping) that identity:

- `root_squash` — UID 0 becomes `nobody`. On by default everywhere.
- `all_squash` — *every* UID becomes one designated user (`anonuid`/`anongid`). Then the UID you present doesn't matter at all; the folder has to be accessible to that designated user.
- No squash — the UID you present is used as-is.

## Find out what the server sees

Tap **Inspect Server** on the server card. It shows **You present** (your UID/GID), **Export owned by** (the folder's owner), the folder's permission bits, and whether **Read** and **Write** actually work — plus a plain-language read on which squash mode you're hitting. Free, no Pro needed.

## Fix it

**Option A — present the right UID.** On the server, run `id yourname` to find your numeric UID and GID (the first user on Synology is usually `1026`, on most Linux boxes `1000`). Put those in the server's **Advanced → User ID / Group ID** in NFS Files.

<div id="nas-synology"></div>

**Option B — squash everyone to one user (simplest).** Make the export map all clients to a user that owns the folder:

- **Synology:** NFS rule → **Squash: Map all users to admin** (or to guest for read-only folders). Then the UID in the app is irrelevant.
- **QNAP:** NFS host access → *Squash option: all_squash*, *Anonymous UID/GID* set to the share's owner.
- **TrueNAS:** share → Advanced → **Mapall User / Mapall Group** set to the owner.
- **Unraid:** the default rule already does this (`all_squash,anonuid=99,anongid=100` = `nobody:users`); make sure the share's files are owned by `nobody:users` (Tools → New Permissions).
- **Linux:** `all_squash,anonuid=1000,anongid=1000` in `/etc/exports`.

**Option C — fix the folder's permissions** on the server so your UID (or group) has access: `chmod`, `chown`, or the NAS's file manager.

## Group-owned folders

NFS Files currently sends one group ID. If access depends on a *secondary* group membership on the server, use Option B or make the folder readable by the primary group. (Extra group IDs are on the roadmap.)

Full background: [User IDs and squash](/help/identity/).
