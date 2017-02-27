import sys
import argparse
from o2scraper.page import InternationalTariffsPage
from itertools import product
import logging
from o2scraper.o2 import Tariff, CallType
from driver import driver

def get_driver():
    driver.implicitly_wait(2)
    return driver

def get_tariff_page():
    return InternationalTariffsPage(get_driver())

def run(country, tariff=Tariff.PAY_MONTHLY, method=CallType.LANDLINE, 
        tariff_page=get_tariff_page()):

    tariff_page.go_to()
    tariff_page.search_for_country(country)
    tariff_page.select_tariff_type(tariff)
    rate = tariff_page.get_rate(tariff, method)
    if not rate:
        return "Rate could not be found for {} in {} on {} contract".format(country, 
                                            method.name.lower(), tariff.name.lower())
    return "The cost of contacting {} via {} on a {} plan is {}".format(country, 
                                        method.name.lower(), tariff.name.lower(), rate)

def get_args():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument("-c", "--countries", dest="countries", nargs="+",
                        default=["Canada", "Germany", "Iceland", "Pakistan", "Singapore", "South Africa"],
                        help="List of Countries to query")
    parser.add_argument("-t", "--tariffTypes", dest="tariffs", choices=["pay_monthly", "pay_and_go"],
                        nargs="+", default=["pay_monthly"],
                        help="The tariff types, one or more of 'pay_monthly' or 'pay_and go').\
                        Defaults to 'pay_monthly'")
    parser.add_argument("-m", "--method", dest="methods", choices=["landline", "mobile", "text"],
                        nargs="+", default=["landline"], 
                        help="The communication method desired. One or more of 'landline',\
                         'mobile', or 'text'")    
    args = parser.parse_args()
    countries = args.countries
    tariffs = [Tariff.from_string(v) for v in args.tariffs]
    methods = [CallType.from_string(v) for v in args.methods]
    return (countries, tariffs, methods)

def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='scraper.log',
                        filemode='a')



if __name__ == "__main__":
    try:
        setup_logging()
        countries, tariffs, methods = get_args()
        logging.info("Starting with args: Countries: {}, Tariffs: {}, Methods: {}"
                    .format(countries, [t.name.lower() for t  in tariffs], 
                            [m.name.lower() for m in methods]))                
        for country, tariff, method in product(countries, tariffs, methods):
            print(run(country, tariff, method))
        logging.info("Completed without errors")
    except:
        print("An error occurred. Check log for details. Exiting")
    finally:
        driver.close()      
