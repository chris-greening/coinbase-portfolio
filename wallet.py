import datetime
import pytz
from decimal import Decimal

import pandas as pd 

from trade import Trade
from transaction import Transaction

class Wallet:
    def __init__(self, coinbase_resp):
        self.coinbase_resp = coinbase_resp

        self.parse_response()
        self._get_all_trades()
        self._get_all_transactions()
        self._calculations()

    def parse_response(self):
        self.amount = Decimal(self.coinbase_resp["balance"].amount)
        self.currency = self.coinbase_resp["currency"]
        self.created_at = datetime.datetime.fromisoformat(self.coinbase_resp["created_at"].replace(
            'Z', '+00:00')).astimezone(pytz.timezone("America/New_York"))
        self.id = self.coinbase_resp["id"]
        self.balance = Decimal(self.coinbase_resp["native_balance"]["amount"])
        print(self.currency)

    @classmethod
    def init(cls, client):
        cls.client = client

    def __repr__(self):
        return f"< {self.currency} Wallet >"

    def _calculate_net_invested(self):
        self.net_invested = Decimal(0)
        for transaction in self.transactions:
            amt = transaction.total
            self.net_invested += amt

    def _calculate_net_gain(self):
        self.net_gain = self.balance - self.net_invested

    def _calculate_net_growth(self):
        try:
            self.net_growth = (self.balance-self.net_invested)/self.net_invested
        except:
            self.net_growth = Decimal(0)

    def _calculations(self):
        self._calculate_net_invested()
        self._calculate_net_gain()
        self._calculate_net_growth()

    def _get_all_transactions(self):
        self.transactions = [Transaction(transaction) for transaction in Wallet.client.get_transactions(self.id)["data"]]
        self.transactions_df = pd.DataFrame([tran.to_dict() for tran in self.transactions])

    def _get_all_trades(self):
        self.buys = sorted([Trade(trade) for trade in Wallet.client.get_buys(self.id)["data"]], key=lambda x: x.created_at)
        self.buys_df = pd.DataFrame([buy.to_dict() for buy in self.buys])
        self.sells = sorted([Trade(trade) for trade in Wallet.client.get_sells(self.id)["data"]], key=lambda x: x.created_at)
        self.sells_df = pd.DataFrame([sell.to_dict() for sell in self.sells])
        self.trades = sorted(self.buys + self.sells, key=lambda x: x.created_at)
        self.trades_df = pd.DataFrame([trade.to_dict() for trade in self.trades])