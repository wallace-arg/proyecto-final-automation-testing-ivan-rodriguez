"""Pruebas de UI sobre https://www.saucedemo.com usando Selenium + POM."""
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.fixture
def logged_inventory(driver, test_data) -> InventoryPage:
    """Deja al usuario autenticado en la página de inventario."""
    user = test_data["valid_user"]
    LoginPage(driver).login(user["username"], user["password"])
    inventory = InventoryPage(driver)
    assert inventory.is_loaded(), "No se cargó el inventario tras el login"
    return inventory


def test_tc1_login_exitoso(driver, test_data):
    """TC1 (Positivo): login con credenciales válidas."""
    user = test_data["valid_user"]
    LoginPage(driver).login(user["username"], user["password"])

    inventory = InventoryPage(driver)
    assert inventory.is_loaded()
    assert inventory.get_title() == "Products"


def test_tc2_login_fallido(driver, test_data):
    """TC2 (Negativo): login con credenciales inválidas muestra mensaje de error."""
    bad = test_data["invalid_user"]
    login = LoginPage(driver)
    login.login(bad["username"], bad["password"])

    assert bad["expected_error"] in login.get_error_message()
    assert "inventory" not in login.current_url


@pytest.mark.parametrize("option", ["name_az", "name_za", "price_low_high", "price_high_low"])
def test_tc3_ordenamiento_productos(logged_inventory, test_data, option):
    """TC3 (Positivo): ordenamiento por nombre y precio."""
    logged_inventory.sort_by(test_data["sorting"][option])

    if option == "name_az":
        names = logged_inventory.get_product_names()
        assert names == sorted(names)
    elif option == "name_za":
        names = logged_inventory.get_product_names()
        assert names == sorted(names, reverse=True)
    elif option == "price_low_high":
        prices = logged_inventory.get_product_prices()
        assert prices == sorted(prices)
    else:
        prices = logged_inventory.get_product_prices()
        assert prices == sorted(prices, reverse=True)


def test_tc4_agregar_productos_al_carrito(logged_inventory, test_data):
    """TC4 (Positivo): agregar productos y validar el contador del carrito."""
    products = test_data["products"]
    assert logged_inventory.get_cart_count() == 0

    for expected_count, product in enumerate(products, start=1):
        logged_inventory.add_product_to_cart(product)
        assert logged_inventory.get_cart_count() == expected_count

    logged_inventory.go_to_cart()
    cart = CartPage(logged_inventory.driver)
    assert cart.is_loaded()
    assert sorted(cart.get_item_names()) == sorted(products)


def test_tc5_flujo_checkout_completo(logged_inventory, test_data):
    """TC5 (Positivo): carrito -> formulario del cliente -> confirmación."""
    product = test_data["products"][0]
    info = test_data["checkout_info"]

    logged_inventory.add_product_to_cart(product)
    logged_inventory.go_to_cart()

    cart = CartPage(logged_inventory.driver)
    assert product in cart.get_item_names()
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_inventory.driver)
    checkout.fill_customer_info(info["first_name"], info["last_name"], info["postal_code"])
    assert product in checkout.get_summary_item_names()
    checkout.finish_order()

    assert checkout.get_confirmation_message() == test_data["checkout_complete_message"]
