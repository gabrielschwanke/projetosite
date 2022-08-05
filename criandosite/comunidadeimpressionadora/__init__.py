from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # isso é oq faz as pastas poderem interagir umas com as outras

app.config['SECRET_KEY'] = 'abc48bae47965b685ba88f80251945bf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.bd'  # caminho que vai criar o banco de dados

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #para direcionar a pagina para fazer login
login_manager.login_message = 'Faça login para acessar essa página'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import routes
#tive que importar em baixo para poder criar o app antes, pois os routes precisam do app