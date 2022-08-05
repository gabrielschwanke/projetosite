from flask import render_template, redirect, url_for, flash, request, abort
from flask_wtf import form

from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os #para separar a extensão da imagem
from PIL import Image #para poder compactar o tamanho da imagem salva no site

lista_usuarios = ['Gabriel', 'Jose', 'Carlos', 'Marcela', 'Sandra']

@app.route("/")  # caminho da página inicial
def home():  # e aq sempre vai o que a pagina vai fazer
    posts = Post.query.order_by(Post.id.desc()) #para ordernar os posts do mais novo pro mais antigo
    return render_template('home.html', posts=posts)


@app.route('/contato')  # o decoreytor é sempre pra atribuir uma funcionalidade para função que está abaixo
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required #só vai aparecer essa página se estiver com o login
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html',lista_usuarios=lista_usuarios)  # o parametro recebe lista usuarios, nesse caso se usa o mesmo nome


# da para fazer um for no html, mas tem que estar dentro de blocos com {% %} e fecha {% endfor %}
# se for só uma variável, dentro de duas chaves {{ }}
@app.route('/login', methods=['GET','POST'])  # quando não se passa metodo nenhum, automatico ele puxa o metodo GET e quando tem formulários tem que passar o POST
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}','alert-success')  # flash para exibir mensagem de alerta, coloquei como variavel o .data que da oque o usuário colocou no campo email
            parametro_next = request.args.get('next')#redirecionando para a pagina que estava tentando logar antes de fazer o login
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))  # redirecionando
        else:
            flash(f'Falha no login. E-mail ou senha incorretos', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        #criar usuario
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        # adicionar a sessao
        database.session.add(usuario)#adicionando o usuario no banco de dados
        #comit na sessao
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
        foto_perfil = url_for('static',filename='fotos_perfil/{}'.format(current_user.foto_perfil))
        return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET','POST'])
@login_required #para essa página aparecer só se estiver com o login feito
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)# adicionar um codigo aleatorio na foto de perfil, para não ter perigo de ter duas fotos com mesmo nome
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (500, 500)#200 de altura e largura, porque foi esse parametro que foi passado no arquivo html
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)# salvar a imagem na pasta fotos_perfil
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                #adicionar o texto do campo.label (Excel Impressionador) na lista de cursos
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)#join vai transformar a lista de cursos em uma lista junta




@app.route('/perfil/editar', methods=['GET','POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()#nesse caso não precisa colocar o usuario no banco de dados, porque ele já está
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":#para deixar os campos preenchidos
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/<post_id>', methods=['GET','POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()#usei o formulário de criar post, pq seria a mesma coisa que criar um novo
        if request.method == 'GET':#para carregar o próprio post na edição e não ter que copiar
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com Sucesso','alert-success')
            return redirect(url_for('home'))

    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET','POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso','alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)#erro para tentar excluir post que não seja do autor