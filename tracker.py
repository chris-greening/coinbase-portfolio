import os

from coinbase.wallet.client import Client

from transaction import Transaction
from wallet import Wallet

API_KEY = os.environ.get("COINBASE_API_KEY")
API_SECRET = os.environ.get("COINBASE_API_SECRET")

client = Client(API_KEY, API_SECRET)
accounts = client.get_accounts()

wallets = [Wallet(wallet, client) for wallet in accounts["data"]]