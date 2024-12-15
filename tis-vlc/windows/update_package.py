from setuphelpers import *

bin_contains = "vlc-"


def update_package():
    # Declaring local variables
    result = False
    proxies = get_proxies()
    if not proxies:
        proxies = get_proxies_from_wapt_console()
    app_name = control.name
    htmlSource = wgets("http://www.videolan.org/vlc/download-windows.html", proxies=proxies).splitlines()

    for line in htmlSource:
        if "downloadOS" in line:
            version = line[line.find("") + 12 : line.find("</span>")]

    win_arch = control.architecture.replace("x", "win")
    if win_arch == "win86":
        win_arch = "win32"
    latest_bin = bin_contains + version + "-" + win_arch + ".exe"
    download_url = "https://get.videolan.org/vlc/" + version + "/%s/" % win_arch + latest_bin

    print("Latest %s version is: %s" % (app_name, version))
    print("Download URL is: %s" % download_url)

    # Downloading latest binaries
    if not isfile(latest_bin):
        print("Downloading: %s" % latest_bin)
        wget(download_url, latest_bin, proxies=proxies)

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
