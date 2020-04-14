import ccxt

class BinanceTrader:

    def __init__(self, api_key, api_secret, pair):
        self.instance = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True
        })
        self.pair = pair

    def fetch_margin_balance(self):


api_key = "XtuGNXXzJTCL6lWkYwSKZ8k7DEiAw37ytTU6U5Z4NETR6NNZHq5w6uOe7NqecWKv"

api_secret = "dsSUOfgJZiyDkWpNwWHmliRLncQy2AN3buGQ6INBdZYvdBdPtLXQzAZEOkrx8Vr8"