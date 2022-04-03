from flask import Flask
from flask_restx import Api


app = Flask(__name__)
app.config["DEBUG"] = False
api = Api(app, 
        version=1.2,
        title='API G1 Noticias',
        description='API com retorno de noticias extraidas da pagina do G1 Noticias.',
        doc='/'
)

from .views import noticias