from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))#encontrar o usuario de acordo com o id dele

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)#chave primaria, para identificar o usuario
    username = database.Column(database.String, nullable=False)#nullable esse campo não pode ta vazio
    email = database.Column(database.String, nullable=False, unique=True)#unique, único, não pode ter dois emails iguais
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)#para interagir com a classe post
    cursos = database.Column(database.String, nullable=False, default='Não informado')

    def contar_posts(self):#só vai receber como instância o self que é a classe que estamos olhando
        return len(self.posts)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)#text porque é um texto grande com paragrafos etc..
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)