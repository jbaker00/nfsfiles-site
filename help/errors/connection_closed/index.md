---
title: "The server closed the connection"
kind: connection_closed
summary: "A machine answered, then hung up before finishing. Usually the NFS service is restarting, a TCP wrapper rule rejected you, or the NAS went to sleep mid-conversation."
description: "NFS Files error connection_closed: A machine answered, then hung up before finishing. Usually the NFS service is restarting, a TCP wrapper rule rejected you, or the NAS went to sleep mid-conversation."
---

## What this means

The TCP connection was established — so the address and port are right — but the server ended it without replying. That's different from a refusal (nothing listening) or a timeout (nothing answering).

## Common causes

- **The NFS service is restarting** on the NAS (after a settings change, an update, or a nightly task). Wait thirty seconds and try again.
- **TCP wrappers** — on Linux servers, `/etc/hosts.deny` with a line like `rpcbind: ALL` or `mountd: ALL` makes the server accept the connection and immediately close it. Add your subnet to `/etc/hosts.allow`, or remove the deny rule.
- **The NAS went to sleep** partway through. Disable HDD hibernation for testing, or turn on wake-on-LAN and wake it first.
- **A proxy or "smart" firewall** in the path is terminating idle connections. Rare on a home network, common on a corporate one.
- **A userspace NFS server** (Docker images, small Go/Rust servers) that crashed on the request. Check its log.

## What to try

Tap **Inspect Server** on the server card. If the RPC table loads but the export list doesn't, the problem is with `mountd`; if nothing loads, the whole RPC stack on the server is refusing you.
