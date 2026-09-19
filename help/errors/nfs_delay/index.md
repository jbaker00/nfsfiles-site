---
title: "The server asked to retry in a moment"
kind: nfs_delay
summary: "The server is busy or the item is temporarily unavailable (a spun-down disk, a snapshot in progress). Wait a few seconds and try again."
description: "NFS Files error nfs_delay: The server is busy or the item is temporarily unavailable (a spun-down disk, a snapshot in progress). Wait a few seconds and try again."
---

## What this means

Status 10008, *DELAY* (called *JUKEBOX* in NFSv3, from the days of tape libraries). The request is valid; the server can't serve it right now.

## Usually

- **A spun-down disk** waking up. Give it 10–20 seconds.
- **A snapshot or scrub** running on that dataset.
- **Hierarchical storage** — a file archived to slower tiers (some enterprise NAS features).

Just try again.
