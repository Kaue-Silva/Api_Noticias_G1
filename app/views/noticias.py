from flask_restx import Resource
from app import api
from ..controllers.noticias import Noticias


@api.route('/noticias')
class resumo_noticias(Resource):
    def get(self):
        noticias = Noticias()
        try:
            noticias.carregamento_pagina()
            noticias.get_titulos()
            noticias.get_complementos()
            noticias.get_hora_local()
            noticias.get_imagem()
            noticias_dados = (noticias.noticias_dados(), 200)
        except:
            noticias_dados = ([{}, "Occoreu um erro inesperado"], 502)
        
        noticias.sair()
        return noticias_dados
