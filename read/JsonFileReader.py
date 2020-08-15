import json

import utils.commonutils as utils


def parse(file_path, encoding=None):
    file_path_str = utils.parse_file_path(file_path, "json")
    if encoding is None:
        with open(file_path_str, "r") as file:
            return json.load(file)
    else:
        with open(file_path_str, "r", encoding=encoding) as file:
            return json.load(file)
