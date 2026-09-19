---
title: "QNAP NFS setup (QTS / QuTS hero)"
kicker: Setup guide
summary: "Enable the NFS service, grant NFS host access to your subnet, and set the squash option. The export path is the odd part — read that bit."
description: "How to set up NFS on a QNAP NAS (QTS and QuTS hero) for NFS Files: NFS service, host access, squash, export paths."
---

## 1. Turn on NFS

Control Panel → Network & File Services → Win/Mac/NFS/WebDAV → **NFS Service** → tick **Enable NFS**. QNAP serves NFSv3 and v4 together; leave the versions alone.

## 2. Grant access to the shared folder

Control Panel → Privilege → Shared Folders → select the folder → **Edit Shared Folder Permission** → **NFS host access** (or: right-click the folder → NFS host access, depending on firmware):

- Add your subnet (e.g. `192.168.1.0/24`) — or a single device IP — and tick it.
- **Access right: read/write** (read-only gives [the share is read-only](/help/errors/nfs_rofs/)).
- **Squash option: all_squash**, with **Anonymous UID/GID** set to the user that owns the share's files. Then the UID in the app is irrelevant and [access denied](/help/errors/nfs_access/) goes away.
- QNAP's NFS server allows non-privileged ports by default — if you see [the server refused this device](/help/errors/mount_access_denied/) on a QNAP, suspect the host-access list first, not ports.

## 3. What to type in NFS Files

QNAP export paths are the fiddly bit. The real path is something like `/share/CACHEDEV1_DATA/Public` — tap **Find Shared Folders** in the app and pick from the list rather than guessing. (Many QNAP models also accept the short form `/Public`; if the long form fails, try the short one, and vice versa.)

**Host:** the NAS's IP. Reserve it in the router's DHCP so it doesn't drift.

## 4. Check your work

**Inspect Server** on the server card: green Read/Write badges mean you're done. Red Write with `all_squash` set means the anonymous UID doesn't own the folder's files — fix ownership in File Station (right-click → Properties) or match the anonymous UID to the owner.
