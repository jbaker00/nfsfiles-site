---
title: "TrueNAS NFS setup (CORE and SCALE)"
kicker: Setup guide
summary: "Start the NFS service, create the share with the right Mapall and network settings, and tick Allow non-root mount. Covers the v3/v4 protocol choice."
description: "How to set up NFS on TrueNAS CORE and SCALE for NFS Files: NFS service, share options, Mapall, authorized networks, NFSv3 vs v4."
---

## 1. Start the NFS service

System → Services → **NFS** → toggle running, and tick **Start Automatically**. Click the edit (⛭) icon for the service settings:

- **Allow non-root mount: ticked.** This is TrueNAS's name for `insecure` — without it, iPhone/iPad/Mac apps get [the server refused this device](/help/errors/mount_access_denied/). It's global, not per share.
- **Enabled Protocols:** leave NFSv3 and NFSv4 both ticked. NFS Files tries v4 first and falls back to v3. If you've disabled v3, set **NFS Version → NFSv4** in the app instead.
- **Require Kerberos for NFSv4: off.** Kerberos-only exports give [rejected credentials](/help/errors/auth_rejected/); NFS Files doesn't do Kerberos.

## 2. Create the share

Sharing → Unix (NFS) Shares → Add. Path: the dataset (e.g. `/mnt/tank/media`).

- **Authorized Networks:** your subnet (`192.168.1.0/24`), or leave empty for everyone the NAS can see. Wrong scope here gives [the server refused this device](/help/errors/mount_access_denied/).
- **Read Only:** unticked (ticked gives [the share is read-only](/help/errors/nfs_rofs/)).
- Advanced → **Mapall User / Mapall Group:** set both to the user that owns the dataset. This is TrueNAS's `all_squash` — then the UID in the app is irrelevant and [access denied](/help/errors/nfs_access/) goes away. (Security dropdown: `sys`.)
- **Enable NFSv4 ACLs** only if you actually use NFSv4 ACLs; for a home share, plain Unix permissions are simpler.

## 3. What to type in NFS Files

- **Host:** the TrueNAS IP (set it static under Network → Interfaces, or DHCP-reserve it).
- **Export path:** the full dataset path, e.g. `/mnt/tank/media`. **Find Shared Folders** lists it — pick from there.
- **Advanced:** defaults. With Mapall set, UID/GID don't matter.

## 4. Check your work

**Inspect Server**: green Read/Write badges mean done. If Write is red despite Mapall, the Mapall user doesn't own the dataset — fix with Storage → the dataset → Edit Permissions, or shell `chown -R user:group`.
