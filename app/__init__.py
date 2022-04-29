from flask import Flask
from flask_restx import Api
# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("config")
api = Api(app, 
        version=1.2,
        title='API G1 Noticias',
        description='API com retorno de noticias extraidas da pagina do G1 Noticias.',
        doc='/'
)
# db = SQLAlchemy(app)


from .views import gerar_noticias