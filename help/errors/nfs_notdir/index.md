---
title: "That item isn't a folder"
kind: nfs_notdir
summary: "The app tried to open or list something that's a file (or a link to a file), not a folder."
description: "NFS Files error nfs_notdir: The app tried to open or list something that's a file (or a link to a file), not a folder."
---

## What this means

NFS status 20, *ENOTDIR*. A path component that should be a folder is a file.

## Usually

- **The export path** points at a file. Use **Find Shared Folders** and pick a folder.
- **A symbolic link** on the server that points at a file (or a dangling one). NFS Files follows links where the server allows; a link to a file can't be opened as a folder. Fix or remove the link on the server.
