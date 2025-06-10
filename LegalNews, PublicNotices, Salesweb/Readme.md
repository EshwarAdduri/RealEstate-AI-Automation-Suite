# Foreclosure & Probate Data Collection  

## Project Overview  
This project automates the daily collection of foreclosure and probate data from various websites. The data is processed and saved into an organized Excel file for further analysis. The system is designed for efficiency, accuracy, and scalability, using web scraping, machine learning, and data validation techniques.  

---

## Features  
- **Web Scraping**: Automated extraction of foreclosure and probate notices from multiple websites.  
- **User-Friendly Interface**: Streamlit-based web app for easy data collection.  
- **Date-Based Filtering**: Select custom date ranges for targeted scraping.  
- **Machine Learning (LLM-Based Extraction)**: Ensures accuracy and relevance in extracted data.  
- **Excel Integration**: Saves collected data in an Excel file for analysis.  
- **Geocoding & Data Validation**: Adds location details (state, zip, county) and prevents duplicate entries.  

---

## Setup Instructions  

### 1. Clone the Repository  
```sh  
git clone <repository-url>  
```

### 2. Navigate to the Project Directory  
```sh  
cd Foreclosure-Data-Collection  
```

### 3. Install Dependencies  
Ensure you have Python installed, then run:  
```sh  
pip install -r requirements.txt  
```

---

## Usage Instructions  

### 1. Run the Streamlit Application  
Launch the web interface using:  
```sh  
streamlit run app.py  
```
This will open a browser with an interactive UI.  

### 2. Select Data Source  
Use the dropdown menu to choose one of the following sources:  
- **Public Notices** (32 websites)  
- **Legal News** (Foreclosure & probate notices)  
- **Sales Web** (Foreclosure data)   

### 3. Set Date Range  
Select the start and end dates using the date picker to filter records.  

### 4. Start Scraping  
Click **"Scrape Data"** to begin data collection. Progress updates will be displayed.  

### 5. Data Processing  
- The application uses **LLM-based extraction (llm.py)** to refine and extract relevant information.  
- Different scripts handle different data sources:  
  - `legalnews_scraper.py` → Scrapes Legal News data  
  - `salesweb_scraper.py` → Extracts foreclosure addresses from Sales Web  
  - `publicnotices_scraper.py` → Gathers data from 32 Public Notices websites  

### 6. Download Processed Data  
Once scraping is complete, an **Excel file** is generated:  
- Download directly from the interface

---

## Daily Data Collection Workflow  
1. Start the **Streamlit app**  
2. Select **website & date range**  
3. Scrape, process, and download the data  

---

## Additional Features  
- **Geocoding**: Enriches data with state, zip code, and county information.  
- **Data Validation**: Ensures quality by filtering duplicates and correcting addresses.  
- **Session Management**: Mimics real-user behavior with cookies for uninterrupted scraping.  

---

## Project Structure  
```
├── app.py                          # Streamlit application  
├── llm.py                           # LLM-based data processing  
├── legalnews_scraper.py  
├── salesweb_scraper.py  
├── public.py 
├── requirements.txt                 # List of dependencies  
├── README.md                        # Project documentation  
```

---

## Contact Information  
For further queries or issues, please contact:  
  
**Project Lead**: Eshwar Adduri  
📧 **Email**: addurieshwar6@gmail.com  
🔗 **GitHub**: [Repository Link](https://github.com/AjayBidyarthy/Justin-Pickell-Foreclosure-Data-Coding-Web-Scrapping/tree/main)  

---

## Conclusion  
This project provides a scalable and efficient solution for collecting foreclosure and probate data. With its integration of automated web scraping, machine learning, and data validation, the process is streamlined for daily use.  

