from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--disable-notifications")

class Noticias:
    imagem_none = ''
    
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
    
    # def elementos_noticias(self):
    #     noticias = self.driver.find_elements_by_xpath('//div [@class="feed-post-body"]')
    #     return noticias


    # def noticias_texto(self):
    #     noticias = self.driver.find_elements_by_xpath('//div [@class="feed-post-body"]//a')
    #     for i, noticia in enumerate(noticias):
    #         noticia = noticia.text
    #         noticia = noticia.split("\n")
    #         print(noticia)
    #         # objeto_noticia = {
    #         #     "imagem":"",
    #         #     "titulo": noticia[0], 
    #         #     "complementar": noticia[2], 
    #         #     "hora_local": noticia[-1]
    #         # }
    #         self.noticias[i] = {"texto":noticia}
    
    
    # def noticias_titulos(self):
    #     # //div [@class="feed-post-body"]/div[@class="feed-post-body-title gui-color-primary gui-color-hover "]/div/a
    #     titulos = self.driver.find_elements_by_xpath('//div[@class="feed-post-body"]/div[2]/div/a')
        
    #     for i, titulo in enumerate(titulos):
    #         titulo = titulo.text
    #         self.noticias[i] = {"titulo":titulo}

    # def noticias_complementar(self):
    #     # //div [@class="feed-post-body"]/div[@class="bstn-related"]/ul/li
    #     complementares = self.driver.find_elements_by_xpath('//ul [@class="bstn-relateditems"]')
    #     for i, complemento in enumerate(complementares):
    #         complemento = complemento.text
    #         complemento = complemento.split('\n')
    #         self.noticias[i]["complemento"] = complemento
            

    # def noticias_hora_local(self):
    #     # //div [@class="feed-post-body"]/div[@class="feed-post-metadata"]
    #     # //div [@class="feed-post-body"]/div[@class="feed-post-metadata"]/span[1] hora
    #     # //div [@class="feed-post-body"]/div[@class="feed-post-metadata"]/span[2] local
    #     pass

    # def noticias_imagens(self):
    #     imagens = self.driver.find_elements_by_xpath('//div [@class="feed-post-body"]//picture//img')
    #     for i, imagem in enumerate(imagens):
    #         imagem = imagem.get_attribute("src")
    #         if imagem == None:
    #             imagem = self.imagem_none
                
    #         self.noticias[i]["imagem"] = imagem
    
    
    def get_elems_noticias(self):
        noticias = self.driver.find_elements(by=By.XPATH, value='//div [@class="feed-post-body"]')
        return noticias
    
    def get_html_noticias(self):
        noticias_elem = []
        noticias = self.get_elems_noticias()
        
        for noticia in noticias:
            noticia = noticia.get_attribute('innerHTML') 
            noticias_elem.append(noticia)

        return noticias_elem
    
    def get_titulos(self):
        html_noticias = self.get_html_noticias()
        for i, html_noticia in enumerate(html_noticias):
            titulo = html_noticia[html_noticia.index('<a'):html_noticia.index('</a>')]
            titulo = titulo.split('>')
            titulo = titulo[1]
            self.noticias[i] = {"titulo":titulo}

    def get_complementos(self):
        html_noticias = self.get_html_noticias()
        for i, html_noticia in enumerate(html_noticias):
            try:
                complementos = []
                complemento = html_noticia[html_noticia.index('<ul'):html_noticia.index('</ul>')]
                complemento_qtd = complemento.count("<li")
                if complemento_qtd > 1:
                    complementos_data = complemento
                    complementos_data = complementos_data.split("<a")
                    for complemento in complementos_data:
                        try:
                            complemento = complemento[complemento.index(">")+1:complemento.index("</a>")]
                            complementos.append(complemento)
                        except:
                            continue
                else:
                    complemento = complemento[complemento.index('<a'):complemento.index('</a>')]
                    complemento = complemento.split(">")
                    complemento = complemento[1]
                    complemento = complemento.replace("</a", "")
            except:
                try:
                    complemento = html_noticia[html_noticia.index('class="feed-post-body-resumo"'):]
                    complemento = complemento[complemento.index(">")+1:complemento.index("</div>")]
                except:
                    complemento = ""
            
            
            if complementos:
                self.noticias[i]["complementos"] = complementos
            else:
                self.noticias[i]["complementos"] = complemento
            
    
    def noticias_dados(self):
        return self.noticias
    
    def sair(self):
        self.driver.close()

noticias = Noticias()
noticias.carregamento_pagina()
noticias.get_titulos()
noticias.get_complementos()
print(noticias.noticias_dados())