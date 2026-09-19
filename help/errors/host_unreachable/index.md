---
title: "No route to the server"
kind: host_unreachable
summary: "Your device couldn't find a path to that address. On iPhone, iPad and Mac the most common cause is the Local Network permission being off."
description: "NFS Files error host_unreachable: Your device couldn't find a path to that address. On iPhone, iPad and Mac the most common cause is the Local Network permission being off."
---

## What this means

The operating system reported *host unreachable*. It didn't even get as far as sending the request — it couldn't work out how to reach that address. On a local network that almost always means one of three things.

## 1. Local Network permission (most likely)

iOS, iPadOS and macOS 15+ ask, the first time an app talks to your LAN, whether to allow it. If that was answered *Don't Allow* — or dismissed — every local connection fails with exactly this error, and the app is never asked again.

- **iPhone / iPad:** Settings → Privacy & Security → **Local Network** → turn on **NFS Files**.
- **Mac (macOS 15 Sequoia and later):** System Settings → Privacy & Security → **Local Network** → turn on **NFS Files**.

Full walkthrough with screenshots: [Local Network permission](/help/local-network/).

## 2. Different subnet

Your device is on `192.168.1.x` but the NAS is on `192.168.2.x` (a second router, a guest network, a VLAN) with no route between them. Check the IP your device has (Settings → Wi-Fi → ⓘ) against the NAS's IP. Same first three numbers, or a router that routes between them, is required.

## 3. The NAS is off, or the IP is wrong

On a LAN, an address that no device answers ARP for can produce this error rather than a timeout. Check the dot on the server card and try **Scan My Network**.
