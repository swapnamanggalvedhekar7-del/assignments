import time

import pytest
from playwright.sync_api import Playwright, Page, expect


#playwright core package is a standalone browser automation library.
# playwright test runner includes browser management, reporting, assertions

#@pytest.mark.only---this will focus on test case
@pytest.mark.smoke
def test_firstsmoketest(page:Page):
    page.goto("https://eventhub.rahulshettyacademy.com/")
    expect(page.locator(".text-xl")).to_have_text("Sign in to EventHub")
    expect(page.get_by_placeholder("you@email.com")).to_be_visible()
    expect(page.get_by_role("button", name="Sign In")).to_be_visible()

@pytest.mark.smoke
def test_secondsmoketest(page:Page):
    page.goto("https://eventhub.rahulshettyacademy.com/")
    expect(page.locator(".text-xl")).to_have_text("Sign in to EventHub")
    password = page.get_by_label("password")
    assert password.is_visible()
    url = page.url
    assert "/login" in url


