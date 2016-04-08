from app import db
from datetime import datetime
from flask.ext.login import LoginManager, login_user,UserMixin, logout_user
from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import INET
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user
from config import UPLOAD_FOLDER
import os




class Categoria(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      titulo        = db.Column(db.String(100), index=True)
      descricao     = db.Column(db.String(255), index=True)          
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)
      cliente       = db.relationship('Cliente', backref='categoria', lazy='dynamic')

      def __repr__(self):
          return '<Categoria %r>' %(self.titulo)


      def __init__(self,titulo, descricao):
          self.titulo         = titulo
          self.descricao      = descricao
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()

          

      def get_id(self):
          return str(self.id)

      def add(self,cat):
          db.session.add(cat)
          return session_commit ()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,cat):
          db.session.delete(cat)
          return session_commit()

class Task(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      titulo        = db.Column(db.String(100), index=True)
      descricao     = db.Column(db.String(100), index=True)
      create_user   = db.Column(db.Integer, db.ForeignKey('usuario.id'))
      update_user   = db.Column(db.Integer, db.ForeignKey('usuario.id'))
      status        = db.Column(db.Integer)
      frequencia    = db.Column(db.String(100))
      data          = db.Column(db.Date) 
      cliente_id    = db.Column(db.Integer, db.ForeignKey('cliente.id'))    
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      def __repr__(self):
          return '<Task %r>' %(self.titulo)


      def __init__(self,titulo,descricao,create_user, frequencia,data, cliente_id):
          #Status
          # 1 - Ativo
          # 2 - Cancelado
          # 3 - Realizado

          self.titulo         = titulo
          self.descricao      = descricao
          self.create_user    = create_user    
          self.frequencia     = frequencia
          self.status         = 1  
          self.data           = data
          self.cliente_id     = cliente_id        
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()



      def get_id(self):
          return str(self.id)

      def add(self,emp):
          db.session.add(emp)          
          return session_commit()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,emp):
          db.session.delete(emp)
          return session_commit()



class Usuario(db.Model,UserMixin):
      id            = db.Column(db.Integer, primary_key=True)
      nome          = db.Column(db.String(100), index=True)
      sobrenome     = db.Column(db.String(255), index=True)
      email         = db.Column(db.String(100), unique=True, index=True)      
      password      = db.Column(db.String(100), index=True)      
      tel1          = db.Column(db.String(100), index=True)  
      tel2          = db.Column(db.String(100), index=True)
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)
      login         = db.Column(db.String(100), unique=True, index=True) 
      create_user   = db.relationship('Task', backref='taskcreate', lazy='dynamic', foreign_keys = 'Task.create_user')
      update_user   = db.relationship('Task', backref='taskupdate', lazy='dynamic', foreign_keys = 'Task.update_user')  



      def __repr__(self):
          return '<Usuario %r>' %(self.nome)


      def __init__(self,nome, sobrenome, email, password, tel1,tel2,login):
          self.nome           = nome.lower()
          self.sobrenome      = sobrenome.lower()
          self.email          = email.lower()         
          self.set_password(password)
          self.tel1           = tel1
          self.tel2           = tel2
          self.login          = login.lower()
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()


      
      def add(self,user):
          db.session.add(user)
          session_commit()
          return True
          

      def update(self):
          self.date_modified  = datetime.utcnow()                    
          return session_commit()
      

      def delete(self,user):
          path = user.empresa.nome + '/' + user.nome
          db.session.delete(user)
          return session_commit()
     
      def set_password(self, password):
          self.password = generate_password_hash(password)
   
      def check_password(self, password):
          return check_password_hash(self.password, password)



