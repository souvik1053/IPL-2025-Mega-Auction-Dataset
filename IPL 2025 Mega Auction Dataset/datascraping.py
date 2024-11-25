from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import time

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH

# Open the URL
url = "https://www.espncricinfo.com/auction/ipl-2025-auction-1460972/all-players"
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ds-w-full")))

# Simulate scrolling to load all data
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Allow time for new content to load

    # Check if new content was loaded
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # If no new content loaded, stop scrolling
        break
    last_height = new_height

# Get the fully loaded page source
html = driver.page_source
soup = BeautifulSoup(html, "lxml")

# Locate the table and extract data
table = soup.find("table", class_="ds-w-full")
header = table.find_all("th")
titles = [i.text.strip() for i in header]

# Create a DataFrame
df = pd.DataFrame(columns=titles)

# Extract all rows
rows = table.find_all("tr")
for i in rows[1:]:  # Skip the header row
    data = i.find_all("td")
    row = [tr.text.strip() for tr in data]  # Clean the text
    df.loc[len(df)] = row

# Close the WebDriver
driver.quit()

# Display the DataFrame
print(df)

# Save to a CSV file 
df.to_csv("ipl_2025_auction_players.csv", index=False)
