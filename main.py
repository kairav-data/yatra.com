from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()

# Initialize the WebDriver with the path to ChromeDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open the webpage
driver.get('https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=DEL&originCountry=IN&destination=BOM&destinationCountry=IN&flight_depart_date=12%2F06%2F2024&ADT=1&CHD=0&INF=0&class=Economy&source=fresco-home&unqvaldesktop=1378626079860')

# Wait for the page to load
time.sleep(5)

# Extract the data
flights = driver.find_elements(By.XPATH, "//div/span[@class='i-b text ellipsis']")
prices = driver.find_elements(By.XPATH, "//div/div[@class='i-b tipsy fare-summary-tooltip fs-18']")

# Collect data into lists
flight_names = [flight.text for flight in flights]
flight_price = [price.text for price in prices]

# Create a DataFrame
data = {'Flight': flight_names, 'Price': flight_price}
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('flight_price.csv', index=False)

# Close the driver
driver.quit()
