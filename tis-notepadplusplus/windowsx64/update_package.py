# -*- coding: utf-8 -*-
from setuphelpers import *
import json

# Declaring global variables - Warnings: 1) WAPT context is only available in package functions; 2) Global variables are not persistent between calls
bin_contains = "npp"


def update_package():
    # Declaring local variables
    result = False
    proxies = get_proxies()
    if not proxies:
        proxies = get_proxies_from_wapt_console()
    if control.architecture == "x64":
        bin_search = "Installer.x64.exe"
        bin_name_sub = "npp.%s.Installer.x64.exe"
    else:
        bin_search = "Installer.exe"
        bin_name_sub = "npp.%s.Installer.exe"
    app_name = control.name
    git_repo = "notepad-plus-plus/notepad-plus-plus"
    url_api = "https://api.github.com/repos/%s/releases/latest" % git_repo

    # Getting latest version information from official sources
    print("API used is: %s" % url_api)
    json_load = json.loads(wgets(url_api, proxies=proxies))
    for download in json_load["assets"]:
        if bin_search in download["name"]:
            url_dl = download["browser_download_url"]
            version = json_load["tag_name"].replace("v", "")
            latest_bin = download["name"]
            break

    print("Latest %s version is: %s" % (app_name, version))
    print("Download URL is: %s" % url_dl)

    # Downloading latest binaries
    if not isfile(latest_bin):
        print("Downloading: %s" % latest_bin)
        wget(url_dl, latest_bin, proxies=proxies)

        # Checking version from file
        version_from_file = get_version_from_binary(latest_bin, "FileVersion")
        if not version_from_file.startswith(version):
            # remove additional .0 at the end of the version from file
            ".".join(get_version_from_binary(latest_bin, "FileVersion").split(".")[:3])
            print("Changing version to the version number of the binary")
            version = version_from_file
            os.rename(latest_bin, bin_name_sub % version)
    # Changing version of the package
    if Version(version) > Version(control.get_software_version()):
        print("Software version updated (from: %s to: %s)" % (control.get_software_version(), Version(version)))
        result = True
    control.version = "%s-%s" % (Version(version), control.version.split("-", 1)[-1])
    # control.set_software_version(Version(version))
    control.save_control_to_wapt()

    # Deleting outdated binaries
    remove_outdated_binaries(version)

    # Validating update-package-sources
    return result
