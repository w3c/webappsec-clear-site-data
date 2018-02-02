# Explainer: Clearing Site Data

## The Problem

Developers wish to have control over the data associated with their origins which users' browsers
store locally on their behalf. In particular, developers wish to take reasonable steps to protect
users from local attackers by ensuring that certain kinds of data are removed from a user's local
machine when it is no longer necessary (for example, upon signing out of an application, or upon
account deletion).

Developers have direct access to a number of storage mechanisms, which makes it possible to perform
this kind of cleanup from JavaScript. `window.localStorage`, for example, is easily dealt with a
simple call to `window.localStorage.clear()`. Other storage mechanisms are trickier. Cookies, for
instance, exist cross-origin, might not be accessible to JavaScript, and could have path
restrictions that can make them quite difficult to enumerate. The browser's various caches are even
more difficult to poke at, as they're intentionally opaque.

It would be nice if browsers offered developers a mechanism that would give them power to remove the
data their applications are responsible for maintaining. Ideally, developers should be able to
reliably ensure the following:

1.  Data stored in an origin's client-side storage mechanisms like IndexedDB, WebSQL, Filesystem,
    `self.localStorage`, `self.sessionStorage`, `self.caches`, etc. is cleared.
2.  Cookies for an origin's host are removed.
3.  Web Workers (dedicated and shared) running for an origin are terminated.
4.  Service Workers registered for an origin are terminated and deregistered.
5.  Resources from an origin are removed from the user agent's local cache.
6.  None of the above can be bypassed by a maliciously active document that
    retains interesting data in memory, and rewrites it if it's cleared.

## The Proposal

One way to give developers the capabilities alluded to above would be to accept a server-sent
assertion that an origin's data be cleared. This could be an HTTP response header whose value
specified a subset of locally stored data to be cleared:
of:

```
Clear-Site-Data: "*"
```

With this kind of assertion, developers could handle a number of use cases:

1.  When a user deletes their account from a given social media application, the "Oh noes, you're
    gone!" page could be served along with `Clear-Site-Data: "*"` to clear out any and all sensitive
    information that may have been persisted to the user's disk.

2.  If a user signs out of a given application, it might do a more targeted cleanup, removing, for
    example, photos from the disk cache, while retaining cookies with interesting user preferences
    by serving `Clear-Site-Data: "cache"`.

3.  In the case of catastrophic failure (perhaps an applications developers learn that their servers
    were compromised for some period of time), developers can reduce the risk of a persistent
    client-side XSS by clearing out local sources of data: `Clear-Site-Data: "*"`.
