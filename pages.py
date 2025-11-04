# pages.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

DEFAULT_TIMEOUT = 25

# ---------------- utilidades de espera / interacción ----------------
def _wait(driver, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout)

def _wait_overlay_gone(driver, timeout=10):
    """
    Espera a que la overlay que bloquea clics desaparezca.
    Si no existe, invisibility_of_element_located devuelve True rápido.
    """
    overlay = (By.CSS_SELECTOR, ".overlay")
    try:
        _wait(driver, timeout).until(EC.invisibility_of_element_located(overlay))
    except TimeoutException:
        # Si no desaparece, lo dejamos pasar; el safe click hará fallback por JS.
        pass

def _scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", element)

def _js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)

def _safe_click(driver, locator, timeout=DEFAULT_TIMEOUT):
    """
    Click robusto: espera overlay, espera clickeable, hace scroll,
    intenta click normal; si se intercepta, reintenta y hace click por JS.
    """
    _wait_overlay_gone(driver)
    el = _wait(driver, timeout).until(EC.element_to_be_clickable(locator))
    _scroll_into_view(driver, el)
    try:
        el.click()
    except ElementClickInterceptedException:
        _wait_overlay_gone(driver, timeout=5)
        _scroll_into_view(driver, el)
        try:
            el.click()
        except ElementClickInterceptedException:
            _js_click(driver, el)
    return el

def _type(driver, locator, text, clear=False, timeout=DEFAULT_TIMEOUT):
    _wait_overlay_gone(driver)
    el = _wait(driver, timeout).until(EC.visibility_of_element_located(locator))
    _scroll_into_view(driver, el)
    if clear:
        el.clear()
    el.send_keys(text)
    return el

def _get_value(driver, locator, timeout=DEFAULT_TIMEOUT):
    el = _wait(driver, timeout).until(EC.presence_of_element_located(locator))
    return el.get_property("value")

def _get_text(driver, locator, timeout=DEFAULT_TIMEOUT):
    el = _wait(driver, timeout).until(EC.visibility_of_element_located(locator))
    return el.text

def _get_attr(driver, locator, attr, timeout=DEFAULT_TIMEOUT):
    el = _wait(driver, timeout).until(EC.presence_of_element_located(locator))
    return el.get_attribute(attr) or ""

def _wait_enabled(driver, locator, timeout=DEFAULT_TIMEOUT):
    """Espera a que el elemento exista y esté habilitado (sin disabled, sin clase 'disabled' ni pointer-events:none)."""
    def _enabled(drv):
        el = drv.find_element(*locator)
        disabled_attr = el.get_attribute("disabled")
        classes = (el.get_attribute("class") or "").lower()
        style = (el.get_attribute("style") or "").replace(" ", "").lower()
        return (disabled_attr is None) and ("disabled" not in classes) and ("pointer-events:none" not in style)
    _wait(driver, timeout).until(_enabled)
    return driver.find_element(*locator)

def _fire_change_and_blur(driver, element):
    """Dispara eventos de input/change y blur para activar validaciones de la UI."""
    driver.execute_script(
        "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));"
        "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));"
        "arguments[0].blur();",
        element
    )

