import time

from playwright.sync_api import Playwright, Page, expect


def test_playwrightBasics(playwright:Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demowebshop.tricentis.com/")

def test_playwrightBasics_1(page:Page):
    page.goto("https://demowebshop.tricentis.com/")

def test_coreLocators(page:Page):
    page.goto("https://demowebshop.tricentis.com/")
    page.get_by_role("link",name="Register").click()
    page.get_by_role("radio",name="Female",exact=True).check()
    page.get_by_label("First name:").fill("pushpavathi8")
    page.get_by_label("Last name:").fill("Gotham1")
    page.get_by_label("Email:").fill("pushpavathi1238@example.com")
    page.locator("//input[@id='Password']").fill("pushpavathi8")
    page.locator("#ConfirmPassword").fill("pushpavathi8")
    page.get_by_role("button",name="Register").click()
    time.sleep(4)
    expect(page.get_by_text("Your registration completed")).to_be_visible()
    #Your registration completed
    #//input[@id='Password']

def test_childWindow(page:Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    with page.expect_popup() as popup:
        page.locator(".blinkingText").click()
        childPage = popup.value
        text = childPage.locator(".red").text_content()
        #print(text)
        #Please email us at mentor@rahulshettyacademy.com with below template to receive response
        words = text.split("at")
        email = words[1].split(" ")[1]
        assert email == "mentor@rahulshettyacademy.com"

def test_UiChecks(page:Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_visible()
    page.locator("#hide-textbox").click()
    time.sleep(5)
    expect(page.get_by_placeholder("Hide/Show Example")).to_be_hidden()
    time.sleep(5)

def test_Alerts(page:Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    page.on("dialog", lambda dialog :dialog.accept())
    time.sleep(3)
    page.locator("#confirmbtn").click()
    time.sleep(3)

def test_frames(page:Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    pageFrame = page.frame_locator("#courses-iframe")
    pageFrame.get_by_role("link",name="All Access plan").click()
    expect(pageFrame.locator("body")).to_contain_text("Happy Subscibers!")

    # Check Discount Price of Strawberry is 15
    # Identify Discount Price column
    # Identify Strawberry row
    # extract the discount price of Strawberry
def test_webTableExample(page:Page):
    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/offers")
    for index in range(page.locator("th").count()):
        if page.locator("th").nth(index).filter(has_text="Discount price").count()>0:
            colValue = index
            print(f"Discount price column value is {colValue}")
            break
    DiscountPriceRow = page.locator("tr").filter(has_text="Strawberry")
    expect(DiscountPriceRow.locator("td").nth(colValue)).to_have_text("15")

def test_mouseHover(page:Page):
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    page.locator("#mousehover").hover()
    time.sleep(5)
    page.get_by_role("link",name="Top").click()
    time.sleep(3)