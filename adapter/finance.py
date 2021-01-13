

import logging
import datetime
from typing import Union

from portfolio.portfolio import Stock

# quandl.ApiConfig.api_key = 'jAzEjxUxgSvbNLxxKffz'


def get_bse_quote(ticker):
    from bsedata.bse import BSE
    bse = BSE()
    return bse.getQuote(ticker)["currentValue"]


def get_nse_quote(ticker):
    from nsetools import Nse
    nse = Nse()
    return nse.get_quote(ticker).get("lastPrice")


def get_price(stock: Union[str, Stock], suffix='', req_date=-1, dur='max'): 
    '''
    dur -> 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    suffix -> NSE:NS, BSE:BO
    period -> index range
    '''
    import yfinance as yf

    ticker = stock.ticker if isinstance(stock, Stock) else stock
    ticker = ticker.replace('.', '-') # companies with multiple class of shares BRK-B instead of BRK.B
    symbol = f'{ticker}.{suffix}' if suffix else ticker
    stock = yf.Ticker(symbol)
    hist = stock.history(period=dur)

    if isinstance(req_date, datetime.date):
        req_date_str = req_date.strftime('%Y-%m-%d')
        while req_date_str not in hist.index:
            req_date = req_date - datetime.timedelta(days=1)
            req_date_str = req_date.strftime('%Y-%m-%d')
        return hist['Close'].loc[req_date_str]
    elif isinstance(req_date, int):
        return hist['Close'].iloc[req_date]
    elif isinstance(req_date, str):
        return hist['Close'].loc[req_date]
    else:
        raise TypeError('req_date should be of type datetime.Date, str(yyyy-mm-dd), int(index)')


def get_fx_rate(fx_from, fx_to, fx_date: datetime.date = None):
    from forex_python.converter import get_rate

    return get_rate(base_cur=fx_from, dest_cur=fx_to, date_obj=fx_date)


def get_dividends(stock: Union[str, Stock], start_date: datetime.date, end_date: datetime.date = None):
    '''
    returns a Pandas Series object containing dividends for the relevant dates with datetime index
    '''
    import yfinance as yf

    ticker = stock.ticker if isinstance(stock, Stock) else stock
    ticker = ticker.replace('.', '-') # companies with multiple class of shares BRK-B instead of BRK.B
    dividends = yf.Ticker(ticker).dividends
    
    
    if end_date:
        idxs = [d for d in dividends.index if d.to_pydatetime().date() > start_date and d.to_pydatetime().date() <= end_date]
        return dividends.loc[idxs]
    else:
        start_date_str = start_date.strftime('%Y-%m-%d')
        return dividends.loc[start_date_str]


    
