# Import modules
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import math

chrome_path = "chromedriver"  # link the path to chrome driver

address = "3145 Newton St NE, Washington, DC 20018"  # the address
url = "https://www.redfin.com/"  # Redfin URL

lot_size = ""  # Lot size variable
ErrorMessage = ""  # Error Message

pattern = 'Lot Size\n.*'  # The pattern with which to find the Lot Size

AcresToSqFt = 43560  # 1 acre is 43,560 Sq. Ft.
divisor = 10  # Footprint = lot size / 10
MaxFootprint = 1210  # Maximum Footprint

# Configuration options
op = Options()
# op.binary_location = chrome_path    # chrome binary location specified here
op.add_argument("--start-maximized")  # open Browser in maximized mode
# op.add_argument("--no-sandbox") #bypass OS security model
op.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
op.add_experimental_option("excludeSwitches", ["enable-automation"])
op.add_experimental_option('useAutomationExtension', False)
op.add_argument("--headless")
op.headless = True  # change to true to hide the browser

s = Service(chrome_path)  # stores the chrome path


with webdriver.Chrome(service=s, options=op) as d:
    try:
        d.get(url)  # opens the URL
    except:
        print("Browser did not open.")
        ErrorMessage = "Error"
    else:
        try:
            d.find_element(By.ID, "search-box-input").send_keys(address)  # Type address
            time.sleep(5)
            # Click search
            d.find_element(by=By.XPATH, value='//*[@id="tabContentId0"]/div/div/form/div/button').click()
            time.sleep(5)
        except:
            print("There was a problem while typing into or clicking the browser.")
            ErrorMessage = "Error"
        else:
            try:
                # Find the table containing lot size
                result = d.find_element(by=By.XPATH, value='//*[@id="basicInfo"]/div[2]/div[1]')
            except:
                print("There was a problem while finding the lot size.")
                ErrorMessage = "Error"
            else:
                # Format the result
                lot_size_table = (BeautifulSoup(result.text, "html.parser")).prettify()
                # print(lot_size_table)
                lot_size_row = re.findall(pattern, lot_size_table)
                lot_size = lot_size_row[0].split("\n")[1].strip().replace(",", "")
                # print(lot_size)

# If the lot size is in acres, convert to Sq. Ft. and format
if "Acres" in lot_size:
    lot_size_in_acres = lot_size.split(" ")[0]
    lot_size = str(math.floor(float(lot_size_in_acres)*AcresToSqFt))

# If the lot size is in Sq. Ft., format
if "Sq. Ft." in lot_size:
    lot_size_in_sq = lot_size.split(" ")[0]
    lot_size = str(math.floor(float(lot_size_in_sq)))

# If a Lot Size was found, process it
if len(lot_size) > 0:
    # If the lot size is written as "—" on the website, ADU cannot be built there
    if "—" in lot_size:
        Footprint = "ADU cannot be built here."
    else:
        # If the lot size is a valid number, find the footprint
        if lot_size.isnumeric():
            usable_lot_size = math.floor(float(lot_size)/divisor)
            # If footprint is less than 1210 Sq. Ft., output it
            if usable_lot_size < MaxFootprint:
                Footprint = str(usable_lot_size) + " Sq. Ft."
            # If footprint is more than 1210 Sq. Ft., output 1210 Sq. Ft.
            else:
                Footprint = str(MaxFootprint) + " Sq. Ft."

        # If the lot size is not a valid number, then output "ADU cannot be built here."
        else:
            Footprint = "ADU cannot be built here."

# If there is no error and a lot size was not found, then output "Maximum footprint could not be found."
elif len(ErrorMessage) == 0:
    Footprint = "Footprint could not be found."

# Output "Error" if there was an error
else:
    Footprint = ErrorMessage

# Prints the output
print(Footprint)
