from doctest import FAIL_FAST
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import csv

def addValues(spans):
    with open('tabela_crash', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for span in spans[:15]:
            data_e_hora_atuais = datetime.now()
            writer.writerow(
                [span.attrs['class'][0], span.text.split('X')[0], ])

      
url = 'https://blaze.com/pt/games/crash'

option = Options()
option.headless = False
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get(url)
element = driver.find_element(By.CLASS_NAME, "entries")

html_content = element.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')
cont = soup.select_one("div.entries")

spans = soup.findAll('span')

addValues(spans)

for span in spans:
    print(dir(span))
    # print(span)
    # break
driver.quit()