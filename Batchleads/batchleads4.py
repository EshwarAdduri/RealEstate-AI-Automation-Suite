import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from concurrent.futures import ThreadPoolExecutor
import os

# Account credentials
account_details = [
    ("@gmail.com", "jhgGF76^%"),
    ("@gmail.com", "JHhgfh^&$654"),
    ("@gmail.com", r"jhgGHF^%%$456"),
    ("@gmail.com", "jhgfhj&^%HJF765"),
    ("@gmail.com", "JHJjj&^%$&654"),
]


# Initialize web driver
def init_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver


# Login to BatchLeads
def login_to_batchleads(driver, email, password):
    driver.get("https://app.batchleads.io/public/login")
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@formcontrolname='email']")
        )
    )
    email_input.clear()
    email_input.send_keys(email)
    password_input = driver.find_element(
        By.XPATH, "//input[@formcontrolname='password']"
    )
    password_input.clear()
    password_input.send_keys(password)
    continue_button = driver.find_element(
        By.XPATH, "//button[contains(@class, 'submit') and text()='Continue']"
    )
    continue_button.click()
    WebDriverWait(driver, 10).until(EC.url_contains("app.batchleads.io/app"))
    handle_login_popup(driver)


# Handle "Use here" popup
def handle_login_popup(driver):
    try:
        use_here_button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "logout_there"))
        )
        use_here_button.click()
    except TimeoutException:
        pass


# Search for an address
def search_address(driver, address):
    driver.get("https://app.batchleads.io/app/property-search-new")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "placeInput"))
    )
    try:
        clear_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'clear-btn')]")
            )
        )
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", clear_button)
            driver.execute_script("arguments[0].click();", clear_button)
        except ElementClickInterceptedException:
            time.sleep(1)
            driver.execute_script("arguments[0].click();", clear_button)
    except TimeoutException:
        pass

    search_input = driver.find_element(By.ID, "placeInput")
    search_input.clear()
    search_input.send_keys(address)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)


# Check if the address is not found
def check_address_not_found(driver):
    try:
        WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(text(), 'No results matching your criteria.')]",
                )
            )
        )
        return True
    except TimeoutException:
        return False


# Extract owner data
def extract_owner_data(driver):
    try:
        owner_name = (
            WebDriverWait(driver, 10)
            .until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(text(), 'Owner Name')]/following-sibling::div",
                    )
                )
            )
            .text
        )
    except (TimeoutException, NoSuchElementException):
        owner_name = "N/A"
    return owner_name


# Extract mortgage data
def extract_mortgage_data(driver):
    data = {}
    fields = [
        "Open Mortgages",
        "Total Mortgage Balance",
        "Recording Date",
        "Sale Amount",
    ]
    for field in fields:
        try:
            data[field] = driver.find_element(
                By.XPATH, f"//*[contains(text(), '{field}')]/following-sibling::div"
            ).text
        except NoSuchElementException:
            data[field] = "N/A"
    return data


# Extract loan data
def extract_loan_data(driver):
    loan_data = []
    try:
        loan_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "pills-mortgage-transaction-tab"))
        )
        driver.execute_script("arguments[0].click();", loan_button)
        first_row = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//app-current-loan-table//tbody[@class='visible_data']/tr[1]",
                )
            )
        )
        cols = first_row.find_elements(By.TAG_NAME, "td")
        loan_data = [col.text.strip() for col in cols[1:] if col.text.strip()]
    except (TimeoutException, NoSuchElementException):
        loan_data = ["N/A"] * 8
    loan_data += ["N/A"] * (8 - len(loan_data))
    return loan_data


# Process an Excel file
def process_excel(input_file, account):
    email, password = account
    df = pd.read_excel(input_file)
    new_columns = [
        "Owner Name",
        "Open Mortgages",
        "Total Mortgage Balance",
        "Recording Date",
        "Sale Amount",
        "Recording Date_curent_loan",
        "Loan Type",
        "Loan Amount",
        "Lender Name",
        "Loan Due Date",
        "Est. Loan Payment",
        "Est. Principle",
        "Est. Interest",
    ]
    for col in new_columns:
        if col not in df.columns:
            df[col] = ""
    driver = init_driver()
    try:
        login_to_batchleads(driver, email, password)
        for i, row in df.iterrows():
            address = row["Address"]
            search_address(driver, address)
            if check_address_not_found(driver):
                for col in new_columns:
                    df.at[i, col] = "N/A"
                continue
            df.at[i, "Owner Name"] = extract_owner_data(driver)
            mortgage_data = extract_mortgage_data(driver)
            loan_data = extract_loan_data(driver)
            df.at[i, "Open Mortgages"] = mortgage_data["Open Mortgages"]
            df.at[i, "Total Mortgage Balance"] = mortgage_data["Total Mortgage Balance"]
            df.at[i, "Recording Date"] = mortgage_data["Recording Date"]
            df.at[i, "Sale Amount"] = mortgage_data["Sale Amount"]
            df.at[i, "Recording Date_curent_loan"] = loan_data[0]
            df.at[i, "Loan Type"] = loan_data[1]
            df.at[i, "Loan Amount"] = loan_data[2]
            df.at[i, "Lender Name"] = loan_data[3]
            df.at[i, "Loan Due Date"] = loan_data[4]
            df.at[i, "Est. Loan Payment"] = loan_data[5]
            df.at[i, "Est. Principle"] = loan_data[6]
            df.at[i, "Est. Interest"] = loan_data[7]
    finally:
        driver.quit()
    return df


# Streamlit app
def main():
    st.title("BatchLeads Scraper for Multiple Accounts")
    st.markdown(
        "Upload **5 Excel files**, each processed using a different BatchLeads account."
    )

    uploaded_files = st.file_uploader(
        "Upload Excel Files", type="xlsx", accept_multiple_files=True
    )
    if len(uploaded_files) != 5:
        st.warning("Please upload exactly 5 Excel files.")
        return

    if st.button("Start Scraping"):
        temp_files = []
        for file in uploaded_files:
            temp_path = f"temp_{file.name}"
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())
            temp_files.append(temp_path)

        output_files = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(process_excel, temp_files, account_details)
            output_files.extend(results)

        st.success("Scraping completed!")
        for i, output_df in enumerate(output_files):
            output_path = f"output_{i + 1}.xlsx"
            output_df.to_excel(output_path, index=False)
            st.download_button(
                label=f"Download {os.path.basename(output_path)}",
                data=open(output_path, "rb").read(),
                file_name=os.path.basename(output_path),
            )


if __name__ == "__main__":
    main()
