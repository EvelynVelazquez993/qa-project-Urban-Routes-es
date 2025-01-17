from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from localizadores import UrbanRoutesLocators

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(UrbanRoutesLocators.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(UrbanRoutesLocators.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*UrbanRoutesLocators.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*UrbanRoutesLocators.to_field).get_property('value')

    def click_on_request_taxi(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(UrbanRoutesLocators.request_taxi_button)
        ).click()

    def select_comfort_tariff(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(UrbanRoutesLocators.comfort_tariff_button)
        ).click()

    def click_to_open_phone_modal(self):
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(UrbanRoutesLocators.phone_modal_button)
        ).click()

    def set_phone_number(self, phone_number):
        self.driver.find_element(*UrbanRoutesLocators.phone_input).send_keys(phone_number)

    def add_credit_card(self, card_number, card_expiry, cvv):
        self.driver.find_element(*UrbanRoutesLocators.add_card_button).click()
        modal = self.driver.find_element(*UrbanRoutesLocators.card_modal_cvv)
        modal.send_keys(cvv)
        modal.send_keys(Keys.TAB)
        submit_button = self.driver.find_element(*UrbanRoutesLocators.card_modal_submit)
        assert submit_button.is_enabled(), "El botón de enviar tarjeta no se activó después de ingresar el CVV"
        submit_button.click()

    def write_driver_message(self, message):
        self.driver.find_element(*UrbanRoutesLocators.driver_message_input).send_keys(message)

    def add_blanket_and_tissues(self, blanket_and_tissues_button):
        slider = self.driver.find_element(blanket_and_tissues_button)
        slider.click()

        # Verificar que el checkbox está activado
        checkbox = self.driver.find_element(blanket_and_tissues_button)
        assert checkbox.is_selected(), "El slider no activó correctamente el checkbox."

    def add_ice_cream(self, ice_cream_button):
        self.driver.find_element(ice_cream_button).click(2)

    def is_taxi_modal_visible(self):
        return self.driver.find_element(*UrbanRoutesLocators.modal_taxi).is_displayed()
