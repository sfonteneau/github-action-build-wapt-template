import hashlib
import requests
import os
import glob
import json

github_token = os.getenv("GITHUB_TOKEN")
github_repository = os.getenv('GITHUB_REPOSITORY')


def check_version(dict_version={}):

    package_name = os.path.realpath(__file__).split(os.path.sep)[-3]
    url = "https://www.7-zip.org/download.html"
    for entry in requests.get(url).content.decode('utf-8').splitlines():
        if "Download 7-Zip " in entry and not "beta" in entry:
            version = entry.split('Download 7-Zip ')[1].split(' ')[0]
            break

    print('Version for %s : %s' % (package_name,version))
    if version != dict_version.get(package_name):
        list_workflows_package = glob.glob(os.path.realpath(os.path.join( os.path.dirname(os.path.realpath(__file__)),'..','..','.github','workflows','%s*.yaml' % package_name)))
        for workflow in list_workflows_package :
            fname_workflow = workflow.split('/')[-1]
            if not github_token:
                continue
            requests.post(f"https://api.github.com/repos/{github_repository}/actions/workflows/{fname_workflow}/dispatches", headers={"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}, json={"ref": "refs/heads/main"})
    dict_version[package_name] = version

       

if __name__ == "__main__":
    check_version()
         
          


