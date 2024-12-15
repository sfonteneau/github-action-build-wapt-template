from setuphelpers import *

app_uninstallkey = "VLC media player"


def install():
    # Declaring local variables
    bin_name = glob.glob("*.exe")[0]

    # Uninstalling wrong arch of software
    for to_uninstall in installed_softwares(uninstallkey=app_uninstallkey):
        if iswin64() and not to_uninstall["win64"]:
            print("Removing: %s (%s)" % (to_uninstall["name"], to_uninstall["version"]))
            killalltasks(control.impacted_process.split(","))
            run(uninstall_cmd(to_uninstall["key"]))
            wait_uninstallkey_absent(to_uninstall["key"], 20)

    # Installing the software
    print("Installing: %s" % bin_name)
    install_exe_if_needed(
        bin_name,
        silentflags="/S",
        key=app_uninstallkey,
        min_version=control.get_software_version(),
    )

    # Removing application desktop shortcut if allowed
    if params.get("remove_desktop_shortcuts"):
        remove_desktop_shortcut(control.name)


def session_setup():
    print("Setting up default preferences for VLC")

    # Specific app values
    user_conf_dir = makepath(user_appdata, "vlc")
    user_conf_file = makepath(user_appdata, "vlc", "vlcrc")
    vlcrc_content = """[qt] # Qt interface
qt-notification=0
qt-updates-notif=0
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
        if "#qt-updates-notif=1" in data:
            data = data.replace("#qt-updates-notif=1", "qt-updates-notif=0")
        if "qt-updates-notif=1" in data:
            data = data.replace("qt-updates-notif=1", "qt-updates-notif=0")
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
