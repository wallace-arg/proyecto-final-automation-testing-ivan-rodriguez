from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    ITEM_CARDS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE) and "inventory" in self.current_url

    def get_title(self) -> str:
        return self.get_text(self.TITLE)

    def sort_by(self, option_value: str):
        """option_value: az, za, lohi, hilo."""
        self.log.info("Ordenando productos por '%s'", option_value)
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(option_value)

    def get_product_names(self) -> list[str]:
        return [el.text for el in self.find_all(self.ITEM_NAMES)]

    def get_product_prices(self) -> list[float]:
        return [float(el.text.replace("$", "")) for el in self.find_all(self.ITEM_PRICES)]

    def add_product_to_cart(self, product_name: str):
        """Agrega un producto buscándolo por su nombre dentro de su tarjeta."""
        self.log.info("Agregando al carrito: %s", product_name)
        for card in self.find_all(self.ITEM_CARDS):
            name = card.find_element(*self.ITEM_NAMES).text
            if name == product_name:
                card.find_element(By.CSS_SELECTOR, "button").click()
                return
        raise AssertionError(f"Producto no encontrado: {product_name}")

    def get_cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.get_text(self.CART_BADGE))

    def go_to_cart(self):
        self.click(self.CART_LINK)
