---
title: "The server rejected the app's credentials"
kind: auth_rejected
summary: "The server won't accept plain AUTH_SYS (uid/gid) authentication. Either the export requires Kerberos, or the security list for the share doesn't include `sys`."
description: "NFS Files error auth_rejected: The server won't accept plain AUTH_SYS (uid/gid) authentication. Either the export requires Kerberos, or the security list for the share doesn't include `sys`."
---

## What this means

NFS has no passwords. Ordinary NFS (what NFS Files speaks) identifies you with a numeric user and group ID — the `sys` security flavour, also called AUTH_UNIX. The server refused that flavour outright at the RPC layer. That happens when the share is configured for **Kerberos only**.

## Fix it on the server

Add `sys` to the share's security options. Kerberos can stay enabled alongside it.

<div id="nas-synology"></div>

- **Synology:** Control Panel → Shared Folder → select the folder → Edit → **NFS Permissions** → edit the rule → **Security**: tick **sys** (you can leave krb5 ticked too).

<div id="nas-truenas"></div>

- **TrueNAS:** Sharing → Unix (NFS) Shares → edit → Advanced Options → **Security**: make sure **SYS** is in the list (it must be first if you want it used by default). Also System → Services → NFS → *Require Kerberos for NFSv4* must be **off**.

<div id="nas-pi"></div>

- **Linux / Raspberry Pi:** in `/etc/exports`, an option like `sec=krb5` restricts the export. Change it to `sec=sys:krb5` (or remove `sec=` — `sys` is the default), then `sudo exportfs -ra`.

- **QNAP, Unraid, UGREEN:** don't offer Kerberos-only NFS from their UIs; if you see this error there, the server is probably restricting by client address instead — see [access denied](/help/errors/mount_access_denied/).

## NFS Files does not support Kerberos

That's deliberate: Kerberos needs a KDC, keytabs, and a domain, none of which exist on a home network. If your workplace NAS is Kerberos-only, ask the administrator for a `sys`-secured export for your subnet, or use their VPN and a different client.
