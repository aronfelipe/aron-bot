from scrap import ScrapScrap
from selenium.webdriver.common.action_chains import ActionChains
import time


class TradingCrawler:

    def __init__(self, chrome_path, url):
        self.bot = ScrapScrap(chrome_path=chrome_path)
        self.bot.get(url)
        self.bot.maximize()
        self.bot.wait()

    def select_currency(self, currency):

        self.bot.clear_text("/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input")
        self.bot.find_xpath("/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input",
                            "send", currency)
        self.bot.find_xpath("/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div/input",
                            "enter")

        time.sleep(5)

    def login_xpath(self, username, password):
        try:
            self.bot.find_xpath("/html/body/div[2]/div[5]/div/div[1]/div[1]/div[1]/div[1]/div[1]/span/input", "send",
                                "BTC")
            time.sleep(1)
            self.bot.find_xpath("/html/body/div[2]/div[5]/div/div[1]/div[1]/div[1]/div[1]/div[1]/span/input", "enter")
            time.sleep(2)

            self.bot.find_xpath(
                "/html/body/div[8]/div/div[2]/div/div/div/div/div/div[1]/div[4]/div/form[1]/div[1]/div[1]/input",
                "send", username)
            time.sleep(1)

            self.bot.find_xpath(
                "/html/body/div[8]/div/div[2]/div/div/div/div/div/div[1]/div[4]/div/form[1]/div[2]/div[1]/div[1]/input",
                "send", password)
            self.bot.find_xpath(
                "/html/body/div[8]/div/div[2]/div/div/div/div/div/div[1]/div[4]/div/form[1]/div[2]/div[1]/div[1]/input",
                "enter")

            time.sleep(10)

        except:
            self.login_name(username, password)

    def login_name(self, username, password):

        self.bot.find_name("username", "send", username)
        self.bot.find_name("username", "enter")
        time.sleep(1)

        self.bot.find_name("password", "send", password)
        self.bot.find_name("password", "enter")

        time.sleep(10)

    def select_time(self, _time):

        self.bot.find_xpath("/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[2]/div/div/div/div",
                            "click")
        if _time == "1":
            self.bot.find_xpath("/html/body/div[7]/div/span/div[1]/div/div/div/div[8]/div", "click")
        elif _time == "3":
            self.bot.find_xpath("/html/body/div[8]/div/span/div[1]/div/div/div/div[5]/div/div[1]/div", "click")
        elif _time == "5":
            self.bot.find_xpath("/html/body/div[8]/div/span/div[1]/div/div/div/div[6]/div/div[1]/div", "click")

    def select_indicator(self, indicator):
        try:
            self.bot.find_xpath("/html/body/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[5]/div/div",
                                "click")
            time.sleep(1)
            self.bot.find_name("q", "send", indicator)
            self.bot.find_name("q", "enter")
            time.sleep(1)
            self.bot.find_xpath("//*[@title='" + indicator + "']", "click")
            time.sleep(1)
            self.bot.find_xpath("/html/body/div[7]/div/div/div[3]", "click")
            time.sleep(1)
        except:
            self.select_indicator(indicator)

    def setting_indicator(self, number):
        indicator_button = self.bot.find_xpath(
            "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[" + str(
                number + 1) + "]/div[1]/div[2]", "find")
        self.bot.driver.implicitly_wait(10)
        ActionChains(self.bot.driver).move_to_element(indicator_button).perform()
        self.bot.find_xpath(
            "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[" + str(
                number + 1) + "]/div[2]/div/div[2]", "click")

    def ema_setting_configuration(self, length):
        input_element_length = self.bot.find_xpath('//input[@value = "9"]', "find")
        clear = self.bot.clear_text("//input[@value = '9']")
        input_element_length.send_keys(length)
        self.bot.find_xpath('/html/body/div[7]/div/div/div[1]/div/div[4]/div/span/button', "click")

    def ema_value(self, number):
        ema = self.bot.find_xpath(
            "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[" + str(
                2 + number) + "]/div[3]/div/div/div", "text")
        return ema

    def click_graph(self):
        self.bot.find_xpath("/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/canvas[2]", "click")

    def click_value(self):
        self.bot.find_xpath("/html/body/div[2]/div[5]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[3]/span[1]", "click")

    def currency_value(self):
        value = self.bot.find_xpath(
            "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[2]/div/div[4]/div[2]",
            "text")
        return value

    def currency_value_header(self):
        value = self.bot.find_xpath(
            "/html/body/div[2]/div[5]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[3]/span[1]",
            "text"
        )
        return value
