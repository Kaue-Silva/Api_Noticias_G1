from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--disable-notifications")

class Noticias:
    def __init__(self):
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://g1.globo.com/")

    def carregamento_pagina(self):
        # pegar altura da pagina
        altura_final = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Botão scroll para baixo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # esperar a pagina carregar
            sleep(0.5)

            # calcular novo scroll e comparar com scroll total da pagina
            altura_nova = self.driver.execute_script("return document.body.scrollHeight")
            if altura_nova == altura_final:
                break
            
            altura_final = altura_nova
    
    def captura_noticias(self):
        resumo_noticias = {}
        noticias = self.driver.find_elements_by_xpath('//div [@class="feed-post-body-resumo"]')
        for n in range(len(noticias)):
            resumo_noticias[n] = f"{n+1}º Noticia: {noticias[n].text}"
        
        return resumo_noticias

    def sair(self):
        self.driver.close()
