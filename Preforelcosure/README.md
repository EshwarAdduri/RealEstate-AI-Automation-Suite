# Preforeclosure Scraper Project

## Overview
This project automates the process of extracting foreclosure and preforeclosure data from [Preforeclosure.com](https://www.preforeclosure.com) using web scraping. The system extracts property notice links without logging in and then scrapes detailed property information using multiple accounts due to daily scraping limits.

---

## Features
- **Extract Links Without Login**: Scrapes notice links from all counties across the USA.
- **Automated Login & Data Extraction**: Logs into the website using multiple accounts to collect property details.
- **Tor Integration for Privacy**: Uses the Tor browser for enhanced anonymity.
- **Pagination Handling**: Scrapes multiple pages efficiently.
- **Dynamic Data Storage**: Saves results in structured Excel files.
- **Account Rotation**: Uses 10 different accounts to bypass the 195-200 daily scraping limit.

---

## Project Structure
```
preforeclosure-scraper/
│── preforeclosure.py   # Extracts property details from each notice link
│── link.py             # Extracts notice links from all states without login
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
```

---

## Installation
### Prerequisites
- **Python 3.8+**
- **Mozilla Firefox & Geckodriver** (for Selenium)
- **Tor Browser** (for privacy)

### Step 1: Clone the Repository
```bash
git clone <repo>
cd <project directory>>
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Selenium & Tor Paths
Update the following paths in **preforeclosure.py** and **link.py**:
- `options.binary_location = "C:\\Path\\To\\Tor\\firefox.exe"`
- `service = Service("C:\\Path\\To\\geckodriver.exe")`

---

## Usage
### 1. Extract Notice Links
Run the following command to collect foreclosure links:
```bash
python link.py
```
- The script will extract all notice links and save them into `.txt` files with a max of **195 links per file**.
- Files are stored in `extracted_links/` directory.

### 2. Extract Property Details
Run the scraper to collect property data:
```bash
python preforeclosure.py
```
- Select an account from the dropdown (Streamlit UI).
- Upload a `.txt` file (one per session, containing 195 links max).
- The script logs in, extracts data, and saves it as an `.xlsx` file.
- Files are stored in `scraped_data/` directory.


## Data Flow
1. **`link.py`** extracts all foreclosure/preforeclosure property notice links (no login required).
2. Links are saved into `.txt` files, each containing **195 links**.
3. **`preforeclosure.py`** logs into the website and extracts details for each property (one `.txt` file per session).
4. Extracted data is saved into `.xlsx` files.

---

## Troubleshooting
### 1. Geckodriver Errors
- Ensure Geckodriver is installed and matches your Firefox version.
- Download the latest Geckodriver from: [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)

### 2. Tor Browser Not Launching
- Verify `firefox.exe` path in `options.binary_location`.
- Open Tor Browser manually and check if it works.

### 3. Streamlit UI Not Displaying
Run manually:
```bash
streamlit run preforeclosure.py
```
-	Select an account from the dropdown menu.
-	Upload a .txt file containing notice links.
-	Click Start Scraping to begin data extraction.
-	The scraped data is saved as an Excel file.


---

## Error Handling & Debugging
- If scraping fails, check for incorrect login credentials.
- Ensure Geckodriver and Firefox/Tor are properly configured.
- Increase WebDriver wait times if elements fail to load.
- If encountering IP bans, consider using a different Tor circuit.
- Implement automated CAPTCHA solving to handle restrictions.


