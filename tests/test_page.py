from unittest.mock import patch, Mock
from o2scraper.page import InternationalTariffsPage, BasePage
import pytest 
from enum import Enum
from pytest_mock import mocker 

@pytest.fixture(scope='session')
def driver():
    return Mock()

@pytest.fixture
def tariffs_page(driver):
    return InternationalTariffsPage(driver)

@pytest.fixture
def call_types():
    class CallTypes(Enum):
        LANDLINE = "Landline"
        MOBILE = "Mobiles"
    return CallTypes

def test_select_tariff_type(mocker, tariffs_page):
    mocker.patch.dict('o2scraper.page.InternationalTariffsPage.tariff_buttons',
                      {("abc",): ["xyz"], ("123",): ["456"]})
    mocker.patch('o2scraper.page.BasePage.find_element')
    tariffs_page.select_tariff_type(tariff_type=("abc",))
    tariffs_page.find_element.assert_called_with("xyz")


def test_go_to(mocker, tariffs_page):
    mocker.patch("o2scraper.page.BasePage.open_page")
    mocker.patch("o2scraper.page.BasePage.title", return_value="the wrong title")
    with pytest.raises(AssertionError):
        tariffs_page.go_to()
    tariffs_page.open_page.assert_called_with(tariffs_page.url)
        
def test_get_rate(mocker, tariffs_page, call_types):
    mock_call_type = Enum
    mock_rows = [("Landline", "£0.99"), ("Mobile", "£0.25")]
    mocker.patch("o2scraper.page.InternationalTariffsPage.get_rates_table")
    mocker.patch("o2scraper.page.InternationalTariffsPage.get_rates", return_value=mock_rows)

    assert tariffs_page.get_rate(call_type=call_types.LANDLINE) == "£0.99"
    