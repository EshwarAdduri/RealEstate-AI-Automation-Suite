import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    options = Options()
    options.headless = False
    options.binary_location = r"C:\Users\addur\OneDrive\Desktop\Tor Browser\Browser\firefox.exe"
    service = Service(r"C:\Justin-Pickell-Foreclosure-Data-Coding-Web-Scrapping\geckodriver-v0.35.0-win64\geckodriver.exe")
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(10)
    return driver

def safe_get(driver, url):
    try:
        print(f"Navigating to: {url}")
        driver.get(url)
    except TimeoutException:
        print(f"Timeout while loading {url}")

def close_popup(driver):
    try:
        popup_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-dialog .btn-close"))
        )
        popup_button.click()
        print("Popup closed.")
    except (TimeoutException, NoSuchElementException):
        print("No popup found or already closed.")

def safely_click_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", element)

def collect_county_links(driver, state_url):
    safe_get(driver, state_url)
    close_popup(driver)

    try:
        search_by_county_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'County')]"))
        )
        safely_click_element(driver, search_by_county_button)
        time.sleep(3)  # Wait for county list

    except TimeoutException:
        print("Search by County button not found.")
        return {}

    county_links = {}
    county_elements = driver.find_elements(By.CSS_SELECTOR, "#topCountyList li a")
    for element in county_elements:
        county_name = element.text.strip()
        county_href = element.get_attribute("href")
        county_links[county_name] = county_href
        print(f"Found county: {county_name} -> {county_href}")

    return county_links

def apply_filters(driver):
    try:
        print("Applying foreclosure and preforeclosure filters...")
        listing_filter = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "headListingType")))
        safely_click_element(driver, listing_filter)
        time.sleep(2)

        foreclosure_checkbox = driver.find_element(By.CSS_SELECTOR, "input[name='lc'][value='foreclosure']")
        if not foreclosure_checkbox.is_selected():
            foreclosure_checkbox.click()
            print("Clicked Foreclosure filter. Waiting for reload...")
            WebDriverWait(driver, 10).until(EC.staleness_of(foreclosure_checkbox))
            time.sleep(5)

        listing_filter = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "headListingType")))
        safely_click_element(driver, listing_filter)
        time.sleep(2)

        preforeclosure_checkbox = driver.find_element(By.CSS_SELECTOR, "input[name='lc'][value='preforeclosure']")
        if not preforeclosure_checkbox.is_selected():
            preforeclosure_checkbox.click()
            print("Clicked Preforeclosure filter. Waiting for reload...")
            WebDriverWait(driver, 10).until(EC.staleness_of(preforeclosure_checkbox))
            time.sleep(5)

        print("Filters applied successfully.")

    except Exception as e:
        print(f"Filter application failed: {e}")

def collect_notice_links(driver, county_url):
    print(f"\nProcessing county page: {county_url}")
    safe_get(driver, county_url)
    close_popup(driver)
    apply_filters(driver)
    
    try:
        per_page_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='propage']"))
        )
        Select(per_page_dropdown).select_by_value("100")
        print("Set results per page to 100.")
        time.sleep(5)

    except Exception as e:
        print(f"Failed to set results per page to 100: {e}")
    
    notice_links = set()
    page_count = 1
    last_page_links = None  # Store previous page links to detect repetition

    while True:
        try:
            # Collect notice links from the current page
            notice_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.contViewDetailsBtn a.inlineDetails"))
            )
            current_page_links = {element.get_attribute("href") for element in notice_elements}

            # Stop if we are collecting duplicate links (looping back to page 1)
            if current_page_links == last_page_links:
                print(f"Detected loop back to page {page_count}, stopping pagination.")
                break

            notice_links.update(current_page_links)
            print(f"Page {page_count}: Collected {len(current_page_links)} notices.")

            # Save current page links for comparison on the next iteration
            last_page_links = current_page_links

            # Check if the "Next" button is disabled (meaning we are on the last page)
            next_button = driver.find_element(By.ID, "pageNextBottom")
            if "disabled" in next_button.get_attribute("class"):
                print("No more pages. Stopping pagination.")
                break

            # Move to the next page
            safely_click_element(driver, next_button)
            time.sleep(3)
            page_count += 1

            # Handle popups if they appear
            if page_count % 2 == 0:
                close_popup(driver)

        except Exception as e:
            print(f"Error navigating pages: {e}")
            break
    
    print(f"Total notices collected from this county: {len(notice_links)}\n")
    return list(notice_links)


def save_links_to_txt(links, filename="notice_links.txt"):
    with open(filename, "w") as file:
        for link in links:
            file.write(link + "\n")
    print(f"\nAll collected links saved to {filename}")

def main():
    driver = setup_driver()
    try:
        state_page = "https://www.preforeclosure.com/state/al"

        # 🔹 Collect county links ONCE at the beginning
        county_links = collect_county_links(driver, state_page)

        all_notice_links = []
        
        for county, link in county_links.items():
            print(f"\n========== START PROCESSING: {county} ==========\n")
            notice_links = collect_notice_links(driver, link)
            all_notice_links.extend(notice_links)
            print(f"Collected {len(notice_links)} notices from {county}")

            # 🔹 DO NOT navigate back to the state page
            # Instead, just continue to the next county

        save_links_to_txt(all_notice_links)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()


