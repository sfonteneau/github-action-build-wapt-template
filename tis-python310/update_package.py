# -*- coding: utf-8 -*-
from setuphelpers import *


def update_package():
    # Declaring local variables
    result = False
    proxies = get_proxies()
    if not proxies:
        proxies = get_proxies_from_wapt_console()
    app_name = control.name
    url = "https://www.python.org/downloads/windows/"
    if control.architecture == "x64":
        arch = "64-bit"
    else:
        arch = "32-bit"

    # Getting latest version from official sources
    version = None
    for bs_search in bs_find_all(url, "a", proxies=proxies):
        if bs_search.string:
            if "https://www.python.org/ftp/python/3.10" in bs_search["href"] and "Windows installer (%s)" % arch in bs_search.string:
                version = bs_search["href"].split("/")[-2]
                latest_bin = bs_search["href"].split("/")[-1]
                download_url = bs_search["href"]
                break

    print("Latest %s version is: %s" % (app_name, version))
    print("Download URL is: %s" % download_url)

    # Downloading latest binaries
    if not isfile(latest_bin):
        print("Downloading: %s" % latest_bin)
        wget(download_url, latest_bin, proxies=proxies)

        # Checking version from file
        version_from_file = get_version_from_binary(latest_bin, "ProductName").split(" (")[0].split(" ")[-1]
        if Version(version) != Version(version_from_file) and version_from_file != "":
            print("Changing version to the version number of the binary (from: %s to: %s)" % (version, version_from_file))
            os.rename(latest_bin, bin_contains + version_from_file + latest_bin.split(version)[-1])
            version = version_from_file

    # Changing version of the package
    if Version(version) > Version(control.get_software_version()):
        print("Software version updated (from: %s to: %s)" % (control.get_software_version(), Version(version)))
        result = True
    else:
        print("Software version up-to-date (%s)" % Version(version))
    control.version = "%s-%s" % (Version(version), control.version.split("-", 1)[-1])
    # control.set_software_version(version)
    control.save_control_to_wapt()

    # Deleting outdated binaries
    remove_outdated_binaries(version)

    # Validating or not update-package-sources
    return result
