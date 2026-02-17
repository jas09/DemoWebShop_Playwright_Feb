from playwright.sync_api import expect

from Utils.Utilities import Utilities


class ThankYouPage:
    def __init__(self,page):
        self.page = page
        self.utils = Utilities(page)

    def verifyOrderSuccessMessage(self):
        #self.page.locator(".title").wait_for(state="visible")
        orderSuccessMessage = self.page.locator("//div[@class='title']/strong").inner_text().strip()
        assert orderSuccessMessage in "Your order has been successfully processed!"

    def verifyOrderNumber(self):
        order_text = self.page.locator("ul.details > li:first-child").inner_text()
        order_number = order_text.split(":")[-1].strip()
        print(f"Captured order number: {order_number}")
        #test_case_id = test_data["ID"]
        # Save to JSON file with mapping {Test_Case_ID: OrderNumber}
        self.utils.update_order_number(order_number)
        return order_number

    def clickContinue_navigateBackTo_DashboardPage(self):
        self.page.locator("//input[@value='Continue']").click()
        expect(self.page.locator(".header-logo")).to_be_visible()
        # Click here for order details. - link
        # //input[@value='Continue']
