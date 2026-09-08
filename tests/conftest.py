import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="session")
def base_url(playwright: Playwright):
    return "https://eventhub.rahulshettyacademy.com"

@pytest.fixture(scope='session',params =['Firefox','Chromium','Webkit'])
def get_browser(playwright: Playwright,request):
    return request.param

@pytest.fixture(scope='session')
def browser_page(playwright: Playwright, get_browser,base_url):
    if get_browser == "firefox":
        browser = playwright.firefox.launch()
    elif get_browser == "webkit":
        browser = playwright.webkit.launch()
    else:
        browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto(base_url)
    yield page
    context.close()
    browser.close()