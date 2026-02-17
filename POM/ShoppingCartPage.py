from playwright.sync_api import Playwright, Page, expect

from POM.CheckOutPage import CheckOutPage
from Utils.Utilities import Utilities


class ShoppingCartPage(Utilities):
    def __init__(self,page:Page):
        super().__init__(page)
        self.page = page

    def provide_estimate_shipping_details(self,country,stateProvince,postalCode):
        self.page.locator("#CountryId").wait_for(state="visible")
        self.page.locator("#StateProvinceId").wait_for(state="visible")
        self.page.locator("#CountryId").select_option(label=country)
        self.page.locator("#StateProvinceId").select_option(label=stateProvince)
        self.page.locator("#ZipPostalCode").fill(str(postalCode))
        self.page.locator("//input[@value='Estimate shipping']").click()
        self.page.locator(".shipping-results").wait_for(state="attached")
        expect(self.page.locator(".shipping-results")).to_be_visible()

    def provide_termsAndConditions_checkout(self):
        self.page.locator("#termsofservice").check()
        expect(self.page.locator("#termsofservice")).to_be_checked()
        self.page.get_by_role("button",name="checkout").click()
        checkOutPage = CheckOutPage(self.page)
        return checkOutPage
