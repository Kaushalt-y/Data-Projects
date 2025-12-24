from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ---------------- SETUP ----------------
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

url = "https://www.myneta.info/LokSabha2024/index.php?action=summary&subAction=serious_crime&sort=criminal&page="   # 🔴 PUT THE EXACT RESULT PAGE URL HERE
driver.get(url)

all_rows = []

# ---------------- SCRAPE FUNCTION ----------------
def scrape_current_page():
    # wait until at least one data row exists
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//table[contains(@class,'w3-table')]/tbody/tr")
        )
    )

    rows = driver.find_elements(
        By.XPATH, "//table[contains(@class,'w3-table')]/tbody/tr"
    )

    print("Rows found on page:", len(rows))

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) < 8:
            continue

        all_rows.append([
            cols[0].text.strip(),                # Sno
            cols[1].text.strip(),                # Candidate
            cols[2].text.strip(),                # Constituency
            cols[3].text.strip(),                # Party
            cols[4].text.strip(),                # Criminal cases
            cols[5].text.strip(),                # Education
            cols[6].text.split("\n")[0].strip(), # Assets
            cols[7].text.split("\n")[0].strip()  # Liabilities
        ])

# ---------------- PAGE 1 ----------------
print("Scraping page 1")
scrape_current_page()

# ---------------- PAGES 2–12 ----------------
for page in range(2, 13):
    print(f"Scraping page {page}")

    page_links = driver.find_elements(By.LINK_TEXT, str(page))
    if not page_links:
        print(f"Page {page} not clickable, skipping")
        continue

    driver.execute_script("arguments[0].click();", page_links[0])
    time.sleep(2)

    scrape_current_page()

driver.quit()

print("Total rows scraped:", len(all_rows))

# ---------------- SAVE TO EXCEL ----------------
df = pd.DataFrame(all_rows, columns=[
    "Sno",
    "Candidate",
    "Constituency",
    "Party",
    "Criminal Cases",
    "Education",
    "Total Assets",
    "Liabilities"
])

df.to_excel(r"C:\Users\thaku\Desktop\myneta_data.xlsx", index=False)

print("✅ Excel saved at: C:\\Users\\thaku\\Desktop\\myneta_data.xlsx")
