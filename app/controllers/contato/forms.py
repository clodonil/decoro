
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField, TextField,validators
from wtforms.validators import DataRequired
from datetime import datetime


class ContatoForm(Form):

     estado = [
               ('SP','São Paulo'),
               ('RJ','Rio de Janeiro'),
               ('DF','Distrito Federal'),
               ('GO','Goiás'),
               ('MT','Mato Grosso'),
               ('MS','Mato Grosso do Sul'),               
               ('AM','Amazonas'),
               ('AC','Acre'),
               ('RO','Rondônia'),
               ('RR','Roraima'),
               ('AP','Amapá'),
               ('TO','Tocantins'),
               ('PA','Para'),
               ('MA','Maranhão'),
               ('PI','Piaui'),
               ('CE','Ceara'),
               ('RN','Rio Grande do Norte'),
               ('PB','Paraiba'),
               ('PE','Pernambuco'),
               ('SE','Sergipe'),
               ('AL','Alagoas'),
               ('BA','Bahia'),               
               ('MG','Minas Gerais'),               
               ('ES','Espirito Santo'),
               ('PR','Parana'),
               ('SC','Santa Catarina'),
               ('RS','Rio Grande do Sul')
              ]
     nome         = StringField('Nome', validators=[DataRequired()])
     tel1          = StringField('Tel')
     tel2          = StringField('Tel')
     tel3          = StringField('Tel') 
     email        = StringField('email')
     outros       = TextAreaField('Outros')
     end          = StringField('Endereço')
     uf           = SelectField('Estado', choices=estado)
     cep          = StringField('CEP')
     cidade       = StringField('Cidade')
     bairro       = StringField('Bairro')