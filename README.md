# 🚕 Automatización de Pruebas: Solicitud de Taxi en Urban Routes

## 📝 Descripción del Proyecto

Este proyecto implementa un conjunto de pruebas de automatización web con **Python** y la librería **Selenium WebDriver** para verificar paso a paso el flujo completo de solicitud de un servicio de taxi en la aplicación web de Urban Routes.

El proyecto utiliza **pruebas atómicas** (una prueba por acción clave) estructuradas bajo el patrón **Page Object Model (POM)**. Esto garantiza que cada interacción del usuario, desde la configuración de la ruta y el pago hasta la asignación del conductor, sea validada de forma independiente y eficiente.

---

## 🛠️ Tecnologías y Técnicas Utilizadas

* **Python**: Lenguaje de programación principal.
* **Selenium WebDriver**: Herramienta de automatización.
* **Pytest**: Framework utilizado para la ejecución y estructuración de los tests.
* **Page Object Model (POM)**: Patrón de diseño para modularizar el código.
* **Manejo de IFrames**: Implementado para interactuar con los campos de la tarjeta de crédito y CVV.
* **Sincronización**: Uso combinado de **Esperas Implícitas** (`implicitly_wait`) y **Esperas Explícitas** (`WebDriverWait`).
* **Manejo de `Options`**: Configuración del *logging* del navegador para la recuperación del código de teléfono, cumpliendo con los estándares de Selenium 4.
* **Localizadores Variados**: Uso de **`By.ID`**, **`By.XPATH`**, **`By.CSS_SELECTOR`**, y **`By.CLASS_NAME`**.

---

## 🧪 Escenarios de Prueba Cubiertos

El archivo `main.py` contiene la clase `TestUrbanRoutes` con los siguientes métodos de prueba secuenciales que validan cada etapa del pedido:

1.  `test_set_route`: Configuración y verificación de las direcciones.
2.  `test_select_rate`: Selección de la tarifa **Comfort**.
3.  `test_get_tel_code`: Ingreso y **confirmación del código de verificación** del teléfono.
4.  `test_add_creditcard`: **Agrega la tarjeta de crédito** (manejando iframes).
5.  `test_send_message`: Escribe el mensaje para el conductor.
6.  `test_add_blanket_and_tissues`: Habilita el requisito de **manta y pañuelos**.
7.  `test_add_two_icecream`: **Agrega 2 helados** al pedido.
8.  `test_order_modal`: Inicia el pedido y verifica que el modal de búsqueda se muestre.
9.  `test_driver_modal`: **Espera y verifica la asignación final del conductor**.

---

## 🚀 Cómo Ejecutar las Pruebas

1. Crear un entorno virtual
python -m venv .venv

2. Activar el entorno virtual

macOS / Linux:
source .venv/bin/activate

Windows (PowerShell):
.venv\Scripts\Activate.ps1

3. Instalar dependencias:
pip install -r requirements.txt

4. Ejecutar las pruebas:
pytest main.py
       
---
---
## **👩‍💻 Autora**: Mónica  Vasco 
 QA  Automation  Engineer  
📫 _monikvasco.d@gmail.com_
