from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE) and "cart" in self.current_url

    def get_item_names(self) -> list[str]:
        return [el.text for el in self.find_all(self.ITEM_NAMES)]

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
