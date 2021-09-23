from main import Noticias
from flask import Flask
from flask_restx import Api, Resource

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app, 
        version=1.0,
        title='API G1 Noticias',
        description='Api que retorna resumo das principais noticias do site G1.',
        doc='/'
        )
    
    def run(self):
        self.app.run()

server = Server()

app, api = server.app, server.api

@api.route('/noticias')
class resumo_noticias(Resource):
    def get(self):
        noticias = Noticias()
        noticias_dados = noticias.captura_noticias()
        noticias.sair()
        return noticias_dados

if __name__ == "__main__":
    server.run()
