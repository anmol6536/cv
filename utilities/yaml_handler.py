from yaml import load, FullLoader
from typing import Callable, Union


def get_yaml_attribute(yaml_file, attribute: Union[str, Callable]):
    with open(yaml_file, 'r') as file:
        yaml_data = load(file, Loader=FullLoader)
        if callable(attribute):
            return attribute(yaml_data)
        return yaml_data.get(attribute)
