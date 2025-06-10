import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import os

# File to store fetched links
FETCHED_LINKS_FILE = "fetched_links2.txt"
LINKS_PER_SCROLL = 6  # Collect 6 links per scroll
MAX_SCROLLS = 8       # Scroll 8 times

def init_driver():
    """Initialize the WebDriver with Chrome options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    return driver

def load_fetched_links():
    """Load previously fetched links to avoid duplicates."""
    if os.path.exists(FETCHED_LINKS_FILE):
        with open(FETCHED_LINKS_FILE, "r") as file:
            return set(file.read().splitlines())
    return set()

def save_fetched_links(links):
    """Save fetched links to file."""
    if links:
        with open(FETCHED_LINKS_FILE, "a") as file:
            file.write("\n".join(links) + "\n")
        print(f"✅ Saved {len(links)} new links to {FETCHED_LINKS_FILE}")

def scroll_and_fetch_links(driver):
    """Scroll and fetch 6 unique property links per scroll for 8 scrolls."""
    fetched_links = load_fetched_links()
    total_new_links = set()

    driver.get("https://investorlift.com/")
    time.sleep(7)  # Ensure the page fully loads

    for scroll_count in range(1, MAX_SCROLLS + 1):
        print(f"\n🔄 Scroll {scroll_count}/{MAX_SCROLLS}...")
        new_links = set()

        # Find and hover over elements to trigger lazy loading
        property_elements = driver.find_elements(By.CSS_SELECTOR, "a.ui-deal-card-link")

        for element in property_elements:
            try:
                link = element.get_attribute("href")
                ActionChains(driver).move_to_element(element).perform()  # Simulate user interaction
                time.sleep(random.uniform(1, 2))

                if link and link not in fetched_links and link not in total_new_links:
                    new_links.add(link)
                    print(f"🔗 Found new link: {link}")

                if len(new_links) >= LINKS_PER_SCROLL:
                    break  # Stop after collecting 6 links per scroll
            except Exception as e:
                print(f"⚠️ Error interacting with element: {e}")

        if new_links:
            save_fetched_links(new_links)
            total_new_links.update(new_links)
            fetched_links.update(new_links)
        else:
            print("⚠️ No new links found during this scroll.")

        # Scroll down slowly to trigger lazy loading
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(random.uniform(4, 6))  # Slower scrolling for content loading

        # Ensure new content appears after scrolling
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ui-deal-card-link"))
            )
        except:
            print(f"⚠️ No new content detected after scroll {scroll_count}.")

    print(f"\n✅ Scraping completed. Total new links collected: {len(total_new_links)}")

def main():
    """Main function to fetch property links."""
    driver = init_driver()
    try:
        scroll_and_fetch_links(driver)
    finally:
        driver.quit()
        print("🚪 Browser closed.")

if __name__ == "__main__":
    main()
