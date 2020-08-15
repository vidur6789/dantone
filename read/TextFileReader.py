def parse_as_list(file_path):
    with open(file_path, "r") as read_file:
        element_list = read_file.readline().lstrip("[").rstrip("]").split(",")
        element_list = [strip_item(item) for item in element_list if len(item) > 0]
    return element_list


def strip_item(item: str):
    return item.strip().strip("'").strip()  # strip whitespace and single quotes
