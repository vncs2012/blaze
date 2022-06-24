from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
from datetime import datetime
import pandas as pd

url = 'https://blaze.com/pt/games/crash'

option = Options()
option.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)

driver.get(url)

element = driver.find_element_by_class_name("entries")
html_content = element.get_attribute('outerHTML')
soup = BeautifulSoup(html_content, 'html.parser')
cont = soup.select_one("div.entries")
spans = soup.findAll('span')

file = open('tabela_crash.csv', 'a', newline='')
writer = csv.writer(file)

while True:
    element = driver.find_element_by_class_name("entries")
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    cont = soup.select_one("div.entries")

    spans2 = soup.findAll('span')
    # print(spans2)

    if len(spans2) != len(spans):
        data_e_hora_atuais = str(datetime.now())

        element = driver.find_element_by_class_name("casino-table-wrapper")
        html_content = element.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(name='table')

        df_full = pd.read_html(str(table))[0]

        valorApostado = 0

        for i in df_full['Aposta']:
            valorApostado += float(i[3:])
        
        valorGanho = 0

        for i in df_full['Lucro']:
            if i != '-':
                valorGanho += float(i[3:])
        
        writer.writerow([spans2[0].text, 
                        spans2[0].attrs['class'][0], 
                        data_e_hora_atuais.split(' ')[1][:5], 
                        valorApostado,
                        valorGanho])    
        
        print((valorGanho*10 - valorApostado)/100, spans2[0].text)
        spans = spans2