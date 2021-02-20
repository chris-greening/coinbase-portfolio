import datetime
import pytz

from transaction import Transaction

class Wallet:
    def __init__(self, coinbase_resp):
        self.coinbase_resp = coinbase_resp

        self.parse_response()
        self.get_all_transactions()

    def parse_response(self):
        self.amount = float(self.coinbase_resp["balance"].amount)
        self.currency = self.coinbase_resp["currency"]
        self.created_at = datetime.datetime.fromisoformat(self.coinbase_resp["created_at"].replace(
            'Z', '+00:00')).astimezone(pytz.timezone("America/New_York"))
        self.id = self.coinbase_resp["id"]
        self.balance = self.coinbase_resp["native_balance"]["amount"]
        print(self.currency)

    def get_all_transactions(self):
        self.buys = [Transaction(transaction) for transaction in Wallet.client.get_buys(self.id)["data"]]
        self.sells = [Transaction(transaction) for transaction in Wallet.client.get_sells(self.id)["data"]]

    def __repr__(self):
        return f"< {self.currency} Wallet >"

    @classmethod
    def init(cls, client):
        cls.client = client