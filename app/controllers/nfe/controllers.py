from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db
from flask.ext.login import login_required, current_user
from datetime import date
from app.controllers.cliente.forms import EmpForm
from app.model import Cliente, Categoria, Usuario
from flask.ext.login import login_required
import os



nfe = Blueprint('nfe',__name__)

@nfe.route('/index')
@nfe.route('/')
@login_required
def index():

    # cliente ativos
    todos = Cliente.query.filter(Cliente.status == 0).order_by('nome').all()

    session['tela'] = "nfe"
    return render_template('nfe/index.html',title='Lista de Empresas com NFe',todos=todos)


@nfe.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = EmpForm()
    form.categoria_id.choices = [(h.id,h.titulo) for h in Categoria.query.all()]
    if form.validate_on_submit():
       emp = Cliente(
                      form.nome.data,
                      form.cnpj.data,
                      form.tel1.data,
                      form.nome_resp.data,
                      form.tel2.data,                           
                      form.email.data,
                      form.categoria_id.data,
                      form.status.data,
                      form.outros.data,
                      form.end.data,
                      form.cep.data,
                      form.uf.data,
                      form.cidade.data,
                      form.bairro.data,
                      form.aniversario.data,
                      form.valor.data,
                    )

       emp.add(emp)
       return redirect(url_for('cliente.index'))
    return render_template('cliente/new.html',title='Cadastro de cliente',form=form)

@nfe.route("/edit/<int:emp_id>", methods = ["GET","POST"])
@login_required
def edit(emp_id):
    emp = Cliente.query.get(emp_id)    
    form = EmpForm(obj=emp)
    form.categoria_id.choices = [(h.id,h.titulo) for h in Categoria.query.all()]
    if form.validate_on_submit():
        emp.nome         = form.nome.data
        emp.cnpj         = form.cnpj.data
        emp.tel1         = form.tel1.data
        emp.nome_resp    = form.nome_resp.data
        emp.tel2         = form.tel2.data                           
        emp.email        = form.email.data
        emp.categoria_id = form.categoria_id.data
        emp.status       = form.status.data
        emp.outros       = form.outros.data
        emp.end          = form.end.data
        emp.cep          = form.cep.data
        emp.uf          = form.uf.data
        emp.cidade       = form.cidade.data
        emp.bairro       = form.bairro.data
        emp.aniversario  = form.aniversario.data
        emp.valor        = form.valor.data 


        emp.update()
        return redirect(url_for('cliente.index'))
    return render_template("cliente/edit.html",title='Alterar de cliente', form=form)


@nfe.context_processor
def utility_processor():
    def cnpj(cnpj ):
           return "%s.%s.%s/%s-%s" % ( cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14] )
     
    return dict(cnpj=cnpj)

@nfe.context_processor    
def dados():
    usuario = Usuario.query.get(current_user.id)
    hoje    = date.today()
    return dict(usuario = usuario.nome,hoje=hoje)


