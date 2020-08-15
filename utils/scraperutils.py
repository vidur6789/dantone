import logging
from enum import Enum
from time import sleep

import constants.constant as constant
import read.JsonFileReader as json_reader
import write.JsonFileWriter as json_writer
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


class SourceRetrieverType(Enum):
    REQUESTS = 1
    SELENIUM = 2


def get_beautiful_soup(request_url, headers=None, soup_parser='html.parser', format_response=None,
                       source_retriever=SourceRetrieverType.REQUESTS):
    logging.info("Requesting :" + request_url)
    if headers is not None:
        headers = get_default_headers()
    if SourceRetrieverType.SELENIUM == source_retriever:
        success = False
        limit = 3
        attempt = 1
        while not success:
            attempt += 1
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('window-size=1024x768')
                driver = webdriver.Chrome(
                    'chromedriver.exe',
                    chrome_options=options)
                driver.get(request_url)
                success = True
            except TimeoutException as te:
                if attempt == limit:
                    print("Reached Selenium attempt limit for " + request_url)
                    raise te
                else:
                    print("Attempt " + str(attempt) + " failed. Trying again. ")
                    print(te.msg)
                    sleep(5)

        text = driver.page_source
    else:
        response = requests.get(request_url, headers, timeout=30)
        text = response.text
    if format_response is not None:
        text = format_response(text)
    beautiful_soup = BeautifulSoup(text, soup_parser)
    return beautiful_soup


def get_default_headers():
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    return headers


def write_stat_names(data_file_path, attrs, stat_name_file_path):
    file_data = json_reader.parse(data_file_path)
    stats = [file_data[0][attr] for attr in attrs]
    stat_names = [stat[constant.ATTR_STAT_NAME] for attr_stats in stats for stat in attr_stats]
    json_writer.write(stat_name_file_path, stat_names)


def json_array_to_df(json_array, row_key, values_key, column_key, value_key):
    data_dict = {json_obj[row_key]: extract_values(json_obj[values_key], value_key) for json_obj in json_array}
    columns = extract_columns(json_array[0][values_key], column_key)
    df = pd.DataFrame.from_dict(data_dict, orient="index", columns=columns)
    return df


def extract_values(values, value_key):
    return [value[value_key] for value in values]


def extract_columns(values, column_key):
    return [value[column_key] for value in values]

def write_progress(scraped, pending, errors):
    os.makedirs(os.path.dirname(str(PATH_TMP)), exist_ok=True)
    with open(str(PATH_TMP / "progress"), "w") as f:
        f.write("scraped :" + str(len(scraped)) + "\n")
        f.write("pending: " + str(len(pending)) + "\n")
        f.write("errors: " + str(len(errors)) + "\n")

    with open(str(PATH_TMP / "pending"), "w") as f:
        f.write(str(list(pending)))



if __name__ == "__main__":
    write_stat_names(constant.PATH_OUT / constant.FILE_MS_STAT,
                     constant.LIST_PARAM_ATTRS,
                     constant.PATH_OUT / constant.FILE_MS_STAT_NAMES)
