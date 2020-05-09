from crawler import TradingCrawler
from report import TradingReport

import time
import datetime

class TradingApp:

    def __init__(self, chrome_path, url, fee, initial):

        self.chrome_path = chrome_path
        self.url = url
        self.fee = fee
        self.initial = initial

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
        self.trading_report.create_df_value()
        self.trading_report.create_df_indicator()

    def make_float(self, num):
        
        num = num.replace(' ', '').replace(',', '.').replace("−", "-")
        try:
            return float(num)
        except:
            return 0

    def loop(self):

        try:
        
            value = self.make_float(self.trading_crawler.currency_value())

            self.currency = (self.initial / 2) * value
            self.amount = self.initial / 2

            buy = None
            sell = None
            counter = 0

            while True:

                if str(datetime.datetime.utcnow().second) == "0":

                    value = self.make_float(self.trading_crawler.currency_value())

                    if (self.trading_report.df_trades[-1:]['side'] == 'sell').any(): 
                        if value > float(self.trading_report.df_trades[-1:]['price']) + (float(self.trading_report.df_trades[-1:]['price']) * 0.0075):
                            self.trading_report.insert_buy("binance", "tema400 < tema100 & BB%B >= 0 ", str(value), (((20/100) * self.currency)/value))
                            self.amount = self.amount + (((20/100) * self.currency)/value)
                            self.currency = self.currency - ((20/100) * self.currency)
                            self.trading_report.insert_value(["BTC", self.amount * value, self.amount, (100 * self.amount * value)/(self.amount * value) + self.currency],
                            ["USDT", self.currency, self.currency, (100 * self.currency)/(self.amount * value) + self.currency])

                    if (self.trading_report.df_trades[-1:]['side'] == 'buy').any():
                        if value > float(self.trading_report.df_trades[-1:]['price']) - (float(self.trading_report.df_trades[-1:]['price']) * 0.0075):
                            self.trading_report.insert_sell("binance", "tema400 > tema100 & BB%B <= 0 ", str(value), ((20/100) * self.amount))
                            self.currency = self.currency + ((20/100) * self.amount * value)
                            self.amount = self.amount - ((20/100) * self.amount)
                            self.trading_report.insert_value(["BTC", self.amount * value, self.amount, (100 * self.amount * value)/(self.amount * value) + self.currency],
                            ["USDT", self.currency, self.currency, (100 * self.currency)/(self.amount * value) + self.currency])


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
                            if (self.trading_report.df_trades[-1:]['side'] == 'sell').any() or self.trading_report.df_trades.empty:
                                self.trading_report.insert_buy("binance", "tema400 < tema100 & BB%B >= 0 ", str(value), (((20/100) * self.currency)/value))
                                self.amount = self.amount + (((20/100) * self.currency)/value)
                                self.currency = self.currency - ((20/100) * self.currency)
                                self.trading_report.insert_value(["BTC", self.amount * value, self.amount, (100 * self.amount * value)/((self.amount * value) + self.currency)],
                                ["USDT", self.currency, self.currency, (100 * self.currency)/(self.amount * value) + self.currency])
                                buy = False
                                counter = 0

                            if (self.trading_report.df_trades[-1:]['side'] == 'buy').any():
                                buy = False

                    if sell:
                        if tema400 - (tema400 * 0.0009) > tema100 and counter <= 0 :
                            if (self.trading_report.df_trades[-1:]['side'] == 'buy').any() or self.trading_report.df_trades.empty:
                                self.trading_report.insert_sell("binance", "tema400 > tema100 & BB%B <= 0 ", str(value), ((20/100) * self.amount))
                                self.currency = self.currency + ((20/100) * self.amount * value)
                                self.amount = self.amount - ((20/100) * self.amount)
                                self.trading_report.insert_value(["BTC", self.amount * value, self.amount, (100 * self.amount * value)/((self.amount * value) + self.currency)],
                                ["USDT", self.currency, self.currency, (100 * self.currency)/(self.amount * value) + self.currency])
                                sell = False
                                counter = 0

                            if (self.trading_report.df_trades[-1:]['side'] == 'sell').any():
                                sell = False

                    compression_opts_trades = dict(method='zip',
                                                archive_name='trades.csv')
                    compression_opts_value = dict(method='zip',
                                                archive_name='value.csv')
                    compression_opts_indicator = dict(method='zip',
                                                archive_name='indicator.csv')

                    self.trading_report.df_trades.to_csv('trades.zip', index=False,
                                                        compression=compression_opts_trades)

                    self.trading_report.df_value.to_csv('value.zip', index=False,
                                                        compression=compression_opts_value)

                    self.trading_report.df_indicator.to_csv('indicator.zip', index=False,
                                                        compression=compression_opts_indicator)

                    time.sleep(5)

        except Exception as e:
            print(e, flush=True)
            time.sleep(30)
            self.loop()


# chrome_path = r"/root/chromedriver"
chrome_path = r"/home/felipe/Documents/chromedriver"

url = "https://www.tradingview.com/chart/"


def initialize_bot(chrome_path, url, fee, initial):
    try:
        app = TradingApp(chrome_path=chrome_path, url=url, fee=fee, initial=initial)
        app.loop()
    except Exception as e:
        print(e, flush=True)
        initialize_bot(chrome_path, url, fee, initial)

initialize_bot(chrome_path, url, 0.00075, 1)
