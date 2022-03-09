from pathlib import Path

# paths
PATH_CONFIG = Path("config")
PATH_TMP = Path("logs")
PATH_OUT = Path("output")
PATH_IN = Path("input")

# url
STMT_TYPE_BALANCE_SHEET = 'bs'
STMT_TYPE_INCOME_STMT = 'is'
STMT_TYPE_CASHFLOW = 'cf'

# keywords
NO_CONTENT = "NA"
LATEST_PERIOD = "LATEST"
EMPTY_CELL = "—"

# attribute keys
ATTR_FIN_STAT = "financeStats"
ATTR_KEY_STAT = "keyStats"
ATTR_BALANCE_SHEET = 'balance_sheet'
ATTR_INCOME_STATEMENT = 'income_statement'
ATTR_CASHFLOW_STATEMENT = 'cashflow_statement'
ATTR_SYMBOL = "symbol"
ATTR_STAT_NAME = "name"
ATTR_PERIOD = "period"
ATTR_VALUES = "values"
ATTR_VALUE = "value"

LIST_PARAM_ATTRS = [ATTR_KEY_STAT, ATTR_FIN_STAT]

# file names
FILE_MS_KEY_STAT = "MorningStarKeyStat"
FILE_MS_FIN_STAT = "MorningStarFinStat"
FILE_MS_STAT = "MorningStarStat"
FILE_MS_STAT_NAMES = "MorningStarStatNames"
FILE_EIDO = "EIDO_2020-08-16051532661688.json"

# parameter names
PARAM_CURR_RATIO = "Current Ratio"
PARAM_CURR_AST = "Total Current Assets"
PARAM_CURR_LIA = "Total Current Liabilities"
PARAM_WORK_CAP = "Working Capital"
PARAM_DIVIDENDS = "Dividends"
PARAM_NET_INC = "Net Income"
PARAM_SHORT_DEBT = "Short-Term Debt"
PARAM_LONG_DEBT = "Long-Term Debt"
PARAM_EPS = "Earnings Per Share"
PARAM_BV = "Book Value Per Share *"

