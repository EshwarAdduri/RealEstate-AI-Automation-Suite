import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os
from datetime import datetime
import time


# Set up Firefox options to use Tor
def init_driver():
    options = Options()
    options.headless = False  # Set to True if you don't want to see the browser
    options.binary_location = r"C:\Users\addur\OneDrive\Desktop\Tor Browser\Browser\firefox.exe"  # Update this path

    # Specify the profile directory
    profile_path = r"C:\Users\addur\OneDrive\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profiles.ini"  # Update this path
    options.set_preference("profile", profile_path)

    # Set the path to the Geckodriver executable
    service = Service(
        r"C:\Justin-Pickell-Foreclosure-Data-Coding-Web-Scrapping\geckodriver-v0.35.0-win64\geckodriver.exe"
    )  # Update this path
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def login_to_preforeclosure(driver, email, password):
    try:
        driver.get("https://www.preforeclosure.com/login.html")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.NAME, "key")))

        email_input = driver.find_element(By.NAME, "key")
        email_input.clear()
        email_input.send_keys(email)

        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)

        sign_in_button = driver.find_element(By.ID, "btnLoginUsernamePassword")
        sign_in_button.click()

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.stateHomeList"))
        )
        st.write("Login successful.")
    except Exception as e:
        st.error(f"An error occurred during login: {e}")


def extract_data_from_notice(driver, notice_link):
    try:
        driver.get(notice_link)

        # Extract address
        try:
            address = driver.find_element(By.CSS_SELECTOR, "div.address span").text
            region = driver.find_element(By.CSS_SELECTOR, "div.region span").text
            full_address = f"{address} {region}"
        except:
            full_address = ""

        # Extract price
        try:
            Mortgage_value = driver.find_element(
                By.CSS_SELECTOR, "div.price strong"
            ).text
        except:
            Mortgage_value = ""

        # Extract auction date
        try:
            auction_date_element = driver.find_element(
                By.XPATH,
                "//li[contains(@class, 'details_li_auction_date')]//span[@class='value bold']",
            )
            auction_date = auction_date_element.text.strip()
        except:
            auction_date = ""

        # Extract listing ID
        try:
            listing_id_element = driver.find_element(By.CSS_SELECTOR, "div.listingId")
            listing_id = listing_id_element.text.split(":")[-1].strip()
        except:
            listing_id = ""

        # Extract additional details with if-else checks
        try:
            defendant_name = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_defendant_name span.value.bold"
            ).text.strip()
        except:
            defendant_name = ""

        try:
            trustee_address = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_trustee_address span.value.bold"
            ).text.strip()
        except:
            trustee_address = ""

        try:
            trustee_name = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_trustee_name span.value.bold"
            ).text.strip()
        except:
            trustee_name = ""

        try:
            trustee_city = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_trustee_city span.value.bold"
            ).text.strip()
        except:
            trustee_city = ""

        try:
            trustee_state = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_trustee_state span.value.bold"
            ).text.strip()
        except:
            trustee_state = ""

        try:
            trustee_zip = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_trustee_zip span.value.bold"
            ).text.strip()
        except:
            trustee_zip = ""

        try:
            trustee_phone = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_trustee_phone span.value.bold"
            ).text.strip()
        except:
            trustee_phone = ""

        try:
            trustee_reference_number = driver.find_element(
                By.CSS_SELECTOR,
                "li.details_li_trustee_reference_number span.value.bold",
            ).text.strip()
        except:
            trustee_reference_number = ""

        try:
            mortgage_balance = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_mortgage_balance span.value.bold"
            ).text.strip()
        except:
            mortgage_balance = ""

        try:
            first_mortgage_date = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_1st_mortgage_date span.value.bold"
            ).text.strip()
        except:
            first_mortgage_date = ""

        # Extract listing type
        try:
            # Find all h3 elements within description divs and check their text
            description_divs = driver.find_elements(
                By.CSS_SELECTOR, "div.description h3"
            )
            listing_type = ""
            for h3 in description_divs:
                if h3.text.strip() not in ["Property Description"]:
                    listing_type = h3.text.strip()
                    break
        except:
            listing_type = ""

        # Extract auction information
        try:
            auction_time = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_auction_time span.value.bold"
            ).text.strip()
        except:
            auction_time = ""

        try:
            auction_address = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_auction_address span.value.bold"
            ).text.strip()
        except:
            try:
                auction_address = driver.find_element(
                    By.CSS_SELECTOR, "li.details_li_auction_location span.value.bold"
                ).text.strip()
            except:
                auction_address = ""

        try:
            auction_city = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_auction_city span.value.bold"
            ).text.strip()
        except:
            auction_city = ""

        try:
            auction_zip = driver.find_element(
                By.CSS_SELECTOR, "li.details_li_auction_zip span.value.bold"
            ).text.strip()
        except:
            auction_zip = ""

        return (
            full_address,
            Mortgage_value,
            auction_date,
            listing_id,
            defendant_name,
            trustee_address,
            trustee_name,
            trustee_city,
            trustee_state,
            trustee_zip,
            trustee_phone,
            trustee_reference_number,
            mortgage_balance,
            first_mortgage_date,
            listing_type,
            auction_time,
            auction_address,
            auction_city,
            auction_zip,
        )
    except Exception as e:
        print(f"Error extracting data from {notice_link}: {e}")
        return (
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        )


