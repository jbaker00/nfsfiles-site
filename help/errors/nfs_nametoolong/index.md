---
title: "The name is too long"
kind: nfs_nametoolong
summary: "Server filesystems cap each name at 255 bytes — and accented or non-Latin characters take two to four bytes each."
description: "NFS Files error nfs_nametoolong: Server filesystems cap each name at 255 bytes — and accented or non-Latin characters take two to four bytes each."
---

## What this means

NFS status 63, *ENAMETOOLONG*. The file or folder name exceeds the server's limit.

## The limit is in bytes, not characters

Linux filesystems allow 255 **bytes** per name. In UTF-8, ASCII letters are one byte, accented Latin letters two, and most CJK characters three — so a 100-character Japanese filename is already 300 bytes. Some NAS models with encrypted shares (Synology eCryptfs) drop the limit to about **143 characters**.

Shorten the name.
