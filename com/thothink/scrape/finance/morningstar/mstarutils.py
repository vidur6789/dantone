import com.thothink.utils.scraperutils as scraperutils
from collections import namedtuple


def attr_count(x: list):
    return len(x) if x is not None and len(x) > 0 else 1


def get_stock_basic(ticker: str):
    url = 'http://www.morningstar.in/handlers/autocompletehandler.ashx?criteria=' + ticker
    soup = scraperutils.get_beautiful_soup(url)
    tables = soup.find_all('table')
    # raise exception if length!=1
    Security = namedtuple('Security', 'id, ticker, description, exchange, type')
    if len(tables) > 0:
        result_table = tables[0]
        security_id = result_table.find('id').string
        ticker = result_table.find('ticker').string
        description = result_table.find('description').string
        exchange = result_table.find('exchange').string
        security_type = result_table.find('type').string
        return Security(security_id, ticker, description, exchange, security_type)
    return None




