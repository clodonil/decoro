from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from app import db
from app.controllers.task.forms import CatForm,PesqForm
from app.model import Task, Cliente, Usuario, Categoria
from flask.ext.login import login_required, current_user
from datetime import datetime, timedelta, date
from sqlalchemy import extract
from datetime import date, timedelta


task = Blueprint('task',__name__)

@task.route('/index')
@task.route('/')
@login_required
def index():
    hoje = date.today()
    session['tela'] = "task"
    

    todos = Task.query.filter((Task.status == 1) | (extract('day',Task.date_modified) == hoje.day)).order_by('data').all()

    return render_template('task/index.html',title='Lançamento de Tarefas',todos=todos)


@task.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = CatForm()
    # tipos de ID
    # 0 - todos
    # C - categoria
    # E - cliente/empresa   
    opcoes = [('0:0','TODOS')]
    categoria = []
    clientes  = []

    for h in Cliente.query.filter(Cliente.status == 0).order_by('nome').all():
       # adicionando clientes na lista
       clientes.append((str(h.id)+':E',h.nome))
       if not  (str(h.categoria.id)+':C',h.categoria.titulo) in categoria:  
          categoria.append((str(h.categoria.id)+':C',h.categoria.titulo))

    opcoes.extend(categoria)
    opcoes.extend(clientes)    

    form.cliente_id.choices = opcoes
    if form.validate_on_submit():       
       titulo      = form.titulo.data
       descricao   = form.descricao.data
       create_user = session['usuario']
       frequencia  = form.frequencia.data
       data        = form.data.data
       cliente_id  = form.cliente_id.data

       (id,cont) = cliente_id.split(":")

       # Verificar se a tarefa eh para todos os clientes
       if cont == '0':          
          for cliente in Cliente.query.filter(Cliente.status == 0):                                 
              tarefa = Task(titulo,descricao,create_user,frequencia,data,cliente.id) 
              tarefa.add(tarefa)

       # Verificar se a tarefa eh por categoria
       if cont == 'C':          
           for cliente in Categoria.query.get(int(id)).cliente.all():
               tarefa = Task(titulo,descricao,create_user,frequencia,data,cliente.id) 
               tarefa.add(tarefa)

       # Verificar se a tarega eh para uma unica empresa        
       if cont == 'E':          
             tarefa = Task(titulo,descricao,create_user,frequencia,data,int(id)) 
             tarefa.add(tarefa)

       return redirect(url_for('task.mytask'))
    return render_template('task/new.html',title='Cadastro de Tarefas',form=form)

@task.route("/edit/<int:cat_id>", methods = ["GET","POST"])
@login_required
def edit(cat_id):
    cat = Task.query.get(cat_id)
    form = CatForm(obj=cat)
    form.cliente_id.choices = [(str(h.id),h.nome) for h in Cliente.query.filter(Cliente.status == 0).order_by('nome').all()]

    if form.validate_on_submit():
       cat.titulo     = form.titulo.data
       cat.descricao  = form.descricao.data
       cat.status     = form.status.data
       cat.data       = form.data.data
       cat.frequencia = form.frequencia.data
       cat.cliente_id = form.cliente_id.data

       if cat.status == '3':
          cat.update_user = session['usuario']

       cat.update()
       return redirect(url_for('task.mytask'))
    return render_template("task/edit.html",title='Alteração de Tarefa', form=form)


@task.route("/mytask")
@login_required
def mytask():
    hoje = date.today()
    session['tela'] = "mytask"
    todos = Task.query.filter((Task.create_user == session['usuario']),((Task.status == 1) | (extract('day',Task.date_modified) == hoje.day))).order_by('data').all()

    return render_template('task/mytask.html',title='Lançamento de Tarefas',todos=todos)

@task.route("/concluido", methods = ["GET","POST"])
@login_required
def concluido():
    session['tela'] = "taskrealizado"

    form = PesqForm()
    form.campo.choices = [(str(h.id),h.nome) for h in Usuario.query.all()]

    if form.validate_on_submit():
       user = form.campo.data
       
       todos = Task.query.filter(Task.status != 1, ((Task.create_user ==  user) | (Task.update_user == user)) ).order_by('data').all() 
    else:  
      todos = Task.query.filter(Task.status != 1).order_by('data').all()
    return render_template('task/concluido.html',title='Todas as Tarefas Realizadas',todos=todos, form=form)


@task.route("/realizado/<int:cat_id>", methods = ["GET","POST"])
@login_required
def realizado(cat_id):
    freq = { 
            '0':0,
            '1':1,
            '2':7,
            '3':10,
            '4':15,
            '5':28,
            '6':30,
            '7':60,
            '8':90,
            '9':120,
            '10':180,
            '11': 365 
           }  
    cat = Task.query.get(cat_id)
    #Novo registro
        
    cat.status = 3
    cat.update_user = session['usuario']
    cat.update()

    if cat.frequencia != '0':
       print(cat.frequencia)
       data = cat.data + timedelta(days=freq[cat.frequencia])
       novo = Task(cat.titulo,cat.descricao,cat.create_user, cat.frequencia,data, cat.cliente_id)
       novo.add(novo)

    return redirect(url_for('task.mytask'))


@task.route("/delete/<int:cat_id>")
@login_required
def delete(cat_id):
    cat = Task.query.get(cat_id)
 
    # Verificar se existe movimentação do usuário antes de apagar ou apagar todas as movimentacoes
    cat.delete(cat)
    return redirect(url_for('task.mystask'))

@task.route("/calendario")
@login_required
def calendario():
    hoje = date.today()
    session['tela'] = "cal"

    todos = Task.query.all()

    return render_template('task/calendario.html',title='Calendário de Tarefas',todos=todos)

@task.context_processor
def dados():
    usuario = Usuario.query.get(current_user.id)
    hoje    = date.today()
    return dict(usuario = usuario.nome,hoje=hoje)