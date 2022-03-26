from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--disable-notifications")

class Noticias:
    def __init__(self):
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://g1.globo.com/")
        self.noticias = {}

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
    
    def elementos_noticias(self):
        noticias = self.driver.find_elements_by_xpath('//div [@class="feed-post-body"]')
        return noticias


    def noticias_texto(self):
        noticias = self.elementos_noticias()
        for i, noticia in enumerate(noticias):
            noticia = noticia.text
            noticia = noticia.split("\n")
            objeto_noticia = {
                "titulo": noticia[0], 
                "complementar": noticia[2], 
                "hora_local": noticia[1]
            }
            self.noticias[i] = objeto_noticia
    

    def noticias_dados(self):
        return self.noticias
    
    def sair(self):
        self.driver.close()



# a = Noticias()
# a.carregamento_pagina()
# a.noticias_imagens()
# print(a.noticias_dados())

# noticias = a.driver.find_elements_by_xpath('//div [@class="feed-post-body"]')

# noticias[0] = noticias[0].find_element(by=By.XPATH, value='//div[@class="feed-media-wrapper"]//picture//img')
# base64a = noticias[0].screenshot_as_base64

# print(base64a)

