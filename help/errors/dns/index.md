---
title: "Couldn't find a server with that name"
kind: dns
summary: "The name you typed didn't resolve to an address. `.local` names only work on the same network segment, and short names like `nas` usually don't work on iOS at all."
description: "NFS Files error dns: The name you typed didn't resolve to an address. `.local` names only work on the same network segment, and short names like `nas` usually don't work on iOS at all."
---

## What this means

Before NFS Files can connect it has to turn the name into an IP address. That lookup failed.

## The usual reasons

- **A `.local` name across VLANs or Wi-Fi bands.** `mynas.local` is a Bonjour (mDNS) name. It resolves only on the same broadcast domain — a NAS on a different VLAN, a wired NAS with Wi-Fi client isolation on, or a mesh network with mDNS reflection off will not answer.
- **A bare short name.** `nas`, `synology`, `truenas` — these depend on a DNS search domain that iOS and iPadOS generally don't apply. Use `nas.local`, the full name your router gives it (`nas.lan`, `nas.home.arpa`), or the IP.
- **A typo.**
- **Pi-hole / custom DNS** that doesn't know the name.

## The reliable fix

Use the IP address. Find it in your router's client list, on the NAS's own status page, or with **Scan My Network** in NFS Files, which sweeps your subnet and shows what's answering. Give the NAS a fixed IP (DHCP reservation on the router) so it doesn't change.
