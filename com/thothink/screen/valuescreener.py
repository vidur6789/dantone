from com.thothink.screen.screener import Screener
from com.thothink.screen.filters import PriceMultipleFilter, CurrentDividendFilter, EarningsGrowthFilter
from com.thothink.screen.filters import CurrentRatioFiler, DebtWorkingCapFilter, NoEarningsDeficitFilter
from com.thothink.constants.namedtuples import OutputVariable
import com.thothink.constants.constant as constant


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
