import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import openpyxl
import pandas as pd
from llm import extract_information2
import requests
import whisper
import os
import random
import warnings
from selenium.common.exceptions import StaleElementReferenceException
from fake_useragent import UserAgent  # Initialize the fake-useragent library
warnings.filterwarnings("ignore")

# Initialize the Whisper model for audio transcription
model = whisper.load_model("base")

# A helper function to simulate human-like typing
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # Simulate a delay between each keystroke

# Function to simulate human-like mouse movements
def move_mouse_to_element(actions, element):
    actions.move_to_element(element).pause(random.uniform(0.5, 1.5)).perform()

# Function to get absolute path of a file based on current working directory
def get_abs_path(file_name):
    return os.path.join(os.getcwd(), file_name)

def transcribe_audio(url):
    try:
        audio_file_path = get_abs_path('temp_audio.wav')  # Use absolute path for audio file
        response = requests.get(url)

        print(f"Saving audio to: {audio_file_path}")  # Debugging statement for path check

        if response.status_code == 200:
            with open(audio_file_path, 'wb') as f:
                f.write(response.content)

            if not os.path.exists(audio_file_path):
                print("Error: Audio file was not saved correctly.")
                return ""

            file_size = os.path.getsize(audio_file_path)
            if file_size == 0:
                print("Error: Audio file is empty after download.")
                return ""

            print(f"Audio file exists and is readable at: {audio_file_path} with size {file_size} bytes.")  # Debugging confirmation

            result = model.transcribe(audio_file_path)  # Make sure you pass the absolute path here
            return result["text"].strip()
        else:
            print(f"Failed to download audio: Status code {response.status_code}")
            return ""
    except Exception as e:
        print(f"Error during audio transcription: {e}")
        return ""

def check_if_captcha_exists(driver):
    try:
        captcha_frame = driver.find_elements(By.XPATH, "//iframe[contains(@title, 'challenge')]")
        return len(captcha_frame) > 0
    except:
        return False

def click_recaptcha_checkbox(driver, wait, actions):
    try:
        driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']"))
        checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
        move_mouse_to_element(actions, checkbox)
        checkbox.click()
        print("Clicked on the reCAPTCHA checkbox.")
        driver.switch_to.default_content()

        time.sleep(random.uniform(2, 4))  # Give time for verification

        try:
            driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']"))
            is_verified = driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-checked")
            driver.switch_to.default_content()
            print("Checkbox verification completed without further challenge.")
            return True
        except Exception:
            print("Verification status check failed, proceeding with audio challenge.")
            driver.switch_to.default_content()
            return False

    except Exception as e:
        print("Moving to audio challenge due to checkbox interaction error.")
        driver.switch_to.default_content()
        return False

def solve_audio_captcha(driver, wait, actions):
    try:
        max_retries = 3
        retry_count = 0
        audio_source = None

        while retry_count < max_retries and not audio_source:
            try:
                audio_source_element = wait.until(EC.presence_of_element_located((By.ID, "audio-source")))
                audio_source = audio_source_element.get_attribute('src')
            except Exception:
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(2)
                    continue
                else:
                    print("Failed to get audio source after maximum retries")
                    return False

        if not audio_source:
            return False

        transcribed_text = transcribe_audio(audio_source)
        if not transcribed_text:
            return False

        try:
            audio_response = wait.until(EC.presence_of_element_located((By.ID, "audio-response")))
            move_mouse_to_element(actions, audio_response)
            audio_response.clear()
            human_typing(audio_response, transcribed_text)

            verify_button = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-verify-button")))
            move_mouse_to_element(actions, verify_button)
            verify_button.click()

            time.sleep(random.uniform(1, 3))
            driver.switch_to.default_content()

            return click_agree_button(driver, wait)

        except Exception as e:
            print(f"Error during audio CAPTCHA verification: {e}")
            return False

    except Exception as e:
        print(f"Error solving audio CAPTCHA: {e}")
        return False

