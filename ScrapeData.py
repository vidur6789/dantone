
import logging
from pathlib import Path

import read.TextFileReader as text_reader
import read.XlsReader as reader
import scrape.finance.morningstar.MorningStarScraper as mstar_scraper
import write.JsonFileWriter as writer
from constants.constant import PATH_IN, PATH_OUT, PATH_TMP


import utils.commonutils as utils

# CONFIG
stock_file_path = PATH_IN / "StockList.xlsx"
stat_file_path = PATH_IN / 'StatList.xlsx'
out_file_name = 'Results ' + utils.current_datetime_str()
# ERROR/WARN(prod)/INFO(dev/monitor)/DEBUG(dev)
logging.basicConfig(filename=str(PATH_TMP / "logs.txt"), format='%(asctime)s -%(levelname)s-%(message)s',
                    level=logging.INFO, filemode="a")


def main():
    tickers = read_request()
    logging.info("Fetching statistics for " + str(tickers))
    response = mstar_scraper.get_results(tickers)
    write_response(response)


def read_request():
    tickers = text_reader.parse_as_list(str(PATH_TMP / "pending"))
    if tickers is None or len(tickers) == 0:
        tickers = reader.parse_as_list(stock_file_path)

    tickers = [str(item) for item in tickers]
    return tickers


def write_response(response):
    writer.write(PATH_OUT / out_file_name, response.data)  # write financial data
    errors = [error._asdict() for error in response.errors]
    writer.write(str(PATH_OUT / out_file_name) + "_errors", errors)


if __name__ == "__main__":
    main()
else:
    print("Executing as Module")

# TODO
'''
- combine key and finance stats
- normalize attribute names
- create stock class
- get attribute names
- region config
'''