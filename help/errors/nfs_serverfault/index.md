---
title: "The server hit an internal error"
kind: nfs_serverfault
summary: "The NFS server itself failed while handling the request. Usually transient; if it repeats, the NAS's own log says why."
description: "NFS Files error nfs_serverfault: The NFS server itself failed while handling the request. Usually transient; if it repeats, the NAS's own log says why."
---

## What this means

Status 10006, *SERVERFAULT*. Not a permissions or network problem — the server's NFS daemon encountered an error it couldn't classify.

## What to do

1. **Retry.** Often it's a momentary condition (a background scrub, a snapshot being taken).
2. **Check the NAS log** — Synology Log Center, QNAP System Logs, TrueNAS Alerts, `journalctl -u nfs-server` on Linux.
3. **Storage** — a dataset that's locked, unmounted or degraded produces this on some servers rather than an I/O error.
