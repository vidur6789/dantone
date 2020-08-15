import constants.constant as constant
from decimal import Decimal
import adapter.FinancialAdapter as finadapter


class Filter:
    @staticmethod
    def evaluate(stock):
        raise NotImplementedError


    @staticmethod
    def is_available(*args):
        for value in args:
            if value is None or value == constant.EMPTY_CELL:
                return False
        return True



class PriceMultipleFilter(Filter):
    @staticmethod
    def evaluate(stock):
        price = finadapter.get_price(stock[constant.ATTR_SYMBOL])
        eps = stock[constant.ATTR_FIN_STAT].loc[constant.PARAM_EPS].iloc[-1]
        bv = stock[constant.ATTR_FIN_STAT].loc[constant.PARAM_BV].iloc[-1]
        if not Filter.is_available(price, eps, bv) or Decimal(eps) <= 0 or Decimal(bv) <= 0:
            return False
        pe = Decimal(price) / Decimal(eps)
        pbv = Decimal(price) / Decimal(bv)

        return pe * pbv < Decimal(12)


# Current Ratio >= 1.5
class CurrentRatioFiler(Filter):
    @staticmethod
    def evaluate(stock):
        cell_value = stock[constant.ATTR_KEY_STAT].loc[constant.PARAM_CURR_RATIO].iloc[-1]
        return Filter.is_available(cell_value) and Decimal(cell_value) >= Decimal(1.5)


# Total Debt > 110% of Working Cap
class DebtWorkingCapFilter(Filter):
    @staticmethod
    def evaluate(stock):
        short_debt = stock[constant.ATTR_KEY_STAT].loc[constant.PARAM_SHORT_DEBT].iloc[-1]
        long_debt = stock[constant.ATTR_KEY_STAT].loc[constant.PARAM_LONG_DEBT].iloc[-1]
        curr_ast = stock[constant.ATTR_KEY_STAT].loc[constant.PARAM_CURR_AST].iloc[-1]
        curr_lia = stock[constant.ATTR_KEY_STAT].loc[constant.PARAM_CURR_LIA].iloc[-1]
        if not Filter.is_available(short_debt, long_debt, curr_ast, curr_lia):
            return False
        debt = Decimal(short_debt) + Decimal(long_debt)
        work_cap = Decimal(curr_ast) - Decimal(curr_lia)

        return work_cap > 0 and debt <= Decimal(1.1) * work_cap


# Some Current Dividend
class CurrentDividendFilter(Filter):
    @staticmethod
    def evaluate(stock):
        cell_value = stock[constant.ATTR_FIN_STAT].loc[constant.PARAM_DIVIDENDS].iloc[-1]
        return Filter.is_available(cell_value) and Decimal(cell_value) > 0



class NoEarningsDeficitFilter(Filter):
    @staticmethod
    def evaluate(stock):
        outcome = False
        earnings = [stock[constant.ATTR_FIN_STAT].loc[constant.PARAM_NET_INC].iloc[-i] for i in range(1, 6)]
        for earning in earnings:
            outcome = Filter.is_available(earning) and Decimal(earning) > 0
        return outcome


# Last Year's Earnings greater than 5 year ago's earnings
class EarningsGrowthFilter(Filter):
    @staticmethod
    def evaluate(stock):
        first_earnings = stock[constant.ATTR_FIN_STAT].loc[constant.PARAM_NET_INC].iloc[-5]
        last_earnings = stock[constant.ATTR_FIN_STAT].loc[constant.PARAM_NET_INC].iloc[-1]
        return Filter.is_available([first_earnings, last_earnings]) and Decimal(last_earnings) > Decimal(first_earnings)


