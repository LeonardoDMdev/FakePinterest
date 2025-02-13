from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user   #login_required exigir q o usuario tenha login
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])      # essa tela qualquer usuario pode acessar
def homepage():
    formlogin = FormLogin()

    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first() # buscando no banco de dados se tem um email igual ao inserido no formulario
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), formlogin.senha.data):
            login_user(usuario)  
            return redirect(url_for("perfil", id_usuario=usuario.id))   
    return render_template("homepage.html", form=formlogin)


@app.route("/criarconta", methods=["POST", "GET"]) 
def criar_conta():
    form_criarconta = FormCriarConta()

    if form_criarconta.validate_on_submit():  #essa condição só vai rodar se o usuario clicar no botao, e se o clique dele está valido
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8") # criptografar senha do usuario
        usuario = Usuario(nome=form_criarconta.nome.data,
                        email=form_criarconta.email.data,
                        senha=senha)
        database.session.add(usuario)
        database.session.commit() #commit executa todas açoes no banco, odemos abrir uma session fazer varias alteraçoes e dar commit
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"]) # essa tela só usuario logados podem acessar
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        #o usuario esta vendo o perfil dele
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data  # se o nome do arquivo tiver caracteres especiais vai dar problema, por isso precisamos tratar mundando o nome do arquivo
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), # está pegando o local onde o arquivo routes está
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # registrar esse arquivo no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None) 


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage")) 


@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao).all()
    return render_template("feed.html", fotos=fotos)
