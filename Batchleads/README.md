# BatchLeads Scraper Bot

This project is an automated **BatchLeads.com** scraper that takes an **Excel sheet** as input, extracts property addresses, searches them on **BatchLeads**, and retrieves detailed property and mortgage data.

## Features

✅ **Automated Address Search**: Extracts addresses from an input Excel file and searches them on **BatchLeads**.  
✅ **Multi-Account Processing**: Uses **5 different accounts** to handle multiple Excel files in parallel.  
✅ **Property Data Extraction**: Scrapes property owner details, mortgage data, and loan information.  
✅ **Streamlit Web Interface**: Provides a user-friendly UI for file upload and result downloads.  
✅ **Saves Data in Excel**: Outputs results in formatted `.xlsx` files.  

---

## 🔧 Installation

Make sure you have **Python 3.x** installed. Then, install dependencies:

```sh
pip install -r requirements.txt
```

---

## 📌 Usage

### 1️⃣ Upload Excel Files
- Prepare **5 Excel files**, each containing an **Address** column.  
- Upload them via the **Streamlit UI**.  

### 2️⃣ Start Scraping
Run the scraper using:

```sh
python batchleads_scraper.py
```

- The scraper will log into BatchLeads using **5 different accounts**.
- It will search for each address and extract property details.  
- **Each file will be processed with a separate account** to avoid login restrictions.  

### 3️⃣ Download Results
- Once processing is complete, automatically download the updated Excel files with additional details.  

---

## 📁 Output Files

- `output_1.xlsx`, `output_2.xlsx`, ..., `output_5.xlsx`:  
  Each file contains **extracted property details** from BatchLeads.  

### Extracted Data Includes:
- **Owner Name**
- **Open Mortgages**
- **Total Mortgage Balance**
- **Recording Date**
- **Sale Amount**
- **Loan Details** (Loan Type, Amount, Lender Name, Due Date, etc.)

---

## ⚙️ Configuration

### Ensure Chrome WebDriver is Installed  
- The script uses **Selenium** and requires **Chrome WebDriver**.  
- Download the correct WebDriver version from [here](https://chromedriver.chromium.org/downloads).  
- Place it in the script directory or set it in system PATH.  

---

## 🛠 Dependencies

Install required Python libraries with:

```sh
pip install selenium pandas openpyxl streamlit
```

Or use:

```sh
pip install -r requirements.txt
```

---

## 📝 Notes

- The scraper **processes 5 Excel files simultaneously** using **5 different accounts**.  
- If an **address is not found**, the script marks it as `"N/A"` in the output file.  
- Ensure **BatchLeads login credentials** are **correct and active** before running the scraper.  
- The extracted loan details might vary depending on property data availability.  

---

🚀 **Automate your BatchLeads searches with this scraper!**  
🔗 Modify, extend, or integrate as needed!  
