from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
from weasyprint import HTML
from PyPDF2 import PdfMerger
import re

# --- Configuration ---
OUTPUT_DIR = "book_chapters"
FINAL_PDF = "Automate_the_Boring_Stuff_with_Python.pdf"


# --- Helper function to clean filenames ---
def clean_filename(title):
    title = title.replace(" - Automate the Boring Stuff with Python, 2nd Edition", "")
    return re.sub(r'[\\/*?:"<>|]', "", title) + ".pdf"


# --- Setup ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
merger = PdfMerger()
pdf_paths = []

# Create an Options object
chrome_options = Options()

# Add the headless argument
chrome_options.add_argument(
    "--headless=new"
)  # Use "--headless=new" for modern Chrome versions

# Initialize the WebDriver with the headless options
driver = webdriver.Chrome(options=chrome_options)

try:
    # --- STEP 1: Navigate to the homepage and click the link ---
    driver.get("https://automatetheboringstuff.com")
    print("Navigated to the website.")

    free_to_read_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Free to read"))
    )
    free_to_read_link.click()
    print("Clicked on 'Free to read'.")

    # --- STEP 2: Wait for the toc's title to appear ---
    toc_header_locator = (By.XPATH, "//h2[text()='Table of Contents']")
    print("Waiting for the Table of Contents page to load...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(toc_header_locator)
    )
    print("Table of Contents page has loaded successfully!")

    # --- STEP 3: Now that we know the page is ready, find the links ---
    chapter_links_locator = (By.XPATH, "//a[contains(@href, 'chapter')]")
    chapter_elements = driver.find_elements(*chapter_links_locator)

    chapter_urls = [elem.get_attribute('href') for elem in chapter_elements]
    print(f"Found {len(chapter_urls)} chapters to process.")

    # --- STEP 4: Main Scraping Loop ---
    for url in chapter_urls:
        driver.get(str(url))
        chapter_title = driver.title
        print(f"Processing: {chapter_title}")

        try:
            for i in range(0, 2):
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(), 'close')]")
                    )
                )
                close_button.click()
        except TimeoutException:
            print(" - No 'close' button found, using current view.")

        html_content = driver.page_source
        clean_title = clean_filename(chapter_title)
        pdf_path = os.path.join(OUTPUT_DIR, clean_title)

        print(f" - Saving to {pdf_path}")
        HTML(string=html_content, base_url=driver.current_url).write_pdf(pdf_path)
        pdf_paths.append(pdf_path)
        time.sleep(1)

    # --- STEP 5: Merge All PDFs ---
    print("\nAll chapters downloaded. Merging into final PDF...")
    for path in pdf_paths:
        merger.append(path)

    merger.write(FINAL_PDF)
    print(f"✅ Done! Final PDF saved as: {FINAL_PDF}")

    os.remove(OUTPUT_DIR)
    print(f"... and cleaned up {OUTPUT_DIR} 🧹🗑️")

except TimeoutException as e:
    # This will catch the error and give us much better debugging info
    print("\n--- A TIMEOUT ERROR OCCURRED ---")
    print("Selenium could not find an element within the time limit.")
    print(
        "I'm saving a screenshot as 'debug_screenshot.png' and the page HTML as 'debug_page.html'."
    )
    print("This will show us what the browser was seeing at the time of the error.")

    # Save a screenshot and the page source for debugging
    driver.save_screenshot("debug_screenshot.png")
    with open("debug_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

finally:
    # This block always runs, ensuring everything is closed properly
    print("Closing resources.")
    merger.close()
    driver.quit()
