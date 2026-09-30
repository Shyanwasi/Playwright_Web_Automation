import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.config import Config
from utils.logger import get_logger

logger = get_logger("TestInventory")

@pytest.mark.smoke
def test_inventory_display_and_add_item(login_page: LoginPage, inventory_page: InventoryPage, page: Page):
    logger.info(f"[{Config.ENV_NAME}] Starting Inventory Display & Add to Cart Test...")
    login_page.navigate()
    login_page.login(Config.STANDARD_USER, Config.STANDARD_PASSWORD)

    items = page.locator(".inventory_item")
    expect(items).to_have_count(6)

    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    expect(inventory_page.shopping_cart_badge).to_have_text("1")
    logger.info("Inventory item addition test passed.")

@pytest.mark.smoke
def test_inventory_sorting(login_page: LoginPage, page: Page):
    logger.info(f"[{Config.ENV_NAME}] Starting Inventory Product Sorting Test...")
    login_page.navigate()
    login_page.login(Config.STANDARD_USER, Config.STANDARD_PASSWORD)

    sort_dropdown = page.locator("[data-test='product-sort-container']")
    sort_dropdown.select_option("hilo")

    first_item_price = page.locator(".inventory_item_price").first
    expect(first_item_price).to_have_text("$49.99")
    logger.info("Inventory sorting test passed.")