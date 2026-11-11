from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test='continue']")
    FINISH_BUTTON = (By.CSS_SELECTOR, "[data-test='finish']")
    SUMMARY_ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self.log.info("Completando formulario del cliente")
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_summary_item_names(self) -> list[str]:
        return [el.text for el in self.find_all(self.SUMMARY_ITEM_NAMES)]

    def finish_order(self):
        self.click(self.FINISH_BUTTON)

    def get_confirmation_message(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)
