from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional
from datetime import datetime, date

import adapter.finance as fin
import pandas as pd

from constants.enums import TransactionType


@dataclass(frozen=True)
class Stock:
    exchange: str
    ticker: str



@dataclass(frozen=True)
class Period:
    start: datetime
    end: datetime

@dataclass(frozen=True)
class Transaction:
    transaction_type: TransactionType
    price: Decimal
    quantity: int 
    stock: Stock
    currency: str
    date: datetime

    def signed_quantity(self):
        return self.quantity * (-1 if self.transaction_type == TransactionType.SELL else 1)


@dataclass(frozen=True)
class Holding:
    stock: Stock
    quantity: int
    invested: Decimal
    value: Decimal




class Portfolio:

    def __init__(self, name: str, transactions: List[Transaction]):
        self.name = name
        self._transactions = sorted(transactions, key=lambda t: t.date)


    @property
    def transactions(self):
        return self._transactions

    def parse_file(self, filename):
        """
        convert excel/csv file of transactions to Portfolio object
        """
        df = pd.read_csv(filename)
        transactions = []
        return Portfolio(name=filename, transactions=transactions)

    def _aggregate_transactions(self, transactions: List[Transaction], sell_strat='fifo'):
        '''
        aggregate buy/sell transactions for a given stock into single net holding
        '''
        txn_dict = {TransactionType.BUY: [], TransactionType.SELL: []}
        for txn in transactions:
            txn_dict[txn.transaction_type].append(txn)
        
        sell_qty = sum([t.quantity for t in txn_dict[TransactionType.SELL]])
        
        # txns sorted in __init__
        # txn_dict[TransactionType.BUY].sort(key=lambda t: t.date)

        net_qty, net_invested = 0, Decimal(0)
        for txn in txn_dict[TransactionType.BUY]:
            # add to net holdings for buy transactions more than sales
            if txn.quantity > sell_qty: 
                remaining = txn.quantity - sell_qty
                net_qty += remaining
                net_invested += remaining * txn.price
            
            sell_qty = max(sell_qty - txn.quantity, 0)

        return net_qty, net_invested


    def net_holdings(self, sell_strat='fifo'):
        '''
        function to return net holdings of the portfolio
        '''
        stock_txns = {}
        for transaction in self.transactions:
            if transaction.stock not in stock_txns:
                stock_txns[transaction.stock] = []  
            stock_txns[transaction.stock].append(transaction)
        
        holdings = []
        for stock, txns in stock_txns.items():
            quantity, invested = self._aggregate_transactions(txns, sell_strat=sell_strat)
            price = fin.get_price(stock)
            value = Decimal(price) * quantity
            holding = Holding(stock=stock, quantity=quantity, invested=invested, value=value)
            holdings.append(holding)
        
        return holdings
        



    def time_weighted_return(self, period: Period = None, currency: str = None):
        '''
        function to return time-weighted return with time periods divided based on txn dates
        '''
        # group transactions by date        
        date_txns = {}
        for txn in self.transactions:
            if txn.date.date() not in date_txns:
                date_txns[txn.date.date()] = []
            date_txns[txn.date.date()].append(txn)

        dates = sorted(date_txns.keys()) + [date.today()]
        returns = []
        holdings = {} 
        holdings_value = Decimal(0)
        
        # for each transaction date
        for i in range(len(dates) - 1):
            beg_date, end_date = dates[i], dates[i+1]
            
            # beginning value
            txns_value = sum([t.signed_quantity() * t.price for t in date_txns[beg_date]])
            beg_value = txns_value + holdings_value
            
            # update holdings
            for txn in date_txns[beg_date]:
                if txn.stock not in holdings:
                    holdings[txn.stock] = 0
                holdings[txn.stock] += txn.signed_quantity()

            # holding period return
            holdings_value = sum([Decimal(fin.get_price(stock, req_date=end_date)) * qty for stock, qty in holdings.items()])

            dividends = Decimal(0) # TODO
            hpr = (holdings_value + dividends - beg_value) / beg_value
            returns.append(hpr)

        return returns

    def unrealised_return(self):

        invested = Decimal(0)
        value = Decimal(0)

        for h in self.net_holdings():
            invested += h.invested
            value += h.value
        
        return (value - invested)/invested



    
def read_csv(filepath: str, name: Optional[str]) -> Portfolio: 

    df = pd.read_csv(filepath)
    transactions = df.apply(
        lambda r: Transaction(
            transaction_type=TransactionType[r['TransactionType']],
            price=Decimal(r['Price']),
            quantity=int(r['Quantity']),
            stock=Stock(exchange=r['Exchange'], ticker=r['Ticker']),
            currency=r['Currency'],
            date=datetime.strptime(r['Date'], "%d/%m/%Y")), 
        axis=1)

    return Portfolio(
        name=name if name else filepath, 
        transactions=transactions)

    

# TODO
# Currency Handling -> Present vs Transaction Date FX rate
# Fees Handling -> Transaction + FX(new Type)
# Dividends
# API
# Dash interface