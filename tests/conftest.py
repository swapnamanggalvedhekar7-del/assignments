import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="session")
def base_url(playwright: Playwright):
    return "https://eventhub.rahulshettyacademy.com"
