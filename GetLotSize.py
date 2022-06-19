from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re


chrome_path = "chromedriver"
address = "6818 Ashleys Crossing Ct, Temple Hills, MD 20748"
url = "https://www.redfin.com/"
pattern = '\nLot Size\n'

op = Options()
#op.binary_location = chrome_path    #chrome binary location specified here
op.add_argument("--start-maximized") #open Browser in maximized mode
#op.add_argument("--no-sandbox") #bypass OS security model
op.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
op.add_experimental_option("excludeSwitches", ["enable-automation"])
op.add_experimental_option('useAutomationExtension', False)
op.headless = False # change to true if we want to hide the browser
s = Service(chrome_path)

with webdriver.Chrome(service=s, options=op) as d:
    d.get(url)
    d.find_element(By.ID, "search-box-input").send_keys(address)
    d.find_element(by=By.XPATH, value='//*[@id="tabContentId0"]/div/div/form/div/button').click()
    time.sleep(5)
    result = d.find_element(by=By.XPATH, value='//*[@id="basicInfo"]/div[2]/div[1]')
    lot_size_table = (BeautifulSoup(result, "html.parser")).prettify()
    print(lot_size_table)
    lot_size = re.match(pattern, lot_size_table)
    print(lot_size)
