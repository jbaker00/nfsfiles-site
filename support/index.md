---
title: "Support"
kicker: NFS Files
summary: "Setup guides, explanations for every error the app can show, and a human mailbox. Start with the guides — they answer most of it."
description: "NFS Files support: per-NAS setup guides, every error explained, Files.app and Finder setup, and email support."
---

## Connecting to your NAS

Most connection problems come down to one server setting. If a connection is refused, the app tells you what to fix — and the walkthroughs are here:

<ul class="cards">
<li><a href="/guides/synology/"><strong>Synology setup</strong><span>DSM 7 — enable NFS, non-privileged ports, squash</span></a></li>
<li><a href="/guides/qnap/"><strong>QNAP setup</strong><span>QTS / QuTS hero — NFS service, host access, squash</span></a></li>
<li><a href="/guides/truenas/"><strong>TrueNAS setup</strong><span>CORE and SCALE — service, shares, Mapall</span></a></li>
<li><a href="/guides/unraid/"><strong>Unraid setup</strong><span>NFS rules, security settings, ownership</span></a></li>
<li><a href="/guides/ugreen/"><strong>UGREEN setup</strong><span>UGOS — shared-folder NFS rules</span></a></li>
<li><a href="/guides/pi/"><strong>Linux / Raspberry Pi</strong><span>nfs-kernel-server, /etc/exports, exportfs</span></a></li>
</ul>

The three pages that solve nearly everything:

- [The server refused this device](/help/errors/mount_access_denied/) — the #1 error (`insecure` / allowed clients)
- [Access denied](/help/errors/nfs_access/) — UID/GID and squash
- [That folder isn't shared](/help/errors/export_not_found/) — export paths per NAS
- [Every error, explained](/help/errors/) — the full list; the app's Learn More button lands on the right one

Background reading: [exports, the insecure option, and ports](/help/exports/), [user IDs, groups and squash](/help/identity/), [the Local Network permission](/help/local-network/).

## Your NAS in Files.app / the Finder (Pro)

- [iPhone and iPad — turn the location on](/help/files-app/)
- [Mac — the Enable banner is in the Finder window, not Settings](/help/finder/)

## Files and transfers

- **Files download before they open in the preview.** Large videos are cached on the device so reopening is instant — clear it anytime in Settings → Downloaded Files.
- **Streaming video** is coming (it's the top Pro request); today, a file downloads fully before the first frame.
- **Are my files private?** Yes. NFS Files talks directly to your server over your local network — files never pass through us or any cloud. See the [Privacy Policy](/privacy/).

## Remove ads / Pro

Settings → NFS Files Pro → Upgrade. One-time purchase, no subscription, removes all ads (including the Mac sponsor strip) and unlocks the Pro features. Already purchased on another device with the same Apple ID? Tap **Restore Purchase**.

## Still stuck?

{% include email.html subject="NFS Files support" %} — a person reads it. Say which NAS you have (model + OS version) and paste the exact message the app showed. Easiest: in the app, **Settings → Contact Support** starts the email with your version and the last error already filled in.
