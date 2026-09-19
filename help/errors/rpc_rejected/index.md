---
title: "The server rejected the request at the RPC layer"
kind: rpc_rejected
summary: "The program version the app asked for isn't what the server offers. Usually a server that speaks only NFSv4 reached through the NFSv3 path, or Custom Port pointing at a different RPC service."
description: "NFS Files error rpc_rejected: The program version the app asked for isn't what the server offers. Usually a server that speaks only NFSv4 reached through the NFSv3 path, or Custom Port pointing at a different RPC service."
---

## What this means

The server answered, but said the RPC program or version doesn't match. NFS Files speaks **NFSv3** (with the separate MOUNT v3 protocol) and **NFSv4.0**. This error means the server doesn't offer the one the app tried.

## Most likely: a version mismatch

- **The server is NFSv4-only** (TrueNAS with NFSv3 disabled, many hardened Linux setups, some Docker images). With *NFS Version: Auto* the app tries v4 first, then v3 — if the v4 attempt failed for some *other* reason, the error you see is from the v3 attempt and can be misleading. Set **NFS Version → NFSv4** in the server's Advanced settings so you see the real v4 error.
- **The server is NFSv2-only.** Very old devices and some routers with USB storage. NFS Files doesn't support NFSv2; there's no fix short of a newer server.
- **NFSv4.1+ only.** A server configured to *require* 4.1 or 4.2 will reject 4.0. On Linux, `/etc/nfs.conf` `[nfsd] vers4.0=y` re-enables it; on TrueNAS, check the NFS service's protocol options.

## Custom Port pointing at the wrong RPC service

If **Custom Port** is on, the port must be the NFS server (and for v3, also the MOUNT server). Pointing it at the portmapper (111) or another RPC program gives this error.

## See what the server offers

**Inspect Server** on the server card shows the RPC table — every program and version registered on the server. Look for `nfs` versions 3 and 4 and `mountd` version 3.
