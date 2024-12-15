# -*- coding: utf-8 -*-
from setuphelpers import *
import requests

r""" PS C:\waptdev\wapt-packages\7zip> wapt-get list-registry zip --json
{
 "output":[],
 "config_filename":"C:\\Program Files (x86)\\wapt\\wapt-get.ini",
 "result":[
  {
   "key":"7-Zip",
   "name":"7-Zip 22.01 (x64)",
   "version":"22.01",
   "install_date":"",
   "install_location":"C:\\Program Files\\7-Zip\\",
   "uninstall_string":"\"C:\\Program Files\\7-Zip\\Uninstall.exe\"",
   "publisher":"Igor Pavlov",
   "system_component":0,
   "win64":true
  },
  {
   "key":"{23170F69-40C1-2702-2201-000001000000}",
   "name":"7-Zip 22.01 (x64 edition)",
   "version":"22.01.00.0",
   "install_date":"2023-06-20 00:00:00",
   "install_location":"",
   "uninstall_string":"MsiExec.exe /I{23170F69-40C1-2702-2201-000001000000}",
   "publisher":"Igor Pavlov",
   "system_component":0,
   "win64":true
  },
  {
   "key":"{23170F69-40C1-2702-2300-000001000000}",
   "name":"7-Zip 23.00 (x64 edition)",
   "version":"23.00.00.0",
   "install_date":"2023-05-17 00:00:00",
   "install_location":"",
   "uninstall_string":"MsiExec.exe /I{23170F69-40C1-2702-2300-000001000000}",
   "publisher":"Igor Pavlov",
   "system_component":0,
   "win64":true
  }
 ]
} """


def update_package():
    # Declaring local variables
    package_updated = False
    proxies = get_proxies()
    if not proxies:
        proxies = get_proxies_from_wapt_console()
    url = "https://www.7-zip.org/download.html"
    download_dict = {
        "windows-x64": "https://www.7-zip.org/a/7znodotversion-x64.exe",
        "windows-arm64": "https://www.7-zip.org/a/7znodotversion-arm64.exe",
        "windows-x86": "https://www.7-zip.org/a/7znodotversion.exe",
        "linux-x64": "https://www.7-zip.org/a/7znodotversion-linux-x64.tar.xz",
        "linux-arm64": "https://www.7-zip.org/a/7znodotversion-linux-arm64.tar.xz",
        "darwin-all": "https://www.7-zip.org/a/7znodotversion-mac.tar.xz",
    }

    # Getting latest version from official sources
    print("URL used is: %s" % url)
    for bs_search in bs_find_all(url, "b", proxies=proxies):
        if "Download 7-Zip " in bs_search.text and not "beta" in bs_search.text:
            version = bs_search.text.split("Zip ")[-1].split(" (")[0]
            nodotversion = version.replace(".", "")
            download_url = download_dict[control.target_os + "-" + ensure_list(control.architecture)[0]].replace("nodotversion", nodotversion)
            latest_bin = download_url.split("/")[-1]
            if requests.head(download_url, proxies=proxies, allow_redirects=True).status_code == 200:
                break

    # Downloading latest binaries
    print("Latest %s version is: %s" % (control.name, version))
    print("Download URL is: %s" % download_url)
    if not isfile(latest_bin):
        print("Downloading: %s" % latest_bin)
        wget(download_url, latest_bin, proxies=proxies)
    else:
        print("Binary is present: %s" % latest_bin)

    # Checking version from file
    version_from_file = get_version_from_binary(latest_bin)
    if Version(version_from_file, 4) != Version(version, 4) and version_from_file != "":
        print("Changing version to the version number of the binary (from: %s to: %s)" % (version, version_from_file))
        # os.rename(latest_bin, latest_bin.replace(version, version_from_file))
        version = version_from_file
    else:
        print("Binary file version corresponds to online version")

    # Changing version of the package
    if Version(version, 4) > Version(control.get_software_version(), 4):
        print("Software version updated (from: %s to: %s)" % (control.get_software_version(), Version(version)))
        package_updated = True
    else:
        print("Software version up-to-date (%s)" % Version(version))
    control.set_software_version(version)
    control.save_control_to_wapt()

    # Deleting outdated binaries
    remove_outdated_binaries(latest_bin)

    # Validating or not update-package-sources
    return package_updated
