import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.config import Config
from utils.logger import get_logger

logger = get_logger("TestLogin")

@pytest.mark.smoke
@pytest.mark.regression
def test_valid_login_positive(login_page: LoginPage, inventory_page: InventoryPage, page: Page):
    logger.info(f"[{Config.ENV_NAME}] Starting Positive Valid Login Test...")
    login_page.navigate()
    login_page.login(Config.STANDARD_USER, Config.STANDARD_PASSWORD)

    expect(page).to_have_url(f"{Config.BASE_URL}inventory.html")
    expect(inventory_page.title_label).to_have_text("Products")
    logger.info("Positive valid login test passed.")

@pytest.mark.smoke
@pytest.mark.regression
def test_locked_out_user_negative(login_page: LoginPage, page: Page):
    logger.info(f"[{Config.ENV_NAME}] Starting Negative Locked-Out User Test...")
    login_page.navigate()
    login_page.login(Config.LOCKED_USER, Config.STANDARD_PASSWORD)

    error_message = page.locator("[data-test='error']")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Sorry, this user has been locked out.")
    logger.info("Locked-out user validation passed.")

@pytest.mark.regression
def test_invalid_password_negative(login_page: LoginPage, page: Page):
    logger.info(f"[{Config.ENV_NAME}] Starting Negative Invalid Password Test...")
    login_page.navigate()
    login_page.login(Config.STANDARD_USER, "wrong_password_123")

    error_message = page.locator("[data-test='error']")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Username and password do not match any user in this service")
    logger.info("Invalid password validation passed.")