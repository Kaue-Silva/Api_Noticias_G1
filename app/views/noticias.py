from flask_restx import Resource
from app import api
from ..controllers.noticias import Noticias


@api.route('/noticias')
class resumo_noticias(Resource):
    def get(self):
        noticias = Noticias()
        noticias_dados = noticias.captura_noticias()
        noticias.sair()
        return noticias_dados