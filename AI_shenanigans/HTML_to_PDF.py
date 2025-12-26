import time
import re
import shutil
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from weasyprint import HTML
from PyPDF2 import PdfMerger

# --- 1. CONFIGURATION (HOT SWAP AREA) ---
# Change these values to scrape a different site
CONFIG = {
    "start_url": "https://automatetheboringstuff.com",
    "output_dir": "temp_chapters",  # Temporary folder for individual PDFs
    "final_filename": "Automate_The_Boring_Stuff_Complete.pdf",
    
    # Selectors (The specific logic for finding things on this site)
    "selectors": {
        "link_to_toc": (By.PARTIAL_LINK_TEXT, "Free to read"), # Step 1 link
        "toc_indicator": (By.XPATH, "//h2[text()='Table of Contents']"), # Wait for this
        "chapter_links": (By.XPATH, "//a[contains(@href, 'chapter')]"), # Find these
        "popups_to_close": (By.XPATH, "//button[contains(text(), 'close')]"), # Click these
    },
    
    # CSS Selectors for elements to DELETE from the HTML before saving
    # (Great for removing ads, navbars, or "Subscribe" headers)
    "elements_to_delete": [
        ".navbar",          # Example: standard bootstrap navbars
        "#ad-container",    # Example: generic ad containers
        "script",           # Remove scripts to prevent print errors
        "style",            # Remove styles if you want raw HTML (optional)
    ]
}

# --- 2. LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BookScraper:
    def __init__(self, config):
        self.conf = config
        self.temp_dir = Path(self.conf["output_dir"])
        self.final_pdf = Path(self.conf["final_filename"])
        self.pdf_paths = []
        
        # Setup Driver
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=opts)

    def clean_filename(self, text):
        """Sanitizes strings to be safe filenames."""
        text = text.replace(" - Automate the Boring Stuff with Python, 2nd Edition", "")
        clean = re.sub(r'[\\/*?:"<>|]', "", text)
        return f"{clean}.pdf"

    def remove_junk_elements(self):
        """Removes unwanted elements from DOM via Javascript."""
        for selector in self.conf["elements_to_delete"]:
            try:
                # Execute JS to remove elements matching the selector
                self.driver.execute_script(
                    f"document.querySelectorAll('{selector}').forEach(el => el.remove());"
                )
            except Exception:
                pass

    def handle_popups(self):
        """Clicks specific popup buttons if they exist."""
        try:
            # Try clicking close buttons up to 2 times
            for _ in range(2):
                btn = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(self.conf["selectors"]["popups_to_close"])
                )
                btn.click()
                time.sleep(0.5)
        except TimeoutException:
            pass # No popup found, move on

    def get_chapter_urls(self):
        """Navigates to TOC and extracts all chapter links."""
        logger.info(f"Navigating to {self.conf['start_url']}")
        self.driver.get(self.conf["start_url"])

        # Click into the book
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.conf["selectors"]["link_to_toc"])
        ).click()

        # Wait for TOC
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.conf["selectors"]["toc_indicator"])
        )

        # Extract Links
        elements = self.driver.find_elements(*self.conf["selectors"]["chapter_links"])
        urls = [e.get_attribute('href') for e in elements]
        logger.info(f"Found {len(urls)} chapters.")
        return urls

    def download_chapters(self, urls):
        """Visits each URL and saves as PDF."""
        # Ensure temp dir exists and is empty
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True)

        for i, url in enumerate(urls, 1):
            logger.info(f"Processing [{i}/{len(urls)}]: {url}")
            self.driver.get(url)
            
            self.handle_popups()
            self.remove_junk_elements()

            # WeasyPrint logic
            html_content = self.driver.page_source
            chapter_title = self.driver.title
            filename = self.clean_filename(chapter_title)
            save_path = self.temp_dir / filename
            
            try:
                HTML(string=html_content, base_url=self.driver.current_url).write_pdf(save_path)
                self.pdf_paths.append(save_path)
            except Exception as e:
                logger.error(f"Failed to render PDF for {url}: {e}")

    def merge_and_cleanup(self):
        """Merges PDFs and deletes temp files."""
        if not self.pdf_paths:
            logger.warning("No PDFs to merge.")
            return

        logger.info("Merging PDFs...")
        merger = PdfMerger()
        
        for path in self.pdf_paths:
            merger.append(str(path))

        merger.write(str(self.final_pdf))
        merger.close()
        logger.info(f"✅ Success! Saved to: {self.final_pdf.absolute()}")

        # Robust Cleanup
        logger.info("Cleaning up temp files...")
        shutil.rmtree(self.temp_dir)

    def run(self):
        try:
            urls = self.get_chapter_urls()
            self.download_chapters(urls)
            self.merge_and_cleanup()
        except Exception as e:
            logger.error(f"Critical Error: {e}")
            self.driver.save_screenshot("error_snapshot.png")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = BookScraper(CONFIG)
    scraper.run()