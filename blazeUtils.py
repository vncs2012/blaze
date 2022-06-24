import os
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
load_dotenv()

def login(driver):
    login_entrar = driver.find_element(By.CLASS_NAME,"unauthed-buttons")
    login_elementoA = login_entrar.find_element(By.CLASS_NAME,"link")
    login_elementoA.click()
    driver.implicitly_wait(5)
    LoginEmail = driver.find_element(By.XPATH,"//input[@name='username']")
    LoginEmail.send_keys(os.getenv('USUARIO'))
    LoginPassword = driver.find_element(By.XPATH,"//input[@type='password']")
    LoginPassword.send_keys(os.getenv('SENHA'))
    logar = driver.find_element(By.CLASS_NAME,"input-footer")
    logar.click()
    driver.implicitly_wait(5)

def insert_valor(driver, value):
    input_Value = driver.find_element(By.XPATH,"//input[@type='number']")
    input_Value.clear()
    input_Value.send_keys(str(value))
    print('inicio')
    driver.implicitly_wait(400)
    print('fin')

def insert_auto_retirar(driver, value):
    input_Value = driver.find_element(By.XPATH,"//input[@data-testid='auto-cashout']")
    input_Value.clear()
    input_Value.send_keys(str(value))

def apostar_retirar(driver,time):
    print('Entrou Apostar|Retirar')
    apostar = driver.find_element(By.CLASS_NAME,"place-bet")
    apostar.click()
    print("delay")
