import pytest
import allure
from pathlib import Path
from playwright.sync_api import Page, Browser
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage
from config.config import Config
from utils.logger import get_logger

logger = get_logger("Conftest")

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Target environment file to load: qa, staging, prod"
    )

def pytest_configure(config):
    env_flag = config.getoption("--env").lower()
    Config.load_environment(env_flag)

    allure_dir = config.getoption("--alluredir")
    if allure_dir:
        allure_path = Path(allure_dir)
        allure_path.mkdir(exist_ok=True)
        env_file = allure_path / "environment.properties"
        with open(env_file, "w") as f:
            f.write(f"Environment={Config.ENV_NAME}\n")
            f.write(f"Base_URL={Config.BASE_URL}\n")

# ============================================================================
# PLAYWRIGHT STORAGE STATE (AUTH SESSION REUSE)
# ============================================================================
@pytest.fixture(scope="session")
def setup_auth_state(browser: Browser):
    state_file = Path(Config.AUTH_STATE_PATH)
    state_file.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Generating session storage state at: {state_file}")
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(Config.STANDARD_USER, Config.STANDARD_PASSWORD)
    page.wait_for_url(f"{Config.BASE_URL}inventory.html")

    context.storage_state(path=str(state_file))
    logger.info("Storage state saved successfully.")
    context.close()
    return str(state_file)

@pytest.fixture
def auth_page(browser: Browser, setup_auth_state: str) -> Page:
    context = browser.new_context(
        storage_state=setup_auth_state,
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def auth_inventory_page(auth_page: Page) -> InventoryPage:
    return InventoryPage(auth_page)

@pytest.fixture
def auth_checkout_page(auth_page: Page) -> CheckoutPage:
    return CheckoutPage(auth_page)

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)

@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    # ============================================================================
# MODULE-SCOPED AUTH PAGE (Runs all tests in a file inside ONE browser window)
# ============================================================================
@pytest.fixture(scope="module")
def shared_auth_page(browser: Browser, setup_auth_state: str):
    """Opens a single browser window pre-loaded with state for the entire test file."""
    context = browser.new_context(
        storage_state=setup_auth_state,
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request, page: Page):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        artifacts_dir = Path("artifacts")
        artifacts_dir.mkdir(exist_ok=True)
        test_name = request.node.name
        screenshot_path = artifacts_dir / f"failure_{test_name}.png"
        
        try:
            screenshot_bytes = page.screenshot(path=str(screenshot_path), full_page=True)
            logger.error(f"Test '{test_name}' FAILED! Screenshot saved: {screenshot_path}")
            allure.attach(
                screenshot_bytes,
                name=f"Failure_{test_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            logger.warning(f"Could not capture failure screenshot: {e}")