# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Plasma 6 applet (plasmoid) that lists GitHub gists in the panel or on the
desktop. Pure QML + JavaScript — there is no C++ component and no compile step.
Developed against Plasma 6.7 / Qt 6.11 on Arch.

## Commands

```sh
# Install / reinstall for the current user (wraps kpackagetool6)
./install.sh
systemctl --user restart plasma-plasmashell

# Lint. The -I is required: qmllint does not find the Plasma/Kirigami modules
# on its own, and without it every import fails and the output is useless.
/usr/lib/qt6/bin/qmllint -I /usr/lib/qt6/qml \
    package/contents/ui/*.qml package/contents/config/*.qml

# Lint the plain JS under package/contents/code (ESLint; dev-only dependency,
# `npm install` once). qmllint does not check var/let/const, ESLint does.
npm run lint

# Format
/usr/lib/qt6/bin/qmlformat -i package/contents/ui/*.qml

# Runtime errors (QML errors never reach stdout — they go to the journal)
journalctl --user -u plasma-plasmashell -f

# System-wide install (needs extra-cmake-modules + libplasma)
cmake -B build && cmake --build build && sudo cmake --install build
```

There is no test suite. Verification is `qmllint` + `npm run lint` plus loading
the widget.

### Previewing without restarting the shell

`plasmawindowed com.github.nmartin867.gists` (ships with plasma-workspace, so
already installed) runs the applet in its own window after `./install.sh` — much
faster than the install/restart loop, `console.log` goes to the terminal instead
of the journal, and `-d` attaches a QML/JS debugger. It only renders the full
representation; the compact one needs `plasmoidviewer -a package -f horizontal`
from `plasma-sdk`, which is installed.

Screenshots: this is a KWin/Wayland session, so `grim` does not work — it needs
the wlroots `wlr-screencopy` protocol. Use `spectacle -a -b -n -o out.png`,
which goes through KWin's own `org.kde.KWin.ScreenShot2`. Note that `-a` grabs
whatever window is *focused*, not the preview, and there is no way to target a
window by title without `kdotool` (AUR).

See the *Development* section of README.md for the rest: resetting settings,
`QML_IMPORT_TRACE`, and reproducing the API request with curl.

### The edit loop is not in-place

Plasma caches QML aggressively. Editing files under
`~/.local/share/plasma/plasmoids` does not reliably take effect — always
`./install.sh` from this tree, then restart plasmashell.

## Architecture

Data flows one way: config → `github.js` → `ListModel` → delegates.

- **`package/contents/ui/main.qml`** is the only stateful file. It owns the
  `gistModel` `ListModel`, the `loading` / `errorMessage` / `lastUpdated` state,
  the poll `Timer`, and `refresh()`. Both representations and the delegate are
  read-only consumers of that state.
- **`package/contents/code/github.js`** is `.pragma library`, so it has no QML
  context: no `i18n`, no access to ids or `Plasmoid`. Every entry point takes an
  explicit options object and reports through `onSuccess` / `onError` callbacks.
  It also normalises GitHub's response into the flat field names the delegate
  renders (`normalise()`) — add a field there before using it in QML.
- **`CompactRepresentation.qml` / `FullRepresentation.qml` / `GistDelegate.qml`**
  reach up to `root` and `gistModel` by id. That resolves at runtime because
  Plasma instantiates them inside `main.qml`'s scope, but a per-file linter
  cannot see it, which is why `.qmllint.ini` disables `unqualified-access`.
  Real typos in those references therefore only surface in the journal.

### Adding a setting

Three places, and the naming is load-bearing:

1. An `<entry name="foo">` in `package/contents/config/main.xml`.
2. A `property alias cfg_foo:` in `ConfigGeneral.qml` — Plasma binds
   `cfg_<name>` to the matching entry purely by name. A mismatch fails silently.
3. Read it as `Plasmoid.configuration.foo`.

If the setting changes which account is listed, also add an
`on<Foo>Changed` handler to the `Connections { target: Plasmoid.configuration }`
block in `main.qml` so the list refetches.

## Plasma 6 / Qt 6 API notes

Most plasmoid examples online are Plasma 5 and will mislead you:

- Root item is `PlasmoidItem` (from `org.kde.plasma.plasmoid`), not `Item` with
  `Plasmoid.fullRepresentation`. Versionless imports (`import QtQuick`).
- Controls come from `org.kde.plasma.components` (Qt Quick Controls 2 based);
  `PlasmaExtras.Representation`, `PlasmoidHeading` and `PlaceholderMessage` come
  from `org.kde.plasma.extras`. Units and colors from `org.kde.kirigami`, never
  hardcoded pixels.
- Context menu entries are `PlasmaCore.Action` in `Plasmoid.contextualActions`.
  Opening the config dialog is `Plasmoid.internalAction("configure").trigger()`.
- `Qt.DefaultLocaleShortDate` and friends were **removed** in Qt 6 — use
  `Locale.ShortFormat`.

## GitHub API

Two listing modes, chosen by the `listOwnGists` setting:
`GET /users/{user}/gists` (public, no auth) or `GET /gists` (the token's own
gists, public + secret). Unauthenticated requests are capped at 60/hour per IP,
so 403 during development usually means rate limiting, not a bad token —
`errorMessage()` in `github.js` distinguishes the two by response body.

The token is stored in plain text in
`~/.config/plasma-org.kde.plasma.desktop-appletsrc`. Moving it to KWallet would
require introducing a C++ QML plugin.
