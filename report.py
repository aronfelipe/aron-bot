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

    def close_trade(self, price):
        self.df_trades.loc[self.df_trades.index[-1], 'price_close'] = price

    def calculate_trade(self, leverage):
        if (self.df_trades[-1:]['type'] == 'buy').any():
            diff = (float(self.df_trades[-1:]['price_close']) * float(self.df_trades[-1:]['amount']) * leverage) - (
                        float(self.df_trades[-1:]['price_entry']) * float(self.df_trades[-1:]['amount']) * leverage)
            diff_minus_fee = diff - (float(self.df_trades[-1:]['price_close']) * float(self.df_trades[-1:]['amount']) * self.fee) - (float(self.df_trades[-1:]['price_entry']) * float(self.df_trades[-1:]['amount']) * self.fee)

            self.df_closed = self.df_closed.append({'id': str(uuid.uuid4()),
                                                    'trade_id': self.df_trades[-1:]['id'],
                                                    'difference': str(diff_minus_fee)}, ignore_index=True)
        else:
            diff = (float(self.df_trades[-1:]['price_entry']) * float(self.df_trades[-1:]['amount']) * leverage) - (
                        float(self.df_trades[-1:]['price_close']) * float(self.df_trades[-1:]['amount']) * leverage)
            diff_minus_fee = diff - (float(self.df_trades[-1:]['price_close']) * float(self.df_trades[-1:]['amount']) * self.fee) - (float(self.df_trades[-1:]['price_entry']) * float(self.df_trades[-1:]['amount']) * self.fee)
            self.df_closed = self.df_closed.append({'id': str(uuid.uuid4()),
                                                    'trade_id': self.df_trades[-1:]['id'],
                                                    'difference': str(diff_minus_fee)}, ignore_index=True)