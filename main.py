import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from metodos import UrbanRoutesPage
from data import urban_routes_url, address_from, address_to, phone_number, card_number, card_cvv, card_expiry, message_for_driver
import phone_code

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(r'C:\Users\msurf\WebDriver\bin\chromedriver-win64\chromedriver-win64\chromedriver.exe'), options=options)

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
        code = phone_code.retrieve_phone_code(self.driver)
        assert code is not None, "No se recuperó el código de confirmación para la tarjeta"

    def test_write_driver_message(self):
        self.routes_page.write_driver_message(message_for_driver)

    def test_add_blanket_and_tissues(self, blanket_and_tissues_button=None):
        self.page.add_blanket_and_tissues(blanket_and_tissues_button)

    def test_add_ice_cream(self, ice_cream_button=None):
       self.page.add_ice_cream(ice_cream_button)

    def test_taxi_modal_visible(self):
        assert self.routes_page.is_taxi_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