def request_audio_challenge(driver, wait, actions):
    max_retries = 3
    for i in range(max_retries):
        try:
            driver.switch_to.default_content()
            challenge_frame = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'challenge')]")))
            driver.switch_to.frame(challenge_frame)

            audio_button = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-audio-button")))
            move_mouse_to_element(actions, audio_button)
            audio_button.click()
            print("Successfully switched to audio challenge")
            return True
        except Exception as e:
            print(f"Attempt {i+1} to request audio challenge failed: {str(e)}")
            if i < max_retries - 1:
                try:
                    driver.switch_to.default_content()
                    time.sleep(2)
                except:
                    pass
            else:
                print("Failed to request audio challenge after all retries")
                return False

def click_agree_button(driver, wait):
    max_retries = 3
    for i in range(max_retries):
        try:
            driver.switch_to.default_content()
            agree_button = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_btnViewNotice")))
            agree_button.click()
            print("Successfully clicked 'I Agree, View Notice'")
            return True
        except Exception as e:
            print(f"Attempt {i+1} to click agree button failed: {str(e)}")
            if i < max_retries - 1:
                time.sleep(2)
            else:
                print("Failed to click agree button after all retries")
                return False

# Define the public notice links and their display names
public_notice_links = {
    "Washington Public Notices": "https://www.wapublicnotices.com/",
    "Texas Public Notices": "https://www.texaspublicnotices.com/",
    "Iowa Public Notices": "https://www.iowapublicnotices.com/",
    "Nevada Public Notice": "https://www.nevadapublicnotice.com/",
    "Virginia Public Notice": "https://www.publicnoticevirginia.com/",
    "Minnesota Public Notice": "https://www.mnpublicnotice.com/",
    "Arizona Public Notices": "https://www.arizonapublicnotices.com/",
    "Missouri Public Notices": "https://www.mopublicnotices.com/",
    "Massachusetts Public Notices": "https://www.masspublicnotices.org/",
    "New Jersey Public Notices": "https://www.njpublicnotices.com/",
    "Illinois Public Notice": "https://www.publicnoticeillinois.com/",
    "Tennessee Public Notice": "https://www.tnpublicnotice.com/",
    "Colorado Public Notices": "https://www.publicnoticecolorado.com/",
    "South Dakota Public Notices": "https://www.sdpublicnotices.com/",
    "Georgia Public Notice": "https://www.georgiapublicnotice.com/",
    "South Carolina Public Notices": "https://www.scpublicnotices.com/"
}

