from playwright.sync_api import sync_playwright
import re
import time

def scrape_tiktok_collection(collection_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(collection_url)

        # Scroll to load more videos
        for _ in range(5):  # Adjust scroll times if needed
            page.mouse.wheel(0, 5000)
            time.sleep(2)

        # Extract video URLs
        video_elements = page.locator("a[href*='/video/']").all()
        video_ids = set()

        for element in video_elements:
            href = element.get_attribute("href")
            match = re.search(r"/video/(\d+)", href)
            if match:
                video_ids.add(match.group(1))

        browser.close()
        return list(video_ids)

# Example Usage
collection_url = "https://www.tiktok.com/@a41k_/collection/Website%20Pulling%20Collection-7474224942796507927"
video_ids = scrape_tiktok_collection(collection_url)
print(video_ids)  # Output video IDs for use in your HTML
