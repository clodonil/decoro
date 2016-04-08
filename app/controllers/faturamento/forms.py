
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField, TextField, FieldList, FormField
from wtforms.validators import DataRequired
from wtforms import Form as NoCsrfForm
import datetime


class ReembolsoForm(Form):
     descricao     = StringField('Descrição', validators=[DataRequired()])
     valor         = FloatField('Valor', validators=[DataRequired()])


class ImpostoForm(Form):
     valor_faturamento = FloatField('Valor Faturamento', default='0.0')
     pis_aliquota      = FloatField('Pis Aliquota',  default='0.0')
     pis_deducao       = FloatField('Pis Deducao',  default='0.0')
     cofins_aliquota   = FloatField('Cofins Aliquota', default='0.0')
     cofins_deducao    = FloatField('Cofins Deducao',  default='0.0')
     csll_aliquota     = FloatField('Csll Aliquota',  default='0.0')
     csll_deducao      = FloatField('Csll Deducao',  default='0.0')
     irpj_aliquota     = FloatField('Irpj Aliquota', default='0.0')
     irpj_deducao      = FloatField('Irpj Deducao',  default='0.0')
     iss_aliquota      = FloatField('Iss Aliquota',  default='0.0')
     iss_deducao       = FloatField('Iss Deducao',   default='0.0')
