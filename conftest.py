"""Fixtures globales de pytest y hook de capturas de pantalla en fallos."""
import base64
from datetime import datetime
from pathlib import Path

import pytest
from pytest_html import extras as pytest_html_extras
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.api_client import ApiClient
from utils.data_loader import get_test_data
from utils.logger import get_logger

log = get_logger("conftest")

SCREENSHOT_DIR = Path(__file__).resolve().parent / "reports" / "screenshots"


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Navegador: chrome o firefox")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Ejecutar el navegador sin interfaz gráfica")


@pytest.fixture(scope="session")
def test_data() -> dict:
    return get_test_data()


@pytest.fixture
def driver(request, test_data):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    log.info("Iniciando navegador: %s (headless=%s)", browser, headless)

    if browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        drv = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )
    else:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        # Evita el aviso de "contraseña filtrada" de Chrome que tapa la página
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        })
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        drv = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )

    drv.maximize_window()
    drv.implicitly_wait(0)  # solo esperas explícitas
    drv.get(test_data["base_url"])
    request.node.driver = drv
    yield drv
    log.info("Cerrando navegador")
    drv.quit()


@pytest.fixture(scope="session")
def api_client(test_data) -> ApiClient:
    return ApiClient(test_data["api"]["base_url"])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test de UI falla, guarda captura con timestamp y la adjunta al HTML."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    drv = getattr(item, "driver", None)
    if drv is None:
        return

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in item.name)
    file_path = SCREENSHOT_DIR / f"{safe_name}_{timestamp}.png"

    try:
        drv.save_screenshot(str(file_path))
        log.error("Test fallido: %s | captura: %s", item.name, file_path)
        b64 = base64.b64encode(file_path.read_bytes()).decode()
        extra = getattr(report, "extras", [])
        extra.append(pytest_html_extras.png(b64, "Screenshot del fallo"))
        report.extras = extra
    except Exception as exc:  # no romper el reporte por un fallo de captura
        log.error("No se pudo capturar la pantalla: %s", exc)
