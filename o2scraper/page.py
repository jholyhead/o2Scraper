from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from o2 import Tariff, CallType
import time

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
    
    @property
    def title(self):
        return self.driver.title

    def find_element(self, *loc):
        return self.driver.find_element(*loc)
    
    def find_elements(self, *loc):
        return self.driver.find_elements(*loc)
    
    def open_page(self, url):
        self.driver.get(url)

class InternationalTariffsPage(BasePage):

    url = "http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk"

    country_text_input = (By.ID, "countryName")
    pay_monthly_button = (By.ID, "paymonthly")
    pay_and_go_button = (By.ID, "payandgo")
    pay_monthly_tariffs_table = (By.CSS_SELECTOR, "#paymonthlyTariffPlan #standardRatesTable")
    pay_and_go_tariffs_table = (By.CSS_SELECTOR, "#payandgoTariffPlan #standardRatesTable")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def go_to(self):
        self.open_page(self.url)

    def search_for_country(self, country):
        elem = self.find_element(*self.country_text_input).send_keys(country + Keys.ENTER)

    def select_tariff_type(self, tariff_type=Tariff.PAY_MONTHLY):
        if tariff_type is Tariff.PAY_MONTHLY:
            loc = self.pay_monthly_button
        elif tariff_type is Tariff.PAY_AND_GO:
            loc = self.pay_and_go_button 
        self.find_element(*loc).click()

    def get_rates_table(self, tariff_type=Tariff.PAY_MONTHLY, call_type=CallType.LANDLINE):
        """Get the tariff table, based on tariff parameter"""
        if tariff_type is Tariff.PAY_MONTHLY:
            loc = self.pay_monthly_tariffs_table
        elif tariff_type is Tariff.PAY_AND_GO:
            loc = self.pay_and_go_tariffs_table
        #we introduce an explicit wait to ensure that the rate details 
        #have been inserted into the rates table
        WebDriverWait(self.driver, 5).until(
            EC.text_to_be_present_in_element(loc, call_type.value))        
        rates_table = self.find_element(*loc)
        return rates_table

    def get_rate(self, tariff_type=Tariff.PAY_MONTHLY, call_type=CallType.LANDLINE):
        
        rates_table = self.get_rates_table(tariff_type, call_type)
        rates_rows = rates_table.find_elements(*(By.TAG_NAME, "tr"))
        rate = ""
        for row in rates_rows:
            cells = row.find_elements(*(By.TAG_NAME, "td"))
            if cells[0].text == call_type.value:
                rate = cells[1].text
        return rate

    

    


