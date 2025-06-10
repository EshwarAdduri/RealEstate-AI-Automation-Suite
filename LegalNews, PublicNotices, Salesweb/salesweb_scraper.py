from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def scrape_addresses_from_county(county_index):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Open the website
    driver.get("https://salesweb.civilview.com/")

    # Optional: wait for the page to load completely
    time.sleep(3)

    # Extract all county links
    county_links = driver.find_elements(By.XPATH, "//div[@class='table-responsive']//a")

    # Check if the county_index is valid
    if county_index < 0 or county_index >= len(county_links):
        driver.quit()
        return []

    # Click on the selected county link
    county_links[county_index].click()

    # Optional: wait for the page to load completely
    time.sleep(3)  # Adjust sleep time if necessary

    # Wait for the table to be present in the DOM
    wait = WebDriverWait(driver, 20)
    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'table-striped')))

    # Find the header row and determine the address column index
    header_row = table.find_element(By.TAG_NAME, 'thead')
    header_columns = header_row.find_elements(By.TAG_NAME, 'th')
    
    address_column_index = -1
    for index, column in enumerate(header_columns):
        if "Address" in column.text or "Address/Description" in column.text:
            address_column_index = index
            break

    # If the address column is not found, exit
    if address_column_index == -1:
        driver.quit()
        return []

    # Find all rows in the table body
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # Extract addresses
    addresses = []
    for row in rows[1:]:  # Skip header row
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) > address_column_index:
            address = cells[address_column_index].text
            addresses.append(address)

    # Close the browser
    driver.quit()

    return addresses