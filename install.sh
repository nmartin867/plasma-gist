#!/usr/bin/env bash
# Install (or reinstall) the widget into ~/.local/share/plasma/plasmoids
# without needing CMake or extra-cmake-modules.
set -euo pipefail

ID="com.github.nmartin867.gists"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/package"

if kpackagetool6 --type Plasma/Applet --show "$ID" >/dev/null 2>&1; then
    kpackagetool6 --type Plasma/Applet --upgrade "$SRC"
else
    kpackagetool6 --type Plasma/Applet --install "$SRC"
fi

# The applet icon has to live in an icon theme, not just in the package:
# KIconLoader resolves metadata.json's Icon through the theme search path and
# knows nothing about plasmoid packages. contents/icons/hicolor mirrors the
# theme layout so this is a plain copy.
ICONS="$(dirname "$SRC")/package/contents/icons/hicolor"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor"
mkdir -p "$DEST"
cp -r "$ICONS/." "$DEST/"
echo "Installed icon into $DEST"

echo "Installed. Restart Plasma to pick up changes:"
echo "  systemctl --user restart plasma-plasmashell"
