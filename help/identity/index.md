---
title: "User IDs, groups and squash"
kicker: Help
summary: "NFS has no passwords. The client states a numeric User ID and Group ID; the server believes it, then applies its own rules. Once you see it that way, every permission problem makes sense."
description: "How NFS identity works — UID, GID, root_squash, all_squash, anonuid — and how to read the Inspect Server screen in NFS Files."
---

## The model in one paragraph

An NFS client doesn't log in. With every request it sends a **UID** (user ID) and a **GID** (group ID) — just numbers — and the server treats the request as coming from that user. There's no way for the server to check, which is why NFS is a *trusted-network* protocol: the export decides which **addresses** may connect, and then trusts what they say. (Kerberos NFS fixes this, but no home NAS ships it turned on, and NFS Files doesn't support it.)

The server then does two things with that identity.

## 1. Squash: the server may rewrite who you are

| Export option | What the server does with the UID you present |
|---|---|
| `root_squash` (default) | UID 0 (root) becomes `nobody`. Everyone else is used as-is. |
| `no_root_squash` | Root stays root. Dangerous; never needed for this app. |
| `all_squash` | **Every** UID becomes the `anonuid`/`anongid` the export specifies. The UID you present is ignored. |

`all_squash` with a fixed `anonuid` is the setup I recommend for home use: every device acts as one designated user, your personal account is never exposed, and revoking access is one line. Synology calls it **Squash: Map all users to admin/guest**; TrueNAS calls it **Mapall User**; Unraid does it by default (`anonuid=99`).

## 2. Then ordinary Unix permissions apply

Every file has an owner UID, a group GID, and a mode (`rwxr-xr-x`). After squashing, the server checks the (possibly rewritten) UID/GID against those, exactly as if you'd logged in locally. So:

- **Access denied** (`nfs_access`) means: the user the server ended up with can't read or write here.
- **Operation not permitted** (`nfs_perm`) means: you're allowed in, but *this* operation (typically changing the owner) needs root, and root is squashed.

## What Inspect Server shows

Tap **Inspect Server** on a server card (it's free). The **Who the server thinks you are** section shows:

- **You present** — the UID/GID from the server's Advanced settings (default 1000/1000, changeable in Settings → Defaults for New Servers).
- **Export owned by** — the owner of the export's root folder, as the server reports it.
- **Permissions** — the root folder's mode, in octal (`755` = owner can write, everyone can read).
- **Read / Write** — whether each actually works: the app tries a read and creates-then-removes a tiny hidden folder to test writing.
- A plain-language read on which squash mode you're hitting, when it can be inferred.

On **NFSv4**, servers report owners as *strings* — `1000`, or `james@nas.local` when the server runs an ID-mapping daemon — so the probe shows the name and doesn't try to reason about numbers.

## Finding the right UID

On the server: `id yourname` prints `uid=1026(james) gid=100(users)`. First-created users are `1000` on most Linux systems and `1026` on Synology. Put those numbers in NFS Files under the server's **Advanced → User ID / Group ID**.

## Secondary groups

Unix users belong to several groups, but NFS Files currently sends only one GID. If a folder is readable only by a group your user belongs to *secondarily*, the server won't know. Use `all_squash` to a user that has access, or make the folder accessible to the primary group. Sending extra group IDs is on the roadmap.

## The permission editor (Pro)

Long-press a file or folder → **Permissions** to change mode, owner and group from the app. It's subject to everything above: changing the owner needs root and is refused under `root_squash`; changing the mode needs you to *be* the owner (after squash). The editor shows the current owner so you can compare it with "You present".
