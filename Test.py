
import adapter.finance as fin
from datetime import datetime
from decimal import Decimal



import pandas as pd
from portfolio.portfolio import Transaction, Portfolio, Stock, read_csv
from constants.enums import TransactionType
 

pf = read_csv('test/data/test3.csv', name='FSM')

returns = pf.time_weighted_return()

print(returns)

holdings = pf.net_holdings()

for t in pf.transactions:
    print(t)

for h in holdings:
    print(h)

print(pf.unrealised_return())


