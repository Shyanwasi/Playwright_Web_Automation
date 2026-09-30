from playwright.sync_api import Page
from pages.base_page import BasePage
from config.config import Config

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")

    def navigate(self):
        self.navigate_to(Config.BASE_URL)

    def login(self, username: str, password: str):
        self.logger.info(f"Attempting login with user: {username}")
        self.fill_field(self.username_input, username, "Username")
        self.fill_field(self.password_input, password, "Password")
        self.click_element(self.login_button, "Login Button")