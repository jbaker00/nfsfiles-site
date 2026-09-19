---
title: "Every error, explained"
kicker: Errors
summary: "What each message NFS Files can show means, and what fixes it. Tap Learn More in the app to land on the right one."
---

## Connecting

<ul class="errlist">
<li><a href="/help/errors/timeout/"><code>timeout</code> The server didn't respond in time</a><br><span>The app sent its request and nothing came back. Usually the NAS is off, asleep, on a different network, or a firewall is silently dropping the packets.</span></li>
<li><a href="/help/errors/refused/"><code>refused</code> The server refused the connection</a><br><span>A machine is at that address, but nothing is listening on the port. The NFS service is probably switched off, or the app is pointed at the wrong port.</span></li>
<li><a href="/help/errors/host_unreachable/"><code>host_unreachable</code> No route to the server</a><br><span>Your device couldn't find a path to that address. On iPhone, iPad and Mac the most common cause is the Local Network permission being off.</span></li>
<li><a href="/help/errors/network_unreachable/"><code>network_unreachable</code> No network for that address</a><br><span>Your device has no usable network interface for that address — Wi-Fi is off, you're on cellular only, or (on a Mac) the Local Network permission is denied.</span></li>
<li><a href="/help/errors/dns/"><code>dns</code> Couldn't find a server with that name</a><br><span>The name you typed didn't resolve to an address. `.local` names only work on the same network segment, and short names like `nas` usually don't work on iOS at all.</span></li>
<li><a href="/help/errors/connection_closed/"><code>connection_closed</code> The server closed the connection</a><br><span>A machine answered, then hung up before finishing. Usually the NFS service is restarting, a TCP wrapper rule rejected you, or the NAS went to sleep mid-conversation.</span></li>
<li><a href="/help/errors/connection_reset/"><code>connection_reset</code> The server dropped the connection</a><br><span>The connection was open and working, then the server reset it. Almost always transient: the NAS rebooted, the NFS service restarted, or a firewall timed out an idle session.</span></li>
<li><a href="/help/errors/connection_failed/"><code>connection_failed</code> Couldn't reach the server</a><br><span>A network error the app couldn't classify further. The system's own description is in the message; the basics below cover most of them.</span></li>
<li><a href="/help/errors/malformed_reply/"><code>malformed_reply</code> The server sent a reply the app couldn't understand</a><br><span>Whatever is on that port isn't speaking NFS. Usually a Custom Port pointed at the wrong service, or a proxy in the way.</span></li>
<li><a href="/help/errors/program_unavailable/"><code>program_unavailable</code> NFS isn't registered on this server</a><br><span>The portmapper answered but has no NFS or MOUNT service registered for the version the app asked for. NFS is probably enabled but not running, or the server is NFSv4-only.</span></li>
<li><a href="/help/errors/rpc_rejected/"><code>rpc_rejected</code> The server rejected the request at the RPC layer</a><br><span>The program version the app asked for isn't what the server offers. Usually a server that speaks only NFSv4 reached through the NFSv3 path, or Custom Port pointing at a different RPC service.</span></li>
<li><a href="/help/errors/auth_rejected/"><code>auth_rejected</code> The server rejected the app's credentials</a><br><span>The server won't accept plain AUTH_SYS (uid/gid) authentication. Either the export requires Kerberos, or the security list for the share doesn't include `sys`.</span></li>
<li><a href="/help/errors/export_not_found/"><code>export_not_found</code> That folder isn't shared</a><br><span>The server has NFS running but doesn't export the path you typed. The path has to match the server's export list exactly — and every NAS spells it differently.</span></li>
<li><a href="/help/errors/mount_access_denied/"><code>mount_access_denied</code> The server refused this device</a><br><span>The most common NFS error there is. Two causes look identical from the client: the share requires privileged ports (add `insecure`), or your device's address isn't in the share's allowed-client list.</span></li>
<li><a href="/help/errors/mount_denied/"><code>mount_denied</code> The server refused to share that folder</a><br><span>The MOUNT request failed with an error other than access denied or not found — the path is a file, is too long, or the server hit an internal error.</span></li>
<li><a href="/help/errors/unsupported/"><code>unsupported</code> The server doesn't support something the app needs</a><br><span>The server answered, but lacks an operation NFS Files relies on. Try pinning the other NFS version; if that doesn't help, email the message.</span></li>
</ul>

## While browsing and transferring

