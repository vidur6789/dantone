import os
from pathlib import  Path
from constants.namedtuples import Error
from constants.namedtuples import Response
from constants.constant import PATH_TMP
import constants.constant as constant
from constants.exceptions import ContentNotFoundException
from scrape.finance.morningstar.MorningStarKeyStatScraper import get_results as keystatscraper
from scrape.finance.morningstar.MorningStarFinanceStatScraper import get_results as finstatscraper
from utils.scraperutils import write_progress
import logging


def get_scrapers():
    return {constant.ATTR_FIN_STAT: finstatscraper,  constant.ATTR_KEY_STAT: keystatscraper}


def get_results(tickers):
    stocks = []
    errors = []
    pending = set(tickers)  # used to track progress
    err_count = 0  # consecutive error count
    scrapers = get_scrapers().items()
    for ticker in tickers:
        try:
            stock = {constant.ATTR_SYMBOL: ticker}
            for key, scrape in scrapers:
                    intermediate_results = scrape(ticker)
                    stock[key] = intermediate_results
                    err_count = 0  # reset consecutive error count
            stocks.append(stock)
            pending.remove(ticker)
        except ContentNotFoundException as ce:
            logging.exception("ContentNotFoundException in MorningStarScraper.get_results for: " + ticker)
            errors.append(Error(ticker, str(ce)))
        except Exception as e:
            logging.exception("Exception in MorningStarScraper.get_results for: " + ticker)
            errors.append(Error(ticker, str(e)))
            err_count += 1
        if err_count >= 5:
            break
    write_progress(stocks, pending, errors)
    return Response(stocks, errors)






