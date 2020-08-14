import time
from random import randint
import datetime


# Read from config and sleep/take input
def random_sleep(min_sleep=1, max_sleep=5):
    sleep_time = randint(min_sleep, max_sleep)
    time.sleep(sleep_time)


# is_substring is used to eval
def is_in(value: str, items, exact_match=False, case_match=False, is_substring='items'):
    # Invalid Input
    if items is None or value is None or (not exact_match and is_substring != 'items' and is_substring != 'value'):
        return False
    # Let Python do the work
    if exact_match and case_match:
        return value in items
    # Otherwise
    match = False
    if not case_match:
        value = value.lower()
    for item in items:
        if not case_match:
            item = item.lower()
        if exact_match:
            if item == value:
                match = True
                break
        else:
            if 'items' == is_substring:
                if item in value:
                    match = True
                    break
            elif 'value' == is_substring:
                if value in item:
                    match = True
                    break

    return match


# return item in items that matches
def find_in(value: str, items, exact_match=False, case_match=False, is_substring='items'):
    # Invalid Input
    if items is None or value is None or (not exact_match and is_substring != 'items' and is_substring != 'value'):
        return False
    # Let Python do the work
    if exact_match and case_match:
        return value in items
    matched_item = None
    # Otherwise
    if not case_match:
        value = value.lower()
    for item in items:
        item_value = item
        if not case_match:
            item_value = item.lower()
        if exact_match:
            if item_value == value:
                matched_item = item
                break
        else:
            if 'items' == is_substring:
                if item_value in value:
                    matched_item = item
                    break
            elif 'value' == is_substring:
                if value in item_value:
                    matched_item = item
                    break
    return matched_item


# Converts Path object into string and adds format suffix if not already added
def parse_file_path(file_path, file_format=""):
    file_path_str = str(file_path)
    suffix = "." + file_format
    suffix = suffix if len(suffix) > 0 and file_path_str.find(suffix) == -1 else ""
    return file_path_str + suffix


def current_datetime_str():
    return str(datetime.datetime.now()).replace('.', '').replace(':', '').replace(' ', '')
