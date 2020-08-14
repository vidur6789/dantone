from typing import List
import com.thothink.constants.constant as constant
import com.thothink.read.JsonFileReader as json_reader
import com.thothink.write.XlsWriter as xls_writer
import com.thothink.utils.scraperutils as scraperutils
import com.thothink.utils.commonutils as utils
from com.thothink.screen.valuescreener import GrahamEnterprisingScreener
from com.thothink.screen.filters import Filter
import logging
import pandas as pd


# config
count_stock = 0
PATH_REPO = constant.PATH_OUT
FILE_REPO = constant.FILE_MS_STAT
FILE_SCREENER = "GrahamScreener" + utils.current_datetime_str()
screener = GrahamEnterprisingScreener

logging.basicConfig(filename=str(constant.PATH_TMP / "logs.txt"), format='%(asctime)s -%(levelname)s-%(message)s',
                    level=logging.INFO, filemode="a")


def filter_stock(stock, filters: List[Filter]):
    try:
        for filter_item in filters:
            if not filter_item.evaluate(stock):
                return False
        return True
    except Exception as e:
        logging.exception("Exception for {}. Error Log: {}".format(stock[constant.ATTR_SYMBOL], str(e)))
        return False



def build_screener():
    stocks = json_reader.parse(PATH_REPO / FILE_REPO)
    transformed_stocks = [transform_stock(stock) for stock in stocks if is_data_available(stock)]
    logging.info("Screening {} stocks".format(str(len(transformed_stocks))))
    filtered_stocks = [stock for stock in transformed_stocks if filter_stock(stock, screener.filters())]
    results_df = create_results(filtered_stocks)
    write_results(results_df)


def is_data_available(stock):
    for attr in constant.LIST_PARAM_ATTRS:
        if stock[attr] != constant.NO_CONTENT:
            return True
    return False


# transform stock from JSON to nested dict of Data Frames
def transform_stock(stock):
    attrs = constant. LIST_PARAM_ATTRS
    for attr in attrs:
        if stock[attr] == constant.NO_CONTENT:
            stock[attr] = pd.DataFrame()
        else:
            stock[attr] = scraperutils.json_array_to_df(stock[attr],
                                                        row_key=constant.ATTR_STAT_NAME,
                                                        column_key=constant.ATTR_PERIOD,
                                                        values_key=constant.ATTR_VALUES,
                                                        value_key=constant.ATTR_VALUE)
    return stock


def create_results(stocks):
    result_list = [extract_columns(stock) for stock in stocks]
    return pd.DataFrame(result_list)


def extract_columns(stock):
    stock_result = {constant.ATTR_SYMBOL: stock[constant.ATTR_SYMBOL]}
    search_attrs = constant.LIST_PARAM_ATTRS
    for output_var in screener.output_variables():
        is_found = False
        for attr in search_attrs:
            if type(stock[attr]) != str and output_var.name in stock[attr].index:
                print(stock[attr])
                # Latest Value
                if output_var.period == constant.LATEST_PERIOD:
                    stock_result[output_var.name] = stock[attr].loc[output_var.name].iloc[-1]
                    is_found = True
                    break
                    # Specific Year Value
                else:
                    stock_result[output_var.name] = stock[attr].at[output_var.name, output_var.period]
                    is_found = True
                    break

        if not is_found:
            logging.warning("Output Variable ({name}, {period}) not found for {symbol}".format(name=output_var.name, period=output_var.period, symbol=stock[constant.ATTR_SYMBOL]))
    return stock_result


def write_results(results_df):
    xls_writer.write_df(constant.PATH_OUT / FILE_SCREENER, results_df)


if __name__ == "__main__":
    build_screener()


# TODO Optimization: Store pre-processed DataFrame as pandas HDF5