class Cliente(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      nome          = db.Column(db.String(100), index=True)
      cnpj          = db.Column(db.String(100), index=True)
      tel1          = db.Column(db.String(100))
      nome_resp     = db.Column(db.String(100))
      tel2          = db.Column(db.String(100))
      email         = db.Column(db.String(100))
      outros        = db.Column(db.Text)      
      end           = db.Column(db.String(100))
      cep           = db.Column(db.String(100))
      uf            = db.Column(db.String(100))
      cidade        = db.Column(db.String(100))
      bairro        = db.Column(db.String(100))
      aniversario   = db.Column(db.Date)
      valor         = db.Column(db.Float) 
      categoria_id  = db.Column(db.Integer, db.ForeignKey('categoria.id'))  
      task          = db.relationship('Task', backref='cliente', lazy='dynamic')
      faturamentos  = db.relationship('Faturas', back_populates="cliente")
      status        = db.Column(db.Integer)
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      def __repr__(self):
          return '<Cliente %r>' %(self.nome)


      def __init__(self,nome, cnpj, tel1, nome_resp, tel2, email, categoria_id, status, outros,end,cep,uf,cidade,bairro, aniversario, valor):
          self.nome           = nome.upper()
          self.cnpj           = cnpj
          self.tel1           = tel1          
          self.nome_resp      = nome_resp.upper()
          self.tel2           = tel2
          self.email          = email
          self.categoria_id   = categoria_id
          self.status         = status
          self.outros         = outros
          self.end            = end
          self.cep            = cep
          self.uf             = uf
          self.cidade         = cidade
          self.bairro         = bairro
          self.aniversario    = aniversario
          self.valor          = valor
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()



      def get_id(self):
          return str(self.id)

      def add(self,emp):
          db.session.add(emp)
          create_dir(emp.cnpj)
          return session_commit()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,emp):
          db.session.delete(emp)
          return session_commit()

     

class Faturamento(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      mes_comp      = db.Column(db.Integer, index=True)
      ano_comp      = db.Column(db.Integer, index=True) 
      clientes      = db.relationship('Faturas',back_populates='faturamento')
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      def __repr__(self):
          return '<Faturamento %r>' %(self.id)


      def __init__(self,mes_comp, ano_comp):
          self.mes_comp       = mes_comp
          self.ano_comp       = ano_comp
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()


      def get_id(self):
          return str(self.id)

      def add(self,emp):
          db.session.add(emp)          
          return session_commit()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,emp):          
          db.session.delete(emp)           
          return session_commit()


'''
  Tabela para armazenar o faturas de imposto
'''

class Faturas(db.Model):
      id                     = db.Column(db.Integer, primary_key=True)
      faturamento_id         = db.Column(db.Integer, db.ForeignKey('faturamento.id'))
      cliente_id             = db.Column(db.Integer, db.ForeignKey('cliente.id'))
      valor                  = db.Column(db.Float)             
      status                 = db.Column(db.Integer)
      data_venc              = db.Column(db.Date) 
      date_created           = db.Column(db.DateTime)
      date_modified          = db.Column(db.DateTime)


      cliente                = db.relationship('Cliente', back_populates = "faturamentos")
      faturamento            = db.relationship('Faturamento', back_populates = "clientes")
      reembolso              = db.relationship('Reembolso', backref='faturas', lazy='dynamic')

      # Relacionamento para tabela Imposto
      imposto                = db.relationship('Imposto', backref='faturas', lazy='dynamic')
      
      def __repr__(self):
          return '<Fatura %r>' %(self.id)


      def __init__(self, faturamento_id, cliente_id,valor,status, data_venc): 
          self.faturamento_id = faturamento_id
          self.cliente_id     = cliente_id         
          self.valor          = valor
          self.status         = status
          self.data_venc      = data_venc
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()

      def add(self,emp):
          db.session.add(emp)          
          return session_commit()

      
class Reembolso(db.Model):
      id              = db.Column(db.Integer, primary_key=True)
      descricao       = db.Column(db.String(100))
      valor           = db.Column(db.Float)             
      date_created    = db.Column(db.DateTime)
      date_modified   = db.Column(db.DateTime)
      faturas_id      = db.Column(db.Integer, db.ForeignKey('faturas.id'))    


      def __repr__(self):
          return '<Reembolso %r>' %(self.descricao)


      def __init__(self,descricao, valor, faturas_id ):
          self.descricao      = descricao
          self.valor          = valor
          self.faturas_id     = faturas_id          
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()


      def get_id(self):
          return str(self.id)

      def add(self,emp):
          db.session.add(emp)          
          return session_commit()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,emp):
          db.session.delete(emp)           
          return session_commit()


'''
Tabela de Imposto
'''

