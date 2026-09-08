import re
import time

import pytest
from playwright.sync_api import expect, Playwright, Page


@pytest.mark.smoke
def test_eventhub_validateFields(browser_page):
    page=browser_page
    expect(page).to_have_url(re.compile(r'/login'))
    expect(page).to_have_title(re.compile(r'EventHub'))
    expect(page.get_by_label("Email")).to_be_visible()
    expect(page.get_by_role("button",name="Sign In")).to_be_visible()

def test_validate_withpf(page:Page):
    page.goto("https://eventhub.rahulshettyacademy.com/")
    email= page.get_by_label("Email")
    email.fill("beginner@sample.com")
    assert email.input_value()=='beginner@sample.com'
    time.sleep(3)
    browser_context = page.context
    page=browser_context.new_page()
    page.goto("https://eventhub.rahulshettyacademy.com/login")
    time.sleep(5)
    expect(page.locator("h1.text-xl")).to_have_text("Sign in to EventHub")
    expect(page.get_by_placeholder("you@email.com")).to_be_empty()
    browser_context.close()