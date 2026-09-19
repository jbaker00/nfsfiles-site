---
title: "The server refused to share that folder"
kind: mount_denied
summary: "The MOUNT request failed with an error other than access denied or not found — the path is a file, is too long, or the server hit an internal error."
description: "NFS Files error mount_denied: The MOUNT request failed with an error other than access denied or not found — the path is a file, is too long, or the server hit an internal error."
---

## What this means

The MOUNT service on the server answered with an unusual status. The alert names it: *not a folder*, *name too long*, *not supported*, or a server fault.

## Check

- **Is the path a folder?** An export path that points at a file returns *not a folder*. Use **Find Shared Folders** to pick from what the server actually exports.
- **Very long paths** — over 255 characters per component — are refused.
- **Server fault** means the server's `mountd` hit an internal error: a disk that isn't mounted, a dataset that's locked (encrypted TrueNAS datasets after a reboot), or a corrupt exports table. Check the NAS's storage page and its NFS log.
- **Not supported** from MOUNT is rare and usually means a minimal userspace server. Try **NFS Version → NFSv4** (no MOUNT protocol at all).
