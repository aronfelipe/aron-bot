from crawler import TradingCrawler
from report import TradingReport

import time
import datetime

class TradingApp:

    def __init__(self, chrome_path, url, fee, initial):

        self.trading_report = TradingReport(fee=fee)

        self.trading_crawler = TradingCrawler(chrome_path, url)
        self.trading_crawler.login_xpath("aronakamoto@outlook.com", "420DevOps")
        self.trading_crawler.select_currency("BINANCE:BTCUSDT")
        self.trading_crawler.select_time("1")
        self.trading_crawler.select_indicator("Triple EMA")
        self.trading_crawler.select_indicator("Triple EMA")
        self.trading_crawler.select_indicator("Bollinger Bands %B")
        self.trading_crawler.setting_indicator(2)
        self.trading_crawler.ema_setting_configuration("400")
        self.trading_crawler.setting_indicator(3)
        self.trading_crawler.ema_setting_configuration("100")
        self.trading_crawler.click_graph()
        self.trading_crawler.click_value()

        self.trading_report.create_df_trades()
        self.trading_report.create_df_closed()
        self.trading_report.create_df_indicator()
        self.trading_report.create_df_value()

        self.initial = initial

    def make_float(self, num):
        num = num.replace(' ', '').replace(',', '.').replace("−", "-")
        try:
            return float(num)
        except:
            return 0

    def loop(self):
        try:

            buy = None
            sell = None
            counter = 0

            value = self.make_float(self.trading_crawler.currency_value())

            self.currency = (self.initial / 2) * value
            self.amount = self.initial / 2
                                
            self.trading_report.insert_value(self.amount, self.currency, value)

            while True:

                if str(datetime.datetime.utcnow().second) == "0":

                    value = self.make_float(self.trading_crawler.currency_value())

                    if (self.trading_report.df_trades[-1:]['type'] == 'sell').any() and \
                           self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                        if value > float(self.trading_report.df_trades[-1:]['price_entry']) + (float(self.trading_report.df_trades[-1:]['price_entry']) * 0.0075):
                            self.amount = self.amount + float(self.trading_report.df_trades[-1:]['amount'])
                            self.currency = self.currency - (float(self.trading_report.df_trades[-1:]['amount']) * value)
                            self.trading_report.close_trade(value)
                            self.trading_report.calculate_trade()
                            self.trading_report.insert_value(self.amount, self.currency, value)

                    if (self.trading_report.df_trades[-1:]['type'] == 'buy').any() and \
                           self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                        if value < float(self.trading_report.df_trades[-1:]['price_entry']) - (float(self.trading_report.df_trades[-1:]['price_entry']) * 0.0075):
                            self.amount = self.amount - float(self.trading_report.df_trades[-1:]['amount'])
                            self.currency = self.currency + (float(self.trading_report.df_trades[-1:]['amount']) * value)
                            self.trading_report.close_trade(value)
                            self.trading_report.calculate_trade()
                            self.trading_report.insert_value(self.amount, self.currency, value)

                    tema400 = self.make_float(self.trading_crawler.bot.find_xpath(
                        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[3]/div[3]/div/div/div",
                        "text"))
                    tema100 = self.make_float(self.trading_crawler.bot.find_xpath(
                        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[4]/div[3]/div/div/div",
                        "text"))
                    bb = self.make_float(self.trading_crawler.bot.find_xpath(
                        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[3]/div/div/div",
                        "text"))

                    if value == 0 or tema400 == 0 or tema100 == 0:
                        self.loop()

                    print("TIME", flush=True)
                    print(str(datetime.datetime.utcnow().hour), flush=True)
                    print("VALUE", flush=True)
                    print(value, flush=True)
                    print("TEMA400", flush=True)
                    print(tema400, flush=True)
                    print("TEMA100", flush=True)
                    print(tema100, flush=True)
                    print("BB", flush=True)
                    print(bb, flush=True)
                    print("COUNTER", flush=True)
                    print(counter, flush=True)
                    print("BUY", flush=True)
                    print(buy, flush=True)
                    print("SELL", flush=True)
                    print(sell, flush=True)

                    self.trading_report.insert_indicator(tema400, tema100, bb, counter, buy, sell)

                    if bb < 0:
                        counter = counter + 1
                    elif bb > 1:
                        counter = counter - 1

                    if tema400 > tema100:
                        buy = True
                    elif tema400 < tema100:
                        sell = True

                    if buy:
                        if (tema400 + (tema400 * 0.0009)) < tema100 and counter >= 0:
                            if (self.trading_report.df_trades[-1:]['type'] == 'sell').any() and \
                                    self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                                
                                self.trading_report.close_trade(value)
                                self.trading_report.calculate_trade()
                                self.amount = self.amount + int(self.trading_report.df_trades[-1:]['amount'])
                                self.currency = self.currency - (int(self.trading_report.df_trades[-1:]['amount']) * value) + (int(self.trading_report.df_closed[-1:]['difference']))

                            if (self.trading_report.df_trades[-1:]['type'] == 'buy').any() and \
                                    self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                                buy = False
                                counter = 0
                            else:
                                self.trading_report.insert_trade("binance", "buy", "tema400 < tema100 & BB%B >= 0 ", str(value), ((self.currency * 20/100)/value))
                                self.amount = self.amount + ((self.currency * 20/100)/value)
                                self.currency = self.currency - (self.currency * 20/100)
                                buy = False
                                counter = 0
                                self.trading_report.insert_value(self.amount, self.currency, value)


                    if sell:
                        if tema400 - (tema400 * 0.0009) > tema100 and counter <= 0:
                            if (self.trading_report.df_trades[-1:]['type'] == 'buy').any() and \
                                    self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                                self.trading_report.close_trade(value)
                                self.trading_report.calculate_trade()
                                self.amount = self.amount - int(self.trading_report.df_trades[-1:]['amount'])
                                self.currency = self.currency + (int(self.trading_report.df_trades[-1:]['amount']) * value) + (int(self.trading_report.df_closed[-1:]['difference']))

                            if (self.trading_report.df_trades[-1:]['type'] == 'sell').any() and \
                                    self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                                sell = False
                                counter = 0
                            else:
                                self.trading_report.insert_trade("binance", "sell", "tema400 > tema100 & BB%B <= 1", str(value), (self.amount * (20/100)))
                                self.currency = self.currency + (self.amount * (20/100) * value)
                                self.amount = self.amount - (self.amount * (20/100))
                                sell = False
                                counter = 0
                                self.trading_report.insert_value(self.amount, self.currency, value)

                    compression_opts_trades = dict(method='zip',
                                                archive_name='trades.csv')
                    compression_opts_closed = dict(method='zip',
                                                archive_name='closed.csv')
                    compression_opts_indicator = dict(method='zip',
                                                archive_name='indicator.csv')
                    compression_opts_value = dict(method='zip',
                                                archive_name='value.csv')

                    self.trading_report.df_trades.to_csv('trades.zip', index=False,
                                                        compression=compression_opts_trades)

                    self.trading_report.df_closed.to_csv('closed.zip', index=False,
                                                        compression=compression_opts_closed)

                    self.trading_report.df_indicator.to_csv('indicator.zip', index=False,
                                                        compression=compression_opts_indicator)
                                                        
                    self.trading_report.df_value.to_csv('value.zip', index=False,
                                                        compression=compression_opts_value)
                    time.sleep(5)

        except Exception as e:
            print(e, flush=True)
            time.sleep(30)
            self.loop()


chrome_path = r"/root/chromedriver"
# chrome_path = r"/home/felipe/Documents/chromedriver"

url = "https://www.tradingview.com/chart/"


def initialize_bot(chrome_path, url, fee, initial):
    try:
        app = TradingApp(chrome_path=chrome_path, url=url, fee=fee, initial=initial)
        app.loop()
    except Exception as e:
        print(e, flush=True)
        initialize_bot(chrome_path, url, fee, initial)

initialize_bot(chrome_path, url, 0.00075, 1)
