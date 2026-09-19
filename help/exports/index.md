---
title: "Exports, the insecure option, and ports"
kicker: Help
summary: "An export is a folder the server shares, plus a rule about who may mount it and how. Three settings in that rule account for nearly every failed first connection."
description: "What an NFS export is, why the insecure option matters for iPhone and Mac apps, and which ports NFS uses."
---

## What an export is

On the server, an export is one line: a folder, and the rule for it.

```
/srv/nfs/media  192.168.1.0/24(rw,sync,insecure,no_subtree_check,all_squash,anonuid=1000,anongid=1000)
```

Every NAS UI is a front end for exactly this. The parts that matter:

| Part | Meaning | If you get it wrong |
|---|---|---|
| `/srv/nfs/media` | The folder — the **export path** you type in NFS Files. | [That folder isn't shared](/help/errors/export_not_found/) |
| `192.168.1.0/24` | Who may connect — a host, a subnet, or `*`. | [The server refused this device](/help/errors/mount_access_denied/) |
| `rw` / `ro` | Read-write or read-only. | [The share is read-only](/help/errors/nfs_rofs/) |
| `insecure` | Accept connections from ports above 1024. **Required for iPhone, iPad and Mac apps.** | [The server refused this device](/help/errors/mount_access_denied/) |
| `all_squash,anonuid=…` | Map every client to one user. Recommended. | [Access denied](/help/errors/nfs_access/) |
| `no_subtree_check` | Skip a check that can spuriously refuse subfolder mounts. Recommended. | subfolder mounts refused |
| `sync` | Commit writes before acknowledging. Safer; the default on modern servers. | — |

## Why `insecure` matters so much

Old NFS servers only trusted clients connecting from **ports below 1024**, because on a 1980s Unix machine only root could open those, and so a low source port "proved" the request came from the OS rather than a user program. On iPhone, iPad and sandboxed Mac apps, *no* app can open a port below 1024. Without `insecure`, the server refuses before it even looks at the UID.

The name is unfortunate: the option doesn't make anything less secure on a network where all clients are personal devices anyway — the "security" it removes never applied to them.

Each NAS has its own name for it — see the [setup guides](/guides/).

## Ports

NFS is really three services:

| Service | Port | Used by |
|---|---|---|
| Portmapper (`rpcbind`) | **111** | NFSv3 — to find the other two |
| NFS (`nfsd`) | **2049** | NFSv3 and NFSv4 |
| MOUNT (`mountd`) | random by default; often pinned to **892** (Synology), **618** (TrueNAS), **20048** (Linux with `nfs.conf`) | NFSv3 only |

Two practical consequences:

- **Firewalls between you and the NAS** need 111, 2049 and the MOUNT port open. Because MOUNT's port is random unless pinned, NFSv3 through a firewall is fiddly. **NFSv4 only needs 2049** — choose it in the app's Advanced settings when a firewall is in the way.
- **Custom Port mode** in NFS Files is for servers that don't run a portmapper at all — userspace servers that put MOUNT and NFS on one port, or NFSv4-only servers on 2049. For a normal NAS, leave it off.

## NFSv3 or NFSv4?

NFS Files speaks both. **Auto** tries v4 first and falls back to v3 — the right default. Pin a version when a server misbehaves on one of them, or when a firewall makes v3 impractical. Differences that matter to you:

- v4 uses one port and no MOUNT protocol.
- v4 reports file owners as *names* (or numeric strings), v3 as numbers — visible in Inspect Server.
- v4 export paths on Linux can be relative to a pseudo-root (`fsid=0`) and differ from the v3 path.
- NFS Files supports **v4.0**; servers that require 4.1+ need v3 or a settings change.
