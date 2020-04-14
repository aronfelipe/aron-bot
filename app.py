from crawler import TradingCrawler
from report import TradingReport

import time
import datetime

class TradingApp:

    def __init__(self, chrome_path, url, fee):

        self.trading_report = TradingReport(fee=fee)

        self.trading_crawler = TradingCrawler(chrome_path, url)
        self.trading_crawler.login_xpath("gubenites99@gmail.com", "plokiju12")
        # self.trading_crawler.login_xpath("aronakamoto@outlook.com", "420DevOps")
        self.trading_crawler.select_currency("BITMEX:XBTUSD")
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

            while True:

                if str(datetime.datetime.utcnow().second) == "1":

                    value = self.make_float(self.trading_crawler.currency_value())

                    if (self.trading_report.df_trades[-1:]['type'] == 'sell').any() and \
                            self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                        if value > float(self.trading_report.df_trades[-1:]['price_entry']) + (float(self.trading_report.df_trades[-1:]['price_entry']) * 0.005):
                            self.trading_report.close_trade(value)
                            self.trading_report.calculate_trade(1)

                    if (self.trading_report.df_trades[-1:]['type'] == 'buy').any() and \
                            self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                        if value < float(self.trading_report.df_trades[-1:]['price_entry']) - (float(self.trading_report.df_trades[-1:]['price_entry']) * 0.005):
                            self.trading_report.close_trade(value)
                            self.trading_report.calculate_trade(1)

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

                    if bb < 0:
                        counter += 1
                    elif bb > 1:
                        counter -= 1

                    if tema400 > tema100:
                        buy = True

                    if buy:
                        if tema400 < tema100 and counter >= 0:
                            if (self.trading_report.df_trades[-1:]['type'] == 'sell').any() and \
                                    self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                                self.trading_report.close_trade(value)
                                self.trading_report.calculate_trade(1)

                            self.trading_report.insert_trade("bitmex", "buy", " tema400 < tema100 & BB%B >= 0 ", str(value), '1.0')
                            buy = False
                            counter = 0

                    if tema400 < tema100:
                        sell = True

                    if sell:
                        if tema400 > tema100 and counter <= 0:
                            if (self.trading_report.df_trades[-1:]['type'] == 'buy').any() and \
                                    self.trading_report.df_trades[-1:]['price_close'].isnull().any():
                                self.trading_report.close_trade(value)
                                self.trading_report.calculate_trade(1)

                            self.trading_report.insert_trade("bitmex", "sell", "tema400 > tema100 & BB%B <= 1", str(value), '1.0')
                            sell = False
                            counter = 0

                    compression_opts_trades = dict(method='zip',
                                                archive_name='trades.csv')
                    compression_opts_closed = dict(method='zip',
                                                archive_name='closed.csv')

                    self.trading_report.df_trades.to_csv('trades.zip', index=False,
                                                        compression=compression_opts_trades)

                    self.trading_report.df_closed.to_csv('closed.zip', index=False,
                                                        compression=compression_opts_closed)

                    time.sleep(5)

        except Exception as e:
            print(e, flush=True)
            time.sleep(30)
            self.loop()


# chrome_path = r"/root/chromedriver"
chrome_path = r"/home/felipe/Documents/chromedriver"

url = "https://www.tradingview.com/chart/"


def initialize_bot(chrome_path, url, fee):
    try:
        app = TradingApp(chrome_path=chrome_path, url=url, fee=fee)
        app.loop()
    except Exception as e:
        print(e, flush=True)
        initialize_bot(chrome_path, url, fee)

initialize_bot(chrome_path, url, 0.00075)
