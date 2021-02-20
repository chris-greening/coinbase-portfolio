import os

from coinbase.wallet.client import Client

from portfolio import Portfolio

API_KEY = os.environ.get("COINBASE_API_KEY")
API_SECRET = os.environ.get("COINBASE_API_SECRET")

Portfolio.init(API_KEY, API_SECRET)
portfolio = Portfolio()