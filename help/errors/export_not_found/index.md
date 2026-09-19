---
title: "That folder isn't shared"
kind: export_not_found
summary: "The server has NFS running but doesn't export the path you typed. The path has to match the server's export list exactly — and every NAS spells it differently."
description: "NFS Files error export_not_found: The server has NFS running but doesn't export the path you typed. The path has to match the server's export list exactly — and every NAS spells it differently."
---

## What this means

The MOUNT request came back *no such folder*. The server is fine; the **export path** doesn't match anything it shares.

## The fix: ask the server

In the add-server form, tap **Find Shared Folders**. The app asks the server for its export list and lets you pick from it. That removes the guesswork entirely.

## Why paths trip people up

Each NAS uses its own layout, and the export path is the server's *internal* path, not the share name:

<div id="nas-synology"></div>

| NAS | Export path looks like |
|---|---|
| Synology | `/volume1/photos` (not `/photos`) |
| QNAP | `/share/CACHEDEV1_DATA/Public` (QNAP also accepts `/Public` on many models) |
| Unraid | `/mnt/user/media` |
| TrueNAS | `/mnt/tank/media` (pool, then dataset) |
| UGREEN | `/volume1/media` |
| Linux / Raspberry Pi | whatever is in `/etc/exports`, e.g. `/srv/nfs/media` |
| macOS | whatever is in `/etc/exports`, e.g. `/Users/Shared/media` |

Case matters. Trailing slashes don't.

## NFSv4 and subfolders

With **NFSv4**, some Linux servers export a *pseudo-root* (`fsid=0`): the path you mount is relative to that root, so `/` or `/media` may be right where NFSv3 needed `/srv/nfs/media`. If Find Shared Folders shows a path that doesn't work on v4, try the shorter form — or set NFS Version to NFSv3.

Synology only lets you mount a *subfolder* of a share if the NFS rule has **Allow users to access mounted subfolders** ticked.
