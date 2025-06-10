# Image Scraper Using Google Image Crawler

This project automates the process of downloading images from Google using the **icrawler** library. It reads keywords from an Excel file and saves images in organized folders based on the keyword names.

---

## 📌 Features
- Reads search keywords from an Excel file.  
- Downloads images from Google using the **icrawler** library.  
- Creates separate folders for each keyword to keep images organized.  
- Avoids duplicate downloads by tracking previously downloaded images.  
- Uses **random user-agents** to minimize blocking by Google.  
- Implements a **retry mechanism** in case of network errors.  

---

## 📂 Project Structure
```
📂 ImageScraper  
│── 📄 scraper.py            # Main script to run the image scraper  
│── 📄 requirements.txt      # List of required dependencies  
│── 📄 README.md            # Project documentation  
│── 📂 images/              # Folder where images are stored  
│── 📄 keywords.xlsx        # Excel file with keywords for searching  
```

---

## 🛠️ Installation & Setup

### 1️⃣ Install Python (if not installed)
Ensure you have Python 3.7 or higher installed. You can download it from:  
🔗 [Python Official Website](https://www.python.org/downloads/)

### 2️⃣ Clone this repository
```sh
git clone <repo>
cd <project directory>
```

### 3️⃣ Install Dependencies
Run the following command to install required Python packages:
```sh
pip install -r requirements.txt
```
Alternatively, you can install the necessary packages manually:
```sh
pip install icrawler pandas openpyxl
```

### 4️⃣ Prepare Keywords Excel File
Create an Excel file (**keywords.xlsx**) with image search terms in **Column A** (first column).

Example:
```
| Keywords   |
|------------|
| Cars       |
| Dogs       |
| Nature     |
```

---

## 🚀 Usage

### Run the Script
Simply execute the script by running:
```sh
python scraper.py
```
The script will:
- Read search terms from **keywords.xlsx**.
- Download **30 images per keyword** (can be adjusted).
- Store images in the **images/** folder inside subfolders named after the keywords.

---

## ⚙️ Customization

### Change the number of images
Update the `num_images` parameter in `download_images()`:
```python
download_images(keyword, num_images=50)
```

### Change the storage path
Modify `save_dir` in the script:
```python
save_dir = "C:\\Users\\YourName\\Downloads\\images"
```

---

## 📝 Notes
- Avoid searching for explicit content, as it might violate Google's terms.
- If Google blocks requests, try using a **VPN** or adjusting the user-agent list in `USER_AGENTS`.
- If the script fails, check the error logs for details.

---

## 📌 Troubleshooting

### 1️⃣ "Quota Exceeded" or "Blocked by Google"
- Reduce the number of concurrent downloads.
- Use different user-agents in `USER_AGENTS`.
- Wait a few hours before retrying.

### 2️⃣ "ModuleNotFoundError"
Run the following command to install missing dependencies:
```sh
pip install icrawler pandas openpyxl
```

### 3️⃣ "PermissionError" (Windows)
Run the script with administrator privileges.

---

