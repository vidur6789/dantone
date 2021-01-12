from enum import Enum

class TransactionType(Enum):
    BUY = 1, 
    SELL = 2

class Exchange(Enum):
    NYSE = 'NYSE',
    BOM = 'BO',
    NSE = 'NS'