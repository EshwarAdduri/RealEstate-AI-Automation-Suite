import os
from openai import OpenAI
import openai

# OpenAI Client Initialization
client = OpenAI(="Your API KEY")


# Function to extract information from notice text
def extract_information(notice: str):
    prompt = f"""
    Extract the following information from the notice Text. 
    It is IMPORTANT TO NOTE THE KEY information to be extracted from the notice are Address, City, State, Zip Code, County, Decedent Name, Sale Date, and Phone Number.

    Follow these instructions to prioritize extraction:

    IMPORTANT TO REMEMBER THESE POINTS WHILE EXTRACTING INFORMATION:
    - Decedent Address: You have to extract the address of the decedent or deceased individual's property.And, In case, If it is not available, keep it empty.
    "DO NOT Extract Court address, Attorney address, or any other address mentioned in the notice here."
    - City: Extract the city corresponding to the selected address.
    - State: Extract the state corresponding to the selected address (Decedent Address or Personal Representative Address).
    - Zip Code: Extract the zip code corresponding to the selected address (Decedent Address or Personal Representative Address). If it's not present, find it using the address, city, and state.
    - County: Extract the county if mentioned; otherwise, find it using the address (Decedent Address or Personal Representative Address).
    - Decedent Name: Extract the full name of the deceased individual.
    - Sale Date: Extract the sale or publication date if available; otherwise, leave it blank.(Note : Example format : Month/Day/Year)
    - Personal Representative Phone Number: Extract the phone number associated with the representative if present. If there are multiple personal representatives, are available in Notice then take count of all phone numbers related to them. But, If multiple phone numbers are other than personal representaive, choose only numbers related to the personal representative. Ensure the phone number contains 10 digits; if not present, return "N/A".(Note format for phone number : ="+1 "&LEFT(,3)&" "&MID(,4,3)&" "&RIGHT(,4))
    - Personal Representative Name: Extract the full name of the personal representative available in the notice. Also, if multiple personal representatives are available, extract all of them.
    - Personal Representative Address: Extract the address of the personal representative available in the notice. Also, if multiple personal representatives are available, extract all of them.

    Return the extracted data in JSON format without quotes around values. Use the following keys:
    - Decedent Address
    - City
    - State
    - Zip Code
    - County
    - Decedent Name
    - Sale Date
    - Personal Representative Phone Number
    - Personal Representative Name
    - Personal Representative Address

    
    If the required field 'Decedent Address' and  Personal Representative Address is missing, skip this notice entirely. and one more thing dont add extra unwanted columns okay i only want above mentioned columns thaats it
    {notice}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )

        content = response.choices[0].message.content.strip()

        if content.lower() == "skip":
            return None  # Indicate to skip this notice

        # Split content by lines to process key-value pairs
        lines = content.split("\n")
        extracted_info = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                # Strip quotes and whitespace from key and value
                extracted_info[key.strip()] = (
                    value.strip().replace('"', "").replace("'", "")
                )

        return extracted_info

    except Exception as e:
        print(f"Error: {e}")
        return {
            "Decedent Address": "N/A",
            "City": "N/A",
            "State": "N/A",
            "Zip Code": "N/A",
            "County": "N/A",
            "Decedent Name": "N/A",
            "Sale Date": "N/A",
            "Personal Representative Phone Number": "N/A",
            "Personal Representative Name": "N/A",
            "Personal Representative Address": "N/A",
        }


# Function to extract information from notice text
def extract_information2(notice: str):
    prompt = f"""
    Extract the following information from the foreclosure notice. If the required field 'Address' is missing, skip this notice entirely and give any response to that notice just skip that notice. 
    If the notice does not contain any useful information, also skip it. Return "N/A" for any field that is not found but has other fields present.

    Follow these instructions to prioritize extraction:

    - Address: Prefer the full property address if mentioned; if not, extract the common name if available.
    - City: Extract the city corresponding to the selected address.
    - State: Extract the state corresponding to the selected address.
    - Zip Code: Extract the zip code corresponding to the selected address. If it's not present, find it using the address, city, and state from map or using nominatim.openstreetmap.org for zipcode finding from address.
    - County: Extract the county if mentioned; otherwise, find it using the address.
    - Sale Date: Extract the sale date if available; otherwise, leave it blank.(Note : Example format : Month/Day/Year)
    - Mode Of Sale: Extract the mode of sale (ex: Foreclosure, TRUSTEE'S SALE, COMMISSIONER'S SALE, Sheriff Sale.... etc)
    - Phone Number: Only Extract the phone number associated with owner if present other wise just leave as empty and dont add any othr phone numbers here.(format for phone nuumber : ="+1 "&LEFT(,3)&" "&MID(,4,3)&" "&RIGHT(,4))
    - Other Phone Number: Only Extract the phone numbers related to the trustee here.If not present leave it empty.(format for phone nuumber : ="+1 "&LEFT(,3)&" "&MID(,4,3)&" "&RIGHT(,4))
    - Property First Name: Extract the first name of the individual related to the property (Note: Just add only property individual First name dont add other names if not present then leave it empty).
    - Property Last Name: Extract the last name of the individual related to the property (Note: Just add only property individual Last name dont add other names if not present then leave it empty).
    - First Name: Only Extract the first name of the trustee or add the individual name according to that Other phone number column, (ex: add trustee names or other which are important names)
    - Last Name: Only Extract the last name of the trustee or add the individual name according to that Other phone number column, (ex: add trustee names or other which are important names)
    Return the extracted data in JSON format without quotes around values. Use the following keys:and i only want these below columns okay dont  add extra columns.
    - Address
    - City
    - State
    - Zip Code
    - County
    - Sale Date
    - Mode Of Sale
    - Phone Number
    - Other Phone Number
    - Property First Name
    - Property Last Name
    - First Name
    - Last Name
    If the notice is missing essential information like Address, return "skip" instead of the JSON. Ensure the phone number contains 10 digits; if not present, return "N/A", and if the zipcode is missing, find it using the address, city, and state from nominatim.openstreetmap.org for zipcode finding from address..

    Foreclosure Notice:
    {notice}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )

        content = response.choices[0].message.content.strip()

        if content.lower() == "skip":
            return None  # Indicate to skip this notice

        # Split content by lines to process key-value pairs
        lines = content.split("\n")
        extracted_info = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                # Strip quotes and whitespace from key and value
                extracted_info[key.strip()] = (
                    value.strip().replace('"', "").replace("'", "")
                )

        return extracted_info

    except Exception as e:
        print(f"Error: {e}")
        return {
            "Address": "N/A",
            "City": "N/A",
            "State": "N/A",
            "Zip Code": "N/A",
            "County": "N/A",
            "Sale Date": "N/A",
            "Phone Number": "N/A",
            "Property First Name": "N/A",
            "Property Last Name": "N/A",
        }


def process_addresses_with_llm(addresses):
    results = []

    for address in addresses:
        prompt = f"""
        Extract the following information from the given address:
        - Full Address: {address}
        Return the following details in JSON format:
        - Address
        - City
        - State
        - Zip Code
        - County
        If the address is unclear, return "skip".
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )

            content = response.choices[0].message.content.strip()

            if content.lower() == "skip":
                continue

            result = {"Original Address": address}
            lines = content.split("\n")
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    result[key.strip()] = (
                        value.strip().replace('"', "").replace("'", "")
                    )
            results.append(result)

        except Exception as e:
            print(f"Error processing address {address}: {e}")

    return results
