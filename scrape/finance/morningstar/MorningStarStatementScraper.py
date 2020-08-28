import logging

import constants.constant as constant
import utils.commonutils as utils
import utils.scraperutils as scraperutils
from constants.namedtuples import Column

def build_request_url(ticker: str, region_code='idn'):
	request_api_prefix = 'http://financials.morningstar.com/finan/financials/getKeyStatPart.html?'
	ticker_param = f'&t={ticker}&region={region_code}&culture=en-US&version=SAL&cur=&order=asc'
	return request_api_prefix + ticker_param


def format_response(text):
	text = text.replace('\/', '/')
	text = text.replace('\\\"', '"')
	begin = text.find('<')
	end = text.find('"}')
	text = text[begin:end]
	return text


def get_results(ticker):
	url = build_request_url(str(ticker))
	soup = scraperutils.get_beautiful_soup(url, format_response=format_response)
	utils.random_sleep(min_sleep=7, max_sleep=13)
	# table_set = soup.find_all('table')
	# if len(table_set) == 0:
	# 	logging.warning("No Content for ticker: " + ticker + ", url:" + url)
	# 	key_stats = constant.NO_CONTENT
	# else:
	# 	key_stats = get_attribute_values(table_set)
	# logging.debug(str(key_stats))
	# return key_stats