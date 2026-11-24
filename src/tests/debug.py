import json

from playwright.sync_api import sync_playwright

URL = "https://www.jstor.org/stable/48669293?seq=1"
CDP_URL = "http://127.0.0.1:9223"


def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)

        context = browser.contexts[0]
        page = context.new_page()

        # Diagnostics
        failed_requests = []
        console_errors = []

        page.on(
            "requestfailed",
            lambda request: failed_requests.append(
                {
                    "url": request.url,
                    "failure": request.failure,
                }
            ),
        )

        page.on(
            "console",
            lambda message: (
                console_errors.append(
                    {
                        "type": message.type,
                        "text": message.text,
                    }
                )
                if message.type == "error"
                else None
            ),
        )

        print(f"Navigating to {URL}")

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        # Allow dynamically loaded page content to settle.
        page.wait_for_timeout(5000)

        # Extract page information.
        data = page.evaluate("""
        () => {
            const clean = text =>
                text?.replace(/\\\\s+/g, " ").trim() || "";

            const links = Array.from(
                document.querySelectorAll("a[href]")
            ).map(a => ({
                text: clean(a.innerText),
                href: a.href,
                title: a.title || null
            }));

            const headings = Array.from(
                document.querySelectorAll("h1, h2, h3, h4")
            ).map(h => ({
                tag: h.tagName.toLowerCase(),
                text: clean(h.innerText)
            }));

            const paragraphs = Array.from(
                document.querySelectorAll("p")
            ).map(p => clean(p.innerText))
             .filter(Boolean);

            return {
                title: document.title,
                url: location.href,
                headings,
                paragraphs,
                body_text: clean(document.body.innerText),
                links,
                metadata: Array.from(
                    document.querySelectorAll("meta")
                ).map(m => ({
                    name: m.name || m.getAttribute("property"),
                    content: m.content
                })).filter(m => m.content)
            };
        }
        """)

        data["diagnostics"] = {
            "failed_requests": failed_requests,
            "console_errors": console_errors,
        }

        # Save output.
        with open("debug_output.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Print summary.
        print("\n========== PAGE SUMMARY ==========")
        print("Title:", data["title"])
        print("URL:", data["url"])
        print("Headings:", len(data["headings"]))
        print("Paragraphs:", len(data["paragraphs"]))
        print("Links:", len(data["links"]))
        print("Text length:", len(data["body_text"]))

        print("\n========== HEADINGS ==========")
        for heading in data["headings"]:
            print(f"[{heading['tag']}] {heading['text']}")

        print("\n========== LINKS ==========")
        for link in data["links"]:
            print(f"{link['text'] or '[No text]'}")
            print(f"  {link['href']}")

        print("\n========== BODY TEXT ==========")
        print(data["body_text"])

        print("\n========== DIAGNOSTICS ==========")
        print("Failed requests:", len(failed_requests))
        print("Console errors:", len(console_errors))

        print("\nSaved to debug_output.json")

        page.close()


if __name__ == "__main__":
    main()
