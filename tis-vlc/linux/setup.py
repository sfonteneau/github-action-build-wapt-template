# -*- coding: utf-8 -*-
from setuphelpers import *
import distro

uninstallkey = []
# Declaring specific app values (TO CHANGE)
package_name = "vlc"


def install():
    # Installing the package
    if type_debian():
        update_apt()
        print("Installing: %s" % package_name)
        install_apt(package_name)

    if type_redhat():
        print("Installing: %s" % package_name)
        install_yum("https://download1.rpmfusion.org/free/el/rpmfusion-free-release-%s.noarch.rpm" % distro.linux_distribution()[1].split(".")[0])
        install_yum(package_name)


def uninstall():
    # Uninstalling the package
    if type_debian():
        print("Uninstalling: %s" % package_name)
        uninstall_apt(package_name)
        autoremove_apt()

    if type_redhat():
        print("Uninstalling: %s" % package_name)
        uninstall_yum(package_name)
        autoremove_yum()


def session_setup():
    print("Setting up default preferences for VLC")

    # Specific app values
    user_conf_dir = makepath(user_home_directory(), ".config", "vlc")
    user_conf_file = makepath(user_conf_dir, "vlcrc")
    vlcrc_content = """[qt] # Qt interface
qt-notification=0
qt-privacy-ask=0
metadata-network-access=0
"""

    if not isfile(user_conf_file):
        if not isdir(user_conf_dir):
            mkdirs(user_conf_dir)
        fichier = open(user_conf_file, "w")
        fichier.write(vlcrc_content)
        fichier.close()
    else:
        fichier = open(user_conf_file, "r")
        data = fichier.read()
        fichier.close()

        if "#qt-notification=1" in data:
            data = data.replace("#qt-notification=1", "qt-notification=0")
        if "qt-notification=1" in data:
            data = data.replace("qt-notification=1", "qt-notification=0")
        if "#qt-privacy-ask=1" in data:
            data = data.replace("#qt-privacy-ask=1", "qt-privacy-ask=0")
        if "qt-privacy-ask=1" in data:
            data = data.replace("qt-privacy-ask=1", "qt-privacy-ask=0")
        if "#metadata-network-access=1" in data:
            data = data.replace("#metadata-network-access=1", "metadata-network-access=0")
        if "metadata-network-access=1" in data:
            data = data.replace("metadata-network-access=1", "metadata-network-access=0")

        fichier = open(user_conf_file, "w")
        fichier.write(data)
        fichier.close()

def update_package():
    pass
