import os
import logging
import random
import time
import pandas as pd
from icrawler.builtin import GoogleImageCrawler

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# List of rotating user-agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]


def read_keywords_from_excel(file_path):
    """Read keywords from an Excel file and return as a list."""
    try:
        df = pd.read_excel(file_path, usecols=[0])  # Read first column (A)
        keywords = df.iloc[:, 0].dropna().tolist()
        logging.info(f"✅ Loaded {len(keywords)} keywords from '{file_path}'.")
        return keywords
    except Exception as e:
        logging.error(f"⚠️ Error reading Excel file '{file_path}': {e}")
        return []


def download_images(keyword, num_images=30, save_dir=None):
    """Download images using iCrawler with user-agent rotation and improved tracking."""
    if save_dir is None:
        # Default save location: ./downloaded_images/
        save_dir = os.path.join(os.getcwd(), "downloaded_images")

    folder_path = os.path.join(save_dir, keyword.replace(" ", "_"))
    os.makedirs(folder_path, exist_ok=True)

    # Track previously downloaded images
    completed_file = os.path.join(folder_path, "completed.txt")
    completed_images = set()

    if os.path.exists(completed_file):
        with open(completed_file, "r") as f:
            completed_images = set(f.read().splitlines())

    existing_count = len(os.listdir(folder_path)) - (
        1 if os.path.exists(completed_file) else 0
    )
    remaining_images = num_images - existing_count

    if remaining_images <= 0:
        logging.info(
            f"✅ All {num_images} images already downloaded for '{keyword}'. Skipping..."
        )
        return

    # Set up the crawler
    google_crawler = GoogleImageCrawler(
        parser_threads=2, downloader_threads=4, storage={"root_dir": folder_path}
    )

    # Set random user-agent
    google_crawler.session.headers.update({"User-Agent": random.choice(USER_AGENTS)})

    # Retry mechanism
    for attempt in range(3):
        try:
            logging.info(f"🔍 Searching for images: {keyword} (Attempt {attempt + 1})")
            google_crawler.crawl(
                keyword=keyword,
                max_num=remaining_images,
                min_size=(500, 500),
                file_idx_offset="auto",
            )
            break
        except Exception as e:
            logging.error(f"⚠️ Error fetching images for '{keyword}': {e}")
            time.sleep(5)

    # Save new downloads to completed.txt
    new_files = set(os.listdir(folder_path)) - completed_images - {"completed.txt"}
    with open(completed_file, "a") as f:
        for file in new_files:
            f.write(file + "\n")

    logging.info(
        f"🎉 Downloaded {len(new_files)} new images for '{keyword}' in '{folder_path}'."
    )


if __name__ == "__main__":
    # Path to your keyword Excel file
    excel_file = "keywords.xlsx"  # Change if needed

    # Read keywords
    keywords = read_keywords_from_excel(excel_file)

    if keywords:
        for keyword in keywords:
            download_images(keyword, num_images=30)
    else:
        logging.error("⚠️ No keywords found. Please check your Excel file.")
