---
title: "Stale file handle"
kind: nfs_stale
summary: "The server no longer recognises the handle the app holds for this item — it was moved or deleted server-side, or the export was restarted. Reconnect from the server list."
description: "NFS Files error nfs_stale: The server no longer recognises the handle the app holds for this item — it was moved or deleted server-side, or the export was restarted. Reconnect from the server list."
---

## What this means

NFS status 70, *ESTALE*. NFS identifies files by an opaque *handle* rather than a path. The server says the handle the app holds doesn't point at anything any more.

## Causes

- **The item was deleted or moved** on the server (by another device, a script, a media manager) while NFS Files still had it open.
- **The export was re-exported** — the NAS rebooted, the NFS service restarted, or the volume was remounted — and the server's handle numbering changed. Common with **USB drives** that were unplugged and re-plugged.
- **The export options changed** (`fsid=`, or the share was recreated).

## Fix

Go back to the server list and reconnect; the app fetches fresh handles. If it keeps happening after every server restart on Linux, add a fixed `fsid=<number>` to the export in `/etc/exports` so handles survive reboots.
