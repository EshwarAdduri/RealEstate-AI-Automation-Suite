import streamlit as st
import pandas as pd
from io import BytesIO
from legalnews_scraper import scrape_foreclosure_data, scrape_probate_data
from salesweb_scraper import scrape_addresses_from_county
from TheMecklenburgTimes_scraper import scrape_mecktimes_data
from public import (
    scrape_data,
    process_notices_with_llm,
    save_to_excel,
    public_notice_links,
)  # Import from public.py
from llm import process_addresses_with_llm
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
import time
from selenium.webdriver.common.by import By
import os
import logging
from selenium.webdriver.common.action_chains import ActionChains

# Configure logging
logging.basicConfig(
    filename="app.log",  # Log file name
    filemode="a",  # Append mode
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Log level
)


geocode_cache = {}


def geocode_address(address, retries=2):
    if address in geocode_cache:
        return geocode_cache[address]  # Return cached result

    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "addressdetails": 1, "limit": 1}
    headers = {"User-Agent": "EshwarAdduri/1.0 (http://localhost:8501/)"}

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data:
                print(f"Geocoding successful for address: {address}")
                geocode_cache[address] = data[0]["address"]  # Cache the result
                return data[0]["address"]
            else:
                print(f"No geocoding results for address: {address}")
        except requests.RequestException as e:
            print(f"Geocoding request failed for address: {address} with error: {e}")
        except ValueError:
            print(f"Failed to parse JSON response for address: {address}")

        # Wait before retrying
        time.sleep(3)

    return None


def split_address(full_address):
    # Remove the trailing "Details" part if present
    if "Details" in full_address:
        full_address = full_address.split("Details")[0].strip()

    # Split the address parts intelligently
    parts = full_address.split(",")

    # Ensure there are enough parts to split
    if len(parts) >= 3:
        street = parts[0].strip()
        city_state_zip = parts[-1].strip()
        city_state_zip_parts = city_state_zip.rsplit(" ", 2)

        if len(city_state_zip_parts) == 3:
            city = city_state_zip_parts[0]
            state = city_state_zip_parts[1]
            zipcode = city_state_zip_parts[2]
            county = parts[1].strip() if len(parts) > 2 else ""
            return street, city, state, zipcode, county
        else:
            logging.warning(f"Unexpected address format: {full_address}")
            return full_address, "", "", "", ""
    else:
        logging.warning(f"Failed to split address: {full_address}")
        return full_address, "", "", "", ""


