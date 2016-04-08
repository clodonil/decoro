#!env/bin/python
from app import db
from app.model import Task, Categoria, Usuario, Cliente, Imposto
import datetime




user = Usuario('admin','admin','admin@localhost','x','1341','342','admin')
user.add(user)


categ = Categoria('MEI','Micro Empresario Indivual')
categ.add(categ)

categ = Categoria('Simples Nacional','Simples Nacional')
categ.add(categ)

categ = Categoria('Lucro Presumido','Lucro Presumido')
categ.add(categ)

categ = Categoria('Lucro Real','Lucro Real')
categ.add(categ)

categ = Categoria('Condomínios','Condomínio')
categ.add(categ)

categ = Categoria('Empregada Doméstica','Empregada Doméstica')
categ.add(categ)

categ = Categoria('Pessoa Fisica','Pessoa Fisica')
categ.add(categ)


imposto = Imposto('PIS')
imposto.add(imposto)

imposto = Imposto('COFINS')
imposto.add(imposto)


imposto = Imposto('CSLL')
imposto.add(imposto)

imposto = Imposto('IRPJ')
imposto.add(imposto)


imposto = Imposto('ISS')
imposto.add(imposto)

