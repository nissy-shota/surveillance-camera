import yaml


def load_yaml(yaml_file:str) -> dict:
    """
    Load yaml file.
    """
    with open(yaml_file) as stream:
        param = yaml.safe_load(stream)
    return param