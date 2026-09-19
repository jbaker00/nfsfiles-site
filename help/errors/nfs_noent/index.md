---
title: "No such file or folder"
kind: nfs_noent
summary: "The item isn't there any more — renamed, moved or deleted by someone else since the listing was loaded — or, on NFSv4, the export path doesn't exist under the server's pseudo-root."
description: "NFS Files error nfs_noent: The item isn't there any more — renamed, moved or deleted by someone else since the listing was loaded — or, on NFSv4, the export path doesn't exist under the server's pseudo-root."
---

## What this means

NFS status 2, *ENOENT*. The server was asked about a name that doesn't exist in that folder.

## Usually

Someone (or something — a sync job, a media server tidying up) changed the folder after NFS Files listed it. Pull to refresh, or go back and re-open the folder.

## On NFSv4, at connect time

If this happened while *connecting*, the export path doesn't exist under the NFSv4 pseudo-filesystem. Linux servers with `fsid=0` present a different root to NFSv4 clients than to NFSv3 ones — `/srv/nfs/media` on v3 may be `/media` on v4. Use **Find Shared Folders**, try the shorter path, or set **NFS Version → NFSv3**. Details on the [not shared](/help/errors/export_not_found/) page.

## Case sensitivity

NFS servers are case-sensitive. `Photos` and `photos` are different folders.
