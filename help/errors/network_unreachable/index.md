---
title: "No network for that address"
kind: network_unreachable
summary: "Your device has no usable network interface for that address — Wi-Fi is off, you're on cellular only, or (on a Mac) the Local Network permission is denied."
description: "NFS Files error network_unreachable: Your device has no usable network interface for that address — Wi-Fi is off, you're on cellular only, or (on a Mac) the Local Network permission is denied."
---

## What this means

The operating system said *network unreachable*: there's no interface that could carry a packet to that address at all.

## Check

- **Wi-Fi is on** and connected to your home network. Cellular can't reach a NAS on your LAN (unless you've set up a VPN to home — in which case check that the VPN is connected).
- **Airplane mode** is off.
- **On a Mac with macOS 15 or later:** a denied **Local Network** permission produces this error. System Settings → Privacy & Security → Local Network → turn on NFS Files. [Details](/help/local-network/).
- **IPv6 address?** If you typed an IPv6 literal and your Wi-Fi has no IPv6, use the IPv4 address instead.
- **Ethernet adapter on iPad or Mac:** make sure it has an address (Settings → Ethernet), not just a link.
