---
title: "UGREEN NFS setup (UGOS)"
kicker: Setup guide
summary: "Enable NFS for the shared folder, add a rule covering your subnet, and allow non-privileged ports. Mirrors Synology closely enough that the Synology page is your backup."
description: "How to set up NFS on a UGREEN NAS (UGOS) for NFS Files: shared-folder NFS rules, client access, non-privileged ports."
---

UGREEN's UGOS borrows its NFS layout from Synology closely enough that, if a screen here has moved in a newer UGOS version, the [Synology guide](/guides/synology/) is a good backup — the option names are nearly the same.

## 1. Enable NFS on the shared folder

Control Panel → Shared Folder → select the folder → **NFS** (or Edit → NFS Permissions) → enable NFS for the folder and add a rule:

| Field | Set it to | Why |
|---|---|---|
| Client | your subnet, e.g. `192.168.1.0/24` | `*` works; a subnet is safer. Wrong scope gives [the server refused this device](/help/errors/mount_access_denied/). |
| Privilege | **Read/Write** | Read-only gives [the share is read-only](/help/errors/nfs_rofs/). |
| Squash | **Map all users** to the folder's owner | Then the UID in the app doesn't matter and [access denied](/help/errors/nfs_access/) goes away. |
| Non-privileged ports | **allowed** | Without this, iPhone/iPad/Mac apps are refused before anything else is checked. |

## 2. What to type in NFS Files

- **Host:** the NAS's IP (reserve it in the router's DHCP).
- **Export path:** `/volume1/media` (volume plus folder). **Find Shared Folders** lists the exports — pick from there.
- **Advanced:** defaults.

## 3. Check your work

**Inspect Server** on the server card: green Read/Write badges mean done.

*I don't own a UGREEN — these steps are from UGOS documentation and the app's own test notes. If a screen has moved, email a screenshot to [jbaker00@mail.com](mailto:jbaker00@mail.com?subject=UGREEN%20guide%20correction) and I'll fix this page the same day.*
