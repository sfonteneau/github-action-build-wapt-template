from setuphelpers import *
import shutil

bin_name_string = "vlc-%s-universal.dmg"


def install():
    package_version = control.version.split("-", 1)[0]
    install_dmg(bin_name_string % package_version)


def uninstall():
    shutil.rmtree("/Applications/VLC.app")
