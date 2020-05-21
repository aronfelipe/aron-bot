import pandas as pandas
import uuid
import datetime

class TradingReport:

    def __init__(self, fee):
        self.fee = fee
        self.pd = pandas

    def create_df_trades(self):
        data = {'id': [], 'exchange': [], 'indicator': [], 'type': [], 'price_entry': [], 'price_close': [],
                'amount': [], "time":[]}
        self.df_trades = self.pd.DataFrame(data)

    def create_df_closed(self):
        data = {'id': [], 'trade_id': [], 'difference': []}
        self.df_closed = self.pd.DataFrame(data)

    def create_df_indicator(self):
        data = {'id': [], 'tema400': [], 'tema100': [], 'bb':[], 'counter':[], 'buy': [], 'sell':[], 'time':[]}
        self.df_indicator = self.pd.DataFrame(data)

    def create_df_value(self):
        data = {'id': [], 'amount': [], 'currency': [], 'total':[], "time": []}
        self.df_value = self.pd.DataFrame(data)

    def insert_value(self, amount, currency, value, reason):
        self.df_value = self.df_value.append({
            'id': str(uuid.uuid4()),
            'amount': amount,
            'currency': currency,
            'total': currency + (amount * value),
            'reason': reason,
            'time': str(datetime.datetime.utcnow())
        }, ignore_index=True)

    def insert_trade(self, exchange, _type, indicator, price, amount):
        self.df_trades = self.df_trades.append({
            'id': str(uuid.uuid4()),
            'exchange': exchange,
            'indicator': indicator,
            'type': _type,
            'price_entry': price,
            'amount': amount,
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

    def close_trade(self, price):
        self.df_trades.loc[self.df_trades.index[-1], 'price_close'] = price

    def calculate_trade(self):
        if (self.df_trades[-1:]['type'] == 'buy').any():
            diff = (float(self.df_trades[-1:]['price_close']) * float(self.df_trades[-1:]['amount'])) - (
                        float(self.df_trades[-1:]['price_entry']) * float(self.df_trades[-1:]['amount']))
            diff_minus_fee = diff - (float(self.df_trades[-1:]['price_close']) * float(self.df_trades[-1:]['amount']) * self.fee) - (float(self.df_trades[-1:]['price_entry']) * float(self.df_trades[-1:]['amount']) * self.fee)

            self.df_closed = self.df_closed.append({'id': str(uuid.uuid4()),
                                                    'trade_id': self.df_trades[-1:]['id'],
                                                    'difference': str(diff_minus_fee)}, ignore_index=True)
        else:
            diff = (float(self.df_trades[-1:]['price_entry']) * float(self.df_trades[-1:]['amount'])) - (
                        float(self.df_trades[-1:]['price_close']) * float(self.df_trades[-1:]['amount']))
            diff_minus_fee = diff - (float(self.df_trades[-1:]['price_close']) * float(self.df_trades[-1:]['amount']) * self.fee) - (float(self.df_trades[-1:]['price_entry']) * float(self.df_trades[-1:]['amount']) * self.fee)
            self.df_closed = self.df_closed.append({'id': str(uuid.uuid4()),
                                                    'trade_id': self.df_trades[-1:]['id'],
                                                    'difference': str(diff_minus_fee)}, ignore_index=True)