import QtQuick

import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami

import "../code/github.js" as GitHub

PlasmoidItem {
    id: root

    readonly property bool configured: Plasmoid.configuration.listOwnGists
        ? Plasmoid.configuration.token !== ""
        : Plasmoid.configuration.username !== ""

    property bool loading: false
    property string errorMessage: ""
    property date lastUpdated: new Date(0)

    switchWidth: Kirigami.Units.gridUnit * 14
    switchHeight: Kirigami.Units.gridUnit * 12

    Plasmoid.icon: "text-x-generic"
    Plasmoid.status: errorMessage !== ""
        ? PlasmaCore.Types.NeedsAttentionStatus
        : PlasmaCore.Types.PassiveStatus

    toolTipMainText: i18n("GitHub Gists")
    toolTipSubText: {
        if (!configured) {
            return i18n("Not configured");
        }
        if (errorMessage !== "") {
            return errorMessage;
        }
        return i18np("%1 gist", "%1 gists", gistModel.count);
    }

    ListModel {
        id: gistModel
    }

    compactRepresentation: CompactRepresentation {}
    fullRepresentation: FullRepresentation {}

    /*
     * Replace the model contents in one pass. ListModel has no bulk assign, so
     * clear-then-append is the only option; the list is small enough (<=100)
     * that the churn is not worth a C++-side model.
     */
    function refresh() {
        if (!configured || loading) {
            return;
        }

        loading = true;
        errorMessage = "";

        GitHub.fetchGists({
            listOwnGists: Plasmoid.configuration.listOwnGists,
            username: Plasmoid.configuration.username,
            token: Plasmoid.configuration.token,
            maxGists: Plasmoid.configuration.maxGists
        }, function(gists) {
            gistModel.clear();
            for (var i = 0; i < gists.length; ++i) {
                gistModel.append(gists[i]);
            }
            root.lastUpdated = new Date();
            root.loading = false;
        }, function(message) {
            gistModel.clear();
            root.errorMessage = message;
            root.loading = false;
        });
    }

    Timer {
        interval: Math.max(1, Plasmoid.configuration.refreshInterval) * 60 * 1000
        running: Plasmoid.configuration.refreshInterval > 0 && root.configured
        repeat: true
        onTriggered: root.refresh()
    }

    // Re-fetch whenever the account being watched changes.
    Connections {
        target: Plasmoid.configuration
        function onUsernameChanged() { root.refresh(); }
        function onTokenChanged() { root.refresh(); }
        function onListOwnGistsChanged() { root.refresh(); }
        function onMaxGistsChanged() { root.refresh(); }
    }

    Plasmoid.contextualActions: [
        PlasmaCore.Action {
            text: i18n("Refresh")
            icon.name: "view-refresh"
            enabled: root.configured && !root.loading
            onTriggered: root.refresh()
        }
    ]

    Component.onCompleted: refresh()
}
