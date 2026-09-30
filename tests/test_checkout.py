import json
import pytest
from playwright.sync_api import Page, expect
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage
from config.config import Config
from utils.logger import get_logger

logger = get_logger("TestCheckoutShared")

@pytest.mark.regression
def test_step_1_add_item_and_checkout(shared_auth_page: Page):
    """Step 1: Navigate to inventory, add item, and start checkout."""
    logger.info(f"[{Config.ENV_NAME}] Step 1: Navigating and adding item to cart...")
    inventory_page = InventoryPage(shared_auth_page)
    checkout_page = CheckoutPage(shared_auth_page)

    shared_auth_page.goto(f"{Config.BASE_URL}inventory.html")
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    checkout_page.go_to_cart_and_checkout()

@pytest.mark.regression
def test_step_2_fill_shipping_and_finish(shared_auth_page: Page):
    """Step 2: Continues in the SAME window to fill shipping details and complete order."""
    logger.info(f"[{Config.ENV_NAME}] Step 2: Continuing checkout in the same window...")
    checkout_page = CheckoutPage(shared_auth_page)

    checkout_page.fill_shipping_info("Senior", "SDET", "10001")
    checkout_page.finish_checkout()

    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
    logger.info("Shared window E2E checkout completed successfully.")