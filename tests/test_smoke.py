from o2scraper.scraper import run
import pytest 
from selenium import webdriver



@pytest.mark.skip()
def test_result():
    assert run("Canada") == "The cost of contacting Canada via landline on a pay_monthly plan is £1.50"
    