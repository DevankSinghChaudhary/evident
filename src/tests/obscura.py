from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")

        context = browser.contexts[0]
        page = context.new_page()

        page.goto("https://substack.com/sponsorships")

        print("Title:", page.title())
        print("URL:", page.url)

        print("HTML:")
        print(page.content())

        print("Body:")
        print(page.locator("body").inner_text(timeout=5000))

        print("Paragraph count:", page.locator("p").count())

        print("Link count:", page.locator("a").count())

        # JavaScript execution
        print("JS title:", page.evaluate("() => document.title"))

        # JavaScript DOM access
        print(
            "Paragraphs via JS:",
            page.evaluate("() => document.querySelectorAll('p').length"),
        )

        # Click an actual link

        print("URL after click:", page.url)
        print("Title after click:", page.title())


if __name__ == "__main__":
    main()
