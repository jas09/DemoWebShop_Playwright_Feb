import time

from playwright.sync_api import Page, expect

from POM.ShoppingCartPage import ShoppingCartPage
from Utils.Utilities import Utilities


class DashBoardPage(Utilities):

    def __init__(self,page:Page):
        super().__init__(page)
        self.page = page

    def verifyHeaderLinks(self,Email):
        expect(self.page.get_by_role("link",name=Email)).to_be_visible()
        expect(self.page.get_by_role("link",name="Log out")).to_be_visible()
        expect(self.page.locator("//div[@class='header-links']//span[normalize-space(text())='Shopping cart']")).to_be_visible()
        expect(self.page.locator("//div[@class='header-links']//span[normalize-space(text())='Wishlist']")).to_be_visible()

    def click_shopping_cart_link(self):
        self.page.locator("//div[@class='header-links']//span[normalize-space(text())='Shopping cart']").click()
        expect(self.page.locator("//div[@class='page-title']//h1[normalize-space(text())='Shopping cart']")).to_be_visible()
        shoppingCartPage = ShoppingCartPage(self.page)
        return shoppingCartPage