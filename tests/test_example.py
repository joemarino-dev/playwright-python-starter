def test_example(page):
    page.goto("https://example.com")
        
    assert "Example Domain" in page.title()
    assert page.get_by_role("heading", name="Example Domain").text_content() == "Example Domain"
    assert "This domain is for use in documentation examples without needing permission. Avoid use in operations." in page.inner_text("body")