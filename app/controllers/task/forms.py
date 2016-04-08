from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, validators
from wtforms.validators import DataRequired
from datetime import datetime

class CatForm(Form):
      
     freq  = [
               ('0','Uma única vez'),
               ('1','Diariamente'),
               ('2','Semanal'),
               ('3','A cada 10 dias'),
               ('4','A cada 15 dias'),
               ('5','A cada 28 dias'),
               ('6','Mensal'),
               ('7','Bimestral'),
               ('8','Trimestral'),
               ('9','Quadrimestral'),
               ('10','Semestral'),
               ('11', 'Anual') 
             ] 
     #Status
          # 1 - Ativo
          # 2 - Cancelado
          # 3 - Realizado
          
     st = [
             ('1','Ativo'),
             ('2','Cancelado'),
             ('3','Realizado') 
          ]     
        
     titulo      = StringField('titulo', validators=[DataRequired()])
     descricao   = TextAreaField('descricao')
     frequencia  = SelectField('Frequencia', choices=freq)
     cliente_id  = SelectField('Cliente', coerce=str)
     status      = SelectField('Status', choices=st, default=1)
     data        = DateField("Until", format="%d/%m/%Y",default=datetime.today, validators=[validators.DataRequired()])


class PesqForm(Form):
      campo      = SelectField('campo')