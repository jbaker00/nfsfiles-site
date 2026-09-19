---
title: "Linux / Raspberry Pi NFS setup"
kicker: Setup guide
summary: "Install nfs-kernel-server, write one /etc/exports line with insecure and all_squash, and apply with exportfs. The same line works on a Pi, a home server, or a VM."
description: "How to set up an NFS export on Linux or Raspberry Pi for NFS Files: install, /etc/exports line, insecure, all_squash, exportfs, firewall."
---

## 1. Install and start

```sh
sudo apt install nfs-kernel-server
sudo systemctl enable --now nfs-server
```

(`nfs-utils` on Fedora/Arch; OpenMediaVault does all of this under Services → NFS instead.)

## 2. Write the export

One line in `/etc/exports` — folder, who may connect, and options:

```
/srv/nfs/media  192.168.1.0/24(rw,sync,insecure,no_subtree_check,all_squash,anonuid=1000,anongid=1000)
```

| Part | Why |
|---|---|
| `192.168.1.0/24` | Only your subnet may mount. Wrong scope gives [the server refused this device](/help/errors/mount_access_denied/). |
| `insecure` | **Required for iPhone/iPad/Mac apps** — they can't use privileged ports. The single most-missed option. |
| `all_squash,anonuid=1000,anongid=1000` | Every client acts as UID 1000 (usually the first user — check with `id`). Then the UID in the app is irrelevant and [access denied](/help/errors/nfs_access/) goes away. Make sure that user owns the folder: `sudo chown -R 1000:1000 /srv/nfs/media`. |
| `no_subtree_check` | Avoids spurious refusals on subfolder mounts. |
| `sync` | Safer writes; the default on modern nfsd. |

Apply it: `sudo exportfs -ra`. Verify: `exportfs -v` and `rpcinfo -p` (you should see `nfs` v3/v4 and `mountd`).

Full background on what each option means: [exports, the insecure option, and ports](/help/exports/).

## 3. Open the firewall (if one runs)

```sh
sudo ufw allow from 192.168.1.0/24 to any port nfs
```

That covers 111 and 2049 on UFW. NFSv3's `mountd` uses a random port unless pinned — either pin it in `/etc/nfs.conf` (`[mountd] port=20048`, then open that too) or use **NFSv4** in the app, which needs 2049 only.

## 4. What to type in NFS Files

- **Host:** the Pi/server IP (DHCP-reserve it on the router).
- **Export path:** exactly what's in `/etc/exports`, e.g. `/srv/nfs/media`. **Find Shared Folders** lists it.
- **Advanced:** defaults. With `all_squash`, UID/GID don't matter.

## NFSv4 note

If you export with `fsid=0` (a pseudo-root), the v4 path differs from the v3 path — `/srv/nfs/media` on v3 may be `/media` on v4. If connecting on v4 gives [that folder isn't shared](/help/errors/export_not_found/), try the shorter path or set NFS Version to v3.
