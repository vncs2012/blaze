from driver.driver import Driver
from blaze import *

driver = Driver()
url = 'https://blaze.com/pt/games'
blaze = Crash(driver.get_driver(), url)
blaze.jogar()
driver.fechar()