from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage

def test_full_e2e_checkout_flow(
    login_page: LoginPage,
    inventory_page: InventoryPage,
    checkout_page: CheckoutPage,
    page: Page
):
    # 1. Navigate & Login
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # 2. Add Item to Cart
    item_name = "Sauce Labs Backpack"
    inventory_page.add_item_to_cart(item_name)
    expect(inventory_page.shopping_cart_badge).to_have_text("1")

    # 3. Proceed to Checkout
    checkout_page.go_to_cart_and_checkout()
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    # 4. Fill Shipping Information
    checkout_page.fill_shipping_info("John", "Doe", "90210")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

    # 5. Finish Purchase
    checkout_page.finish_checkout()

    # 6. Verify Confirmation
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")