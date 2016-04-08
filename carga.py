#!env/bin/python
# -*- coding: latin1 -*-

from app import db
from app.model import Task, Categoria, Usuario, Cliente
import datetime
import csv
import glob
import time
import sys
import shutil
import codecs


class CargaDados:
     def __init__(self):
         self.dir = "/opt/sistema_decoro/"
         self.dados = []

     def carga(self,file):
         
         with open(file,'rb') as csvfile:
            spamreader = csv.reader(codecs.iterdecode(csvfile,'latin1'), delimiter=';', quotechar='|')
            for row in spamreader:
              if row[0].upper() != "CNPJ" and len(row[0]) > 0:
                self.dados.append(row)

     def verificafile(self,dir):
         filedir=dir+"*.csv"
         files=glob.glob(filedir)
         return files

     def gerar(self,d_nota):
             nome           = d_nota[1]
             cnpj           = d_nota[0]
             tel1           = ''
             nome_resp      = ''
             tel2           = ''
             email          = 'empresa@empresa.com'
             categoria_id   = 1
             status         = 0
             outros         = ''
             end            = ''
             cep            = '05858-001'
             uf             = 'SP'
             cidade         = 'SP'
             bairro         = 'SP'
             aniversario    = datetime.date.today()
             valor          = '0'

             dados = Cliente(nome.upper(),cnpj,tel1,nome_resp,tel2,email,categoria_id,status,outros,end,cep,uf,cidade,bairro,aniversario,valor)
             print(dados.add(dados))
             



     def run(self):
          cont=0
          for file in self.verificafile(self.dir):
              self.date=time.strftime("%d-%m-%Y")
              self.carga(file)             
              
              for nota in self.dados:
                  self.gerar(nota)                 
                  

              print("---> FIM")
        


escola_unicao = CargaDados()
escola_unicao.run()
