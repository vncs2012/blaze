
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


class Driver:

    def __init__(self) -> None:
        self._driver = self.init_driver()

    def get_driver(self):
        return self._driver

    def init_driver(self):
        option = Options()
        option.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        return driver
    
    def fechar(self):
        self._driver.quit()
