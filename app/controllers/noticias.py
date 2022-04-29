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
            # titulo = html_noticia[html_noticia.index('<a'):html_noticia.index('</a>')]
            # titulo = titulo.split('>')
            # titulo = titulo[1]
            soup = BeautifulSoup(html_noticia, "html.parser")
            titulo = soup.a.text
            # self.noticias.append({"id":i,"titulo":titulo})
            self.noticias[i]["titulo"] = titulo

    def get_complementos(self):
        html_noticias = self.noticias_elem
        for i, html_noticia in enumerate(html_noticias):
            # try:
            #     complementos = []
            #     complemento = html_noticia[html_noticia.index('<ul'):html_noticia.index('</ul>')]
            #     complemento_qtd = complemento.count("<li")
            #     if complemento_qtd > 1:
            #         complementos_data = complemento
            #         complementos_data = complementos_data.split("<a")
            #         for complemento in complementos_data:
            #             try:
            #                 complemento = complemento[complemento.index(">")+1:complemento.index("</a>")]
            #                 complementos.append(complemento)
            #             except:
            #                 continue
            #     else:
            #         complemento = complemento[complemento.index('<a'):complemento.index('</a>')]
            #         complemento = complemento.split(">")
            #         complemento = complemento[1]
            #         complemento = complemento.replace("</a", "")
            # except:
            #     try:
            #         complemento = html_noticia[html_noticia.index('class="feed-post-body-resumo"'):]
            #         complemento = complemento[complemento.index(">")+1:complemento.index("</div>")]
            #     except:
            #         complemento = ""

            # if complementos:
            #     self.noticias[i]["complementos"] = complementos
            # else:
            #     self.noticias[i]["complementos"] = [complemento]

            soup = BeautifulSoup(html_noticia, "html.parser")
            try:
                complementos_html = soup.find_all("li")
                complementos = []

                for complemento in complementos_html:
                    complemento = complemento.a
                    complemento = complemento.text
                    complementos.append(complemento)

            except:
                try:
                    complementos_html = soup.find_all("div")
                    for complemento in complementos_html:
                        try:
                            for complementos_class in complemento["class"]:
                                if complementos_class == "feed-post-body-resumo":
                                    complementos = [complemento.text]
                        except:
                            continue
                except:
                    complementos = []

            self.noticias[i]["complementos"] = complementos

    def get_hora_local(self):
        html_noticias = self.noticias_elem

        for i, html_noticia in enumerate(html_noticias):
            # hora_local = []
            # hora_local_html = html_noticia
            # hora_local_html = hora_local_html[
            #     hora_local_html.index('class="feed-post-datetime"') :
            # ]
            # hora_local_html = hora_local_html[hora_local_html.index(">") + 1 :]
            # hora_local_html = hora_local_html.split("</span>")
            # hora_local.append(hora_local_html[0])
            # hora_local_html = hora_local_html[1]
            # hora_local_html = hora_local_html[hora_local_html.index(">") + 1 :]
            # hora_local.append(hora_local_html)
            # hora_local[1] = hora_local[1].strip()
            # hora_local = f"{hora_local[0]} - {hora_local[1]}"

            soup = BeautifulSoup(html_noticia, "html.parser")

            hora = soup.find_all("span", class_="feed-post-datetime")
            hora = hora[0]
            hora = hora.text

            local = soup.find_all("span", class_="feed-post-metadata-section")
            local = local[0]
            local = local.text

            hora_local = f"{hora} - {local}"

            self.noticias[i]["hora_local"] = hora_local

    def get_imagem(self):
        html_noticias = self.noticias_elem
        for i, html_noticia in enumerate(html_noticias):
            try:
                imagem = html_noticia
                imagem = imagem[imagem.index("src=") + 5 :]
                imagem = imagem[: imagem.index('"')]

            except:
                imagem = ""

            self.noticias[i]["imagem"] = imagem

    def noticias_dados(self):
        return self.noticias

    def sair(self):
        self.driver.close()
