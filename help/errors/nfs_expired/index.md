---
title: "The connection to the server expired"
kind: nfs_expired
summary: "The NFSv4 lease timed out — usually after the app was in the background a while or the NAS restarted. Reconnect from the server list."
description: "NFS Files error nfs_expired: The NFSv4 lease timed out — usually after the app was in the background a while or the NAS restarted. Reconnect from the server list."
---

## What this means

NFSv4 status 10011 / 10022 (*EXPIRED* / *STALE_CLIENTID*). NFSv4 servers give each client a lease that must be renewed. After a long pause — the app suspended in the background, the device asleep, the NAS restarted — the server forgets the client.

## Fix

Go back to the server list and reconnect. The app establishes a fresh client ID. Nothing on the server needs changing.
