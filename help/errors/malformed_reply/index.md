---
title: "The server sent a reply the app couldn't understand"
kind: malformed_reply
summary: "Whatever is on that port isn't speaking NFS. Usually a Custom Port pointed at the wrong service, or a proxy in the way."
description: "NFS Files error malformed_reply: Whatever is on that port isn't speaking NFS. Usually a Custom Port pointed at the wrong service, or a proxy in the way."
---

## What this means

NFS Files got a response, but it didn't parse as an ONC RPC / NFS message. The most likely explanation: the port belongs to something else.

## Check

- **Custom Port on?** Make sure the port is the NFS/MOUNT port, not SMB (445), the web UI (5000/5001 on Synology, 8080 on QNAP), or SSH (22).
- **A proxy or load balancer** in the path is unlikely at home, but if this is a corporate network, ask whether NFS traffic is inspected.
- **A broken or very old userspace server.** Some NFS implementations in Docker images or embedded devices send non-standard replies. Try forcing **NFSv3** in the server's Advanced settings; if that doesn't help, check for an updated image.
- **Inspect Server** on the server card shows the server's RPC table — if that loads, the portmapper is fine and the problem is specific to NFS or MOUNT.
