import sys
sys.path.append('/opt/wapt')
import glob
import os

from waptpackage import HostCapabilities,PackageEntry

dict_host = {
        'ubuntu-latest':{'host_capa': HostCapabilities(language= 'en', 
                                   os ='ubuntu',
                                   tags=['ubuntu-jammy', 'ubuntu', 'ubuntu22', 'ubuntu-22', 'debian_based', 'linux', 'unix'], 
                                   os_version= '22.04',
                                   kernel_version= '6.5.0-1025-azure',
                                   architecture='x64',
                                   packages_maturities= ['PROD', 'PREPROD'] ),
                          'wgetwapt':'curl -L "https://wapt.tranquil.it/wapt/releases/wapt-2.6.0.16613-4de25b0a/tis-waptagent-2.6.0.16613-4de25b0a-amd64.deb" -o "/tmp/waptsetup.deb"',
                          'installwapt' : 'sudo apt-get install /tmp/waptsetup.deb -y',
                          'cmdwapt':'sudo /opt/wapt/wapt-get.bin',
                          "shell" : "bash"},
        'windows-latest':{ 'host_capa': HostCapabilities(language= 'en', 
                                   os ='windows',
                                   tags= ['windows-10', 'win-10', 'w-10', 'windows10', 'win10', 'w10', 'windows', 'win', 'w'], 
                                   os_version= '10.0.20348',
                                   architecture='x64',
                                   packages_maturities= ['PROD', 'PREPROD'] ),
                          'wgetwapt':'curl -L "https://wapt.tranquil.it/wapt/releases/latest/waptsetup.exe" -o "c:\\waptsetup.exe"',
                          'installwapt' : '"C:\waptsetup.exe" /VERYSILENT',
                          'cmdwapt':'"C:\Program Files (x86)\wapt\wapt-get.exe" ',
                          "shell" : "cmd"},
        'macos-latest': {'host_capa': HostCapabilities(language= 'en', 
                                   os ='macos',
                                   tags= ['macos', 'mac', 'darwin', 'unix', 'sonoma'],
                                   os_version= '14.7.1', 
                                   kernel_version= '23.6.0', 
                                   architecture='x64',
                                   packages_maturities= ['PROD', 'PREPROD'] ),
                          'wgetwapt':'curl -L "https://wapt.tranquil.it/wapt/releases/latest/tis-waptagent-2.6.0.16613-4de25b0a-macos-all-x86_64.pkg" -o "/tmp/waptsetup.pkg"',
                          'installwapt' : 'sudo installer -pkg /tmp/waptsetup.pkg -target /',
                          'cmdwapt':'sudo /opt/wapt/wapt-get.bin',
                          "shell" : "bash"},
 
 }

base_folder = os.path.realpath(os.path.join( os.path.dirname(os.path.realpath(__file__))))
for f in glob.glob(os.path.join(base_folder,'.github','workflows','*.yaml')):
    if not f.split(os.path.sep)[-1] in ['monitor.yaml']:
        os.remove(f)

for package in glob.glob(os.path.join('**','control'), recursive=True):
    pfolder = package.rsplit(os.path.sep,2)[0]
 
    pe = PackageEntry(waptfile=pfolder)
    for host in dict_host:
        hostcap = dict_host[host]['host_capa']
        if hostcap.is_matching_package(pe):
            datayaml = f"""name: {pfolder.replace(os.path.sep,'_')}

on:
  workflow_dispatch:  

jobs:
  run-build-wapt-package:
    runs-on: {host}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4 

      - name: Download binary
        run: |
          {dict_host[host]['wgetwapt']}
        shell: {dict_host[host]['shell']}

      - name: Install wapt
        run: |
          {dict_host[host]['installwapt']}
        shell: {dict_host[host]['shell']}

      - name: Run updatepackage
        run: |
          {dict_host[host]['cmdwapt']} update-package-sources ./{pfolder}
        shell: {dict_host[host]['shell']}

      - name: Upload build
        uses: actions/upload-artifact@v4
        with:
          name: {pfolder.replace('/','-')}.wapt
          path: {pfolder}

      - name: Run install
        run: |
          {dict_host[host]['cmdwapt']} install ./{pfolder}
        shell: {dict_host[host]['shell']}

      - name: Run session-setup
        run: |
          {dict_host[host]['cmdwapt']} session-setup ALL
        shell: {dict_host[host]['shell']}

      - name: Run audit
        run: |
          {dict_host[host]['cmdwapt']} audit ./{pfolder}
        shell: {dict_host[host]['shell']}

      - name: Run remove
        run: |
          {dict_host[host]['cmdwapt']} uninstall ./{pfolder}
        shell: {dict_host[host]['shell']}
            """
            with open(os.path.join(base_folder,'.github','workflows','%s.yaml' % pfolder.replace(os.path.sep,'-')) ,'w') as f :
                f.write(datayaml)
            print('Generate %s' % os.path.join(base_folder,'.github','workflows','%s.yaml' % pfolder.replace(os.path.sep,'-')))
            break
