import pandas as pandas
import uuid
import datetime

class TradingReport:

    def __init__(self, fee):
        self.fee = fee
        self.pd = pandas

    def create_df_trades(self):
        data = {'id': [], 'exchange': [], 'indicator': [], 'side': [], 'price': [], 'amount': [], 'time': []}
        self.df_trades = self.pd.DataFrame(data)

    def create_df_value(self):
        data = {'id': [], 'currency_one_name': [], 'currency_one_value': [], 'currency_one_amount': [], 'currency_one_percentage': [], \
            'currency_two_name': [], 'currency_two_value': [], 'currency_two_amount': [], 'currency_two_percentage': [], \
            'total_value': [], 'time': []}
        self.df_value = self.pd.DataFrame(data)

    def create_df_indicator(self):
        data = {'id': [], 'tema400': [], 'tema100': [], 'bb': [], 'counter': [], 'buy': [], 'sell': [], 'time': []}
        self.df_indicator = self.pd.DataFrame(data)

    def insert_buy(self, exchange, indicator, price, amount):
        self.df_trades = self.df_trades.append({
            'id': str(uuid.uuid4()),
            'exchange': str(exchange),
            'indicator': str(indicator),
            'side': "buy",
            'price': str(price),
            'amount': str(amount),
            'time': str(datetime.datetime.utcnow())
        }, ignore_index=True)

    def insert_sell(self, exchange, indicator, price, amount):
        self.df_trades = self.df_trades.append({
            'id': str(uuid.uuid4()),
            'exchange': str(exchange),
            'indicator': str(indicator),
            'side': "sell",
            'price': str(price),
            'amount': str(amount),
            'time': str(datetime.datetime.utcnow())
        }, ignore_index=True)

    def insert_value(self, currency_one, currency_two):
        self.df_value = self.df_value.append({
            'id': str(uuid.uuid4()),
            'currency_one_name': str(currency_one[0]),
            'currency_one_value': str(currency_one[1]),
            'currency_one_amount': str(currency_one[2]),
            'currency_one_percentage': str(currency_one[3]),
            'currency_two_name': str(currency_two[0]),
            'currency_two_value': str(currency_two[1]),
            'currency_two_amount': str(currency_two[2]),
            'currency_two_percentage': str(currency_two[3]),
            'total_value': str(currency_one[1] + currency_two[1]),
            'time': str(datetime.datetime.utcnow())
        }, ignore_index=True)

    def insert_indicator(self, tema400, tema100, bb, counter, buy, sell):
        self.df_indicator = self.df_indicator.append({
            'id': str(uuid.uuid4()),
            'tema400': tema400,
            'tema100': tema100,
            'bb': bb,
            'counter': counter,
            'buy': buy,
            'sell': sell,
            'time': str(datetime.datetime.utcnow())
        }, ignore_index=True)