import pytest
from pathlib import Path
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage  # <-- Import CheckoutPage


# ==========================================
# 1. PAGE OBJECT FIXTURES
# ==========================================
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)

@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:  # <-- Added Fixture
    return CheckoutPage(page)


# ==========================================
# 2. AUTOMATIC SCREENSHOT ON FAILURE HOOK
# ==========================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request, page: Page):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        artifacts_dir = Path("artifacts")
        artifacts_dir.mkdir(exist_ok=True)
        test_name = request.node.name
        screenshot_path = artifacts_dir / f"failure_{test_name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"\n[FAILURE SCREENSHOT SAVED] -> {screenshot_path}")