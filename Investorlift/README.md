# InvestorLift Scraper Bot

This project consists of two Python scripts that automate data collection from **InvestorLift**.  
One script (`link_bot.py`) collects property links from the website without login, while the other (`investorlift_bot.py`) logs in, visits the collected links, and scrapes property details.

## Features

### `link_bot.py` (Collect Property Links Without Login)
- Scrapes **public** property links from **InvestorLift** without requiring login.
- Scrolls multiple times to dynamically load and collect new property links.
- Saves collected links in `fetched_links2.txt` to avoid duplicates.
- **No limit on the number of links collected.**

### `investorlift_bot.py` (Scrape Property Details After Login)
- Logs into **InvestorLift** using email and password.
- Visits the collected links (**limited to 50 per account** due to site restrictions).
- Extracts property details, including:
  - **Price, ARV, Gross Margin, Beds, Baths, Sq. Ft, Parking, Lot Size, etc.**
- Saves data to `Property_Data.xlsx` (with links for manual address verification).

## Installation

Ensure you have **Python 3.x** installed. Then, install the required dependencies:

```sh
pip install -r requirements.txt
```

## Usage

### 1️⃣ Collect Property Links (Without Login)
Run `link_bot.py` to fetch property links from InvestorLift:

```sh
python link_bot.py
```

- The script will scroll multiple times and save unique links to `fetched_links2.txt`.

### 2️⃣ Scrape Property Details (Requires Login)
Run `investorlift_bot.py` to log in and scrape data from collected links:

```sh
python investorlift_bot.py
```

- This script will log in, visit up to **50 property links per account**, extract details, and save them in `Property_Data.xlsx`.

## Output Files

- **`fetched_links2.txt`** → Stores collected property links.
- **`Property_Data.xlsx`** → Contains scraped property details with a **link column** (since full addresses require manual verification).

## Configuration

- **Update Login Credentials**  
  Modify `investorlift_bot.py` with your **email and password** before running.

- **Modify Scroll Settings**  
  Change `MAX_SCROLLS` in `link_bot.py` to adjust the number of scrolls.

- **Ensure Chrome WebDriver is Installed**  
  The script requires Chrome WebDriver **compatible with your Chrome version**.

## Dependencies

The required Python libraries are listed in `requirements.txt`.  
To manually install them, use:

```sh
pip install selenium openpyxl
```

## Notes

- `link_bot.py` collects **publicly available** property links from InvestorLift.
- `investorlift_bot.py` is **limited to 50 property views per login session**.
- Collected links are included in `Property_Data.xlsx` for **manual address verification**.

---

✅ **Automated property data collection from InvestorLift**  


