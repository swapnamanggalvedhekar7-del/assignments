import re
import time

from playwright.sync_api import Playwright, expect


def test_eventhub_e2e(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page =  context.new_page()
    #Sign in and open the Events page from Browse Events.
    page.goto("https://eventhub.rahulshettyacademy.com/")
    page.wait_for_load_state("networkidle")
    page.get_by_label("email").fill("swapnamanggalvedhekar@gmail.com")
    page.get_by_label("password").fill("Password@7")
    page.locator("button.login-submit-btn").click()
    browse_events_btn = page.locator("//span[text() = 'Browse Events →']")
    browse_events_btn.click()
    #Confirm the Upcoming Events heading is visible
    expect(page.locator("h1").filter(has_text="Upcoming Events")).to_be_visible()
    #Use several locator strategies on the filter area: search for World, choose category Conference, and choose city Hyderabad.
    page.wait_for_load_state("networkidle")
    page.get_by_placeholder("Search events, venues…").fill("World")
    category_dropdown = page.locator("select").filter(has_text="All Categories")
    category_dropdown.select_option(value="Conference")
    city_dropdown = page.locator("select").filter(has_text="All Cities")
    city_dropdown.select_option(value="Hyderabad")
    #page.screenshot(path="search_results.png")
    #Work with the visible event cards: confirm at least one card matches, narrow to the card that shows World Tech Summit, and confirm exactly one match.
    page.wait_for_load_state("networkidle")
    event_count = page.get_by_test_id("event-card")
    #print(event_count)
    expect(event_count).to_have_count(1, timeout=7000)
    event_card = page.get_by_test_id("event-card").first
    #From that matching card, capture the event title, price text, and seats text.
    event_title = event_card.locator("h3").filter(has_text='World Tech Summit').text_content()
    event_price = event_card.locator("p.text-lg").text_content()
    event_seats = event_card.locator("span.text-xs.font-bold.text-amber-600").text_content()
    print("event_title",event_title,"event_price",event_price, "event_seats",event_seats)
    available_seat_count = event_seats.split(" ")
    #Confirm the title is World Tech Summit, the price text contains $, and the available seat count parsed from the seats text is greater than 0.
    assert event_title == "World Tech Summit", f"Expected 'World Tech Summit' but got '{event_title}'"
    assert "$" in event_price, "event_price does not contain $"
    assert available_seat_count[0] > "0", f"Expected available seats to be greater than 0 but got '{available_seat_count[0]}'"
    #From inside that same card only, open Book Now.
    event_card.get_by_test_id("book-now-btn").click()
    #page.wait_for_load_state("networkidle")
    expect(page).to_have_url(re.compile(r'/events/'))
    #assert page.url == url,f"f Expected url is {url} but got {page.url}"
    event_title_stored = page.locator("h1").filter(has_text="World Tech Summit").text_content()
    assert event_title_stored == "World Tech Summit", f"Expected 'World Tech Summit' but got '{event_title_stored}'"
    event_price_per_ticket = page.locator("//p[text()='Price per ticket']/following-sibling::p[text()='$1,500']")
    assert event_price == event_price_per_ticket.text_content(), f"Expected '{event_price}' but got '{event_price_per_ticket.text_content()}'"
    #Return to the Events list, clear filters back to all categories and cities, and confirm at least three cards are visible.
    page.go_back()
    page.wait_for_load_state("networkidle")
    clear_filter_btn = page.locator("button").filter(has_text='Clear filters')
    clear_filter_btn.click()
    card = page.locator("//div/child::article")
    count = card.count()
    expect(card).to_have_count(3, timeout=7000)
    # print(count)
    #assert count >= 3, f"Expected at least 3 events but got {count}"
    for i in range(count):
        card_nth = card.nth(i)
        print(card_nth.locator("h3").text_content())
    #Compare the first, second, and last card titles: all must be non-empty, and the first and last titles must differ.
    first_card = card.nth(0).locator("h3").text_content()
    second_card = card.nth(1).locator("h3").text_content()
    third_card = card.nth(2).locator("h3").text_content()
    assert first_card != second_card, "First and second event cards are the same"
    assert second_card != third_card, "Second and third event cards are the same"
    assert first_card != third_card, "First and third event cards are the same"