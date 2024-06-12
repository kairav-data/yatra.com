from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_flight_data(origin_city, destination_city, departure_date):
    try:
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()

        # Initialize the WebDriver with the path to ChromeDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        # Open the webpage
        driver.get('https://www.yatra.com/')

        # Wait for the page to load
        time.sleep(5)

        # Find and click the origin city input field by ID
        flight_origin = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "BE_flight_origin_city"))
        )
        flight_origin.click()

        # Wait for the input field to be present and then type text into it
        input_field_FO = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='BE_flight_origin_city']"))
        )
        input_field_FO.send_keys(origin_city)
        input_field_FO.send_keys(Keys.ENTER)

        # Find and click the arrival city input field by ID
        flight_arrival = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "BE_flight_arrival_city"))
        )
        flight_arrival.click()

        # Wait for the input field to be present and then type text into it
        input_field_FA = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='BE_flight_arrival_city']"))
        )
        input_field_FA.send_keys(destination_city)
        input_field_FA.send_keys(Keys.ENTER)

        # Wait for the departure date picker to be clickable and then click it
        dep_date_picker = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "BE_flight_origin_date"))
        )
        dep_date_picker.click()

        # Select the desired departure date
        dep_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[@data-date='{departure_date}']"))
        )
        dep_date.click()

        # Click on the submit button
        sub_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "BE_flight_flsearch_btn"))
        )
        sub_button.click()

        time.sleep(10)


        # Scrolling down to the bottom of the page
        while True:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for some time to let new content load
            time.sleep(2)
            # Capture current scroll position
            current_scroll_position = driver.execute_script("return window.scrollY;")
            # Scroll again
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait a bit for the scroll to take effect
            time.sleep(2)
            # Check if scroll position changed
            new_scroll_position = driver.execute_script("return window.scrollY;")
            if new_scroll_position == current_scroll_position:
                # If scroll position didn't change, it means we reached the bottom of the page
                break

        # Wait for some time to let new content load
        driver.implicitly_wait(5)

        # Extract the data
        flights = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='flightItem border-shadow pr']"))
        )

        flight_names = []
        flight_depart_time = []
        flight_arrival_time = []
        flight_dur_time = []
        flight_price=[]

        for flight in flights:
            try:
                name = flight.find_element(By.XPATH, ".//div[@class='fs-14 airline-name no-pad col-8']").text
                depart_time = flight.find_element(By.XPATH, ".//div[@class='depart-details']/p[@class='fs-20 bold']").text
                arrival_time = flight.find_element(By.XPATH, ".//div[@class='arrival-details text-right']/p[@class='fs-20 bold']").text
                dur_time = flight.find_element(By.XPATH, ".//div[@class='stops-details font-lightgrey']/p[@class='fs-12']").text
                category=flight.find_elements(By.XPATH,".//p[@class='fs-18 fare-title text-center']")
                prices = flight.find_elements(By.XPATH,".//p[@class='fs-18 bold price-color text-center fare-price']")

                #iterate through price and category
                category=[cat.text for cat in category]
                prices=[price.text for price in prices]
                flight_cat_price= {'Offer': category, 'Price': prices}

                flight_price.append(flight_cat_price)
                flight_names.append(name)
                flight_depart_time.append(depart_time)
                flight_arrival_time.append(arrival_time)
                flight_dur_time.append(dur_time)

            except Exception as e:
                print(f"An error occurred while extracting flight data: {e}")

        # Create a DataFrame
        data = {'Flight': flight_names, 'Depart time': flight_depart_time, 'Arrival time': flight_arrival_time,
                'Journey duration': flight_dur_time, 'Price': flight_price}
        df = pd.DataFrame(data)

        # Save to CSV
        df.to_csv('flight_details.csv',index=False)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the driver
        driver.quit()

# Executing......

scrape_flight_data("Banglore", "Mumbai", "20/06/2024")
