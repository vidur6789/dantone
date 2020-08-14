import quandl
from nsetools import Nse
from bsedata.bse import BSE
import logging


bse = BSE()
nse = Nse()
quandl.ApiConfig.api_key = 'jAzEjxUxgSvbNLxxKffz'


def get_price(ticker: str):
    try:
        return get_bse_quote(ticker) if ticker.isnumeric() else get_nse_quote(ticker)
    except Exception as e:
        logging.exception("Exception for {}. Logs:{}".format(ticker, str(e)))


def get_bse_quote(ticker):
    return bse.getQuote(ticker)["currentValue"]
    # quote_key = "BSE/" + "BOM"+ticker
    # return quandl.get(quote_key, start_date='2019-07-18', end_date='2019-07-21')['Close'].iat[0]


def get_nse_quote(ticker):
    return nse.get_quote(ticker).get("lastPrice")
