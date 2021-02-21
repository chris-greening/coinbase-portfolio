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

    def to_csv(fpath: str) -> None:
        pass 

    @classmethod
    def init(cls, api_key: str, api_secret: str) -> None:
        """Sets the API tokens for the Coinbase API"""
        cls.api_key = api_key
        cls.api_secret = api_secret

    def _load_wallets(self):
        Wallet.init(self.client)
        self.wallets = {wallet["currency"]: Wallet(wallet) for wallet in self.accounts["data"]}
        self.buys = [buy for wallet in self.wallets.values() for buy in wallet.buys]
        self.buys = sorted(self.buys, key=lambda x: x.created_at)

        self.sells = [sell for wallet in self.wallets.values() for sell in wallet.sells]
        self.sells = sorted(self.sells, key=lambda x: x.created_at)