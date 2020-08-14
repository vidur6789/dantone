import os
from pathlib import  Path
from com.thothink.constants.namedtuples import Error
from com.thothink.constants.namedtuples import Response
from com.thothink.constants.constant import PATH_TMP
import com.thothink.constants.constant as constant
from com.thothink.constants.exceptions import ContentNotFoundException
from com.thothink.scrape.finance.morningstar.MorningStarKeyStatScraper import get_results as keystatscraper
from com.thothink.scrape.finance.morningstar.MorningStarFinanceStatScraper import get_results as finstatscraper
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
        stock = {constant.ATTR_SYMBOL: ticker}
        for key, scrape in scrapers:
            try:
                intermediate_results = scrape(ticker)
                stock[key] = intermediate_results
                stocks.append(stock)
                pending.remove(ticker)
                err_count = 0  # reset consecutive error count
            except ContentNotFoundException as ce:
                logging.exception("ContentNotFoundException in MorningStarScraper.get_results for: " + ticker)
                errors.append(Error(ticker, ce))
            except Exception as e:
                logging.exception("Exception in MorningStarScraper.get_results for: " + ticker)
                errors.append(Error(ticker, e))
                err_count += 1
        if err_count >= 5:
            break
    write_progress(stocks, pending, errors)
    return Response(stocks, errors)


def write_progress(stocks, pending, errors):
    os.makedirs(os.path.dirname(str(PATH_TMP)), exist_ok=True)
    with open(str(PATH_TMP / "progress"), "w") as f:
        f.write("scraped :" + str(len(stocks)) + "\n")
        f.write("pending: " + str(len(pending)) + "\n")
        f.write("errors: " + str(len(errors)) + "\n")

    with open(str(PATH_TMP / "pending"), "w") as f:
        f.write(str(list(pending)))


# Things  to improve
# Config
# Dev Config
# Continue?
# Use relative path from main
