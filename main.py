from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--disable-notifications")

class Noticias:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"./chromedriver.exe", options=options)
        self.driver.get("https://g1.globo.com/")

    def captura_noticias(self):
        # pegar altura da pagina
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Botão scroll para baixo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # esperar a pagina carregar
            sleep(0.5)

            # calcular novo scroll e comparar com scroll total da pagina
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            
            last_height = new_height
        
        # pagina = self.driver.find_element_by_xpath('//body')
        # pagina.send_keys(Keys.END)
        
        # sleep(5)
        
        resumo_noticias = {}
        noticias = self.driver.find_elements_by_xpath('//div [@class="feed-post-body-resumo"]')
        for n in range(len(noticias)):
            resumo_noticias[n] = f"{n+1}º Noticia: {noticias[n].text}"
        
        return resumo_noticias

    def sair(self):
        self.driver.close()
