from playwright.sync_api import Page, Locator
from utils.logger import get_logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def navigate_to(self, url: str):
        self.logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)

    def click_element(self, locator: Locator, description: str = "Element"):
        self.logger.info(f"Clicking on: {description}")
        locator.click()

    def fill_field(self, locator: Locator, value: str, description: str = "Input Field"):
        self.logger.info(f"Entering text in {description}")
        locator.fill(value)

    def get_text(self, locator: Locator) -> str:
        text = locator.inner_text()
        self.logger.info(f"Retrieved text: {text}")
        return text