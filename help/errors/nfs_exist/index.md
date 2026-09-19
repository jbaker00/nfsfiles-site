---
title: "An item with that name already exists"
kind: nfs_exist
summary: "The server already has something with that name in this folder — possibly one you can't see because it differs only by case, or is a hidden file."
description: "NFS Files error nfs_exist: The server already has something with that name in this folder — possibly one you can't see because it differs only by case, or is a hidden file."
---

## What this means

NFS status 17, *EEXIST*. You tried to create, rename or move something to a name that's taken.

## Check

- **Refresh the folder.** Another device may have created it since you loaded the list.
- **Hidden files.** NFS Files shows dotfiles (`.DS_Store`, `._name` AppleDouble files) so you can see them, but Files.app and the Finder hide them — the conflicting item may be one of those.
- **Case.** The server is case-sensitive, but if it's a share on a case-insensitive volume (some Synology btrfs shares configured for Windows, macOS APFS exports), `Photo.jpg` and `photo.jpg` collide.

Pick a different name.
