import time

from playwright.sync_api import Playwright, Page, expect

def test_DemoWebShopRegistration(page:Page):
    page.goto("https://demowebshop.tricentis.com/")
    page.get_by_role("link",name="Register").click()
    page.get_by_role("radio",name="Female",exact=True).check()
    page.get_by_label("First name:").fill("pushpavathi9")
    page.get_by_label("Last name:").fill("Gotham1")
    page.get_by_label("Email:").fill("pushpavathi1239@example.com")
    page.locator("//input[@id='Password']").fill("pushpavathi9")
    page.locator("#ConfirmPassword").fill("pushpavathi9")
    page.get_by_role("button",name="Register").click()
    time.sleep(4)
    expect(page.get_by_text("Your registration completed")).to_be_visible()