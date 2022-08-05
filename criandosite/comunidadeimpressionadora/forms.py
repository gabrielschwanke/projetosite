from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed #filefield abre a janela para abrir um arquivo do computador e fileallowed é um validador para escolher qual tipo de arquivo
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message='Digite um nome de usuário válido')])
    email = StringField('E-mail',validators=[DataRequired(), Email(message='Digite um endereço de e-mail válido')])
    senha = PasswordField('Senha',validators=[DataRequired(), Length(6, 20,message='Digite uma senha de 6 a 20 caracteres')])
    confirmacao_senha = PasswordField('Confirmação da Senha',validators=[DataRequired(message='Digite a senha igual a anterior'), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')

class FormLogin(FlaskForm):
    email = StringField('E-mail',validators=[DataRequired(), Email(message='Digite um nome de usuário válido')])
    senha = PasswordField('Senha',validators=[DataRequired(), Length(6, 20,message='Digite uma senha de 6 a 20 caracteres')])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto Perfil',validators=[FileAllowed(['jpg','png'],'Apenas .jpg ou png')])#uma lista de extensões que é permitido

    curso_excel = BooleanField('Excel')
    curso_vba = BooleanField('Visual Basic for Applications "VBA"')
    curso_powerbi = BooleanField('Power BI')
    curso_python = BooleanField('Python')
    curso_html = BooleanField('HyperText Markup Language "HTML"')
    curso_sql = BooleanField('Standard Query Language "SQL"')
    curso_js = BooleanField('JavaScript "JS"')
    curso_php = BooleanField('Hypertext Preprocessor "PHP"')

    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:#para verificar se ta mudando o email
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail')

class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140 )])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')