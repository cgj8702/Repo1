import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- CHANGE THESE THREE ---
TARGET_URL = ""
SAVE_PATH = ""
LINK_TEXT = ""

# 1. Setup Folder
download_dir = os.path.abspath(SAVE_PATH)
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 2. Setup Options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True 
})

driver = webdriver.Chrome(options=chrome_options)

# 3. THE KEY: Enable headless downloads via DevTools
driver.execute_cdp_cmd('Page.setDownloadBehavior', {
    'behavior': 'allow', 
    'downloadPath': download_dir
})

try:
    print(f"Opening: {TARGET_URL}")
    driver.get(TARGET_URL)
    time.sleep(3)

    # 4. Find and Click
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, LINK_TEXT)
    print(f"Found {len(links)} links.")

    # Finds the link that says "Final shooting script" ONLY inside the Big Fish section
    #links = driver.find_elements(By.XPATH, "//a[contains(@href, 'big-fish') and contains(text(), 'Final shooting script')]")
    #print(f"Found {len(links)} link(s).")

    for link in links:
        title = link.text.strip()
        url = link.get_attribute('href')
        print(f"Clicking {url}")

        driver.execute_script("arguments[0].click();", link)
        time.sleep(3) 

    # 5. THE ROBUST WAIT
    print("Waiting for downloads to start...")
    for _ in range(15): # Wait up to 15 seconds for the first file to appear
        if len(os.listdir(download_dir)) > 0:
            break
        time.sleep(1)

    print("Downloading... (Waiting for .crdownload files to vanish)")
    while any(f.endswith(".crdownload") for f in os.listdir(download_dir)):
        time.sleep(1)
        
finally:
    driver.quit()

print(f"Success! Files saved to: {download_dir}")