class Imposto(db.Model):
      id                = db.Column(db.Integer, primary_key=True)
      valor_faturamento = db.Column(db.Float)
      pis_aliquota      = db.Column(db.Float)
      pis_deducao       = db.Column(db.Float)
      cofins_aliquota   = db.Column(db.Float)
      cofins_deducao    = db.Column(db.Float)
      csll_aliquota     = db.Column(db.Float)
      csll_deducao      = db.Column(db.Float)
      irpj_aliquota     = db.Column(db.Float)
      irpj_deducao      = db.Column(db.Float)
      iss_aliquota      = db.Column(db.Float)
      iss_deducao       = db.Column(db.Float)
      faturas_id        = db.Column(db.Integer, db.ForeignKey('faturas.id'))    
      date_created      = db.Column(db.DateTime)
      date_modified     = db.Column(db.DateTime)


      def __repr__(self):
          return '<Imposto %r>' %(self.id)


      def __init__(self,valor_faturamento, pis_aliquota, pis_deducao, cofins_aliquota,cofins_deducao, csll_aliquota,csll_deducao, irpj_aliquota, irpj_deducao, iss_aliquota, iss_deducao, faturas_id):          
          self.valor_faturamento = valor_faturamento
          self.pis_aliquota      = pis_aliquota
          self.pis_deducao       = pis_deducao
          self.cofins_aliquota   = cofins_aliquota
          self.cofins_deducao    = cofins_deducao
          self.csll_aliquota     = csll_aliquota
          self.csll_deducao      = csll_deducao
          self.irpj_aliquota     = irpj_aliquota
          self.irpj_deducao      = irpj_deducao
          self.iss_aliquota      = iss_aliquota
          self.iss_deducao       = iss_deducao
          self.faturas_id        = faturas_id
          self.date_created      = datetime.utcnow()
          self.date_modified     = datetime.utcnow()


      def get_id(self):
          return str(self.id)

      def add(self,emp):
          db.session.add(emp)          
          return session_commit()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,emp):
          db.session.delete(emp)           
          return session_commit()




class Contato(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      nome          = db.Column(db.String(100), index=True)
      tel1          = db.Column(db.String(100))
      tel2          = db.Column(db.String(100))
      tel3          = db.Column(db.String(100))
      email         = db.Column(db.String(100))
      outros        = db.Column(db.Text)      
      end           = db.Column(db.String(100))
      cep           = db.Column(db.String(100))
      uf            = db.Column(db.String(100))
      cidade        = db.Column(db.String(100))
      bairro        = db.Column(db.String(100))
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      def __repr__(self):
          return '<Contato %r>' %(self.nome)


      def __init__(self,nome, tel1, tel2, tel3, email, outros,end,cep,uf,cidade,bairro):
          self.nome           = nome.lower()
          self.tel1           = tel1          
          self.tel2           = tel2
          self.tel3           = tel3
          self.email          = email
          self.outros         = outros
          self.end            = end
          self.cep            = cep
          self.uf             = uf
          self.cidade         = cidade
          self.bairro         = bairro
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()



      def get_id(self):
          return str(self.id)

      def add(self,emp):
          db.session.add(emp)
          return session_commit()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,emp):
          db.session.delete(emp)
          return session_commit()


def create_dir(path_dir):
    path = UPLOAD_FOLDER+"/"+ path_dir.lower()    
    if not os.path.exists(path):
       os.makedirs(path)    

def delete_dir(path_dir):
    src_path = UPLOAD_FOLDER+"/"+ path_dir.lower()
    dst_path = UPLOAD_FOLDER+"/"+ path_dir.lower() + '_deletado'
    if os.path.exists(src_path):
       os.rename(src_path,dst_path)    

def edit_dir(src_path,dst_path):
    src_path = UPLOAD_FOLDER+"/"+ src_path.lower()
    dst_path = UPLOAD_FOLDER+"/"+ dst_path.lower()
    if os.path.exists(src_path):
       os.rename(src_path,dst_path)



#Universal functions

def  session_commit():
      try:
        db.session.commit()
      except SQLAlchemyError as e:             
         db.session.rollback()
         reason=str(e)
         return reason
