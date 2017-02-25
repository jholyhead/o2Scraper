from selenium import webdriver
import argparse
from page import InternationalTariffsPage
from itertools import product
from o2 import Tariff, CallType

def run(driver, country, tariff, method):
    #try:
        
        tariff_page = InternationalTariffsPage(driver)
        tariff_page.go_to()
        tariff_page.search_for_country(country)
        tariff_page.select_tariff_type(tariff)
        rate = tariff_page.get_rate(tariff, method)
        
        return "The cost of contacting {} via {} on a {} plan is {}".format(country, method.name.lower(), 
                                                                            tariff.name.lower(), rate)
    #except:
     #   driver.save_screenshot("screen.png")
      #  driver.quit()


def get_args():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument("-c", "--countries", dest="countries", nargs="+",
                        default=["Canada", "Germany", "Iceland", "Pakistan", "Singapore", "South Africa"],
                        help="List of Countries to query")
    parser.add_argument("-t", "--tariffTypes", dest="tariffs", choices=["pay_monthly", "pay_and_go"],
                        nargs="+", default=["pay_and_go"],
                        help="The tariff types, one or more of 'pay_monthly' or 'pay_and go').\
                        Defaults to 'pay_monthly'")
    parser.add_argument("-m", "--method", dest="methods", choices=["landline", "mobile", "text"],
                        nargs="+", default=["landline"], 
                        help="The communication method desired. One or more of 'landline', 'mobile', \
                        or 'text'")    
    args = parser.parse_args()
    countries = args.countries
    tariffs = [Tariff.from_string(v) for v in args.tariffs]
    methods = [CallType.from_string(v) for v in args.methods]
    return (countries, tariffs, methods)


if __name__ == "__main__":
    try:
        countries, tariffs, methods = get_args()
        driver = webdriver.PhantomJS()
        driver.implicitly_wait(2)
        for country, tariff, method in product(countries, tariffs, methods):
            print(run(country, tariff, method))
    except:
        print("An unexpected error occurred. Exiting")
    finally:
        driver.quit()
