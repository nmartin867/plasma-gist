import QtQuick

import org.kde.plasma.plasmoid
import org.kde.kirigami as Kirigami

MouseArea {
    id: compact

    property bool wasExpanded: false

    Kirigami.Icon {
        anchors.fill: parent
        source: Plasmoid.icon
        active: compact.containsMouse
    }

    // Unread-style badge carrying the gist count.
    Rectangle {
        visible: gistModel.count > 0
        anchors {
            right: parent.right
            bottom: parent.bottom
        }
        width: Math.max(height, countLabel.implicitWidth + Kirigami.Units.smallSpacing)
        height: Math.round(parent.height / 2.5)
        radius: height / 2
        color: Kirigami.Theme.highlightColor

        Text {
            id: countLabel
            anchors.centerIn: parent
            text: gistModel.count
            color: Kirigami.Theme.highlightedTextColor
            font.pixelSize: Math.round(parent.height * 0.7)
        }
    }

    // Plasma toggles the popup on release, so the press only records state.
    onPressed: wasExpanded = root.expanded
    onClicked: root.expanded = !wasExpanded
}
