from playwright.sync_api import Page
from pages.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title_label = page.locator(".title")
        self.shopping_cart_badge = page.locator(".shopping_cart_badge")

    def add_item_to_cart(self, item_name: str):
        formatted_name = item_name.lower().replace(" ", "-")
        add_btn = self.page.locator(f"[data-test='add-to-cart-{formatted_name}']")
        self.click_element(add_btn, f"Add {item_name} to Cart")