# ---------------- Page Object ----------------
class UrbanRoutesPage:
    # --- Direcciones
    from_field = (By.ID, "from")
    to_field   = (By.ID, "to")

    # --- Botones/controles principales
    button_comfort_xpath = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    select_taxi_xpath    = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')

    # --- Teléfono
    phone_popup_btn   = (By.CLASS_NAME, "np-text")
    input_phone       = (By.ID, "phone")
    input_phone_xpath = (By.XPATH, '//*[@id="phone"]')
    next_btn          = (By.XPATH, '//*[text()="Siguiente"]')
    input_phone_code  = (By.ID, "code")
    confirm_phone_btn = (By.XPATH, '//*[text()="Confirmar"]')

    # --- Pago
    payment_btn       = (By.CLASS_NAME, "pp-button")
    add_card_btn      = (By.CLASS_NAME, "pp-plus")
    card_input_focus  = (By.CLASS_NAME, "card-number-input")
    card_input        = (By.XPATH, '//*[@id="number"]')
    cvv_input         = (By.XPATH, '//div[@class="card-code-input"]/input[@id="code"]')
    save_card_btn     = (By.XPATH, '//*[text()="Agregar"]')
    close_modal_btn   = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    # (opcional) fecha de expiración si tu UI la pide:
    # expiry_input   = (By.CSS_SELECTOR, 'input[name*="exp"], input[id*="exp"]')

    # --- Mensaje y extras
    comment_input          = (By.CSS_SELECTOR, "#comment")
    blanket_tissues_toggle = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    blanket_tissues_slider = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/input')
    icecream_plus          = (By.CLASS_NAME, "counter-plus")
    # corregido /div/3/ -> /div[3]/
    icecream_counter_value = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')

    # --- Pedido / modal
    smart_order_btn     = (By.CLASS_NAME, "smart-button-main")
    order_header_title  = (By.CLASS_NAME, "order-header-title")

    # --- Cookies (opcional)
    cookie_accept_any = (By.XPATH, '//*[contains(text(),"Aceptar") or contains(text(),"Accept") or contains(text(),"Allow")]')

    def __init__(self, driver):
        self.driver = driver

    # ----------- Helpers opcionales -----------
    def maybe_accept_cookies(self):
        try:
            _safe_click(self.driver, self.cookie_accept_any)
        except TimeoutException:
            pass

    # ----------- Direcciones -----------
    def set_route(self, from_address, to_address):
        _type(self.driver, self.from_field, from_address)
        _type(self.driver, self.to_field, to_address)

    def get_from_value(self):
        return _get_value(self.driver, self.from_field)

    def get_to_value(self):
        return _get_value(self.driver, self.to_field)

    # ----------- Taxi + Comfort -----------
    def select_taxi(self):
        _safe_click(self.driver, self.select_taxi_xpath)

    def select_comfort_rate(self):
        _safe_click(self.driver, self.button_comfort_xpath)

    def get_comfort_button_classes(self):
        return _get_attr(self.driver, self.button_comfort_xpath, "class")

    # ----------- Teléfono -----------
    def open_phone_popup(self):
        _safe_click(self.driver, self.phone_popup_btn)

    def type_phone_number(self, phone):
        _type(self.driver, self.input_phone_xpath, phone)

    def get_phone_value(self):
        return _get_value(self.driver, self.input_phone)

    def click_next_phone_step(self):
        _safe_click(self.driver, self.next_btn)

    def type_phone_code(self, code):
        _type(self.driver, self.input_phone_code, code)

    def confirm_phone_code(self):
        _safe_click(self.driver, self.confirm_phone_btn)

    # ----------- Pago -----------
    def open_payment_method(self):
        _safe_click(self.driver, self.payment_btn)

    def choose_add_card(self):
        _safe_click(self.driver, self.add_card_btn)

    def focus_card_number(self):
        _safe_click(self.driver, self.card_input_focus)

    def type_card_number(self, number):
        el = _type(self.driver, self.card_input, number)
        _fire_change_and_blur(self.driver, el)

    # (Opcional si tu UI lo pide)
    # def type_expiry(self, mm_yy: str):
    #     el = _type(self.driver, self.expiry_input, mm_yy)
    #     _fire_change_and_blur(self.driver, el)

    def type_cvv(self, cvv):
        el = _type(self.driver, self.cvv_input, cvv)
        _fire_change_and_blur(self.driver, el)

    def save_card(self):
        _wait_overlay_gone(self.driver)
        btn = _wait_enabled(self.driver, self.save_card_btn)
        _scroll_into_view(self.driver, btn)
        try:
            btn.click()
        except ElementClickInterceptedException:
            _wait_overlay_gone(self.driver, timeout=5)
            _scroll_into_view(self.driver, btn)
            _js_click(self.driver, btn)

    def close_payment_modal(self):
        _safe_click(self.driver, self.close_modal_btn)

    def get_card_number_value(self):
        return _get_value(self.driver, self.card_input)

    def get_cvv_value(self):
        return _get_value(self.driver, self.cvv_input)

    # ----------- Mensaje y extras -----------
    def type_driver_message(self, msg):
        _type(self.driver, self.comment_input, msg)

    def get_driver_message(self):
        return _get_value(self.driver, self.comment_input)

    def toggle_blanket_and_tissues(self):
        _safe_click(self.driver, self.blanket_tissues_toggle)

    def extras_slider_is_selected(self):
        return _wait(self.driver).until(EC.presence_of_element_located(self.blanket_tissues_slider)).is_selected()

    def add_two_icecreams(self):
        _safe_click(self.driver, self.icecream_plus)
        _safe_click(self.driver, self.icecream_plus)

    def get_icecream_counter(self):
        return _get_text(self.driver, self.icecream_counter_value)

    # ----------- Pedido / Modal -----------
    def click_smart_order(self):
        _safe_click(self.driver, self.smart_order_btn)

    def get_order_header_title(self):
        return _get_text(self.driver, self.order_header_title)

    def wait_order_header_any(self, timeout=DEFAULT_TIMEOUT):
        """
        Espera a que el encabezado sea:
        'Buscar automóvil' o 'El conductor llegará ...'
        """
        def ready(_):
            txt = self.get_order_header_title()
            return txt if (("Buscar automóvil" in txt) or ("El conductor llegará" in txt)) else False
        return WebDriverWait(self.driver, timeout).until(ready)