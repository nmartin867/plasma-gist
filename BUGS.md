# Known bugs

Found in a code review of `main` at `1e6e4ae`. Each entry says what the user
sees, why it happens, and a proposed fix. Line numbers are for that commit.
Delete an entry when its fix lands.

The redesign in `design/` builds on these fixes; `design/IMPLEMENTATION_PROMPT.md`
schedules them as its first step.

## 1. Auto-refresh closes the gist you are reading

**Severity:** high. It happens every refresh interval (15 minutes by default),
and once inline editing exists it will throw away unsaved edits.

**Seen:** you open a gist in the popup, and after the poll timer fires the popup
jumps back to the list.

**Cause:** `refresh()` calls `closeGist()` unconditionally
(`package/contents/ui/main.qml:65`). The poll `Timer` (`main.qml:128-133`),
the Refresh button and the context-menu action all go through `refresh()`, so
a background poll resets the detail view the same way an account change does.

**Fix:** only reset the detail view when the account being listed changes.
Split the two cases, for example by giving `refresh()` a parameter
(`refresh({ resetView: true })`) that the `Connections` handlers
(`main.qml:136-142`) pass and the timer does not. If the open gist is no longer
in the new list, leave it open; the next explicit navigation will pick that up.

## 2. Any error empties the list

**Severity:** medium.

**Seen:** a transient failure (a rate limit, a dropped connection, a laptop
waking from sleep before the network is up) replaces the whole list with the
"Could not load gists" placeholder, even though the previous results were fine.

**Cause:** the error callback of `fetchGists` calls `gistModel.clear()`
(`main.qml:80`) before setting `errorMessage`.

**Fix:** leave `gistModel` untouched on error and show `errorMessage` above the
list (a `Kirigami.InlineMessage` with a Retry action; see
`design/boards/State-Error.dc.html`). Keep `lastUpdated` as it is, so the
footer shows how old the list is. Only fall back to the full placeholder when
the model is empty.

## 3. A config change during a refresh is ignored

**Severity:** medium.

**Seen:** you change the username (or token, or mode) in settings while a fetch
is in flight. The widget keeps showing the old account's gists until the next
poll, up to 15 minutes later, or never if polling is off.

**Cause:** `refresh()` returns early when `loading` is true (`main.qml:59`).
The `onUsernameChanged` / `onTokenChanged` / `onListOwnGistsChanged` /
`onMaxGistsChanged` handlers (`main.qml:138-141`) call `refresh()` and are
dropped, and the in-flight response for the old account is then applied.

**Fix:** give each request a generation number. Increment it in `refresh()`,
capture it in the callbacks, and ignore any response whose number is stale.
Then an account change can always start a new request instead of returning
early. The timer can keep the early return, so polls still don't overlap.

## 4. Opening a deleted gist says "No such GitHub user"

**Severity:** low.

**Seen:** you open a gist that was deleted since the list loaded (or one you
can't see with the current token), and the detail view reports
"No such GitHub user."

**Cause:** `errorMessage()` in `package/contents/code/github.js:182-205` maps
every 404 to that text, but it is shared by `fetchGists` (`github.js:72`),
where 404 does mean an unknown user, and by `fetchGist` (`github.js:121`),
where it means the gist is gone.

**Fix:** pass the context in, for example `errorMessage(xhr, { notFound: "…" })`,
with each caller supplying its own 404 text ("This gist no longer exists." for
`fetchGist`).

## 5. The rate-limit message doesn't say when to retry, and misses 429

**Severity:** low.

**Seen:** "GitHub rate limit reached. Add a token or wait." gives no idea how
long to wait. GitHub also signals rate limits with HTTP 429, which falls
through to the default branch and shows the raw API message.

**Cause:** `errorMessage()` only looks at the 403 body (`github.js:193-197`)
and never reads the rate-limit headers.

**Fix:** treat 403-with-"rate limit" and 429 the same way. Read
`X-RateLimit-Reset` (epoch seconds) with `xhr.getResponseHeader()` and include
the reset time in the message. `github.js` is a `.pragma library` with no
locale context, so pass the reset time back as a number next to the message
and let `main.qml` format it with `Locale.ShortFormat`.

## 6. Header reads "Gists of " when no username is set

**Severity:** cosmetic.

**Seen:** on first run in username mode, the popup header says "Gists of "
with nothing after it.

**Cause:** the heading text (`package/contents/ui/FullRepresentation.qml:53-55`)
formats `Plasmoid.configuration.username` without checking that it is set.

**Fix:** when `!root.configured`, show "GitHub Gists".

## 7. Outdated user-facing text

**Severity:** cosmetic. These become wrong as the redesign lands, but one is
wrong already.

- `README.md:4` says "Clicking a gist opens it in the browser." It has opened
  inside the popup since `GistDetail.qml` was added.
- `package/contents/ui/ConfigGeneral.qml:43` says a read-only Gists token is
  enough. That stops being true once inline editing (a `PATCH /gists/{id}`)
  exists; the text should say editing needs Gists write access.
