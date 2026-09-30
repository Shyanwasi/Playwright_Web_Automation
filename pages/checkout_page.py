from playwright.sync_api import Page
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_link = page.locator(".shopping_cart_link")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.complete_header = page.locator(".complete-header")

    def go_to_cart_and_checkout(self):
        self.click_element(self.cart_link, "Shopping Cart")
        self.click_element(self.checkout_button, "Checkout Button")

    def fill_shipping_info(self, first_name: str, last_name: str, postal_code: str):
        self.fill_field(self.first_name_input, first_name, "First Name")
        self.fill_field(self.last_name_input, last_name, "Last Name")
        self.fill_field(self.postal_code_input, postal_code, "Postal Code")
        self.click_element(self.continue_button, "Continue Button")

    def finish_checkout(self):
        self.click_element(self.finish_button, "Finish Button")