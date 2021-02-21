# Author: Chris Greening 
# Date: 02/19/2021
# Purpose: Coinbase portfolio contents 

from coinbase.wallet.client import Client 
import pandas as pd

from wallet import Wallet

class Portfolio:
    def __init__(self):
        self.client = Client(Portfolio.api_key, Portfolio.api_secret)

        self.accounts = self.client.get_accounts()

        self._load_wallets()
        self._calculations()

    def to_csv(fpath: str) -> None:
        pass 

    @classmethod
    def init(cls, api_key: str, api_secret: str) -> None:
        """Sets the API tokens for the Coinbase API"""
        cls.api_key = api_key
        cls.api_secret = api_secret

    def __getitem__(self, key):
        return self.wallets[key]

    def _calculations(self):
        self.balance = sum([wallet.balance for wallet in self.wallets.values()])
        self.net_invested = sum([wallet.net_invested for wallet in self.wallets.values()])
        self.net_gain = sum([wallet.net_gain for wallet in self.wallets.values()])
        self.net_growth = (self.balance-self.net_invested)/self.net_invested

    def _load_wallets(self):
        Wallet.init(self.client)
        self.wallets = {wallet["currency"]: Wallet(wallet) for wallet in self.accounts["data"]}
        
        self.buys = [buy for wallet in self.wallets.values() for buy in wallet.buys]
        self.buys = sorted(self.buys, key=lambda x: x.created_at)
        self.buys_df = pd.DataFrame([buy.to_dict() for buy in self.buys])    
        
        self.sells = [sell for wallet in self.wallets.values() for sell in wallet.sells]
        self.sells = sorted(self.sells, key=lambda x: x.created_at)
        self.sells_df = pd.DataFrame([sell.to_dict() for sell in self.sells])

        self.trades = sorted(self.buys + self.sells, key=lambda x: x.created_at)
        self.trades_df = pd.DataFrame([trade.to_dict() for trade in self.trades])

        self.transactions = sorted([transaction for wallet in self.wallets.values() for transaction in wallet.transactions], key=lambda x: x.created_at)
        self.transactions_df = pd.DataFrame([tran.to_dict() for tran in self.transactions])