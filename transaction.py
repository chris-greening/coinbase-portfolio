import datetime
import pytz
from decimal import Decimal 

class Transaction: 
    TYPE_TO_RESOURCE_MAP = {
        "buy": "buy",
        "send": "from",
        "sell": "sell"
    }
    def __init__(self, coinbase_resp):
        self.coinbase_resp = coinbase_resp
        self.parse_response()

    def parse_response(self):
        self.amount = Decimal(self.coinbase_resp["amount"]["amount"])
        self.currency = self.coinbase_resp["amount"]["currency"]
        self.id = self.coinbase_resp["id"]
        self.created_at = datetime.datetime.fromisoformat(self.coinbase_resp["created_at"].replace(
            'Z', '+00:00')).astimezone(pytz.timezone("America/New_York"))
        self.total = Decimal(self.coinbase_resp["native_amount"]["amount"])
        self.resource = self.coinbase_resp["type"]
        transaction_type = Transaction.TYPE_TO_RESOURCE_MAP[self.resource]
        self.transaction_id = self.coinbase_resp[transaction_type]["id"]

    def to_dict(self):
        return {
            # "id":self.id,
            # "transaction_id":self.transaction_id,
            "resource":self.resource,
            "amount":self.amount,
            "currency":self.currency,
            "created_at":self.created_at,
            "total":self.total
        }

    def __repr__(self):
        transaction_type = Transaction.TYPE_TO_RESOURCE_MAP[self.resource]
        return f"< {transaction_type.upper()}: {self.amount} (${self.total}) {self.currency} >"