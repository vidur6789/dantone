import pandas as pd
import utils.commonutils as utils
import utils.scraperutils as scraperutils
import scrape.finance.morningstar.mstarutils as mstarutils
from collections import namedtuple
from utils.scraperutils import SourceRetrieverType


def get_attribute_values(attr_requests: dict, ul_set):
	results = {}
	attr_request_count_list = [mstarutils.attr_count(x) for x in attr_requests.values()]
	attr_request_count = sum(attr_request_count_list)
	for ul in ul_set:
		results.update(get_attribute_values_from_ul(attr_requests, ul))
		if len(results.keys()) >= attr_request_count:
			break
	return results



# returns dict of results with key as (row,col) tuple
def get_attribute_values_from_ul(attr_requests: dict, ul):
	# throw exception if not tableSoup
	# search values
	results = {}
	if ul is not None:
		for list_item in ul.find_all('li'):
			list_item_divs = list_item.find_all('div')
			attr_name = list_item_divs[1].string
			attr_value = list_item_divs[2].string
			attr_key = utils.find_in(attr_name, attr_requests.keys(), exact_match=True)
			if attr_key is not None:
				results[attr_key] = attr_value
	return results


def get_column_set(attr_requests: dict):
	column_names = set()
	for row, column_name_items in attr_requests.items():
		for column_name in column_name_items:
			column_names.add(column_name)
	return column_names


def get_column_dict(names, iterable):
	i = -1  # first item is useless  row-header column
	column_dict = {}
	Column = namedtuple('Column', 'index, name')
	for tag in iterable:
		value_text = tag.contents[0]
		name = utils.find_in(value_text, names)
		if name is not None:
			column_dict[name] = Column(i, value_text)
		i += 1
	return column_dict


def build_request_url(ticker: str):
	request_prefix = 'http://www.morningstar.in/stocks/'
	stock = mstarutils.get_stock_basic(ticker)
	stock_url = stock.id + '/' + stock.exchange.lower() + '-' + stock.description.lower().replace(' ', '-')
	request_suffix = '/overview.aspx'
	return request_prefix+stock_url+request_suffix


def get_results(tickers, attr_requests: dict):
	results = None
	for ticker in tickers:
		url = build_request_url(ticker)
		soup = scraperutils.get_beautiful_soup(url, source_retriever=SourceRetrieverType.SELENIUM)
		utils.random_sleep()
		ul_set = soup.find_all('ul', {'class': 'small-block-grid-3 large-block-grid-4 sal-component-band-grid'})
		ticker_results = get_attribute_values(attr_requests, ul_set)
		# print("Results for " + ticker + str(ticker_results))
		if results is None:
			results = pd.DataFrame(data=ticker_results, index=[ticker])
		else:
			results.loc[ticker] = ticker_results
		# print(results)
	return results

# Logging
# Other Access Methods
