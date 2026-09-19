---
title: "The server refused the connection"
kind: refused
summary: "A machine is at that address, but nothing is listening on the port. The NFS service is probably switched off, or the app is pointed at the wrong port."
description: "NFS Files error refused: A machine is at that address, but nothing is listening on the port. The NFS service is probably switched off, or the app is pointed at the wrong port."
---

## What this means

The server answered — with a TCP reset. That's what an operating system says when nothing is listening on a port. So the address is right; the service isn't there.

## If you're using the normal (portmapper) mode

The app first asks the **portmapper on port 111**. A refusal here means `rpcbind` isn't running. Two very different explanations:

1. **NFS is switched off on the NAS.** Every NAS ships with NFS disabled.
   - **Synology:** Control Panel → File Services → NFS → *Enable NFS service*.
   - **QNAP:** Control Panel → Network & File Services → Win/Mac/NFS/WebDAV → NFS Service → enable.
   - **TrueNAS:** System → Services → NFS → running (and *Start automatically*).
   - **Unraid:** Settings → NFS → *Enable NFS: Yes*.
   - **Linux / Raspberry Pi:** `sudo apt install nfs-kernel-server` and `sudo systemctl enable --now nfs-server`.
2. **The server is NFSv4-only and doesn't run a portmapper.** Some servers (TrueNAS with NFSv3 disabled, hardened Linux boxes, some Docker images) only speak NFSv4 on port 2049 and never start `rpcbind`. In NFS Files, open the server's Advanced settings, set **NFS Version → NFSv4**, turn on **Custom Port** and enter **2049**. The app then skips the portmapper entirely.

## If you're using Custom Port

Then the port you typed is closed. Check the server's configuration for the port it actually uses. Userspace servers commonly use 2049 or a high port like 20490; check their log line on startup.

## A firewall can also "refuse"

Most firewalls silently drop (which gives a [timeout](/help/errors/timeout/)), but some are configured to reject, which looks like this. If the NAS firewall is on, add a rule allowing 111 and 2049 (and mountd) from your subnet.
