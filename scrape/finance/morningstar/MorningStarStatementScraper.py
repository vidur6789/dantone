import logging
import json
import re

from attr import attr

import constants.constant as constant
import utils.commonutils as utils
import utils.scraperutils as scraperutils
from constants.namedtuples import Column

def build_request_url(stmt_type: str, ticker: str, region_code='usa'):
	request_api_prefix = 'http://financials.morningstar.com/ajax/ReportProcess4HtmlAjax.html?'	
	ticker_param = f't={ticker}&region={region_code}&culture=en-US&reportType={stmt_type}&period=12&dataType=A&order=asc&columnYear=5&curYearPart=1st5year&rounding=3&number=1'
	return request_api_prefix + ticker_param


def format_response(text):
	text = re.sub('\'', '', text)
	js = json.loads(text)
	html = js['result']
	return html


def get_attribute_values(soup):
	tags = soup.find_all('div')
	info = {}

	for tag in tags:
		attrs = tag.attrs
		if 'id' in attrs:
			tag_id = tag['id']
			value = tag.text
				
			# Parse currency and FY End month number
			if tag_id == 'unitsAndFiscalYear':
				info['fye_month'] = int(tag['fyenumber'])
				info['currency'] = tag['currency']

			# Parse Yrly or Qtrly values
			elif tag_id[:2] == 'Y_':
				parent_id = tag.parent['id']
				key = f'{parent_id}_{tag_id}'

				if 'rawvalue' in attrs:
					# parse values i.e data_{statid}_{yearid} -> float value
					if tag['rawvalue'] in ['—', 'nbsp']:
						continue
					info[key] = float(re.sub(',', '', tag['rawvalue']))
					logging.debug(f'2.1, {key}')
				else:
					# parse year labels i.e. Y_1 -> 2017-12
					if 'title' in attrs:
						value = tag['title']
					info[key] = value
					logging.debug(f'2.2, {key}, {value}')

			# Parse labels i.e. label_i4 -> Inventories
			elif tag_id[:3] == 'lab' and 'padding' not in tag_id:
				lbl_tag = tag.find("div", class_="lbl")
				value = lbl_tag['title'] if 'title' in lbl_tag.attrs else lbl_tag.text
				info[tag_id] = value
				logging.debug(f'3, {tag_id}, {value}')
	return info


def transform_data(info):
	label_pattern = re.compile(r'label_(.*)')
	year_pattern = re.compile(r'Year_(.*)')
	stats = [k for k in info if label_pattern.search(k)]
	years = [k for k in info if year_pattern.search(k)]
	stmt_data = []
	for stat in stats:
		sid = label_pattern.search(stat).group(1)
		stat_values = []
		for year in years:
			yid = year_pattern.search(year).group(1)
			key = f'data_{sid}_{yid}'
			stat_values.append({'period': info[year], 'value': info.get(key, 'nan')})
		stmt_data.append({'name': info[stat], 'values': stat_values})
	return stmt_data



def get_results(stmt_type, ticker):
	url = build_request_url(stmt_type, str(ticker))
	soup = scraperutils.get_beautiful_soup(url, format_response=format_response)
	utils.random_sleep(min_sleep=7, max_sleep=13)
	attribute_values = get_attribute_values(soup)
	stmt_data = transform_data(attribute_values)
	logging.debug(str(stmt_data))
	return stmt_data