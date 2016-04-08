from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db
from app.controllers.contato.forms import ContatoForm
from app.model import Cliente, Contato, Usuario
from flask.ext.login import login_required, current_user
from datetime import date
import os



contato = Blueprint('contato',__name__)

@contato.route('/index', methods=['GET','POST'])
@contato.route('/', methods=['GET','POST'])
@login_required
def index():
    menu = [
             "A-B",   
             "C-D",
             "E-F",
             "G-H",
             "I-J",
             "K-L",
             "M-N",
             "O-P",   
             "Q-R",
             "S-T",
             "U-V",
             "W-X",
             "Y-Z",
             "0-9"           
    ]

    form  =  ContatoForm()

    if form.validate_on_submit(): 
       emp = Contato(
                      form.nome.data,                    
                      form.tel1.data,
                      form.tel2.data,
                      form.tel3.data,                      
                      form.email.data,
                      form.outros.data,
                      form.end.data,
                      form.cep.data,
                      form.uf.data,
                      form.cidade.data,
                      form.bairro.data,
                    )

       emp.add(emp)
    


    todos = Cliente.query.all()
    todos = todos + Contato.query.all()
    todos = todos + Usuario.query.filter(Usuario.id != 1).all()
    todos = sorted(todos, key=lambda x: x.nome, reverse=False)


    session['tela'] = "contato"
    return render_template('contato/index.html',title='Lista de contatos',todos=todos, form = form, menu=menu)


@contato.route("/view/<int:emp_id>/<int:obj>")
@login_required
def view(emp_id,obj):
   if obj == 1:
      reg = Cliente.query.get(emp_id)
   elif obj == 2:
      reg = Contato.query.get(emp_id)
   else:
      reg = Usuario.query.get(emp_id)   

   return render_template("contato/view.html",title='Contatos', reg=reg, obj=obj)   


@contato.route("/edit/<int:emp_id>", methods = ["GET","POST"])
@login_required
def edit(emp_id):
    emp = Contato.query.get(emp_id)    
    form = ContatoForm(obj=emp)
    
    if form.validate_on_submit():
          emp.nome   = form.nome.data                    
          emp.tel1   = form.tel1.data
          emp.tel2   = form.tel2.data
          emp.tel3   = form.tel3.data                      
          emp.email  =form.email.data
          emp.outros = form.outros.data
          emp.end    =form.end.data
          emp.cep    = form.cep.data
          emp.uf     = form.uf.data
          emp.cidade = form.cidade.data
          emp.bairro =form.bairro.data

          emp.update()
          return redirect(url_for('contato.index'))
    return render_template("contato/edit.html",title='Alterar de cliente', form=form)

@contato.route("/delete/<int:emp_id>")
@login_required
def delete(emp_id):
    emp = Contato.query.get(emp_id)
    emp.delete(emp)
    return redirect(url_for('contato.index'))


@contato.context_processor

def utility_processor():
    def ordenar_nomes(letras):
       (l1,l2) = letras.split("-")       
       todos = Cliente.query.filter(Cliente.nome.like(l1+'%')|Cliente.nome.like(l2+'%')).all()
       todos = todos + Contato.query.filter(Contato.nome.like(l1+'%')|Contato.nome.like(l2+'%')).all()
       todos = todos + Usuario.query.filter((Usuario.nome.like(l1+'%')|Usuario.nome.like(l2+'%')), Usuario.id != 1).all()
       todos = sorted(todos, key=lambda x: x.nome, reverse=False)      
       return todos
    def tags(letras):
       return letras.replace(" ","")

    # Saber de qual classe é um registro   
    def isclass(reg):
        if isinstance(reg, Cliente):
           return 1
        elif isinstance(reg, Contato):
           return 2 
        else:
           return 3         
   
    return dict(ordenar_nomes=ordenar_nomes, tags = tags, isclass=isclass)


@contato.context_processor
def dados():
    usuario = Usuario.query.get(current_user.id)
    hoje    = date.today()
    return dict(usuario = usuario.nome,hoje=hoje)

