import yaml

def read_config(use_case):
    with open ("./main_project/Config/config.yaml") as openFile:
        parsed_yaml = yaml.load(openFile, Loader=yaml.FullLoader)
        return parsed_yaml[use_case]

def available_apis():
    with open ("./main_project/Config/config.yaml") as openFile:
        parsed_yaml = yaml.load(openFile, Loader=yaml.FullLoader)
        return list(parsed_yaml.keys())