<ul class="errlist">
<li><a href="/help/errors/nfs_perm/"><code>nfs_perm</code> Operation not permitted</a><br><span>The server allows you into the folder but refused this particular change. Almost always: changing an owner or group needs root, and the export squashes root.</span></li>
<li><a href="/help/errors/nfs_noent/"><code>nfs_noent</code> No such file or folder</a><br><span>The item isn't there any more — renamed, moved or deleted by someone else since the listing was loaded — or, on NFSv4, the export path doesn't exist under the server's pseudo-root.</span></li>
<li><a href="/help/errors/nfs_io/"><code>nfs_io</code> The server reported an I/O error</a><br><span>The server tried to read or write the disk and failed. That's a storage problem on the NAS, not a network one — check its storage health.</span></li>
<li><a href="/help/errors/nfs_access/"><code>nfs_access</code> Access denied by the server</a><br><span>You're connected, but the server won't let the user you present read or write here. NFS has no passwords — the numeric User ID is your identity, and the export may squash it.</span></li>
<li><a href="/help/errors/nfs_exist/"><code>nfs_exist</code> An item with that name already exists</a><br><span>The server already has something with that name in this folder — possibly one you can't see because it differs only by case, or is a hidden file.</span></li>
<li><a href="/help/errors/nfs_notdir/"><code>nfs_notdir</code> That item isn't a folder</a><br><span>The app tried to open or list something that's a file (or a link to a file), not a folder.</span></li>
<li><a href="/help/errors/nfs_isdir/"><code>nfs_isdir</code> That item is a folder</a><br><span>A file operation was attempted on a folder. Refresh — the item may have changed type on the server since it was listed.</span></li>
<li><a href="/help/errors/nfs_fbig/"><code>nfs_fbig</code> The file is too large for this server</a><br><span>The server can't hold a file this size — usually a 4 GB limit on an exFAT/FAT32 volume (USB drives), or a per-file quota.</span></li>
<li><a href="/help/errors/nfs_nospc/"><code>nfs_nospc</code> The server is out of space</a><br><span>The volume the share lives on is full. Free some space on the NAS, or check whether snapshots or a recycle bin are holding it.</span></li>
<li><a href="/help/errors/nfs_rofs/"><code>nfs_rofs</code> The share is read-only</a><br><span>The export is shared read-only, or the volume under it went read-only after an error.</span></li>
<li><a href="/help/errors/nfs_nametoolong/"><code>nfs_nametoolong</code> The name is too long</a><br><span>Server filesystems cap each name at 255 bytes — and accented or non-Latin characters take two to four bytes each.</span></li>
<li><a href="/help/errors/nfs_notempty/"><code>nfs_notempty</code> The folder isn't empty</a><br><span>The server won't delete a folder that still has something in it — sometimes a hidden file you can't see in Files.app or the Finder.</span></li>
<li><a href="/help/errors/nfs_dquot/"><code>nfs_dquot</code> Storage quota exceeded</a><br><span>The user you present (or the user the export squashes you to) has hit their quota on the NAS.</span></li>
<li><a href="/help/errors/nfs_stale/"><code>nfs_stale</code> Stale file handle</a><br><span>The server no longer recognises the handle the app holds for this item — it was moved or deleted server-side, or the export was restarted. Reconnect from the server list.</span></li>
<li><a href="/help/errors/nfs_badhandle/"><code>nfs_badhandle</code> The file handle is no longer valid</a><br><span>An NFSv4 server rejected the handle the app holds. Same cure as a stale handle: reconnect from the server list.</span></li>
<li><a href="/help/errors/nfs_notsupp/"><code>nfs_notsupp</code> The operation isn't supported by this server</a><br><span>The server doesn't implement this NFS operation. Small userspace servers skip things like SETATTR (used by the permission editor); do that action on the server instead.</span></li>
<li><a href="/help/errors/nfs_serverfault/"><code>nfs_serverfault</code> The server hit an internal error</a><br><span>The NFS server itself failed while handling the request. Usually transient; if it repeats, the NAS's own log says why.</span></li>
<li><a href="/help/errors/nfs_delay/"><code>nfs_delay</code> The server asked to retry in a moment</a><br><span>The server is busy or the item is temporarily unavailable (a spun-down disk, a snapshot in progress). Wait a few seconds and try again.</span></li>
<li><a href="/help/errors/nfs_expired/"><code>nfs_expired</code> The connection to the server expired</a><br><span>The NFSv4 lease timed out — usually after the app was in the background a while or the NAS restarted. Reconnect from the server list.</span></li>
<li><a href="/help/errors/nfs_grace/"><code>nfs_grace</code> The server is still starting up</a><br><span>The NFSv4 server just restarted and is in its grace period (typically 90 seconds) while old clients reclaim their state. Wait a minute and retry.</span></li>
</ul>

Something not listed? The app shows codes like `nfs_status_123` for statuses it hasn't seen before — email the code and what you were doing.
