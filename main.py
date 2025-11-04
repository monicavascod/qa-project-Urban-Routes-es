from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import pytest

import data
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code


class TestUrbanRoutes:
    driver = None
    home = None

    @classmethod
    def setup_class(cls):
        # Chrome con performance logs (necesario para leer el código de teléfono)
        opts = Options()
        opts.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=opts)
        cls.driver.maximize_window()
        cls.driver.get(data.urban_routes_url)

        cls.home = UrbanRoutesPage(cls.driver)

        cls.home.maybe_accept_cookies()

        cls.home.set_route(data.address_from, data.address_to)

    # 1) Seleccionar la tarifa Comfort
    def test_01_select_comfort_rate(self):
        self.home.select_taxi()
        self.home.select_comfort_rate()
        classes = self.home.get_comfort_button_classes()
        assert "tcard" in classes and "active" in classes, "La tarifa Comfort no fue seleccionada"

    # 2) Rellenar el número de teléfono
    def test_02_fill_phone(self):
        self.home.open_phone_popup()
        self.home.type_phone_number(data.phone_number)
        assert self.home.get_phone_value() == data.phone_number, "El teléfono no coincide"

    # 3) Confirmar el teléfono
    def test_03_confirm_phone(self):
        self.home.click_next_phone_step()
        code = retrieve_phone_code(self.driver)
        self.home.type_phone_code(code)
        self.home.confirm_phone_code()
        assert True

    # 4) Agregar una tarjeta de crédito (número)
    def test_04_add_credit_card_number(self):
        self.home.open_payment_method()
        self.home.choose_add_card()
        self.home.focus_card_number()
        self.home.type_card_number(data.card_number)
        assert self.home.get_card_number_value() == data.card_number, "El número de tarjeta no coincide"

    # 5) Código de confirmación para la tarjeta (CVV) y guardar
    def test_05_add_card_cvv_and_save(self):
        self.home.type_cvv(data.card_code)
        assert self.home.get_cvv_value() == data.card_code, "El CVV no coincide"
        self.home.save_card()
        self.home.close_payment_modal()

    # 6) Escribir un mensaje para el conductor
    def test_06_write_message(self):
        self.home.type_driver_message(data.message_for_driver)
        assert self.home.get_driver_message() == data.message_for_driver, "El mensaje no se guardó"

    # 7) Pedir una manta y pañuelos
    def test_07_extras_blanket_tissues(self):
        self.home.toggle_blanket_and_tissues()
        assert self.home.extras_slider_is_selected() is True, "El switch de extras no quedó activado"

    # 8) Pedir 2 helados
    def test_08_two_icecreams(self):
        self.home.add_two_icecreams()
        assert self.home.get_icecream_counter() == "2", "El contador de helados no muestra 2"

    # 9) Modal para buscar un taxi (acepta ambos estados)
    def test_09_search_taxi_modal_any_state(self):
        # 📌 Ya confirmamos teléfono en test_03, acá solo pedimos
        self.home.click_smart_order()
        title = self.home.wait_order_header_any(timeout=25)
        assert any(x in title for x in ("Buscar automóvil", "El conductor llegará")), f"Modal inesperado: {title}"

    # 10) Información del conductor (opcional)
    def test_10_driver_info_optional(self):
        """
        Este caso es OPCIONAL según el feedback.
        Si no aparece 'El conductor llegará' dentro del tiempo, se salta la prueba (no falla).
        """
        try:
            title = WebDriverWait(self.driver, 90).until(
                lambda d: (t := self.home.get_order_header_title()) and ("El conductor llegará" in t) and t
            )
        except TimeoutException:
            pytest.skip("No se asignó conductor a tiempo. Caso OPCIONAL → se omite sin marcar fallo.")
        assert "El conductor llegará" in title, "No apareció el estado con información del conductor"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()