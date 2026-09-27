from playwright.sync_api import Page

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        # Locators
        self.title_label = page.locator(".title")
        self.shopping_cart_badge = page.locator(".shopping_cart_badge")

    def add_item_to_cart(self, item_name: str):
        # Dynamically locate product card by item name
        product_card = self.page.locator(".inventory_item").filter(has_text=item_name)
        product_card.get_by_role("button", name="Add to cart").click()