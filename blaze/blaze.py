from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
load_dotenv()

class Blaze:

    def __init__(self, driver) -> None:
        self.driver = driver

    def login(self):
        login_entrar = self.driver.find_element(By.CLASS_NAME, "unauthed-buttons")
        login_elementoA = login_entrar.find_element(By.CLASS_NAME, "link")
        login_elementoA.click()
        self.driver.implicitly_wait(5)
        LoginEmail = self.driver.find_element(By.XPATH, "//input[@name='username']")
        LoginEmail.send_keys(os.getenv('USUARIO'))
        LoginPassword = self.driver.find_element(By.XPATH, "//input[@type='password']")
        LoginPassword.send_keys(os.getenv('SENHA'))
        logar = self.driver.find_element(By.CLASS_NAME, "input-footer")
        logar.click()
        self.driver.implicitly_wait(5)

    def inserir_valor(self, value):
        input_Value = self.driver.find_element(By.XPATH, "//input[@type='number']")
        input_Value.clear()
        input_Value.send_keys(str(value))
        self.driver.implicitly_wait(400)

    def iserir_auto_retirar(self, value):
        input_Value = self.driver.find_element(By.XPATH, "//input[@data-testid='auto-cashout']")
        input_Value.clear()
        input_Value.send_keys(str(value))

    def apostar_retirar(self, time):
        print('Entrou Apostar|Retirar')
        apostar = self.driver.find_element(By.CLASS_NAME, "place-bet")
        apostar.click()

    # def game_crash(self):
    #     url_game =f"{self.url}/crash"
    #     self.driver.get(url_game) 
    #     # self.login()
    #     crash = Crash(self.driver)
    #     crash.jogar()
        