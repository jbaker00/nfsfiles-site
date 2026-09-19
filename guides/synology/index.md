---
title: "Synology NFS setup (DSM 7)"
kicker: Setup guide
summary: "Enable the NFS service, add a per-share rule with non-privileged ports, let your subnet in, and squash to one user. Five minutes."
description: "How to set up NFS on a Synology NAS (DSM 7) for NFS Files: enable NFS, NFS permissions, non-privileged ports, squash."
---

## 1. Turn on NFS

Control Panel → File Services → **NFS** tab → tick **Enable NFS service**. Leave the NFSv4 options as they are — NFS Files speaks both versions, and DSM serves both at once. Note the port fields if you ever need them through a firewall (default: NFS port 2049, MOUNT port 892 — Synology pins MOUNT, which is convenient).

## 2. Add an NFS rule to the shared folder

Control Panel → Shared Folder → select the folder → **Edit** → **NFS Permissions** tab → **Create**:

| Field | Set it to | Why |
|---|---|---|
| Hostname or IP | your subnet, e.g. `192.168.1.0/24` | `*` works but lets any network the NAS can see mount it; a subnet is safer. Find your device's IP in its Wi-Fi settings to confirm the first three numbers. |
| Privilege | **Read/Write** | Read-only gives [the share is read-only](/help/errors/nfs_rofs/) on every write. |
| Squash | **Map all users to admin** (or to guest for a read-only folder) | Then the UID in the app doesn't matter and [access denied](/help/errors/nfs_access/) goes away. |
| Security | **sys** | `krb5`-only rules give [rejected credentials](/help/errors/auth_rejected/). |
| ☑ Allow connections from non-privileged ports | **ticked** | Without this, iPhone/iPad/Mac apps get [the server refused this device](/help/errors/mount_access_denied/). |
| ☑ Allow users to access mounted subfolders | **ticked** if you connect to a subfolder | Otherwise subfolder mounts fail with [that folder isn't shared](/help/errors/export_not_found/). |

Save, then Save again on the folder. DSM applies it immediately — no service restart needed.

## 3. What to type in NFS Files

- **Host:** the NAS's IP (DHCP-reserve it on the router so it doesn't move). `.local` names work on the same network.
- **Export path:** `/volume1/photos` — the *volume* plus the folder, not just `/photos`. Tap **Find Shared Folders** and pick from the list instead of typing.
- **Advanced:** leave everything default. UID/GID are irrelevant while Squash maps everyone.

## 4. Check your work

Tap **Inspect Server** on the server card: green Read/Write badges mean you're done. If Write is red, re-read the Squash and Privilege rows above.
