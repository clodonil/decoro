from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField, PasswordField,validators
from wtforms.validators import DataRequired, EqualTo

class UserForm(Form):
     nome       = StringField('Nome', validators=[DataRequired()])
     sobrenome  = StringField('SobreNome', validators=[DataRequired()])
     email      = StringField('E-Mail', validators=[DataRequired()])
     password   = PasswordField('New Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
     confirm    = PasswordField('Repeat Password')
     tel1       = StringField('Telefone Fixo')
     tel2       = StringField('Telefone Cel')
     login      = StringField('Login', validators=[DataRequired()])



class UserEditForm(Form):
     nome       = StringField('Nome', validators=[DataRequired()])
     sobrenome  = StringField('SobreNome', validators=[DataRequired()])
     email      = StringField('E-Mail', validators=[DataRequired()])
     tel1       = StringField('Telefone Fixo')
     tel2       = StringField('Telefone Cel')
     login      = StringField('Login', validators=[DataRequired()])



class UserPassForm(Form):
     password   = StringField('Password', validators=[DataRequired()])
     password   = PasswordField('New Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
     confirm    = PasswordField('Repeat Password')