def save_to_excel(data, filename):
    columns = [
        "Address",
        "Mortgage Value",
        "Auction Date",
        "Listing ID",
        "Defendant Name",
        "Trustee Address",
        "Trustee Name",
        "Trustee City",
        "Trustee State",
        "Trustee Zip",
        "Trustee Phone",
        "Trustee Reference Number",
        "Mortgage Balance",
        "1st Mortgage Date",
        "Listing Type",
        "Auction Time",
        "Auction Address",
        "Auction City",
        "Auction Zip",
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(filename, index=False)


def main():
    st.title("Preforeclosure Scraper")

    accounts = {
        1: ("@.com", "mooth23$"),
        2: ("@yahoo.com ", "Foreclosure123$"),
        3: ("@gmail.com", "Foreclosure123$"),
        4: ("Dispo@.com", "Foreclosure123$"),
        5: ("@gmail.com", "Foreclosure123$"),
        6: ("craig@.com", "Foreclosure123$"),
        7: ("malachi@.com", "Foreclosure123$"),
        8: ("judytifrere@.com", "Foreclosure123$"),
        9: ("connorh@.com", "Foreclosure123$"),
        10: ("investments1@gmail.com", "Jsmooth23$"),
    }

    account_choice = st.selectbox("Select an account", options=list(accounts.keys()))
    uploaded_file = st.file_uploader("Upload a file with notice links", type="txt")

    if st.button("Start Scraping"):
        if uploaded_file is None:
            st.error("Please upload a file.")
            return
        start_time = time.time()
        email, password = accounts[account_choice]

        driver = init_driver()
        login_to_preforeclosure(driver, email, password)

        file_name = uploaded_file.name
        links = [
            line.strip()
            for line in uploaded_file.read().decode("utf-8").splitlines()
            if line.strip()
        ]

        all_data = []

        for link in links:
            st.write(f"Processing link: {link}")
            data = extract_data_from_notice(driver, link)
            if data:
                all_data.append(data)

        output_filename = os.path.splitext(file_name)[0] + ".xlsx"
        save_to_excel(all_data, output_filename)

        driver.quit()
        end_time = time.time()  # End measuring time
        elapsed_time = end_time - start_time

        st.success(f"Scraping completed in {elapsed_time:.2f} seconds.")
        st.info(f"Data saved to file: {output_filename}")


if __name__ == "__main__":
    main()
