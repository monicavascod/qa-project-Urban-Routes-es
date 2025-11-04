
import json
import time
from selenium.common import WebDriverException


def retrieve_phone_code(driver, attempts=10, pause_sec=1) -> str:
    """
    Devuelve el código de confirmación del teléfono como string.
    Llamar solo después de solicitarlo en la app (la API ya debe haberse disparado).
    Lee el cuerpo de la respuesta desde los performance logs de Chrome.
    """
    code = None
    for _ in range(attempts):
        try:
            logs = [
                log["message"]
                for log in driver.get_log("performance")
                if log.get("message") and "api/v1/number?number" in log.get("message")
            ]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {"requestId": message_data["params"]["requestId"]},
                )
                digits = [x for x in body.get("body", "") if x.isdigit()]
                if digits:
                    code = "".join(digits)
                    break
        except WebDriverException:
            time.sleep(pause_sec)
            continue

        if code:
            return code

        time.sleep(pause_sec)

    raise Exception(
        "No se encontró el código de confirmación del teléfono.\n"
        "Usa 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación."
    )