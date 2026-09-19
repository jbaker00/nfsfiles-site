---
title: "That item is a folder"
kind: nfs_isdir
summary: "A file operation was attempted on a folder. Refresh — the item may have changed type on the server since it was listed."
description: "NFS Files error nfs_isdir: A file operation was attempted on a folder. Refresh — the item may have changed type on the server since it was listed."
---

## What this means

NFS status 21, *EISDIR*. The name refers to a folder, and the operation (download, overwrite, delete-as-file) only works on files.

## Usually

The listing was stale: a file was deleted and a folder created with the same name, or a symbolic link now points at a folder. Pull to refresh and try again. If it persists for one specific item, look at it on the server itself.
