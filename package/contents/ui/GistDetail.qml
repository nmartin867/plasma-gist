import QtQuick
import QtQuick.Layouts

import org.kde.plasma.components as PlasmaComponents3
import org.kde.plasma.extras as PlasmaExtras
import org.kde.kirigami as Kirigami
import org.kde.syntaxhighlighting as SyntaxHighlighting

/*
 * The in-popup reader for a single gist: every file, one after another, with
 * its body highlighted according to the language GitHub reports.
 */
Item {
    id: detail

    PlasmaComponents3.BusyIndicator {
        anchors.centerIn: parent
        running: root.detailLoading
        visible: running
    }

    PlasmaExtras.PlaceholderMessage {
        anchors.centerIn: parent
        width: parent.width - (Kirigami.Units.gridUnit * 4)
        visible: root.detailError !== ""

        iconName: "dialog-error"
        text: i18n("Could not open this gist")
        explanation: root.detailError

        helpfulAction: Kirigami.Action {
            icon.name: "internet-web-browser"
            text: i18n("View on Web")
            onTriggered: Qt.openUrlExternally(root.selectedGist
                ? root.selectedGist.htmlUrl
                : "https://gist.github.com/" + root.selectedGistId)
        }
    }

    PlasmaComponents3.ScrollView {
        id: scrollView
        anchors.fill: parent
        visible: root.selectedGist !== null

        // Code should scroll sideways rather than wrap, so the content is
        // allowed to exceed the viewport width.
        contentWidth: Math.max(availableWidth, files.implicitWidth)

        ColumnLayout {
            id: files
            width: scrollView.availableWidth
            spacing: Kirigami.Units.largeSpacing

            Repeater {
                model: root.selectedGist ? root.selectedGist.files : []

                ColumnLayout {
                    id: fileBlock

                    required property var modelData

                    Layout.fillWidth: true
                    spacing: Kirigami.Units.smallSpacing

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: Kirigami.Units.smallSpacing

                        Kirigami.Icon {
                            implicitWidth: Kirigami.Units.iconSizes.small
                            implicitHeight: Kirigami.Units.iconSizes.small
                            source: "text-x-generic"
                        }

                        PlasmaComponents3.Label {
                            Layout.fillWidth: true
                            text: fileBlock.modelData.filename
                            font.bold: true
                            elide: Text.ElideRight
                        }

                        PlasmaComponents3.Label {
                            font: Kirigami.Theme.smallFont
                            opacity: 0.7
                            text: fileBlock.modelData.language
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: body.implicitHeight + (Kirigami.Units.smallSpacing * 2)
                        radius: Kirigami.Units.cornerRadius
                        color: Kirigami.Theme.alternateBackgroundColor
                        border.width: 1
                        border.color: Kirigami.ColorUtils.linearInterpolation(
                            Kirigami.Theme.backgroundColor,
                            Kirigami.Theme.textColor, 0.15)

                        TextEdit {
                            id: body

                            anchors.fill: parent
                            anchors.margins: Kirigami.Units.smallSpacing

                            text: fileBlock.modelData.content
                            font: Kirigami.Theme.fixedWidthFont
                            color: Kirigami.Theme.textColor
                            selectionColor: Kirigami.Theme.highlightColor
                            selectedTextColor: Kirigami.Theme.highlightedTextColor

                            readOnly: true
                            selectByMouse: true
                            wrapMode: TextEdit.NoWrap
                            textFormat: TextEdit.PlainText
                        }

                        // setDefinition() takes the language name GitHub
                        // reports; an unknown name simply leaves it unstyled.
                        SyntaxHighlighting.SyntaxHighlighter {
                            textEdit: body
                            definition: fileBlock.modelData.language
                        }
                    }

                    PlasmaComponents3.Label {
                        Layout.fillWidth: true
                        visible: fileBlock.modelData.truncated
                        font: Kirigami.Theme.smallFont
                        opacity: 0.7
                        wrapMode: Text.WordWrap
                        text: i18n("This file is too large to show in full — open it on the web to read the rest.")
                    }
                }
            }
        }
    }
}
