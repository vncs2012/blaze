from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import blazeUtils as util

BET_PERCENTAGE = 0.05
balance = 5
amount = round(balance * BET_PERCENTAGE, 2)
STOP_WIN = 2.00
aposta = 0
BancaInicial = balance
url = 'https://blaze.com/pt/games/crash'

option = Options()
option.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

driver.get(url)
#################Realiza Login##################
util.login(driver)

element = driver.find_element(By.CLASS_NAME,"entries")
html_content = element.get_attribute('outerHTML')
soup = BeautifulSoup(html_content, 'html.parser')
cont = soup.select_one("div.entries")
spans = soup.findAll('span')
util.insert_auto_retirar(driver,STOP_WIN)
file = open('salva_win.csv', 'a', newline='')
writer = csv.writer(file)
init = False
while True:
    element = driver.find_element(By.CLASS_NAME,"entries")
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    cont = soup.select_one("div.entries")

    spans2 = soup.findAll('span')

    if len(spans2) != len(spans):
        data_e_hora_atuais = str(datetime.now())
        print(len(spans2))

        valoreSpans = [float(x.text.split('X')[0]) for x in spans2]
        Regra3Loss = list(filter(lambda x: x < 2, valoreSpans[:3]))
        regraNaoEntrar4Loss = list(filter(lambda x: x < 2, valoreSpans[:5]))
        Regra4Win = list(filter(lambda x: x > 2, valoreSpans[:4]))
        RegraMaior15 = list(filter(lambda x: x > 15, valoreSpans[:1]))
        regra2WinDaMaior15 = list(filter(lambda x: x > 15, valoreSpans[1:3]))
        crash_point = valoreSpans[:1]
        if(init):
            print("Crash : {}".format(crash_point))
            if (crash_point[0] > STOP_WIN):
                status = "win"
                balance += round(float((aposta * STOP_WIN)), 2)
                amount = round(float((balance * BET_PERCENTAGE)), 2)
                aposta = 0
            else:
                status = "loss"
                if(len(regraNaoEntrar4Loss) == 5):
                    amount = round((amount*1.50),2) 
                else:
                    amount *= 2

            print(f'Status: {status}: Banca: {balance}')
            writer.writerow([status,aposta, crash_point[0],data_e_hora_atuais,balance,BET_PERCENTAGE,STOP_WIN,])
            if((balance-BancaInicial) > 150):
                driver.quit()

            aposta = 0
            init = False

        if(balance > amount):
            
            if len(Regra3Loss) == 3 and not len(regraNaoEntrar4Loss) == 5:
                balance = float(balance - amount)
                aposta = round(float((balance * BET_PERCENTAGE)), 2)
                print(f'Entrar Regra3Loss {Regra3Loss} , Aposta de :{aposta}')
                init = True
                # util.insert_valor(driver, amount)
                # util.apostar_retirar(driver,4)
                # util.apostar_retirar(driver,10)
            elif(len(Regra4Win) == 4):
                balance =  float(balance - amount)
                aposta = round(float((balance * BET_PERCENTAGE)), 2)
                print(f'entrar Regra4Win {Regra4Win} , Aposta de :{aposta}')
                init = True
                # util.insert_valor(driver, amount)
                # util.apostar_retirar(driver,4000)
            elif((len(RegraMaior15) == 1 and len(regra2WinDaMaior15) == 0) or (len(RegraMaior15) == 1 and len(regra2WinDaMaior15) == 1)):
                balance = float(balance - amount)
                aposta = round(float((balance * BET_PERCENTAGE)), 2)
                init = True
                print(f'Entrar RegraMaior15 {RegraMaior15}  , Aposta de :{aposta}')
            else:
                print('não entrar')
        else:
            print('VALOR INSUFICIENTE')

        # element = driver.find_element_by_class_name("casino-table-wrapper")
        # html_content = element.get_attribute('outerHTML')
        # soup = BeautifulSoup(html_content, 'html.parser')
        # table = soup.find(name='table')

        # df_full = pd.read_html(str(table))[0]
        if((balance-BancaInicial) > 150):
            print('Chegou Meta do dia/Rodagem do software')

        spans = spans2
