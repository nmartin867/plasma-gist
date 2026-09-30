# Implementation prompt: bring the Gist widget in line with the mockups

Paste everything below the line into a Claude Code session opened on
`nmartin867/plasma-gist`.

Mockups: https://claude.ai/artifact/6RA5wrVoTKfe44fcYyk595
(source files for each screen are in `design/boards/` next to this prompt).

---

You are working on `nmartin867/plasma-gist`, a Plasma 6 plasmoid in pure QML +
JS (no C++). Read `CLAUDE.md` first and follow it: `.pragma library` rules for
`github.js`, the three-place rule for settings, Plasma 6 imports, and
`qmllint -I /usr/lib/qt6/qml` plus `npm run lint` (ESLint, `no-var` and
`prefer-const`, for `package/contents/code/*.js`) as the checks. New JS uses
`const`/`let`, never `var`, including the JS inside `.qml` files, which ESLint
cannot see. There is no test suite; verify with both linters and, where you
can, `plasmawindowed com.github.nmartin867.gists` (full view) and
`plasmoidviewer -a package -f horizontal` (panel icon; plasma-sdk is installed).

The goal is a widget that lists a user's gists, shows each gist as rendered
Markdown or raw source, and lets the owner edit it inline. The design is
eight screens (Breeze styling; use Kirigami units/colours, never the hex
values from the mockups):

1. **List**: header with title, Refresh, Configure; a filter field
   ("Filter by description or filename") and an All / Public / Secret
   segmented control (Secret only meaningful in "my gists" mode). Rows: public
   or lock icon, title, a "Secret" tag on secret gists, secondary line
   `Language · N files · N comments`, relative updated time on the right;
   on hover the time is replaced by View on web / Copy URL. Footer:
   `Updated 14:32` left, gist count right.
2. **Viewer, rendered**: header with Back, title, Edit (pencil), Copy
   contents, View on web. Under it, one tab per file and a Rendered / Source
   toggle. Markdown files open rendered (headings, code blocks, GFM task
   lists, block quotes, links). Footer: `Markdown · 1.8 KB` and comment
   count + updated time.
3. **Viewer, source**: same header; monospace, line numbers, syntax
   highlighting; footer shows language and line count. Non-Markdown files
   show only this view (hide the toggle).
4. **Inline edit**: header becomes Discard (X), "Editing “…”", Cancel,
   Save (primary). A Description field. File tabs mark unsaved files with an
   orange dot. Write / Preview toggle (Preview renders Markdown from the
   buffer). Footer: "Unsaved changes" indicator, `Ctrl+S save · Esc cancel`,
   cursor line/column.
5. **First run**: centred "Connect to GitHub" with two actions, "Use an
   access token…" (primary) and "Browse a username…", both opening the
   config dialog, plus a link to create a token.
6. **Error**: keep the last good list visible but dimmed, with an inline
   warning banner (title, detail incl. rate-limit reset time and the time
   of the list being shown, Retry button). Footer says the list is not
   current.
7. **Settings**: "Show:" radio between "My gists (public and secret)" and
   "Public gists of a user:" with the username field enabled only for the
   latter; token field with a Test button and a result line ("Signed in as
   <login> · Gists: read and write"); help text saying editing needs Gists
   write access; "Open Markdown as: Rendered/Source"; gists to show;
   refresh interval; tooltips checkbox.
8. **Panel icon**: the applet's own icon (`com.github.nmartin867.gists`,
   shipped under `contents/icons/hicolor`); no badge when idle; a badge counting gists updated since
   the popup was last opened; an orange dot on error. Tooltip:
   `42 gists · 2 updated · checked 14:32`.

## Fix these first (bugs found in review; full write-up in `BUGS.md`)

- `main.qml` `refresh()` calls `closeGist()`, so the poll `Timer` kicks the
  user out of the gist they are reading every `refreshInterval` minutes.
  Once editing exists this would silently discard edits. Only reset the
  detail view on an explicit account change, and skip or defer background
  refreshes while editing.
- `refresh()` clears `gistModel` on error, so a rate-limit blip empties the
  list. Keep the previous rows and surface the error in the banner (screen 6).
- `refresh()` returns early while `loading`, so an account change made
  during a fetch is dropped and the old account's response is applied. Tag
  each request with a generation number and ignore stale responses.
- `github.js` `errorMessage()` maps every 404 to "No such GitHub user.",
  which is wrong for `fetchGist` (a deleted gist). Pass a context (list vs
  gist) or let the caller supply the 404 text.
- For 403 rate limits, read `X-RateLimit-Reset` and include the reset time
  in the message.
