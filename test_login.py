from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

def test_user_can_login_and_add_item(
    login_page: LoginPage, 
    inventory_page: InventoryPage, 
    page: Page
):
    # 1. Login
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # 2. Verify Login
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(inventory_page.title_label).to_have_text("Products")

    # 3. Add Item to Cart
    inventory_page.add_item_to_cart("Sauce Labs Backpack")

    # 4. Verify Cart Badge
    expect(inventory_page.shopping_cart_badge).to_have_text("1")