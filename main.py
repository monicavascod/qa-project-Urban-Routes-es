# main.py
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


# no modificar (salvo que ya uses Options abajo p/ logging)
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
            time.sleep(1)  # Instrucción inicial: No modificar"
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    button_round = (By.CLASS_NAME, "button round")
    set_phone_number = (By.CLASS_NAME, 'np-text')
    button_comfort_xpath = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    input_phone_number = (By.ID, 'phone')
    number = (By.XPATH, '//*[@id="phone"]')
    button_next_xpath = (By.XPATH, '//*[text()="Siguiente"]')
    input_code = (By.ID, 'code')
    button_confirm_xpath = (By.XPATH, '//*[text()="Confirmar"]')
    select_taxi_xpath = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    button_payment_method = (By.CLASS_NAME, "pp-button")
    button_add_card = (By.CLASS_NAME, "pp-plus")
    set_credit_card = (By.CLASS_NAME, 'card-number-input')
    input_credit_card_xpath = (By.XPATH, '//*[@id="number"]')
    input_card_cvv_xpath = (By.XPATH, '//div[@class="card-code-input"]/input[@id="code"]')
    submit_card_xpath = (By.XPATH, '//*[text()="Agregar"]')
    button_close_xpath = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    input_comment_css = (By.CSS_SELECTOR, "#comment")
    checkbox_bket_scrvs_xpath = (By.XPATH,
                                 '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    checkbox_slide_bket_scrvs_xpath = (By.XPATH,
                                       '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/input')
    counter_ice_cream = (By.CLASS_NAME, "counter-plus")
    counter_ice_cream_value_2 = (By.XPATH,
                                 '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')
    button_smart_order = (By.CLASS_NAME, "smart-button-main")
    order_header_title = (By.CLASS_NAME, 'order-header-title')
    modal_order = (By.CLASS_NAME, "order-details")

    def __init__(self, driver):
        self.driver = driver

    # -------- Direcciones
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    # -------- Taxi + Comfort
    def select_taxi(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.select_taxi_xpath).click()

    def select_comfort_rate(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.button_comfort_xpath).click()

    # -------- Teléfono
    def select_number_button(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.set_phone_number).click()

    def add_phone_number(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.number).send_keys(data.phone_number)

    def set_phone(self):
        self.driver.implicitly_wait(25)
        self.select_number_button()
        self.driver.implicitly_wait(25)
        self.add_phone_number()

    def click_on_next_button(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_next_xpath).click()

    def send_cell_info(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.button_confirm_xpath).click()

    def get_phone(self):
        return self.driver.find_element(*self.input_phone_number).get_property('value')

    def code_number(self):
        self.driver.implicitly_wait(15)
        phone_code = retrieve_phone_code(driver=self.driver)
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.input_code).send_keys(phone_code)

    # -------- Pago
    def payment_method(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.button_payment_method).click()

    def add_card_option(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.button_add_card).click()

    def card_register(self):
        self.driver.implicitly_wait(25)
        self.payment_method()
        self.driver.implicitly_wait(25)
        self.add_card_option()

    def select_number(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.set_credit_card).click()

    def input_number(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.input_credit_card_xpath).send_keys(data.card_number)

    def card_input(self):
        self.driver.implicitly_wait(15)
        self.select_number()
        self.driver.implicitly_wait(15)
        self.input_number()

    def get_card_input(self):
        return self.driver.find_element(*self.input_credit_card_xpath).get_property('value')

    def code_card_input(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.input_card_cvv_xpath).send_keys(data.card_code)

    def cvv_code(self):
        self.driver.implicitly_wait(15)
        self.code_card_input()

    def get_cvv_card(self):
        return self.driver.find_element(*self.input_card_cvv_xpath).get_property('value')

    def registered_card(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.submit_card_xpath).click()

    def add_card(self):
        self.driver.implicitly_wait(25)
        self.card_input()
        self.driver.implicitly_wait(25)
        self.cvv_code()
        self.driver.implicitly_wait(25)
        self.registered_card()

    def close_modal(self):
        self.driver.implicitly_wait(25)
        self.driver.find_element(*self.button_close_xpath).click()

    # -------- Mensaje y extras
    def set_message(self, message):
        self.driver.implicitly_wait(15)
        message_field = self.driver.find_element(*self.input_comment_css)
        message_field.send_keys(message)

    def get_message(self):
        return self.driver.find_element(*self.input_comment_css).get_property('value')

    def select_blanket_and_tissues(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.checkbox_bket_scrvs_xpath).click()

    def get_slider_status(self):
        return self.driver.find_element(*self.checkbox_slide_bket_scrvs_xpath).is_selected()

    def get_icecream_counter(self):
        return self.driver.find_element(*self.counter_ice_cream_value_2).text

    def select_ice_cream(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.counter_ice_cream).click()
        self.driver.find_element(*self.counter_ice_cream).click()

    # -------- Pedido
    def select_order(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_smart_order).click()

    def get_order_header_title(self):
        return self.driver.find_element(*self.order_header_title).text

    def get_driver_modal_info(self):
        return self.driver.find_element(*self.order_header_title).text

    # -------- Esperas robustas para el encabezado del modal
    def wait_order_header_any(self, timeout=25):
        """
        Espera hasta que el encabezado sea alguno de los dos estados válidos:
        'Buscar automóvil' o 'El conductor llegará ...'
        Devuelve el texto actual del encabezado.
        """

        def ready(_):
            txt = self.get_order_header_title()
            return txt if (("Buscar automóvil" in txt) or ("El conductor llegará" in txt)) else False

        return WebDriverWait(self.driver, timeout).until(ready)


