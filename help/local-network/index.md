---
title: "The Local Network permission"
kicker: Help
summary: "iPhone, iPad and (since macOS 15) Mac ask once whether an app may talk to devices on your network. If NFS Files was told no, every connection to your NAS fails — and the system never asks again."
description: "How to turn on the Local Network permission for NFS Files on iPhone, iPad and Mac, and how to tell that's the problem."
---

## How to tell this is the problem

- Connections fail with **"No route to the server"** (`host_unreachable`), **"No network for that address"** (`network_unreachable`) or sometimes a plain **timeout** — even though the NAS is on and other apps or devices reach it fine.
- The dots on the server cards are grey for every server.
- **Scan My Network** finds nothing at all, and **Found on Your Network** stays empty.

## Turn it on

<div data-platform="ios" markdown="1">

### iPhone and iPad

1. Open **Settings** (the system app, not NFS Files' own settings).
2. Scroll to **Privacy & Security** → **Local Network**.
3. Find **NFS Files** and turn it **on**.
4. Go back to NFS Files and tap the server again.

If NFS Files isn't in the list, the system hasn't asked yet: connect to a server once, and the prompt appears. Tap **Allow**.

</div>

<div data-platform="mac" markdown="1">

### Mac (macOS 15 Sequoia and later)

1. Open **System Settings**.
2. **Privacy & Security** → **Local Network**.
3. Turn on **NFS Files**.
4. Quit and reopen NFS Files, then connect again.

On macOS 14 and earlier there is no such permission; if you're on 14 the cause is something else — see [No route to the server](/help/errors/host_unreachable/).

</div>

## Why this exists

Apple added the Local Network permission so apps can't quietly map your home network. NFS Files needs it for the obvious reason — your NAS *is* on your local network — and uses it for nothing else: it connects to the servers you add, finds servers advertising NFS over Bonjour, and (only when you tap Scan My Network) checks the addresses on your subnet for an RPC responder. Nothing it learns leaves the device.

## Still failing with it on?

Then the network path itself is the problem: [No route to the server](/help/errors/host_unreachable/) covers subnets and VLANs, and [timeout](/help/errors/timeout/) covers firewalls.
