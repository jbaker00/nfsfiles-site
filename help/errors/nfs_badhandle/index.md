---
title: "The file handle is no longer valid"
kind: nfs_badhandle
summary: "An NFSv4 server rejected the handle the app holds. Same cure as a stale handle: reconnect from the server list."
description: "NFS Files error nfs_badhandle: An NFSv4 server rejected the handle the app holds. Same cure as a stale handle: reconnect from the server list."
---

## What this means

NFSv4 status 10001, *BADHANDLE*. The server considers the file handle malformed or from a different generation — typically after the NFS service restarted, the export was re-created, or the volume was remounted.

## Fix

Reconnect from the server list. If it recurs on one specific item, look at that item on the server; if it recurs after every NAS restart, the export needs a stable `fsid`. See [stale file handle](/help/errors/nfs_stale/).
