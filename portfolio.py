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

        Wallet.init(self.client)
        self.wallets = {wallet["currency"]: Wallet(wallet) for wallet in self.accounts["data"]}

    def to_csv(fpath: str) -> None:

    @classmethod
    def init(cls, api_key: str, api_secret: str) -> None:
        """Sets the API tokens for the Coinbase API"""
        cls.api_key = api_key
        cls.api_secret = api_secret
