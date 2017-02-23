from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def run(country):
    url = "http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk"

    driver = webdriver.PhantomJS()
    driver.get(url)

    assert driver.title == "O2 | International | International Caller Bolt On"

    elem = driver.find_element_by_id("countryName")
    elem.clear()
    elem.send_keys(country)
    elem.send_keys(Keys.ENTER)

    button = driver.find_element_by_id("paymonthly").click()

    assert "Available rates when calling or texting {}".format(country) in driver.page_source

    rates_table = driver.find_element_by_id("standardRatesTable")
    rates_rows = rates_table.find_elements_by_tag_name("tr")
    rate = ""
    for row in rates_rows:
        cells = row.find_elements_by_tag_name("td")
        if cells[0].text == "Landline":
            rate = cells[1].text

    driver.quit()
    return "The cost of calling a landline in {} is {}".format(country, rate)

if __name__ == "__main__":
    run("Canada")