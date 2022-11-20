import yaml

def dev_connect(testbed):
    for dev in testbed.devices:
        testbed.devices[dev].connect(mit=True)

def scheme_parse(file_path):
    with open(file_path, 'r') as in_file:
        scheme = yaml.safe_load(in_file)
    
    return scheme
