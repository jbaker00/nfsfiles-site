---
title: "The server is still starting up"
kind: nfs_grace
summary: "The NFSv4 server just restarted and is in its grace period (typically 90 seconds) while old clients reclaim their state. Wait a minute and retry."
description: "NFS Files error nfs_grace: The NFSv4 server just restarted and is in its grace period (typically 90 seconds) while old clients reclaim their state. Wait a minute and retry."
---

## What this means

NFSv4 status 10013, *GRACE*. After a restart, an NFSv4 server refuses new operations for a grace period so clients that were mid-write can recover. NFS Files has nothing to recover, but it still has to wait.

## Fix

Wait 60–90 seconds and try again. On Linux the period is `/proc/fs/nfsd/nfsv4gracetime` (default 90 s); on a NAS it isn't adjustable. If the server *always* reports grace, its NFS service is crash-looping — check the NAS log.
