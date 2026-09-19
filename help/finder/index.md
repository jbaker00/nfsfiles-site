---
title: "Your NAS in the Finder"
kicker: Help · NFS Files Pro
summary: "With Pro, every saved server appears in the Finder sidebar — usable from every Mac app's Open and Save dialogs. macOS makes you enable the location yourself, and the switch is not where you'd expect."
description: "How to enable the NFS Files location in the macOS Finder — the Enable button is in a banner inside the Finder window, not in System Settings."
---

## Where the switch actually is

This trips everyone up, including me. macOS does **not** put the toggle in System Settings → Login Items & Extensions, where you'd look for it. Instead:

1. Open a **Finder** window.
2. In the sidebar, under *Locations*, click **NFS Files**.
3. A banner appears across the **top of that Finder window** with an **Enable** button. Click it.
4. Your servers appear as folders inside the NFS Files location.

If you don't see NFS Files in the sidebar: Finder → Settings → Sidebar → make sure **NFS Files** is ticked under Locations (it may take a few seconds to appear after the first launch with Pro).

The server card in NFS Files stays amber — *Finish setup* — until this is done, and re-checks each time the app becomes active.

## What you can do there

- Open and save from any Mac app's file dialogs, directly on the NAS.
- Drag files and folders in and out; drag between folders on the same server for a server-side move.
- Quick Look with the space bar, Get Info, rename, trash.
- Files download on demand when opened. Nothing is synced in bulk; nothing is kept once macOS evicts it.

## If the location lists nothing

- **Not enabled** — the banner step above. Nearly always this.
- **Renamed the server** — that re-registers the location and resets the switch; enable it again.
- **Two copies of NFS Files installed** — the Mac App Store version *and* the iPhone/iPad version running on Apple silicon. They share an identity and only one can own the Finder location; the loser fails silently. Keep the Mac version and delete the other (Launchpad → hold the icon).
- **The server isn't reachable** from this Mac right now.
- **Pro isn't active on this Mac** — NFS Files → Settings → *Restore Purchase* if you bought on another device with the same Apple ID.

## Speed

NFS Files talks NFS directly from the Finder extension — no proxy through the app — so throughput is the same as in the app. On the menu-bar NAS Monitor, transfers done through the Finder don't yet show in the live-speed row; that's a known gap.
