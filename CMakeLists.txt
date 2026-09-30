cmake_minimum_required(VERSION 3.20)

project(plasma-gist-widget VERSION 0.1.0)

set(QT_MIN_VERSION 6.6.0)
set(KF6_MIN_VERSION 6.0.0)

find_package(ECM ${KF6_MIN_VERSION} REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH})

include(KDEInstallDirs)
include(KDECMakeSettings)
include(KDECompilerSettings NO_POLICY_SCOPE)

find_package(Plasma ${KF6_MIN_VERSION} REQUIRED)

plasma_install_package(package com.github.nmartin867.gists)

# Also install the applet icon into the system icon theme. The copy inside the
# package is the source of truth; KIconLoader only ever finds this one.
install(DIRECTORY package/contents/icons/hicolor
        DESTINATION ${KDE_INSTALL_ICONDIR})
