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

echo "Installed. Restart Plasma to pick up changes:"
echo "  systemctl --user restart plasma-plasmashell"
