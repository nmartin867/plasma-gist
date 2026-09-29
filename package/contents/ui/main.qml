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

    // Detail view. `selectedGist` is null until the second request lands, so
    // `selectedGistId` is what decides which page the popup shows.
    property string selectedGistId: ""
    property var selectedGist: null
    property bool detailLoading: false
    property string detailError: ""

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
        closeGist();

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

    /*
     * Open a gist inside the popup. The list response carries no file bodies,
     * so this always costs a second request; the id is set immediately so the
     * view can switch and show its own spinner.
     */
    function openGist(id) {
        selectedGistId = id;
        selectedGist = null;
        detailError = "";
        detailLoading = true;

        GitHub.fetchGist(id, {
            token: Plasmoid.configuration.token
        }, function(gist) {
            // Ignore a response for a gist the user has already navigated away from.
            if (root.selectedGistId !== gist.id) {
                return;
            }
            root.selectedGist = gist;
            root.detailLoading = false;
        }, function(message) {
            if (root.selectedGistId !== id) {
                return;
            }
            root.detailError = message;
            root.detailLoading = false;
        });
    }

    function closeGist() {
        selectedGistId = "";
        selectedGist = null;
        detailError = "";
        detailLoading = false;
    }

    // Reopening the popup should land on the list, not on whatever was last read.
    onExpandedChanged: {
        if (!expanded) {
            closeGist();
        }
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
