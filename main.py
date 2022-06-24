from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import csv
from datetime import datetime
# import win32api

def addValues(spans):
    with open('tabela_crash', 'a', newline='') as file:    
        writer = csv.writer(file)

        for span in spans[15:]:
            data_e_hora_atuais = datetime.now()
            writer.writerow([span.text, span.attrs['class'][0]])      

      
url = 'https://blaze.com/pt/games/crash'

option = Options()
option.headless = False
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",options=option)

driver.get(url)

# while win32api.GetKeyState(27) >= 0:
#     pass
element = driver.find_element_by_class_name("entries")

html_content = element.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')
cont = soup.select_one("div.entries")

spans = soup.findAll('span')

addValues(spans)

for span in spans:
    # print(dir(span))
    print(span.attrs['class'])
    # break


driver.quit()