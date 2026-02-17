from playwright.sync_api import Page, expect

from POM.DashBoardPage import DashBoardPage


class LoginPage:
    def __init__(self,page):
        self.page = page

    def login(self,Email,Password):
        self.page.get_by_role("link", name="Log in").click()
        self.page.get_by_label("Email:").fill(Email)
        self.page.locator("#Password").fill(Password)
        self.page.get_by_role("button", name="Log in").click()
        expect(self.page.get_by_role("link", name=Email)).to_be_visible()
        dashBoardPage = DashBoardPage(self.page)
        return dashBoardPage

