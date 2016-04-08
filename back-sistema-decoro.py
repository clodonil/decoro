#!env/bin/python
from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from app import db
from app.controllers.task.forms import CatForm
from app.model import Task, Cliente, Usuario, Categoria
from flask.ext.login import login_required, current_user
from datetime import datetime, timedelta, date
from sqlalchemy import extract
from datetime import date, timedelta



class BackGround():
    def __init__(self):
        self.hoje  = date.today()
        self.tasks = Task.query.filter((Task.status == 1) | (extract('day',Task.date_modified) == self.hoje.day)).order_by('data').all() 

     
    def task_vencida(self):
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

         
         for task in self.tasks:
              if task.data <  hoje:
                 if task.frequencia != '0':
                      data = task.data + timedelta(days=freq[task.frequencia])
                      novo = Task(task.titulo,task.descricao,task.create_user, task.frequencia,data, task.cliente_id)
                      novo.add(novo)                 


    def lista_task(self):
        user = {}

        for task in self.tasks:
            nome  = task.create_user
            email = task.create_user
            list_vencido = []
            list_hoje    = []
            list_amanha  = []
            amanha= task.data + timedelta(days=1)

            if task.data <  self.hoje:
               list_vencido.append(task)

            elif task.data == self.hoje:
               list_hoje.append(task)

            elif task.data ==  amanha:    
                list_amanha(task)

            print(nome,email)
            print("VENCIDO")
            print(list_vencido)   
            print("HOJE")
            print(list_hoje)   
            print("AMANHA")
            print(list_amanha)   


    def email(self):
        vencidas = self.lista_task()
        hoje     = self.lista_task()
        amanha   = self.lista_task()

    







app = BackGround()
#app.task_vencida()
app.lista_task()