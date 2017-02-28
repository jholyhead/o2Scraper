from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from o2scraper.o2 import Tariff, CallType
import logging

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
    
    @property
    def title(self):
        return self.driver.title

    def find_element(self, *loc):
        try:
            elem = self.driver.find_element(*loc)
            return elem
        except NoSuchElementException:
            logging.error("We couldn't find the element {}".format(loc))
            raise 
    
    def find_elements(self, *loc):
        return self.driver.find_elements(*loc)
    
    def open_page(self, url):
        self.driver.get(url)

class InternationalTariffsPage(BasePage):

    url = "http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk"
    expected_title = "O2 | International | International Caller Bolt On"

    country_text_input = (By.ID, "countryName")
    tariff_buttons = {Tariff.PAY_MONTHLY: (By.ID, "paymonthly"), 
                      Tariff.PAY_AND_GO: (By.ID, "payandgo")}
    tariff_tables = {
        Tariff.PAY_MONTHLY: (By.CSS_SELECTOR, "#paymonthlyTariffPlan #standardRatesTable"),
        Tariff.PAY_AND_GO: (By.CSS_SELECTOR, "#payandgoTariffPlan #standardRatesTable")}
    
    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def go_to(self):
        try:
            self.open_page(self.url)
            assert self.title == self.expected_title
        except AssertionError:
            print("ERROR: Page hasn't loaded correctly; title is different than expected")
            raise AssertionError

    def search_for_country(self, country):
        self.find_element(*self.country_text_input).send_keys(country + Keys.ENTER)

    def select_tariff_type(self, tariff_type=Tariff.PAY_MONTHLY):
        _loc = self.tariff_buttons[tariff_type] 
        self.find_element(*_loc).click()

    def get_rates_table(self, tariff_type=Tariff.PAY_MONTHLY, call_type=CallType.LANDLINE):
        """Get the tariff table, based on tariff parameter"""
        _loc = self.tariff_tables[tariff_type]
        #we introduce an explicit wait to ensure that the rate details 
        #have been inserted into the rates table
        try:
            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element(_loc, call_type.value))        
            rates_table = self.find_element(*_loc)
            return rates_table
        except TimeoutException:
            logging.error("Rates table did not load data in time")
            raise

    def get_rates(self, rates_table):
        rates_rows = rates_table.find_elements(*(By.TAG_NAME, "tr"))
        rates = []
        for row in rates_rows:
            cells = row.find_elements(*(By.TAG_NAME, "td"))
            rates.append((cells[0].text, cells[1].text))
        return rates

    def get_rate(self, tariff_type=Tariff.PAY_MONTHLY, call_type=CallType.LANDLINE):
        rates_table = self.get_rates_table(tariff_type, call_type)
        rates = self.get_rates(rates_table)
        rate = ""
        for r in rates:
            if r[0] == call_type.value:
                rate = r[1]
        return rate

    
