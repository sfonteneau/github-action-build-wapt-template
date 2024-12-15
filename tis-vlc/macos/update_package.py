from setuphelpers import *

bin_name_string = "vlc-%s-universal.dmg"


def update_package():
    print("Update package content from upstream binary sources")
    from waptpackage import PackageEntry

    # Get Proxy informations from WAPT settings
    proxies = {}
    if isfile(makepath(user_local_appdata(), "waptconsole", "waptconsole.ini")):
        proxywapt = inifile_readstring(makepath(user_local_appdata(), "waptconsole", "waptconsole.ini"), "global", "http_proxy")
        if proxywapt:
            proxies = {"http": proxywapt, "https": proxywapt}

    htmlSource = wgets("https://www.videolan.org/vlc/download-macosx.html", proxies=proxies).splitlines()

    for line in htmlSource:
        if "downloadOS" in line:
            realversion = line[line.find("") + 12 : line.find("</span>")]
            latest_bin = bin_name_string % realversion

    # Deleting outdated binaries
    for actual_bin in glob.glob("*.dmg"):
        if actual_bin == latest_bin:
            continue
        print(actual_bin + " Deleted")
        remove_file(actual_bin)

    # Downloading latest binaires
    if not isfile(latest_bin):
        print("Download " + latest_bin)
        wget("https://get.videolan.org/vlc/" + realversion + "/macosx/" + latest_bin, latest_bin, proxies=proxies)

        pe = PackageEntry().load_control_from_wapt(".")
        pe.version = "%s-%s" % (realversion, int(pe.version.split("-", 1)[1]) + 1)
        pe.save_control_to_wapt(".")
        print("Changing version to " + pe.version + " in WAPT\\control")