def setup_driver():
    chrome_options = Options()
    ua = UserAgent()  # Instantiate UserAgent to generate random user agents
    user_agent = ua.random

    # Set user-agent
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Optionally use headless
    # chrome_options.add_argument("--headless")

    # Initialize the Selenium WebDriver with user-agent rotation
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to scrape data
def scrape_data(selected_url, start, end):
    driver = setup_driver()  # Set up driver with possible user-agent rotation
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(selected_url)
        time.sleep(random.uniform(1, 3))  # Random delay to simulate human-like visit

        keyword_input = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_as1_txtSearch")))
        move_mouse_to_element(actions, keyword_input)
        keyword_input.clear()
        human_typing(keyword_input, "Foreclosure")

        date_range_section = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_as1_divDateRange")))
        move_mouse_to_element(actions, date_range_section)
        date_range_section.click()
        time.sleep(random.uniform(1, 2))

        date_range_radio = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_as1_rbRange")))
        move_mouse_to_element(actions, date_range_radio)
        date_range_radio.click()

        start_date_input = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_as1_txtDateFrom")))
        move_mouse_to_element(actions, start_date_input)
        start_date_input.clear()
        human_typing(start_date_input, start.strftime("%m/%d/%Y"))

        end_date_input = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_as1_txtDateTo")
        move_mouse_to_element(actions, end_date_input)
        end_date_input.clear()
        human_typing(end_date_input, end.strftime("%m/%d/%Y"))

        search_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_as1_btnGo")
        move_mouse_to_element(actions, search_button)
        search_button.click()

        time.sleep(random.uniform(2, 4))

        from selenium.webdriver.support.ui import Select
        try:
            results_per_page_dropdown = wait.until(EC.presence_of_element_located(
                (By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_ddlPerPage")
            ))
            move_mouse_to_element(actions, results_per_page_dropdown)
            select = Select(results_per_page_dropdown)
            select.select_by_value("50")
        except Exception as e:
            print(f"Error page dropdown: {e}")

        time.sleep(random.uniform(2, 4))

        notices_list = []

        def extract_notice_details(index):
            try:
                notice_content = wait.until(EC.presence_of_element_located(
                    (By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_lblContentText")
                )).text
                notices_list.append(f"Notice {index}:\n{notice_content}")
                print(f"Notice {index} content saved to list.")
            except Exception as e:
                print(f"Error extracting notice content: {e}")

        def handle_captcha():
            captcha_detected = False
            try:
                captcha_message = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_pnlReCaptcha")
                if captcha_message.is_displayed():
                    captcha_detected = True
            except:
                captcha_detected = False

            if captcha_detected:
                print("CAPTCHA detected. Attempting to solve...")
                is_verified = click_recaptcha_checkbox(driver, wait, actions)
                if is_verified:
                    try:
                        agree_button = wait.until(EC.element_to_be_clickable(
                            (By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_btnViewNotice")
                        ))
                        move_mouse_to_element(actions, agree_button)
                        agree_button.click()
                        print("Clicked on 'I Agree, View Notice'.")
                        return True
                    except Exception as e:
                        print(f"Error clicking 'I Agree, View Notice': {e}")
                        return False
                else:
                    print("Checkbox not verified, attempting audio challenge...")
                    request_audio_challenge(driver, wait, actions)
                    return solve_audio_captcha(driver, wait, actions)
            return True

        notice_count = 0
        processed_notices = set()
        page_number = 1

        while True:
            try:
                notice_rows = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "tr[style*='background-color']")
                ))

                for index in range(len(notice_rows)):
                    try:
                        notice_row = notice_rows[index]
                        if index not in processed_notices:
                            view_button = notice_row.find_element(By.CSS_SELECTOR, "input[id*='btnView']")
                            move_mouse_to_element(actions, view_button)
                            view_button.click()

                            if not handle_captcha():
                                driver.quit()
                                return

                            extract_notice_details(f"Page {page_number} - Notice {index + 1}")
                            notice_count += 1
                            processed_notices.add(index)

                            back_link = wait.until(EC.element_to_be_clickable(
                                (By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_hlBackFromBodyTop")
                            ))
                            move_mouse_to_element(actions, back_link)
                            back_link.click()
                            time.sleep(random.uniform(3, 6))

                            notice_rows = wait.until(EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "tr[style*='background-color']")
                            ))

                    except StaleElementReferenceException:
                        print(f"Encountered a stale element, refetching notice rows on page {page_number}...")
                        notice_rows = wait.until(EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "tr[style*='background-color']")
                        ))
                        continue

                if len(processed_notices) >= len(notice_rows):
                    next_page_button = wait.until(EC.element_to_be_clickable(
                        (By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_btnNext")
                    ))
                    if next_page_button and next_page_button.is_displayed() and next_page_button.is_enabled():
                        move_mouse_to_element(actions, next_page_button)
                        next_page_button.click()
                        print(f"Moving to page {page_number + 1}...")
                        page_number += 1

                        processed_notices.clear()
                        time.sleep(random.uniform(3, 6))
                        notice_rows = wait.until(EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "tr[style*='background-color']")
                        ))
                    else:
                        print("No more pages available. All notices have been processed.")
                        break

            except Exception as e:
                print(f"An error occurred while processing the notice: {e}")
                break

    except Exception as e:
        print(f"An error occurred during the initial setup: {e}")
    finally:
        driver.quit()
        print("Browser closed.")
    return notices_list

def process_notices_with_llm(notices_list):
    if notices_list is None:
        return []
    processed_data = []
    for notice in notices_list:
        extracted_info = extract_information2(notice)
        if extracted_info and extracted_info != "skip":
            processed_data.append(extracted_info)
    return processed_data

def save_to_excel(data, filename="Processed_Notices.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename