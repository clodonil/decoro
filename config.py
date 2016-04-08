import os

WTF_CSRF_ENABLED=True
SECRET_KEY = "you-will-never-guess"


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/banco_de_dados.db')
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:nisled@localhost/xoola'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

# upload_documentos

UPLOAD_FOLDER = os.path.join(basedir,"app/static/docs_repository")



#EMAIL SETTINGS
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
MAIL_USE_SSL=False
MAIL_USE_TLS=True
MAIL_USERNAME = 'clodonil@decoroecsa.com.br'
MAIL_PASSWORD = 'AkugF176.'
