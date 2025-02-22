from playwright.sync_api import sync_playwright
import re
import time

def scrape_tiktok_collection(collection_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(collection_url)

        video_ids = set()
        last_count = 0

        while True:
            page.mouse.wheel(0, 5000)  # Scroll down
            time.sleep(3)  # Allow time to load more content

            video_elements = page.locator("a[href*='/video/']").all()
            for element in video_elements:
                href = element.get_attribute("href")
                match = re.search(r"/video/(\d+)", href)
                if match:
                    video_ids.add(match.group(1))

            if len(video_ids) == last_count:  # Stop if no new videos are found
                break
            last_count = len(video_ids)

        browser.close()
        return list(video_ids)

# Example usage:
collection_url = "https://www.tiktok.com/@a41k_/collection/repost-7451339507582012162?is_from_webapp=1&sender_device=pc"
video_ids = scrape_tiktok_collection(collection_url)
print(video_ids)  # Use these IDs in your HTML
