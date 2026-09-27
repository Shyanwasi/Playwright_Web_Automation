from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Cart & Navigation Locators
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        
        # Step 1: Shipping Form Locators
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.postal_code_input = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")
        
        # Step 2: Overview & Finish Locators
        self.finish_button = page.get_by_role("button", name="Finish")
        self.complete_header = page.locator(".complete-header")

    def go_to_cart_and_checkout(self):
        self.shopping_cart_link.click()
        self.checkout_button.click()

    def fill_shipping_info(self, first_name: str, last_name: str, zip_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(zip_code)
        self.continue_button.click()

    def finish_checkout(self):
        self.finish_button.click()