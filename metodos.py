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
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(UrbanRoutesLocators.phone_input)
        ).send_keys(phone_number)

    def add_credit_card(self, card_number, card_expiry, cvv):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(UrbanRoutesLocators.add_card_button)
        ).click()
        modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(UrbanRoutesLocators.credit_click)
        )
        modal.send_keys(card_number)
        modal.send_keys(Keys.TAB)
        self.driver.find_element(*UrbanRoutesLocators.card_cvv).send_keys(cvv)
        self.driver.find_element(*UrbanRoutesLocators.agree_card).click()

    def write_driver_message(self, message):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(UrbanRoutesLocators.driver_message_input)
        ).send_keys(message)

    def add_blanket_and_tissues(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(UrbanRoutesLocators.blanket_and_tissues_button)
        ).click()

    def add_ice_cream(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(UrbanRoutesLocators.ice_cream_button)
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(UrbanRoutesLocators.ice_cream_button)
        ).click()

    def is_taxi_modal_visible(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(UrbanRoutesLocators.modal_taxi)
        ).is_displayed()
