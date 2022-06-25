from selenium.webdriver.common.by import By
from blaze.blaze import Blaze
from datetime import datetime
from bs4 import BeautifulSoup
import csv

class Crash(Blaze):

    BET_PERCENTAGE = 0.05
    BALANCE = 5
    AMOUNT = round(BALANCE * BET_PERCENTAGE, 2)
    STOP_WIN = 2.00
    APOSTA = 0
    BANCA_INICIAL = BALANCE

    def __init__(self, driver,url) -> None:
        self.driver = driver
        self.url = f"{url}/crash"
        super().__init__(driver)
    
    def set_url_driver(self):
        self.driver.get(self.url)     

    def jogar(self) -> None:
        self.set_url_driver()
        # self.login()
        self.init = False
        self.salvar_win = self.init_arquivo('salva_win.csv')
        self.spans_crash_atual = self.get_spans_do_ultimos_crash()
        while True:
            self.spans_crash_ultimo = self.get_spans_do_ultimos_crash()
            if self.spans_crash_diferentes():
                self.valoreSpans = self.get_valores_spans()
                self.regras_geral()
                if(self.init):
                    self.historico_gravar_ganhos()
                if(self.balance_vs_amount()):
                    self.jogar_regras_padrao_1x() if self.crash_point[0] == 1 else self.jogar_regras_gerais()
                else:
                    print('VALOR INSUFICIENTE')
            self.spans_crash_atual = self.spans_crash_ultimo

    def get_spans_do_ultimos_crash(self):
        element = self.driver.find_element(By.CLASS_NAME, "entries")
        html_content = element.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        cont = soup.select_one("div.entries")
        return soup.findAll('span')

    def get_valores_spans(self):
        return [float(x.text.split('X')[0]) for x in self.spans_crash_ultimo]

    def spans_crash_diferentes(self):
        return len(self.spans_crash_ultimo) != len(self.spans_crash_atual)

    def regras_geral(self) -> None:
        self.data_e_hora_atuais = str(datetime.now())
        self.regra3Loss = list(filter(lambda x: x < 2, self.valoreSpans[:3]))
        self.regraNaoEntrar4Loss = list(filter(lambda x: x < 2, self.valoreSpans[:5]))
        self.regra4Win = list(filter(lambda x: x > 2, self.valoreSpans[:4]))
        self.regraMaior15 = list(filter(lambda x: x > 15, self.valoreSpans[:1]))
        self.regra2WinDaMaior15 = list( filter(lambda x: x > 15, self.valoreSpans[1:3]))
        self.crash_point = self.valoreSpans[:1]

    def historico_gravar_ganhos(self):
        print("Crash : {}".format(self.crash_point[0]))
        if (self.crash_point[0] >= self.STOP_WIN):
            self.STATUS = "win"
            self.BALANCE += round(float((self.APOSTA * self.STOP_WIN)), 2)
            self.AMOUNT = round(float((self.BALANCE * self.BET_PERCENTAGE)), 2)
            self.APOSTA = 0
        else:
            self.STATUS = "loss"
            if(len(self.regraNaoEntrar4Loss) == 5):
                self.AMOUNT = round((self.AMOUNT*1.50), 2)
            else:
                self.AMOUNT *= 2

        print(f'---------------------------------\nStatus: {self.STATUS}: Banca: {round(self.BALANCE,2)}')
        self.inserir_arquivo(self.salvar_win, [self.STATUS, self.APOSTA, self.crash_point[0], self.data_e_hora_atuais.split(' ')[1][:5], self.BALANCE, self.BET_PERCENTAGE, self.STOP_WIN, ])
        self.APOSTA = 0
        self.init = False
        self.fechar_o_dia()

    def balance_vs_amount(self):
        return self.BALANCE > self.AMOUNT
        
    def init_arquivo(self, arquivo) -> csv:
        file = open(arquivo, 'a', newline='\n')
        writer = csv.writer(file, delimiter=';')
        return writer

    def inserir_arquivo(self, salavr, dados) -> None:
        salavr.writerow(dados)

    def fechar_o_dia(self) -> None:
        if((self.BALANCE-self.BANCA_INICIAL) > 150):
            print('Chegou Meta do dia/Rodagem do software')
            self.driver.quit()

    def jogar_regras_gerais(self)->None:
        if len(self.regra3Loss) == 3 and not len(self.regraNaoEntrar4Loss) == 5:
            self.fazer_aposta()
            print(f'---------------------------------\nEntrar Regra3Loss {self.regra3Loss} , Aposta de :{self.APOSTA}')
        elif(len(self.regra4Win) == 4):
            self.fazer_aposta()
            print( f'---------------------------------\nEntrar Regra4Win {self.regra4Win} , Aposta de :{self.APOSTA}')
        elif((len(self.regraMaior15) == 1 and len(self.regra2WinDaMaior15) == 0) or (len(self.regraMaior15) == 1 and len(self.regra2WinDaMaior15) == 1)):
            self.fazer_aposta()
            print( f'---------------------------------\nEntrar RegraMaior15 {self.regraMaior15}  , Aposta de :{self.APOSTA}')
        else:
            print('---------------------------------\nNENHUM REGRA SE APLICA')
    def jogar_regras_padrao_1x(self)->None:
        ...
    
    def fazer_aposta(self)->None:
        self.BALANCE = float( self.BALANCE - self.AMOUNT)
        self.APOSTA = round(float((self.BALANCE * self.BET_PERCENTAGE)), 2)
        self.init = True
        # util.insert_valor(driver, amount)
        # util.apostar_retirar(driver,4)
        # util.apostar_retirar(driver,10) 


