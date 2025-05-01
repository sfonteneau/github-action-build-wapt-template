# -*- coding: utf-8 -*-
from setuphelpers import *

r"""
Installation procedure: https://docs.python.org/3.10/using/windows.html
"""
bin_contains = "python-"
python_version_to_uninstall_list = []
python_version_to_keep_list = ["3.6"]


def install():
    # Declaring local variables
    package_version = control.get_software_version()
    short_version = ".".join(package_version.split(".")[:2])
    digit_version = "".join(package_version.split(".")[:2])
    bin_name = glob.glob("*%s*.exe" % bin_contains)[0]
    app_name = control.name
    product_name = get_file_properties(bin_name)["ProductName"]
    if control.architecture == "x64":
        arch = "64-bit"
        app_dir_sub = makepath(programfiles, "Python%s")
    elif not iswin64():
        arch = "32-bit"
        app_dir_sub = makepath(programfiles, "Python%s-32")
        if not isdir(app_dir_sub) and isdir(makepath(programfiles, "Python%s")):
            # app_dir_sub = makepath(programfiles, "Python%s")
            uninstall_python(short_version)
    else:
        arch = "32-bit"
        app_dir_sub = makepath(programfiles32, "Python%s-32")
    app_dir = app_dir_sub % digit_version
    silent_args = '/quiet InstallAllUsers=1 PrependPath=1 AssociateFiles=1 Include_launcher=0 InstallLauncherAllUsers=0 TargetDir="%s"' % app_dir
    # silent_args = '/quiet InstallAllUsers=1 PrependPath=1 AssociateFiles=1 Include_launcher=0 InstallLauncherAllUsers=0'

    # Uninstalling Python 3.9 for Python 3.1x
    for python_version_to_uninstall in python_version_to_uninstall_list:
        if installed_softwares("Python %s" % python_version_to_uninstall):
            try:
                uninstall_python(python_version_to_uninstall)
            except:
                print("WARNING: Unable to uninstall Python %s.x" % python_version_to_uninstall)

    # Repairing if older installation is incomplete
    python_app = installed_softwares(name="Python %s" % short_version)
    if python_app and len(python_app) < 9 and not force:
        print("Repairing: %s in: %s" % (product_name, app_dir))
        run('"%s" /repair %s' % (bin_name, silent_args))

    # Installing the package
    if need_install(name="Python %s..*(%s)" % (short_version, arch), min_version=get_version_from_binary(bin_name), force=force):
        print("Installing: %s in: %s" % (product_name, app_dir))
        install_exe_if_needed(
            bin_name,
            silentflags=silent_args,
            key="",
            min_version=package_version,
        )
        if need_install(name="Python %s..*(%s)" % (short_version, arch), min_version=get_version_from_binary(bin_name)):
            error("%s is not installed" % app_name)
    else:
        print("%s is already installed and up-to-date" % app_name)

    # Copying installer for future uninstall
    if not isfile(makepath(app_dir, bin_name)):
        print("Copying: %s in: %s for future uninstall" % (bin_name, app_dir))
        filecopyto(bin_name, app_dir)


def uninstall():
    # Declaring local variables
    package_version = control.get_software_version()
    short_version = ".".join(package_version.split(".")[:2])
    uninstall_python(short_version)


def uninstall_python(python_version):
    # Declaring local variables
    digit_version = "".join(python_version.split(".")[:2])
    silent_uninst_args = "/uninstall /quiet"
    if control.architecture == "x64":
        arch = "64-bit"
        old_app_dir_sub = makepath(programfiles, "Python%s")
    elif not iswin64():
        arch = "32-bit"
        old_app_dir_sub = makepath(programfiles, "Python%s-32")
        if not isdir(old_app_dir_sub) and isdir(makepath(programfiles, "Python%s")):
            old_app_dir_sub = makepath(programfiles, "Python%s")
    else:
        arch = "32-bit"
        old_app_dir_sub = makepath(programfiles32, "Python%s-32")
    old_app_dir = old_app_dir_sub % digit_version

    # uninstalling it first avoids errors
    skip_uninstall = ["Executables", "Core Interpreter"]
    for p in skip_uninstall:
        for soft in installed_softwares(name="^Python %s" % python_version):
            if p in soft["name"]:
                continue
            for python_to_keep in python_version_to_keep_list:
                if python_to_keep in soft["name"]:
                    continue
            if iswin64() and (not arch in soft["name"]):
                continue
            print("Removing: %s" % soft["name"])
            run(uninstall_cmd(soft["key"]))

    # Uninstalling the package
    try:
        old_app_installer_path = glob.glob(r"%s\*%s*.exe" % (old_app_dir, bin_contains))[0]
        print("Removing Python %s with installer in folder: %s" % (python_version, old_app_dir))
        run('"%s" %s' % (old_app_installer_path, silent_uninst_args))
    except:
        print("Unable to remove Python %s with installer in folder: %s" % (python_version, old_app_dir))

    for soft in installed_softwares(name="^Python %s" % python_version):
        for python_to_keep in python_version_to_keep_list:
            if python_to_keep in soft["name"]:
                continue
        if iswin64() and (not arch in soft["name"]):
            continue
        print("Removing: %s" % soft["name"])
        run(uninstall_cmd(soft["key"]))

    # Removing remaining files of this Python version
    try:
        if isdir(old_app_dir):
            print("Removing remaining folder: %s" % old_app_dir)
            remove_tree(old_app_dir)
    except:
        print("Unable to remove Python %s remaining folder: %s" % (python_version, old_app_dir))

    # Removing system environment variables
    remove_from_system_path(old_app_dir)
    remove_from_system_path(makepath(old_app_dir, "Scripts"))
