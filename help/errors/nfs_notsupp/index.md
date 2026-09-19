---
title: "The operation isn't supported by this server"
kind: nfs_notsupp
summary: "The server doesn't implement this NFS operation. Small userspace servers skip things like SETATTR (used by the permission editor); do that action on the server instead."
description: "NFS Files error nfs_notsupp: The server doesn't implement this NFS operation. Small userspace servers skip things like SETATTR (used by the permission editor); do that action on the server instead."
---

## What this means

NFS status 10004, *NOTSUPP*. The server understood the request and declined to implement it. Full servers (Linux `nfsd`, every major NAS) support everything NFS Files uses; small userspace ones don't.

## Where you'll see it

- **Editing permissions** on a server without SETATTR. Some Go/Rust/Python NFS servers, some Docker "nfs-server" images, and a few embedded devices. Change permissions on the server itself.
- **Renaming across folders** on servers that don't implement RENAME between directories.
- **NFSv4 servers** that omit optional operations. Try **NFS Version → NFSv3** in the app.

## Which server is it?

If it's a NAS you'd expect to work, email me the model and the operation named in the alert.
