import QtQuick
import QtQuick.Controls as QQC2
import QtQuick.Layouts

import org.kde.plasma.components as PlasmaComponents3
import org.kde.plasma.extras as PlasmaExtras
import org.kde.plasma.plasmoid
import org.kde.kirigami as Kirigami

PlasmaExtras.Representation {
    id: full

    // Reading code in a narrow column is miserable, so the popup is wider
    // than a typical plasmoid's.
    Layout.minimumWidth: Kirigami.Units.gridUnit * 20
    Layout.minimumHeight: Kirigami.Units.gridUnit * 16
    Layout.preferredWidth: Kirigami.Units.gridUnit * 30
    Layout.preferredHeight: Kirigami.Units.gridUnit * 26

    readonly property bool showingDetail: root.selectedGistId !== ""

    collapseMarginsHint: true

    header: PlasmaExtras.PlasmoidHeading {
        contentItem: RowLayout {
            spacing: Kirigami.Units.smallSpacing

            PlasmaComponents3.ToolButton {
                visible: full.showingDetail
                icon.name: "draw-arrow-back"
                display: QQC2.AbstractButton.IconOnly
                text: i18n("Back to list")
                onClicked: root.closeGist()

                PlasmaComponents3.ToolTip.text: text
                PlasmaComponents3.ToolTip.visible: hovered
                PlasmaComponents3.ToolTip.delay: Kirigami.Units.toolTipDelay
            }

            PlasmaExtras.Heading {
                Layout.fillWidth: true
                level: 4
                elide: Text.ElideRight
                text: {
                    if (full.showingDetail) {
                        if (root.selectedGist === null) {
                            return i18n("Loading…");
                        }
                        return root.selectedGist.description !== ""
                            ? root.selectedGist.description
                            : root.selectedGist.files[0].filename;
                    }
                    return Plasmoid.configuration.listOwnGists
                        ? i18n("My Gists")
                        : i18n("Gists of %1", Plasmoid.configuration.username);
                }
            }

            PlasmaComponents3.ToolButton {
                visible: full.showingDetail
                icon.name: "internet-web-browser"
                display: QQC2.AbstractButton.IconOnly
                text: i18n("View on Web")
                onClicked: Qt.openUrlExternally(root.selectedGist
                    ? root.selectedGist.htmlUrl
                    : "https://gist.github.com/" + root.selectedGistId)

                PlasmaComponents3.ToolTip.text: text
                PlasmaComponents3.ToolTip.visible: hovered
                PlasmaComponents3.ToolTip.delay: Kirigami.Units.toolTipDelay
            }

            PlasmaComponents3.ToolButton {
                visible: !full.showingDetail
                icon.name: "view-refresh"
                enabled: root.configured && !root.loading
                display: QQC2.AbstractButton.IconOnly
                text: i18n("Refresh")
                onClicked: root.refresh()

                PlasmaComponents3.ToolTip.text: text
                PlasmaComponents3.ToolTip.visible: hovered
                PlasmaComponents3.ToolTip.delay: Kirigami.Units.toolTipDelay
            }

            PlasmaComponents3.ToolButton {
                visible: !full.showingDetail
                icon.name: "configure"
                display: QQC2.AbstractButton.IconOnly
                text: i18n("Configure…")
                onClicked: Plasmoid.internalAction("configure").trigger()

                PlasmaComponents3.ToolTip.text: text
                PlasmaComponents3.ToolTip.visible: hovered
                PlasmaComponents3.ToolTip.delay: Kirigami.Units.toolTipDelay
            }
        }
    }

    contentItem: StackLayout {
        currentIndex: full.showingDetail ? 1 : 0

        PlasmaComponents3.ScrollView {
            id: scrollView
            contentWidth: availableWidth

            ListView {
                id: gistList
                model: gistModel
                clip: true
                currentIndex: -1
                reuseItems: true
                boundsBehavior: Flickable.StopAtBounds

                delegate: GistDelegate {
                    width: gistList.width
                }

                // One placeholder covers every empty state: unconfigured,
                // loading, request failed, or simply no gists on the account.
                PlasmaExtras.PlaceholderMessage {
                    anchors.centerIn: parent
                    width: parent.width - (Kirigami.Units.gridUnit * 4)
                    visible: gistList.count === 0

                    iconName: {
                        if (!root.configured) return "configure";
                        if (root.errorMessage !== "") return "dialog-error";
                        return "text-x-generic";
                    }
                    text: {
                        if (!root.configured) return i18n("Not configured");
                        if (root.loading) return i18n("Loading…");
                        if (root.errorMessage !== "") return i18n("Could not load gists");
                        return i18n("No gists");
                    }
                    explanation: {
                        if (!root.configured) {
                            return Plasmoid.configuration.listOwnGists
                                ? i18n("Add a personal access token to list your own gists.")
                                : i18n("Set a GitHub username in the widget settings.");
                        }
                        return root.errorMessage;
                    }

                    helpfulAction: Kirigami.Action {
                        visible: !root.configured
                        icon.name: "configure"
                        text: i18n("Configure…")
                        onTriggered: Plasmoid.internalAction("configure").trigger()
                    }
                }
            }
        }

        GistDetail {}
    }

    footer: PlasmaExtras.PlasmoidHeading {
        position: PlasmaExtras.PlasmoidHeading.Position.Footer
        visible: !full.showingDetail && root.lastUpdated.getTime() > 0

        contentItem: PlasmaComponents3.Label {
            horizontalAlignment: Text.AlignHCenter
            font: Kirigami.Theme.smallFont
            opacity: 0.7
            elide: Text.ElideRight
            text: i18n("Updated %1", Qt.formatTime(root.lastUpdated, Locale.ShortFormat))
        }
    }
}
