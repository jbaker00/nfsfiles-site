---
title: "The server doesn't support something the app needs"
kind: unsupported
summary: "The server answered, but lacks an operation NFS Files relies on. Try pinning the other NFS version; if that doesn't help, email the message."
description: "NFS Files error unsupported: The server answered, but lacks an operation NFS Files relies on. Try pinning the other NFS version; if that doesn't help, email the message."
---

## What this means

NFS Files asked for an operation the server says it doesn't implement. Full servers (Linux `nfsd`, every major NAS) implement everything the app uses; the ones that don't are usually small userspace servers.

## Try

1. In the server's Advanced settings, set **NFS Version** explicitly — **NFSv3** if it was Auto or v4, **NFSv4** if it was v3. The two versions have different required operations.
2. If the server is a Docker image or a small Go/Rust/Python NFS server, check for an updated version; several gained missing operations recently.
3. Email the exact message from the alert (**Settings → Contact Support** fills it in). Knowing which operation and which server lets me either work around it or document it here.
