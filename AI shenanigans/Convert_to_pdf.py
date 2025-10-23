import os
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from PyPDF2 import PdfMerger
import time

# === CONFIGURE ===
BASE_URL = "https://automatetheboringstuff.com"  # Replace with actual base URL
TOC_URL = BASE_URL + "/#toc"  # Table of contents page
OUTPUT_DIR = "book_chapters"
FINAL_PDF = "my_book.pdf"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === STEP 1: Get Chapter Links ===
print("Fetching chapter links...")
response = requests.get(TOC_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Adjust this selector based on the actual HTML structure
# Example: if chapters are in <a href="/chapter1">Chapter 1</a>
# <a href="/3e/chapter0.html">Introduction</a>
# <a href="/3e/chapter1.html">Chapter 1 - Python Basics</a>
chapter_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    href_str = str(href)
    if href_str.startswith('/') or href_str.startswith(BASE_URL):
        full_url = href_str if href_str.startswith(BASE_URL) else BASE_URL + href_str
        href_str_lower = str(href).lower()
        if 'chapter' in href_str_lower or 'part' in href_str_lower:  # Customize filter
            chapter_links.append(full_url)

print(f"Found {len(chapter_links)} chapters.")

# === STEP 2: Download & Convert Each Chapter to PDF ===
merger = PdfMerger()

for i, url in enumerate(chapter_links, 1):
    print(f"Processing Chapter {i}: {url}")

    try:
        # Fetch chapter HTML
        chapter_response = requests.get(url)
        chapter_html = chapter_response.text

        # Save as temporary HTML file (optional, for debugging)
        html_path = os.path.join(OUTPUT_DIR, f"chapter_{i:03d}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(chapter_html)

        # Convert HTML to PDF
        pdf_path = os.path.join(OUTPUT_DIR, f"chapter_{i:03d}.pdf")
        HTML(string=chapter_html, base_url=url).write_pdf(pdf_path)

        # Add to merger
        merger.append(pdf_path)

        # Be polite: delay between requests
        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Failed to process {url}: {e}")

# === STEP 3: Merge All PDFs ===
print("Merging all chapters into final PDF...")
merger.write(FINAL_PDF)
merger.close()

print(f"✅ Done! Final PDF saved as: {FINAL_PDF}")
