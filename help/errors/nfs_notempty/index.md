---
title: "The folder isn't empty"
kind: nfs_notempty
summary: "The server won't delete a folder that still has something in it — sometimes a hidden file you can't see in Files.app or the Finder."
description: "NFS Files error nfs_notempty: The server won't delete a folder that still has something in it — sometimes a hidden file you can't see in Files.app or the Finder."
---

## What this means

NFS status 66, *ENOTEMPTY*. Deleting a folder over NFS only works when it's empty.

## Check inside it in NFS Files

The app shows hidden files (`.DS_Store`, `._something` AppleDouble files, `@eaDir` on Synology, `.Trash` folders) that Files.app and the Finder hide. Delete those first, then the folder.

If you're deleting from the Finder or Files.app through the NFS Files location, the system asks the app to delete items one at a time; a folder whose contents failed to delete will show this. Open the folder in NFS Files to see what's left.
