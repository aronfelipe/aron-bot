from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

class ScrapScrap:

    def __init__(self, chrome_path, options=None):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

    def get(self, url):
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()
        time.sleep(5)

    def wait(self):
        time.sleep(20)

    def maximize(self):
        self.driver.maximize_window()

    def clear_text(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        length = len(element.get_attribute('value'))
        element.send_keys(length * Keys.BACKSPACE)

    def find_xpath(self, xpath, operation, element=None):
        if operation == "click":
            self.driver.find_element_by_xpath(xpath).click()
        elif operation == "send":
            self.driver.find_element_by_xpath(xpath).send_keys(element)
        elif operation == "enter":
            self.driver.find_element_by_xpath(xpath).send_keys(Keys.ENTER)
        elif operation == "find":
            return self.driver.find_element_by_xpath(xpath)
        elif operation == "text":
            return self.driver.find_element_by_xpath(xpath).text

    def find_all_xpath(self, xpath, operation, element=None):
        if operation == "click":
            self.driver.find_elements_by_xpath(xpath).click()
        elif operation == "send":
            self.driver.find_elements_by_xpath(xpath).send_keys(element)
        elif operation == "enter":
            self.driver.find_elements_by_xpath(xpath).send_keys(Keys.ENTER)
        elif operation == "find":
            return self.driver.find_elements_by_xpath(xpath)

    def find_name(self, name, operation, element=None):
        if operation == "click":
            self.driver.find_element_by_name(name).click()
        elif operation == "send":
            self.driver.find_element_by_name(name).send_keys(element)
        elif operation == "enter":
            self.driver.find_element_by_name(name).send_keys(Keys.ENTER)
        elif operation == "find":
            return self.driver.find_element_by_name(name)
