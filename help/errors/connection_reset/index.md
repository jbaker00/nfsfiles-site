---
title: "The server dropped the connection"
kind: connection_reset
summary: "The connection was open and working, then the server reset it. Almost always transient: the NAS rebooted, the NFS service restarted, or a firewall timed out an idle session."
description: "NFS Files error connection_reset: The connection was open and working, then the server reset it. Almost always transient: the NAS rebooted, the NFS service restarted, or a firewall timed out an idle session."
---

## What this means

*Connection reset by peer*. Something on the server end tore down an established connection.

## What to do

1. **Try again.** If the NAS was restarting, the second attempt usually works.
2. **Was it idle for a long time?** Some routers and firewalls expire idle TCP sessions after a few minutes and reset them when traffic resumes. Reconnecting fixes it; if it keeps happening, look for an "idle timeout" setting on the firewall.
3. **Check the NAS log** if it recurs — a crashing NFS daemon or a storage error underneath will show there.
4. **On Linux servers:** TCP wrappers (`/etc/hosts.deny`) can reset connections from addresses that aren't allowed. Make sure your subnet is in `/etc/hosts.allow`.
