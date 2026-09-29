import QtQuick
import QtQuick.Controls as QQC2
import QtQuick.Layouts

import org.kde.plasma.components as PlasmaComponents3
import org.kde.plasma.plasmoid
import org.kde.kirigami as Kirigami

PlasmaComponents3.ItemDelegate {
    id: delegate

    // A gist has no title; GitHub itself falls back to the first filename.
    readonly property string title: model.description !== ""
        ? model.description
        : model.primaryFilename

    hoverEnabled: true
    height: layout.implicitHeight + (Kirigami.Units.smallSpacing * 2)

    // Opens in the popup; the browser is one more click away, in the header.
    onClicked: root.openGist(model.id)

    PlasmaComponents3.ToolTip.text: model.description
    PlasmaComponents3.ToolTip.visible: Plasmoid.configuration.showDescriptionTooltip
        && hovered && model.description !== ""
    PlasmaComponents3.ToolTip.delay: Kirigami.Units.toolTipDelay

    contentItem: RowLayout {
        id: layout
        spacing: Kirigami.Units.smallSpacing

        Kirigami.Icon {
            Layout.alignment: Qt.AlignTop
            implicitWidth: Kirigami.Units.iconSizes.smallMedium
            implicitHeight: Kirigami.Units.iconSizes.smallMedium
            source: model.isPublic ? "text-x-generic" : "object-locked"
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 0

            PlasmaComponents3.Label {
                Layout.fillWidth: true
                text: delegate.title
                elide: Text.ElideRight
                maximumLineCount: 1
            }

            PlasmaComponents3.Label {
                Layout.fillWidth: true
                font: Kirigami.Theme.smallFont
                opacity: 0.7
                elide: Text.ElideRight
                maximumLineCount: 1
                text: [
                    model.language,
                    i18np("%1 file", "%1 files", model.fileCount),
                    model.commentCount > 0
                        ? i18np("%1 comment", "%1 comments", model.commentCount)
                        : ""
                ].filter(function(part) { return part !== ""; }).join(" · ")
            }
        }

        PlasmaComponents3.ToolButton {
            visible: delegate.hovered
            icon.name: "internet-web-browser"
            text: i18n("View on Web")
            display: QQC2.AbstractButton.IconOnly
            onClicked: Qt.openUrlExternally(model.htmlUrl)

            PlasmaComponents3.ToolTip.text: text
            PlasmaComponents3.ToolTip.visible: hovered
            PlasmaComponents3.ToolTip.delay: Kirigami.Units.toolTipDelay
        }

        PlasmaComponents3.ToolButton {
            visible: delegate.hovered
            icon.name: "edit-copy"
            text: i18n("Copy URL")
            display: QQC2.AbstractButton.IconOnly
            onClicked: clipboardHelper.copy(model.htmlUrl)

            PlasmaComponents3.ToolTip.text: text
            PlasmaComponents3.ToolTip.visible: hovered
            PlasmaComponents3.ToolTip.delay: Kirigami.Units.toolTipDelay
        }
    }

    /*
     * QML has no clipboard API, so round-trip through a hidden TextEdit —
     * the standard workaround for plasmoids that avoid a C++ plugin.
     */
    TextEdit {
        id: clipboardHelper
        visible: false

        function copy(text) {
            clipboardHelper.text = text;
            clipboardHelper.selectAll();
            clipboardHelper.copy();
        }
    }
}
