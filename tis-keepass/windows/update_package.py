# -*- coding: utf-8 -*-
from setuphelpers import *
import platform
import requests
import time


def update_package():
    print("Download/Update package content from upstream binary sources")

    # Getting proxy informations from WAPT settings
    proxy = {}
    if platform.system() == "Windows" and isfile(makepath(user_local_appdata(), "waptconsole", "waptconsole.ini")):
        proxywapt = inifile_readstring(makepath(user_local_appdata(), "waptconsole", "waptconsole.ini"), "global", "http_proxy")
        if proxywapt:
            proxy = {"http": proxywapt, "https": proxywapt}

    url = requests.head("https://sourceforge.net/projects/keepass/files/latest/download?source=files", proxies=proxy).headers["Location"]
    dstzip = requests.head(url, proxies=proxy).headers["Location"]
    filename = dstzip.rsplit("/", 1)[1]

    print(filename)
    version = filename.replace("KeePass-", "").split(".zip")[0]

    filenameexe = "KeePass-%s-Setup.exe" % version
    dstexe = dstzip.replace(filename, filenameexe)
    print("Latest Version : " + version)

    exes = glob.glob("*.exe")
    for fn in exes:
        if fn != filenameexe:
            remove_file(fn)

    if not isfile(filenameexe):
        print("Downloading %s " % (filenameexe))
        wget(dstexe, filenameexe, proxies=proxy)
    else:
        print("Already up to date, skipped")

    control.version = "%s-%s" % (version, int(control.version.split("-", 1)[1]) + 1)
    control.save_control_to_wapt()
    print("Changing version to " + control.version + " in WAPT\\control")
    print("Update package done. You can now build-upload your package")

    for lngx in glob.glob("*.lngx"):
        remove_file(lngx)

    for line in wgets("https://keepass.info/translations.html", proxies=proxy).splitlines():
        if "KeePass-%s" % version[:2] in line:
            lfd = line.replace('<td><a href="', "").replace('" target="_blank">', "")
            if not "-Help-" in lfd.rsplit("/", 1)[1]:
                if not lfd.startswith('http'):
                    lfd = "https://keepass.info/" + lfd 
                # BUG
                if not "Portuguese_BR" in lfd.rsplit("/", 1)[1]:
                    try:
                        print("Try Download %s" % lfd)
                        wget(lfd, lfd.rsplit("/", 1)[1], connect_timeout=30, proxies=proxy)
                    except:
                        # Try Again
                        wget(lfd, lfd.rsplit("/", 1)[1], connect_timeout=30, proxies=proxy)

                    unzip(lfd.rsplit("/", 1)[1], target=".")

                    remove_file(lfd.rsplit("/", 1)[1])

                    time.sleep(2)


