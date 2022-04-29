from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

options = webdriver.ChromeOptions()
options.headless = True


options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-dev-shm-usage")


class Noticias:
    imagem_none = ""

    def __init__(self):
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://g1.globo.com/")
        self.noticias = []

    def get_noticias(self):
        noticias_elem = []
        noticias = self.driver.find_elements(
            by=By.XPATH, value='//div [@class="feed-post-body"]'
        )

        for i, noticia in enumerate(noticias):
            noticia = noticia.get_attribute("innerHTML")
            noticias_elem.append(noticia)
            self.noticias.append({"id": i})

        self.noticias_elem = noticias_elem

    def carregamento_pagina(self):
        # pegar altura da pagina
        altura_final = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Botão scroll para baixo
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # esperar a pagina carregar
            sleep(0.5)

            # calcular novo scroll e comparar com scroll total da pagina
            altura_nova = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            if altura_nova == altura_final:
                break

            altura_final = altura_nova

        self.get_noticias()

    def get_titulos(self):
        html_noticias = self.noticias_elem
        for i, html_noticia in enumerate(html_noticias):
            soup = BeautifulSoup(html_noticia, "html.parser")
            titulo = soup.a.text
            self.noticias[i]["titulo"] = titulo

    def get_complementos(self):
        html_noticias = self.noticias_elem
        for i, html_noticia in enumerate(html_noticias):
            soup = BeautifulSoup(html_noticia, "html.parser")
            complementos = []

            complementos_elem = soup.find_all("ul", class_="bstn-relateditems")
            if complementos_elem != []:
                for complemento in complementos_elem:
                    complemento = complemento.a
                    complemento = complemento.text
                    complementos.append(complemento)
            else:
                try:
                    complemento_elem = soup.find_all(
                        "div", class_="feed-post-body-resumo"
                    )
                    complemento = complemento_elem[0]
                    complemento = complemento.text
                    complementos.append(complemento)
                except:
                    complementos = []

            self.noticias[i]["complementos"] = complementos

    def get_hora_local(self):
        html_noticias = self.noticias_elem

        for i, html_noticia in enumerate(html_noticias):

            soup = BeautifulSoup(html_noticia, "html.parser")

            hora = soup.find_all("span", class_="feed-post-datetime")
            hora = hora[0]
            hora = hora.text
            hora = hora.strip()

            local = soup.find_all("span", class_="feed-post-metadata-section")
            local = local[0]
            local = local.text
            local = local.strip()

            hora_local = f"{hora} - {local}"

            self.noticias[i]["hora_local"] = hora_local

    def get_imagem(self):
        html_noticias = self.noticias_elem
        for i, html_noticia in enumerate(html_noticias):
            soup = BeautifulSoup(html_noticia, "html.parser")
            try:
                imagem = soup.img
                imagem = imagem.get_attribute_list("src")
                imagem = imagem[0]
            except:
                imagem = None

            self.noticias[i]["imagem"] = imagem

    def noticias_dados(self):
        return self.noticias

    def sair(self):
        self.driver.close()
