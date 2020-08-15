from screen.screener import Screener
from screen.filters import PriceMultipleFilter, CurrentDividendFilter, EarningsGrowthFilter
from screen.filters import CurrentRatioFiler, DebtWorkingCapFilter, NoEarningsDeficitFilter
from constants.namedtuples import OutputVariable
import constants.constant as constant


class GrahamEnterprisingScreener(Screener):
    @staticmethod
    def filters():
        return [
            CurrentRatioFiler,
            CurrentDividendFilter,
            EarningsGrowthFilter,
            NoEarningsDeficitFilter,
            DebtWorkingCapFilter,
            PriceMultipleFilter
        ]

    @staticmethod
    def output_variables():
        return [
            OutputVariable(constant.PARAM_CURR_RATIO, constant.LATEST_PERIOD)
        ]
