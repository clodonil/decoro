from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db
from flask.ext.login import login_required, current_user
from datetime import date
from app.controllers.usuario.forms import UserForm, UserEditForm, UserPassForm
from app.model import Usuario
from flask.ext.login import login_required




usuario = Blueprint('usuario',__name__)

@usuario.route('/index')
@usuario.route('/')
@login_required
def index():
    session['tela'] = "usuario"
    todos = Usuario.query.all() 
    return render_template('usuario/index.html',title='Lista de Usuario',todos=todos)


@usuario.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = UserForm()        
    if form.validate_on_submit():
       user = Usuario(
                           nome       = form.nome.data,
                           sobrenome  = form.sobrenome.data,
                           email      = form.email.data,
                           password   = form.password.data,
                           tel1       = form.tel1.data,
                           tel2       = form.tel2.data,
                           login      = form.login.data,
                          )
       user.add(user)
       return redirect(url_for('usuario.index'))
    return render_template('usuario/new.html',title='Cadastro de Usuario',form=form)

@usuario.route("/edit/<int:user_id>", methods = ["GET","POST"])
@login_required
def edit(user_id):
    user = Usuario.query.get(user_id)    
    form = UserEditForm(obj=user)
    form.login.data    = user.login
    
    
    if form.validate_on_submit():
       user.nome       = form.nome.data
       user.sobrenome  = form.sobrenome.data
       user.email      = form.email.data
       user.login      = form.login.data
       user.tel1       = form.tel1.data
       user.tel2       = form.tel2.data


       user.update()
       return redirect(url_for('usuario.index'))
    return render_template("usuario/edit.html",title='Alterar de Empresa', form=form)


@usuario.route("/editpass/<int:user_id>", methods = ["GET","POST"])
@login_required
def editpass(user_id):
    user = Usuario.query.get(user_id)    
    form = UserPassForm(obj=user)
    
    
    if form.validate_on_submit():
       user.set_password(form.password.data)
       user.update()
       return redirect(url_for('usuario.index'))
    return render_template("usuario/editpass.html",title='Alterar de Senha', form=form, user=user)


@usuario.route("/delete/<int:user_id>")
@login_required
def delete(user_id):
    user = Usuario.query.get(user_id)
 
    # Verificar se existe movimentação do usuário antes de apagar ou apagar todas as movimentacoes
    user.delete(user)
    return redirect(url_for('usuario.index'))


@usuario.context_processor
def dados():
    usuario = Usuario.query.get(current_user.id)
    hoje    = date.today()
    return dict(usuario = usuario.nome,hoje=hoje)

