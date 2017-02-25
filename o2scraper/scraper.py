from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from page import InternationalTariffsPage

def run(country):
    url = "http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk"

    driver = webdriver.PhantomJS()
    tariff_page = InternationalTariffsPage(driver)
    tariff_page.go_to()
    tariff_page.search_for_country(country)
    tariff_page.select_tariff_type()
    rate = tariff_page.get_rate()
    print("The cost of calling a landline in {} is {}".format(country, rate))


if __name__ == "__main__":
    run("Canada")