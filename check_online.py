import imp
import os
import glob
import json
import copy

def load_module(modulename, setupfilename):
    module = imp.load_source(modulename, setupfilename)
    return module

if __name__ == "__main__":

    dict_last_version_file = os.path.realpath(os.path.join( os.path.dirname(os.path.realpath(__file__)),'dict_last_version.json'))
    if os.path.isfile(dict_last_version_file):
        with open(dict_last_version_file,'r') as f:
            dict_all_version = json.load(f)
    else:
        dict_all_version = {}
    print(dict_all_version)

    dict_old_version = copy.deepcopy(dict_all_version)

    for f in glob.glob(os.path.realpath(os.path.join( os.path.dirname(os.path.realpath(__file__)),'*','monitor','check.py'))):
        module_name = 'check'  
        module = load_module(module_name, f)
        module.check_version(dict_all_version)

    with open(dict_last_version_file,'w') as f:
        f.write(json.dumps(dict_all_version))

    print(dict_all_version)
    change = str(dict_old_version != dict_all_version).lower()
    if os.getenv('GITHUB_REPOSITORY'):
        with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
            f.write("DICT_CHANGED=%s\n" % change)
        
 


