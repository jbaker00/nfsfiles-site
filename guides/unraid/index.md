---
title: "Unraid NFS setup"
kicker: Setup guide
summary: "Enable NFS, check the share's rule includes insecure, and make sure the files are owned by nobody:users. The ownership bit is the Unraid-specific gotcha."
description: "How to set up NFS on Unraid for NFS Files: enable NFS, share security settings, rules, and fixing nobody:users ownership."
---

## 1. Turn on NFS

Settings → **NFS** → **Enable NFS: Yes**. Unraid serves NFSv3 and v4 together by default.

## 2. Export the share

Shares → click the share → **NFS Security Settings**:

- **Export: Yes.**
- **Security:** Public (anyone on the allowed networks) or Secure/Private with your network listed.
- **Rule:** must start with your subnet or `*` and must include `insecure` (Unraid's default rule already does, e.g. `192.168.1.0/24(sec=sys,rw,insecure,anongid=100,anonuid=99,all_squash)`). If a customised rule lost `insecure`, iPhone/iPad/Mac apps get [the server refused this device](/help/errors/mount_access_denied/).
- The default rule squashes everyone to `nobody:users` (`anonuid=99,anongid=100`) — so the UID in the app is irrelevant, **provided the files are actually owned by `nobody:users`**.

## 3. The ownership gotcha

Unraid writes new share files as `nobody:users`, but files copied over SMB as a specific user, or moved in from a disk share, often aren't. Then you connect fine, list fine, and get [access denied](/help/errors/nfs_access/) on write.

Fix: Tools → **New Permissions** (Docker/VM tabs → run it against the share), or shell `chown -R nobody:users /mnt/user/media`. **Inspect Server** in the app shows "Export owned by" so you can confirm.

## 4. What to type in NFS Files

- **Host:** the Unraid IP (Settings → Network Settings → static, or DHCP-reserve it).
- **Export path:** `/mnt/user/media` — the share name under `/mnt/user/`, *not* `/mnt/disk1/...` (disk paths bypass the user-share layer). **Find Shared Folders** lists them.
