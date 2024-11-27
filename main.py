import pytest

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_tariff = (By.ID, 'comfort-tariff')
    phone_input = (By.ID, 'phone')
    add_card_button = (By.ID, 'add-card')
    card_modal_cvv = (By.ID, 'code')
    card_modal_submit = (By.ID, 'submit-card')
    driver_message_input = (By.ID, 'driver-message')
    blanket_button = (By.ID, 'add-blanket')
    tissues_button = (By.ID, 'add-tissues')
    ice_cream_button = (By.ID, 'add-icecream')
    modal_taxi = (By.ID, 'taxi-modal')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def set_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_input).send_keys(phone_number)

    def add_credit_card(self, card_number, card_expiry, cvv):
        self.driver.find_element(*self.add_card_button).click()
        modal = self.driver.find_element(*self.card_modal_cvv)
        modal.send_keys(cvv)
        modal.send_keys(Keys.TAB)  # Simula cambio de foco
        self.driver.find_element(*self.card_modal_submit).click()

    def write_driver_message(self, message):
        self.driver.find_element(*self.driver_message_input).send_keys(message)

    def add_item(self, item_button, quantity=1):
        for _ in range(quantity):
            self.driver.find_element(*item_button).click()

    def is_taxi_modal_visible(self):
        return self.driver.find_element(*self.modal_taxi).is_displayed()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options

        # Configuración de opciones
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        # Inicialización del driver
        cls.driver = webdriver.Chrome(service=Service("C:\\Users\\msurf\\WebDriver\\bin\\chrome-win64\\chrome.exe"), options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_full_taxi_process(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Configurar la dirección
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        # Seleccionar tarifa Comfort
        routes_page.select_comfort_tariff()

        # Rellenar número de teléfono
        phone_number = data.phone_number
        routes_page.set_phone_number(phone_number)

        # Agregar tarjeta de crédito
        card_number = data.card_number
        expiry = data.card_expiry
        cvv = data.card_cvv
        routes_page.add_credit_card(card_number, expiry, cvv)

        # Recuperar código de confirmación y verificar tarjeta
        code = retrieve_phone_code(self.driver)
        assert code is not None

        # Escribir mensaje al controlador
        driver_message = "Muéstrame el camino al museo"
        routes_page.write_driver_message(driver_message)

        # Pedir artículos
        routes_page.add_item(routes_page.blanket_button)
        routes_page.add_item(routes_page.tissues_button)
        routes_page.add_item(routes_page.ice_cream_button, quantity=2)

        # Confirmar que el modal de taxi aparece
        assert routes_page.is_taxi_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
