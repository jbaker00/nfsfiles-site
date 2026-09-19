---
title: "NFS isn't registered on this server"
kind: program_unavailable
summary: "The portmapper answered but has no NFS or MOUNT service registered for the version the app asked for. NFS is probably enabled but not running, or the server is NFSv4-only."
description: "NFS Files error program_unavailable: The portmapper answered but has no NFS or MOUNT service registered for the version the app asked for. NFS is probably enabled but not running, or the server is NFSv4-only."
---

## What this means

The portmapper on port 111 is running — so the server is up and RPC works — but when NFS Files asked "where is NFS version 3 / MOUNT version 3?", the portmapper said *no such program*.

## Causes and fixes

1. **NFS service enabled but not started.** On Linux, `sudo systemctl status nfs-server` and `rpcinfo -p` on the server; on a NAS, toggle the NFS service off and on.
2. **NFSv4-only server.** NFSv4 doesn't use the MOUNT protocol, so a server with NFSv3 disabled registers no `mountd`. Set **NFS Version → NFSv4** in the app's Advanced settings.
   - **TrueNAS:** System → Services → NFS → Advanced → *Enabled Protocols*. If only NFSv4 is ticked, either tick NFSv3 as well or use NFSv4 in the app.
   - **Linux:** `/etc/nfs.conf` `[nfsd] vers3=n` means v3 is off.
3. **A stale portmapper.** After reconfiguring NFS, `rpcbind` can hold an out-of-date table. Restart the NFS service (or the NAS).

## See for yourself

**Inspect Server** on the server card shows the RPC table — the same output as `rpcinfo -p`. If `nfs` is there but `mountd` isn't, that's case 2.
