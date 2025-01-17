from selenium.webdriver.common.by import By

class UrbanRoutesLocators:
    from_field = (By.CSS_SELECTOR, '#from') #Campos de dirección de origen
    to_field = (By.CSS_SELECTOR, '#to') #Campos de dirección de destino
    request_taxi_button = (By.CSS_SELECTOR, "button.button.round") #Botón de "Pedir taxi"
    comfort_tariff_button = (By.CSS_SELECTOR, '#root') #Seleccionar tarifa "Comfort"
    phone_modal_button = (By.NAME, "Número de teléfono") #Activar campo para "Número de Teléfono"
    phone_input = (By.CSS_SELECTOR, "label[for='phone']") #Introducir "Número de Teléfono"
    add_card_button = (By.CSS_SELECTOR, '#add-card') #Botón para agregar una tarjeta de crédito
    card_modal_cvv = (By.CSS_SELECTOR, '#cvv') #Agregar datos de tarjeta de crédito
    card_modal_submit = (By.CSS_SELECTOR, '#submit-card') #Aceptar tarjeta de credito
    driver_message_input = (By.CSS_SELECTOR, '#driver-message') #Mensaje al conductor
    blanket_and_tissues_button = (By.CSS_SELECTOR, "span.slider.round") #Pedir una manta y pañuelos
    ice_cream_button = (By.CSS_SELECTOR, "div.counter-plus") #Pedir helado
    modal_taxi = (By.CSS_SELECTOR, '#taxi-modal') #Modo taxi
