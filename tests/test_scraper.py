from unittest.mock import patch, Mock
import pytest
from pytest_mock import mocker 
from enum import Enum
from o2scraper.scraper import run
from o2scraper.page import InternationalTariffsPage, BasePage

@pytest.fixture(scope='session')
def driver():
    return Mock()

@pytest.fixture
def tariffs_page(driver):
    return Mock()

@pytest.fixture
def landline():
    class CallTypes(Enum):
        LANDLINE = "Landline"
    return CallTypes.LANDLINE

@pytest.fixture
def pay_monthly():
    class TariffType(Enum):
        PAY_MONTHLY = 1
    return TariffType.PAY_MONTHLY

def test_scraper_run(mocker, tariffs_page, landline, pay_monthly):
    mocker.patch("o2scraper.page.InternationalTariffsPage")
    run("Canada", tariff=pay_monthly, method=landline, tariff_page=tariffs_page)
    tariffs_page.go_to().assert_called_once()
    tariffs_page.search_for_country.assert_called_once_with("Canada")
    tariffs_page.select_tariff_type.assert_called_once_with(pay_monthly)
    tariffs_page.get_rate.assert_called_once_with(pay_monthly, landline)