########################################################################
#######################    TEST   ######################################
########################################################################

class TestUrbanRoutes:
    driver = None
    home = None

    @classmethod
    def setup_class(cls):
        # Activar performance logs con Options (evita desired_capabilities=)
        opts = Options()
        opts.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=opts)
        cls.home = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # 1.Configurar las direcciones
        address_from = data.address_from
        address_to = data.address_to
        self.driver.implicitly_wait(10)
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # 2.Seleccionar taxi y tarifa
    def test_select_rate(self):
        self.home.select_taxi()
        self.home.select_comfort_rate()

        # Checar que la tarifa de confort se haya seleccionado
        comfort_rate_button = self.driver.find_element(*self.home.button_comfort_xpath)
        assert 'tcard active' in comfort_rate_button.get_attribute('class'), "La tarifa comfort no fue seleccionada"

    # 3.Rellenar el número de teléfono y obtener código
    def test_get_tel_code(self):
        self.home.set_phone()
        self.home.click_on_next_button()
        self.home.code_number()
        self.home.send_cell_info()

        # Checar que el teléfono ingresado es el esperado
        phone_number = self.home.get_phone()
        assert phone_number == data.phone_number, f"Número esperado {data.phone_number}, pero se tiene {phone_number}"

    # 4.Agregar una tarjeta de crédito
    def test_add_creditcard(self):
        self.home.card_register()
        self.home.add_card()
        self.home.close_modal()

        # Verificar que el número de tarjeta ingresado es el esperado
        card_number = self.home.get_card_input()
        assert card_number == data.card_number, f"credit card esperada {data.card_number}, pero se tiene {card_number}"

        # Verificar que el código CVV ingresado es el esperado
        cvv_code = self.home.get_cvv_card()
        assert cvv_code == data.card_code, f"CVV code esperado {data.card_code}, pero se tiene {cvv_code}"

    # 5.Escribir un mensaje para el conductor
    def test_send_message(self):
        message = data.message_for_driver
        self.home.set_message(message)

        entered_message = self.home.get_message()
        assert entered_message == message, f"Mensaje esperado {message}, pero se tiene {entered_message}"

    # 6.Pedir una manta y pañuelos
    def test_add_blanket_and_tissues(self):
        self.home.select_blanket_and_tissues()
        assert self.home.get_slider_status() is True

    # 7.Pedir 2 helados
    def test_add_two_icecream(self):
        self.home.select_ice_cream()
        assert self.home.get_icecream_counter() == '2'

    # 8. Aparece el modal (acepta ambos estados)
    def test_order_modal(self):
        self.home.select_order()
        title = self.home.wait_order_header_any(timeout=25)
        assert any(
            x in title for x in ("Buscar automóvil", "El conductor llegará")), f"Título inesperado del modal: {title}"

    # 9. Esperar a que aparezca la información del conductor
    def test_driver_modal(self):
        # Espera explícitamente el estado con conductor
        title = WebDriverWait(self.driver, 60).until(
            lambda d: (t := self.home.get_order_header_title()) and ("El conductor llegará" in t) and t
        )
        assert "El conductor llegará" in title, f"Se esperaba 'El conductor llegará', pero se tiene: {title}"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
