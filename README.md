# GitHub Gists — Plasma 6 widget

A Plasma 6 applet that lists GitHub gists in the panel or on the desktop.
Clicking a gist opens it in the browser.

Targets Plasma 6.x / Qt 6 (developed against Plasma 6.7).

## Layout

```
package/
├── metadata.json                 Plugin id, name, category, API version
└── contents/
    ├── config/
    │   ├── main.xml              KConfigXT schema — the settings themselves
    │   └── config.qml            Which pages the config dialog shows
    ├── code/
    │   └── github.js             REST client (pragma library, no QML context)
    └── ui/
        ├── main.qml              PlasmoidItem: state, model, refresh timer
        ├── CompactRepresentation.qml   Panel icon + count badge
        ├── FullRepresentation.qml      Popup: header, list, placeholder, footer
        ├── GistDelegate.qml            One row
        └── ConfigGeneral.qml           Settings page
CMakeLists.txt                    System-wide install via plasma_install_package
install.sh                        Per-user install via kpackagetool6
```

## Installing

Per user, no build dependencies:

```sh
./install.sh
systemctl --user restart plasma-plasmashell
```

System-wide:

```sh
cmake -B build -DCMAKE_INSTALL_PREFIX="$(kf6-config --prefix)"
cmake --build build
sudo cmake --install build
```

Then: right-click the desktop or panel → *Add Widgets…* → *GitHub Gists*.

## Configuring

| Setting | Meaning |
| --- | --- |
| Username | Whose **public** gists to list |
| List my own gists | Use `GET /gists` instead — public *and* secret, needs a token |
| Access token | Fine-grained PAT with read-only Gists access |
| Gists to show | `per_page`, 1–100 |
| Refresh every | Minutes; `0` disables polling |

Unauthenticated requests to api.github.com are capped at 60/hour per IP; a
token raises that to 5000/hour.

### Token storage

The token is written to the plasmoid's config file
(`~/.config/plasma-org.kde.plasma.desktop-appletsrc`) in plain text. That file
is user-readable only, but it is not a secret store. Moving the token into
KWallet needs a small C++ plugin — see *Next steps*.

## Development

### Previewing

Fastest loop — run the applet in its own window, no panel and no shell restart:

```sh
./install.sh
plasmawindowed com.github.nmartin867.gists
```

`plasmawindowed` ships with plasma-workspace, so it is already present. It
renders the **full** representation only; to exercise the compact
representation and the panel/desktop form factors you need `plasmoidviewer`
from the `plasma-sdk` package:

```sh
sudo pacman -S plasma-sdk
plasmoidviewer -a package -f horizontal   # as if docked in a panel
plasmoidviewer -a package -f planar       # as if on the desktop
plasmoidviewer --help                     # form factors, locations, themes
```

Finally, in the real shell: *Add Widgets…* → *GitHub Gists*, or drag it onto a
panel. This is the only way to check that the compact representation sizes
correctly against a real panel thickness, and that `switchWidth` /
`switchHeight` in `main.qml` flip the representation where you expect.

### The reinstall loop

Plasma caches QML aggressively, and editing the installed copy under
`~/.local/share/plasma/plasmoids/` is **not** reliably picked up. Always
reinstall from this tree, then restart the shell:

```sh
./install.sh && systemctl --user restart plasma-plasmashell
```

The restart takes over the current session's plasmashell — the panel and
desktop blink out for a second or two. Windows are unaffected.

To check what is currently installed, or to get back to a clean slate:

```sh
kpackagetool6 --type Plasma/Applet --list | grep gists
kpackagetool6 --type Plasma/Applet --remove com.github.nmartin867.gists
```

### Debugging

QML errors and warnings never reach the terminal that launched the shell — they
go to the journal. Keep this running in a second pane:

```sh
journalctl --user -u plasma-plasmashell -f
```

`console.log()` from any of the QML files lands in the same place. A prefix
makes it greppable amid the rest of the shell's chatter:

```sh
journalctl --user -u plasma-plasmashell -f | grep -a '\[gists\]'
```

Under `plasmawindowed` the applet is a plain process, so `console.log` goes
straight to your terminal and `-d` attaches a QML/JS debugger:

```sh
plasmawindowed -d com.github.nmartin867.gists
```

Two environment variables worth knowing when things fail silently — an import
that resolves in `qmllint` but not at runtime is the classic case:

```sh
QML_IMPORT_TRACE=1 plasmawindowed com.github.nmartin867.gists
QT_LOGGING_RULES='qt.qml.binding.removal.info=true' plasmawindowed com.github.nmartin867.gists
```

The shell also has a live scripting console, useful for poking at a running
instance without a restart:

```sh
qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript \
    'print(panels()[0].widgets().map(w => w.type).join("\n"))'
```

#### Settings

Configuration lives in one big INI file, keyed by applet instance id, not by
plugin name — so find the group before reading it:

```sh
grep -n -A12 'gists' ~/.config/plasma-org.kde.plasma.desktop-appletsrc
```

Removing and re-adding the widget is the reliable way to reset a bad
configuration, since `main.xml` defaults only apply to a fresh instance.

#### The GitHub request

When the list is empty or errors, take QML out of the picture and reproduce the
exact request `github.js` makes:

```sh
# What the widget sends for a public-gists lookup
curl -sD- -o /dev/null \
    -H 'Accept: application/vnd.github+json' \
    -H 'X-GitHub-Api-Version: 2022-11-28' \
    'https://api.github.com/users/octocat/gists?per_page=30'

# Is a 403 rate limiting, or a bad token?
curl -s https://api.github.com/rate_limit | jq '.rate'
```

An unauthenticated 60/hour ceiling is easy to hit while iterating, especially
with a short refresh interval — a 403 during development is far more often rate
limiting than a credential problem.

### Linting and formatting

```sh
/usr/lib/qt6/bin/qmllint -I /usr/lib/qt6/qml \
    package/contents/ui/*.qml package/contents/config/*.qml
/usr/lib/qt6/bin/qmlformat -i package/contents/ui/*.qml
```

The `-I` is not optional: without it every Plasma and Kirigami import fails and
the output is nothing but import errors. `qmllint` is the only automated check
in the project — there is no test suite.

`.qmllint.ini` disables `unqualified-access`. The representations legitimately
reach for `root` and `gistModel` declared in `main.qml`, and the delegate reads
its `model` context property; none of that is visible to a per-file linter. The
tradeoff is that a genuine typo in one of those references only shows up in the
journal at runtime.

## Next steps

- Translations: add `po/` and wire up `ki18n_install` in CMakeLists.txt.
- KWallet-backed token storage (needs a C++ QML plugin).
- Inline file preview using the gist `raw_url` and Kirigami syntax highlighting.
- Starred gists (`GET /gists/starred`) as a third listing mode.
- Etag-based conditional requests so polling does not burn rate limit.
