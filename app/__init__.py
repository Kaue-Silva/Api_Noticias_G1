from flask import Flask
from flask_restx import Api


app = Flask(__name__)
# app.config["DEBUG"] = True
api = Api(app, 
        version=1.0,
        title='API G1 Noticias',
        description='Api que retorna resumo das principais noticias do site G1.',
        doc='/'
)

from .views import noticias