#!env/bin/python
#from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from app import app, mail
from flask_mail import Mail, Message
from app.controllers.task.forms import CatForm,PesqForm
from app.model import Task, Cliente, Usuario, Categoria
#from flask.ext.login import login_required, current_user
from datetime import datetime, timedelta, date
from sqlalchemy import extract



class TaskMail():

    def __init__(self):
        self.sender = ['clodonil@decoroecsa.com.br','raquel@decoroecsa.com.br']
        self.hoje   = date.today()

    def send_mail(self,subject, sender, recipients, text_body, html_body):
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        with app.app_context():
           mail.send(msg)

           

    def lista_tarefa(self):
        todos = Task.query.filter( Task.status == 1 ).order_by('create_user').all()
        
        task_user = {}

        for task in todos:
            

            if task.data < self.hoje:
                situacao = 'vencido'
            elif task.data == self.hoje:
                situacao = 'hoje'
            elif task.data == self.hoje + timedelta(days=1):
                 situacao = 'amanha'        

            if situacao:
               item = "<tr>\
                          <td> {} </td>\
                          <td> {} </td>\
                          <td> {} </td>\
                      </tr>".format(task.data.strftime('%d/%m/%Y'),task.titulo,task.descricao)
               
               if task.taskcreate.email in task_user:
                  if situacao in task_user[task.taskcreate.email] :
                     task_user[task.taskcreate.email][situacao].append(item)
                  else:
                     task_user[task.taskcreate.email][situacao] = [item] 
                     

               else:
                  task_user[task.taskcreate.email] = {}
                  task_user[task.taskcreate.email][situacao] = [item]

            situacao = ""   
               
        for user in task_user:
            html = "<h1> Lista de Tarefas do {}</h1><br/><br/>".format(user)

            
            if 'vencido' in task_user[user]:
                html = html + "<h1> {} </h1>".format('Vencidos')
                html = html + "<table border=1><tr><td>Data</td><td>Titulo</td><td>Descricao</td></tr>"

            
                for cat in task_user[user]['vencido']:                
                     html = html + cat                
                html = html + "</table>" 
       
            if 'hoje' in task_user[user]:
                html = html + "<h1> {} </h1>".format('Hoje')
                html = html + "<table border=1><tr><td>Data</td><td>Titulo</td><td>Descricao</td></tr>"

                for cat in task_user[user]['hoje']:                
                    html = html + cat                
                html = html + "</table>" 
        
            if "amanha" in task_user[user]:
                html = html + "<h1> {} </h1>".format('Amanha')
                html = html + "<table border=1><tr><td>Data</td><td>Titulo</td><td>Descricao</td></tr>"

                for cat in task_user[user]['amanha']:                
                    html = html + cat                
                html = html + "</table>" 

        
            self.send_mail('[DECORO]: Relatorio de Atividades', 'clodonil@decoroecsa.com.br', self.sender,'teste',html)

    

nw = TaskMail()
nw.lista_tarefa()


#send_mail('Teste de envio de email do python', 'clodonil@decoroecsa.com.br',['clodonil@nisled.org'],'teste','<h1> teste </h1>')