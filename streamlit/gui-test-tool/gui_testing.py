import time

from playwright.sync_api import Page, expect

timeout_val = 15000


def test_streamlit_homepage_loads(page: Page):
    page.goto("http://localhost:8501/")
    expect(
        page.get_by_text("🔎 Multilingual NER with Gliner", exact=True)
    ).to_be_visible(timeout=timeout_val)
    expect(page.get_by_text("Submit", exact=True)).to_be_visible(timeout=timeout_val)


def test_streamlit_default_input_output(page: Page):
    page.goto("http://localhost:8501/")

    expect(page.get_by_text("Submit", exact=True)).to_be_visible(timeout=timeout_val)
    page.get_by_text("Submit", exact=True).click()

    expect(page.get_by_text("Gevonden entiteiten:", exact=True)).to_be_visible(
        timeout=timeout_val
    )
    expect(page.get_by_text("start", exact=True)).to_be_visible(timeout=timeout_val)
    expect(page.get_by_text("end", exact=True)).to_be_visible(timeout=timeout_val)


def test_streamlit_user_input_output(page: Page):
    page.goto("http://localhost:8501/")

    expect(page.get_by_text("Submit", exact=True)).to_be_visible(timeout=timeout_val)

    iframe = page.frame_locator("iframe")
    for aria_label in ["person", "country", "food", "dj"]:
        expect(iframe.get_by_text(aria_label)).to_be_visible(timeout=timeout_val)
        iframe.get_by_label(f"remove {aria_label}").click()
        expect(iframe.get_by_text(aria_label)).not_to_be_visible()

    expect(page.get_by_text("Submit", exact=True)).to_be_visible(timeout=timeout_val)
    page.get_by_text("Submit", exact=True).click()

    expect(page.get_by_text("Gevonden entiteiten:", exact=True)).to_be_visible(
        timeout=timeout_val
    )
    expect(page.get_by_text("empty", exact=True)).to_be_visible(timeout=timeout_val)

    locator = iframe.locator("input").first
    locator.click()

    # tags
    for _ in range(4):
        locator.press("Backspace")

    for tag in ["animal", "body of water", "altitude"]:
        locator.fill(tag)
        time.sleep(0.5)
        locator.press("Enter")

    # text
    locator = page.locator("textarea")
    locator.click()
    time.sleep(0.5)
    locator.press("Control+A")
    time.sleep(0.5)
    locator.press("Backspace")
    time.sleep(0.5)
    locator.fill(
        "Blobfish are usually found in dark, cold habitats deep at the bottom of "
        " the Atlantic, Indian, and Pacific oceans, between 1,970 and 3,940 feet deep."
    )

    expect(page.get_by_text("Submit", exact=True)).to_be_visible(timeout=timeout_val)
    page.get_by_text("Submit", exact=True).click()

    expect(page.get_by_text("Gevonden entiteiten:", exact=True)).to_be_visible(
        timeout=timeout_val
    )
    expect(page.get_by_text("start", exact=True)).to_be_visible(timeout=timeout_val)
    expect(page.get_by_text("end", exact=True)).to_be_visible(timeout=timeout_val)

    expect(page.get_by_text("122")).to_be_visible(timeout=timeout_val)
    expect(page.get_by_text("142")).to_be_visible(timeout=timeout_val)
    expect(page.get_by_text("98")).to_be_visible(timeout=timeout_val)
    expect(page.get_by_text("112")).to_be_visible(timeout=timeout_val)


if __name__ == "__main__":
    test_streamlit_homepage_loads()
    test_streamlit_default_input_output()
    test_streamlit_user_input_output()
