import logging

import constants.constant as const
import utils.commonutils as utils
import utils.scraperutils as scraperutils
from constants.namedtuples import Column
from constants.exceptions import ContentNotFoundException


def get_attribute_values(table_set):
	key_stats = []
	for table in table_set:
		key_stats.extend(get_attribute_values_from_table(table))
	return key_stats


def get_attribute_values_from_table(table_soup):
	key_stats = []
	name_prefix = ''
	thead = table_soup.find('thead')
	columns = get_columns(thead.find_all('th'))
	tbody = table_soup.find('tbody')
	if tbody is not None:
		for row_head in tbody.find_all('th'):
			cell_tags = row_head.find_next_siblings('td')
			row_name = row_head.string
			# header row with no cell data. use as prefix for next row's name
			if len(cell_tags) < 1:
				name_prefix = row_name + " "
				continue
			stat_values = []
			for column in columns:
				value = cell_tags[column.index].string
				stat_values.append({const.ATTR_PERIOD: column.name, const.ATTR_VALUE: value})
			stat = {const.ATTR_STAT_NAME: f"{name_prefix}{row_name}", const.ATTR_VALUES: stat_values}
			key_stats.append(stat)
	return key_stats


def get_columns(iterable):
	i = 0
	columns = []

	# first item is useless  row-header column
	for tag in iterable[1:]:
		column_name = tag.contents[0]
		columns.append(Column(i, column_name))
		i += 1
	return columns


def build_request_url(ticker: str, region_code='usa'):
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
	table_set = soup.find_all('table')
	if len(table_set) == 0:
		logging.warning("No Content for ticker: " + ticker + ", url:" + url)
		key_stats = const.NO_CONTENT
		raise ContentNotFoundException(f'No content for {ticker}')
	else:
		key_stats = get_attribute_values(table_set)
	logging.debug(str(key_stats))
	return key_stats

