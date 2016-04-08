#coding: utf-8
from flask import Flask
from flask_mail import Mail, Message
import os
from flask import Flask, Blueprint, redirect,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir


app = Flask(__name__)
app.config.from_object('config')

# Servidor de Email
mail = Mail(app)

# Banco de Dados
db = SQLAlchemy(app)

# Basic Routes #

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

#@app.errorhandler(404)
#def not_found(error):
#    return render_template('layout/404.html'), 404


# Autenticação
login_manager = LoginManager()
login_manager.init_app(app)

# Modulos
from app import model
from app.controllers.auth.controllers import auth
from app.controllers.cliente.controllers import cliente
from app.controllers.usuario.controllers import usuario
from app.controllers.nfe.controllers import nfe
from app.controllers.contato.controllers import contato
from app.controllers.task.controllers import task
from app.controllers.faturamento.controllers import faturamento
#from app.controllers.relatorio.controllers import relatorio


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(cliente, url_prefix='/cliente')
app.register_blueprint(usuario, url_prefix='/usuario')
app.register_blueprint(nfe, url_prefix='/nfe')
app.register_blueprint(contato, url_prefix='/contato')
app.register_blueprint(task, url_prefix='/task')
app.register_blueprint(faturamento, url_prefix='/faturamento')
#app.register_blueprint(relatorio, url_prefix='/relatorio')