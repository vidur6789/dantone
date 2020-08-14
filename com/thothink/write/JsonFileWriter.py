import json
import com.thothink.utils.commonutils as utils


def write(file_path, data_dict):
    file_path_str = utils.parse_file_path(file_path, "json")
    with open(file_path_str, "w") as write_file:
        json.dump(data_dict, write_file)
