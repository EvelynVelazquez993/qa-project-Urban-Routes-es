import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from metodos import UrbanRoutesPage
from data import urban_routes_url, address_from, address_to, phone_number, card_number, card_cvv, card_expiry, \
    message_for_driver
import phone_code
from localizadores import UrbanRoutesLocators


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(
            service=Service(r'C:\Users\msurf\WebDriver\bin\chromedriver-win64\chromedriver-win64\chromedriver.exe'),
            options=options)

    def setup_method(self):
        self.driver.get(urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)

    def test_set_route(self):
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        self.routes_page.select_comfort_tariff()

    def test_fill_phone_number(self):
        self.routes_page.click_to_open_phone_modal()
        self.routes_page.set_phone_number(phone_number)

    def test_add_credit_card(self):
        self.routes_page.add_credit_card(card_number, card_expiry, card_cvv)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(UrbanRoutesLocators.agree_card)
        ).click()

        code = phone_code.retrieve_phone_code(self.driver)
        assert code is not None, "No se recuperó el código de confirmación para la tarjeta"

    def test_write_driver_message(self):
        self.routes_page.write_driver_message(message_for_driver)

    def test_add_blanket_and_tissues(self):
        self.routes_page.add_blanket_and_tissues()

    def test_add_ice_cream(self):
        self.routes_page.add_ice_cream()

    def test_taxi_modal_visible(self):
        assert self.routes_page.is_taxi_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()