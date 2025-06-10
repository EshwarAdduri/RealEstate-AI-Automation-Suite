import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import openpyxl


def simulate_typing(input_element, text):
    """Simulate typing with random pauses between keystrokes."""
    for char in text:
        input_element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))


def simulate_mouse_movement(driver, element):
    """Move the mouse to the element smoothly, as a user would do."""
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(random.uniform(1, 2))  # Pause before interacting with the element


def login_to_investorlift(driver, email, password):
    """Handles the login process by automating user interaction."""
    driver.get("https://investorlift.com/")  # Navigate to the main login page

    try:
        # Wait for the main "Log in" button and click it
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[span/span[contains(text(), 'Log in')]]")
            )
        )
        driver.execute_script("arguments[0].click();", login_button)

        # Wait for email input field to appear
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Email address']")
            )
        )

        # Simulate typing the email
        simulate_mouse_movement(driver, email_input)
        email_input.clear()
        simulate_typing(email_input, email)

        # Click "Continue" button for email entry
        continue_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'enter-email-form_action')]/button")
            )
        )
        simulate_mouse_movement(driver, continue_button)
        driver.execute_script("arguments[0].click();", continue_button)

        # Wait for password field to appear
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Enter password']")
            )
        )

        # Simulate typing the password
        simulate_mouse_movement(driver, password_input)
        password_input.clear()
        simulate_typing(password_input, password)

        # Click the "Continue" button for password entry
        try:
            # Wait and click the "Continue" button after entering password
            continue_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'enter-password-form_action')]//button",
                    )
                )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
            simulate_mouse_movement(driver, continue_button)
            driver.execute_script("arguments[0].click();", continue_button)

            # Wait for successful login confirmation
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='name']/span[text()='Search by location']")
                )
            )

        except Exception as e:
            print(f"Failed to click 'Continue' button after entering password: {e}")

    except Exception as e:
        print(f"Error during login: {e}")
        return False

    return True


def scrape_property_data(driver, sheet):
    """Scrapes property data after login and appends it to the sheet."""
    try:
        property_data = {}

        # Extract additional data
        property_data["Address"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[3]/div[1]/div/span[1]",
        ).text
        property_data["Price"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[2]/div[1]/div[1]/div[1]/span[2]",
        ).text
        property_data["ARV"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/span[2]",
        ).text
        property_data["Gross margin"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[2]/div[1]/div[1]/div[3]/span[2]",
        ).text
        property_data["Sq.Ft"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[1]/div[1]/div[1]/div[4]/div/div[2]",
        ).text
        property_data["Type"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]",
        ).text
        property_data["Parking"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]",
        ).text
        property_data["Build in"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[2]/div[3]/div[2]/div[2]",
        ).text
        property_data["Lot size"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]",
        ).text
        property_data["Beds"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div/div[2]",
        ).text
        property_data["Baths"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div/div[2]",
        ).text
        property_data["Half Bath"] = driver.find_element(
            By.XPATH,
            "//*[@id='__nuxt']/div/div[2]/div/div/div[1]/div[4]/div[1]/div[1]/div[1]/div[3]/div/div[2]",
        ).text

        # Append data
        sheet.append(
            [
                property_data["Address"],
                property_data["Price"],
                property_data["ARV"],
                property_data["Gross margin"],
                property_data["Sq.Ft"],
                property_data["Type"],
                property_data["Parking"],
                property_data["Build in"],
                property_data["Lot size"],
                property_data["Beds"],
                property_data["Baths"],
                property_data["Half Bath"],
            ]
        )

    except Exception as e:
        print(f"Could not extract data: {e}")


def init_driver():
    """Set up the Chrome WebDriver with options."""
    chrome_options = Options()
    # Uncomment the line below if you want the browser to run in headless mode
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # Wait for elements to load before interacting
    return driver


def init_excel():
    """Initialize an Excel workbook and worksheet."""
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Property Data"
    # Add headers to the sheet
    sheet.append(
        [
            "Property Address",
            "Price",
            "ARV",
            "Gross Margin",
            "Sq.Footage",
            "Type",
            "Parking",
            "Built in",
            "Lot size",
            "Beds",
            "Baths",
            "Half Bath",
        ]
    )
    return wb, sheet


def main():
    """Main function to log into InvestorLift and navigate multiple pages."""
    email = "@gmail.com"  # Your email address
    password = "@123"  # Your password
    driver = init_driver()
    wb, sheet = init_excel()

    try:
        # Login to InvestorLift
        if not login_to_investorlift(driver, email, password):
            print("Login failed. Exiting program.")
            return

        # Navigating multiple times to different pages
        links_to_visit = [
            "https://investorlift.com/deal/218198",
            "https://investorlift.com/deal/218199",
            "https://investorlift.com/deal/218118",
        ]

        for link in links_to_visit:
            driver.get(link)  # Navigate to each page
            scrape_property_data(driver, sheet)
            time.sleep(10)  # Wait before visiting the next link

        # Save the data to an Excel file
        wb.save("Property_Data.xlsx")
        print("Data saved to 'Property_Data.xlsx'.")

        print("Automation completed. The browser will remain open.")
        print("You can manually close the browser when done.")

        # Keep the browser open
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure that the driver quits even if there was an error
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()
