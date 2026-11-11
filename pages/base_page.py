"""Clase base de todas las páginas: esperas explícitas y acciones genéricas."""
from datetime import datetime
from pathlib import Path

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import get_logger

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "reports" / "screenshots"


class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.log = get_logger(self.__class__.__name__)

    def find(self, locator):
        """Espera a que el elemento sea visible y lo devuelve."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Espera a que haya al menos un elemento presente y devuelve la lista."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.log.info("Clic en %s", locator)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text: str):
        self.log.info("Escribiendo en %s", locator)
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def is_visible(self, locator) -> bool:
        try:
            self.find(locator)
            return True
        except Exception:
            return False

    def wait_for_url_contains(self, fragment: str):
        self.wait.until(EC.url_contains(fragment))

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    def take_screenshot(self, name: str = "screenshot") -> str:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = SCREENSHOT_DIR / f"{name}_{timestamp}.png"
        self.driver.save_screenshot(str(path))
        self.log.info("Captura guardada en %s", path)
        return str(path)