def main():
    logging.info("Application started.")
    st.title("Foreclosure and Probate Data Scraper")

    source = st.selectbox(
        "Select Source", options=["LegalNews", "SalesWeb", "Public Notices"]
    )

    if source == "Public Notices":
        selected_site = st.selectbox(
            "Select a Public Notice Site",
            options=["All Public Notices"] + list(public_notice_links.keys()),
        )

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

        if st.button("Scrape Public Notices Data"):
            logging.info(f"Scraping public notices from {selected_site}...")
            if start_date and end_date:
                with st.spinner("Scraping data... This may take a few minutes."):
                    if selected_site == "All Public Notices":
                        all_notices = []
                        for site_name, site_url in public_notice_links.items():
                            st.write(f"Scraping {site_name}...")
                            notices = scrape_data(site_url, start_date, end_date)
                            all_notices.extend(notices)
                        notices = all_notices
                    else:
                        notices = scrape_data(
                            public_notice_links[selected_site], start_date, end_date
                        )

                st.write("Extracting data from notices...")
                processed_notices = process_notices_with_llm(notices)

                if processed_notices:
                    excel_filename = save_to_excel(processed_notices)
                    st.write(f"Data saved to {excel_filename}")
                    with open(excel_filename, "rb") as file:
                        st.download_button(
                            label="Download Excel File",
                            data=file,
                            file_name=excel_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                else:
                    st.warning("No data extracted from notices.")
            else:
                st.write("Please select both a start date and an end date.")
    elif source == "LegalNews":
        county = st.selectbox("Select County", options=["All Counties"])

        notice_type = st.selectbox(
            "Select Notice Type", options=["Foreclosure", "Probate"]
        )
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

        if st.button("Scrape Legal News Data"):
            if start_date and end_date:
                with st.spinner("Scraping data... This may take a few minutes."):
                    if notice_type == "Foreclosure":
                        addresses = scrape_foreclosure_data(
                            start_date.strftime("%d-%m-%Y"),
                            end_date.strftime("%d-%m-%Y"),
                            county,
                        )
                    else:
                        data = scrape_probate_data(
                            start_date.strftime("%d-%m-%Y"),
                            end_date.strftime("%d-%m-%Y"),
                        )

                if notice_type == "Foreclosure":
                    st.success(f"Scraped {len(addresses)} addresses.")
                    with st.spinner("Geocoding addresses..."):
                        geocoded_data = []
                        for address in addresses:
                            location_data = geocode_address(address)
                            if location_data:
                                geocoded_data.append(
                                    {
                                        "Address": address,
                                        "State": location_data.get("state", ""),
                                        "Zipcode": location_data.get("postcode", ""),
                                        "County": location_data.get("county", ""),
                                    }
                                )
                            time.sleep(1)
                    if geocoded_data:
                        df = pd.DataFrame(geocoded_data)
                        st.dataframe(df)

                        # Save in the same directory as the Streamlit script
                        current_directory = os.path.dirname(os.path.abspath(__file__))
                        save_path = os.path.join(
                            current_directory, "Foreclosure_addresses.xlsx"
                        )
                        df.to_excel(save_path, index=False)

                        excel_file = BytesIO()
                        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                            df.to_excel(writer, index=False, sheet_name="Addresses")
                        st.download_button(
                            label="Download Excel file",
                            data=excel_file.getvalue(),
                            file_name="Foreclosure_addresses.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    else:
                        st.warning("No data to display or download.")

                else:
                    df = pd.DataFrame(data)
                    st.dataframe(df)

                    # Save in the same directory as the Streamlit script
                    current_directory = os.path.dirname(os.path.abspath(__file__))
                    save_path = os.path.join(
                        current_directory, "Probate_Notice_Descriptions.xlsx"
                    )
                    df.to_excel(save_path, index=False)

                    excel_file = BytesIO()
                    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
                        df.to_excel(writer, sheet_name="Probate Notices", index=False)
                    st.download_button(
                        label="Download data as Excel",
                        data=excel_file.getvalue(),
                        file_name="Probate_Notice_Descriptions.xlsx",
                    )
    elif source == "SalesWeb":
        county_names = []

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://salesweb.civilview.com/")
        county_links = driver.find_elements(
            By.XPATH, "//div[@class='table-responsive']//a"
        )
        for link in county_links:
            county_names.append(link.text)
        driver.quit()

        selected_county = st.selectbox("Select a County", options=county_names)

        if st.button("Scrape and Process Addresses"):
            county_index = county_names.index(selected_county)
            with st.spinner("Scraping addresses..."):
                addresses = scrape_addresses_from_county(county_index)

            st.success(f"Scraped {len(addresses)} addresses.")

            if addresses:
                with st.spinner("Processing addresses..."):
                    processed_data = process_addresses_with_llm(addresses)

                if processed_data:
                    df = pd.DataFrame(processed_data)
                    st.dataframe(df)

                    excel_file = BytesIO()
                    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                        df.to_excel(
                            writer, index=False, sheet_name="Processed Addresses"
                        )

                    st.download_button(
                        label="Download Excel file",
                        data=excel_file.getvalue(),
                        file_name="processed_addresses.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.warning("No valid data processed.")
            else:
                st.warning("No addresses found for the selected county.")

    elif source == "TheMecklenburgTimes":
        if st.button("Scrape Meck Times Data"):
            with st.spinner("Scraping data from Meck Times..."):
                data = scrape_mecktimes_data()
                st.success(f"Scraped {len(data)} records.")

            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)

                excel_file = BytesIO()
                with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="Meck Times Data")

                st.download_button(
                    label="Download Excel file",
                    data=excel_file.getvalue(),
                    file_name="meck_times_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.warning("No data found for the selected time period.")


if __name__ == "__main__":
    main()