- `ConfigGeneral.qml` tells users a read-only token is enough; that stops
  being true once editing lands.
- `FullRepresentation.qml` heading reads "Gists of " with an empty username
  when unconfigured; show "GitHub Gists" instead.
- `README.md` still says clicking a gist opens the browser.

## Build order

1. **Bug fixes above.** Small, independent; one commit each is fine.
2. **Viewer restructure** (`GistDetail.qml`): replace the stacked Repeater
   with a file tab bar (`PlasmaComponents3.TabBar`) and a single file pane.
   Add a `viewMode` ("rendered" | "source") on `root`, defaulting from a new
   `markdownDefaultView` setting. Rendered mode: a read-only `TextEdit`
   with `textFormat: TextEdit.MarkdownText`, `wrapMode: Text.Wrap`,
   `onLinkActivated: Qt.openUrlExternally(link)`. Treat a file as Markdown
   when GitHub's `language` is "Markdown" or the filename ends in `.md` /
   `.markdown`. Source mode: keep the existing highlighted `TextEdit`, add
   a line-number gutter. Check how `SyntaxHighlighter.definition` resolves
   GitHub language names (e.g. GitHub "Shell" vs KSyntaxHighlighting "Bash");
   prefer a lookup by filename if the QML API offers one (unverified).
   Add Copy contents to the header (reuse the clipboard helper from
   `GistDelegate.qml`; move it somewhere shared). Footer with language,
   size, comments, updated time: add `size`, `updatedAt`, `commentCount` to
   `normaliseDetail()` first.
3. **List improvements** (`FullRepresentation.qml`, `GistDelegate.qml`):
   filter field and All/Public/Secret control. Filter client-side with a
   `DelegateModel` or by keeping a full array in `main.qml` and rebuilding
   the visible model; do not refetch. Relative time from `updatedAt`
   (locale-aware; fall back to `Locale.ShortFormat` dates past a week).
   Secret tag. Footer gist count.
4. **Inline editing.** In `github.js` add
   `updateGist(id, { description, files: { name: { content } } }, opts, onSuccess, onError)`
   using `PATCH /gists/{id}`; it returns the updated gist, so run it through
   `normaliseDetail()`. In `main.qml` hold `editing`, a per-file draft map,
   and `dirty`; only offer Edit when a token is set and the gist's owner is
   the token's user. For that, fetch `GET /user` once per token change and
   store `authLogin`, and add `ownerLogin` to both normalisers. Save sends
   only changed files; on success replace `selectedGist` and update the
   matching `gistModel` row. On 404/403 while saving, explain that the token
   needs Gists write access. Escape cancels (ask first when dirty); Ctrl+S
   saves (`Shortcut` inside the representation). Preview renders the draft
   with the same Markdown view as step 2. Do not refresh the list while
   `editing` is true.
5. **Settings** (`main.xml`, `ConfigGeneral.qml`, following CLAUDE.md's
   three-place rule): radio layout for the account mode (same
   `listOwnGists` entry), `markdownDefaultView` (String, default
   "rendered"), and a Test button that calls `GET /user` and shows the
   login. Report write access from the `X-OAuth-Scopes` header for classic
   tokens; fine-grained tokens do not report permissions, so for those say
   "Signed in as <login>" and let a failed save explain the rest.
6. **First run and error states**: replace the single
   `PlaceholderMessage` branch for "not configured" with screen 5, and add
   the error banner from screen 6 above the list
   (`Kirigami.InlineMessage`, type Warning, with a Retry action).
7. **Panel icon** (`CompactRepresentation.qml`): drop the total-count
   badge. Track `lastSeen` (a Date written to a hidden config entry when the
   popup opens) and badge the number of gists with `updatedAt > lastSeen`.
   Orange dot when `errorMessage !== ""`. Update `toolTipSubText`. Keep
   `Plasmoid.icon` as the custom icon; the badge sits over its lower-right
   corner, clear of the three code bars.
8. Update `README.md` (features, token permission) and the layout tree.

## Constraints

- No C++ plugin; Qt/Plasma/Kirigami components only.
- All user-facing strings through `i18n()` in QML.
- Kirigami units for spacing and sizes; theme colours only.
- After each step run qmllint with `-I /usr/lib/qt6/qml` and `npm run lint`,
  and fix what they report before moving on.
- Screenshots for checking the result: `spectacle -a -b -n -o out.png`
  (KWin/Wayland; `grim` does not work). `-a` grabs the focused window.
- Keep `main.qml` the only stateful file, as CLAUDE.md describes.
