import pytest

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="browser selection")
    parser.addoption("--url_key", action="store", default="DemoWebShop", help="Choose URL key")

URL_MAP = {"DemoWebShop": "https://demowebshop.tricentis.com/"}

@pytest.fixture(scope="function")
def browserInstance(playwright,request):
    browser_name = request.config.getoption("browser_name")
    url_key = request.config.getoption("url_key")
    base_url = URL_MAP.get(url_key)
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=True,args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=True,args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
    #context = browser.new_context()
    page = context.new_page()
    # Start tracing manually
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page.goto(base_url)
    yield page
    # Stop tracing and save file
    context.tracing.stop(path=f"test-results/{request.node.name}-trace.zip")
    context.close()
    browser.close()