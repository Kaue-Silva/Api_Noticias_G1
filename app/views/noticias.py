from flask_restx import Resource
from app import api
from ..controllers.noticias import Noticias


@api.route('/noticias')
class resumo_noticias(Resource):
    def get(self):
        noticias = Noticias()
        noticias.carregamento_pagina()
        noticias.noticias_titulos()
        # noticias.noticias_texto()
        # noticias.noticias_imagens()
        noticias_dados = noticias.noticias_dados()
        noticias.sair()
        return noticias_dados
