from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from o2 import Tariff, CallType

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
    
    @property
    def title(self):
        return self.driver.title

    def find_element(*loc):
        return self.driver.find_element(*loc)
    
    def open_page(self, url):
        self.driver.get(url)

class InternationalTariffsPage(BasePage):

    url = "http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk"

    country_text_input = (By.ID, "countryName")
    pay_monthly_button = (By.ID, "paymonthly")
    pay_and_go_button = (By.ID, "payandgo")
    tariffs_table = (By.ID, "standardRatesTable")

    def go_to(self):
        self.open_page(self.url)

    def search_for_country(self, country):
        elem = self.find_element(*self.country_text_input).send_keys(country)
        elem.send_keys(Keys.ENTER)

    def select_tariff_type(self, tariff_type=Tariff.PAY_MONTHLY):
        if tariff_type is Tariff.PAY_MONTHLY:
            loc = self.pay_monthly_button
        elif tariff_type is Tariff.PAY_AND_GO:
            loc = self.pay_and_go_button 
        self.find_element(*loc).click()

    

    

    


