import QtQuick
import QtQuick.Controls as QQC2
import QtQuick.Layouts

import org.kde.kirigami as Kirigami

Kirigami.FormLayout {
    id: page

    // Each `cfg_<name>` property is bound by Plasma to the matching entry in
    // config/main.xml; the naming is what wires save/restore up.
    property alias cfg_username: usernameField.text
    property alias cfg_token: tokenField.text
    property alias cfg_listOwnGists: ownGistsCheck.checked
    property alias cfg_maxGists: maxGistsSpin.value
    property alias cfg_refreshInterval: refreshSpin.value
    property alias cfg_showDescriptionTooltip: tooltipCheck.checked

    QQC2.TextField {
        id: usernameField
        Kirigami.FormData.label: i18n("Username:")
        enabled: !ownGistsCheck.checked
        placeholderText: i18n("octocat")
    }

    QQC2.CheckBox {
        id: ownGistsCheck
        Kirigami.FormData.label: i18n("Account:")
        text: i18n("List my own gists (requires a token)")
    }

    QQC2.TextField {
        id: tokenField
        Kirigami.FormData.label: i18n("Access token:")
        echoMode: TextInput.Password
        placeholderText: i18n("Optional — raises the rate limit")
    }

    QQC2.Label {
        Layout.maximumWidth: Kirigami.Units.gridUnit * 20
        wrapMode: Text.WordWrap
        font: Kirigami.Theme.smallFont
        text: i18n("A fine-grained token with read-only Gists access is enough. It is stored in the widget's plain-text config file.")
    }

    Item {
        Kirigami.FormData.isSection: true
    }

    QQC2.SpinBox {
        id: maxGistsSpin
        Kirigami.FormData.label: i18n("Gists to show:")
        from: 1
        to: 100
    }

    QQC2.SpinBox {
        id: refreshSpin
        Kirigami.FormData.label: i18n("Refresh every:")
        from: 0
        to: 1440
        textFromValue: function(value) {
            return value === 0 ? i18n("Never") : i18np("%1 minute", "%1 minutes", value);
        }
        valueFromText: function(text) {
            return parseInt(text, 10) || 0;
        }
    }

    QQC2.CheckBox {
        id: tooltipCheck
        Kirigami.FormData.label: i18n("Tooltips:")
        text: i18n("Show full description on hover")
    }
}
