import datetime
import pytz
from decimal import Decimal

class Trade:
    def __init__(self, coinbase_resp):
        """Parse response data from Coinbase API"""
        self.coinbase_resp = coinbase_resp
        self.parse_response()

    def parse_response(self):
        self.amount = Decimal(self.coinbase_resp["amount"].amount)
        self.currency = self.coinbase_resp["amount"]["currency"]
        self.created_at = datetime.datetime.fromisoformat(self.coinbase_resp["created_at"].replace(
            'Z', '+00:00')).astimezone(pytz.timezone("America/New_York"))
        self.fee = Decimal(self.coinbase_resp["fees"][0]["amount"].amount)
        self.id = self.coinbase_resp["id"]
        self.resource = self.coinbase_resp["resource"]
        self.subtotal = Decimal(self.coinbase_resp["subtotal"]["amount"])
        self.total = Decimal(self.coinbase_resp["total"]["amount"])
        self.price = Decimal(self.coinbase_resp["unit_price"]["amount"])

    def to_dict(self):
        return {
            "currency":self.currency,
            "resource":self.resource,
            "created_at":self.created_at,
            "amount":self.amount,
            "total":self.total,
            "subtotal":self.subtotal,
            "fee":self.fee,
            "price":self.price
        }

    def __repr__(self):
        return f"< {self.resource.upper()}: {self.amount} (${self.total}) {self.currency} >"