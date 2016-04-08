#!env/bin/python
from app import db
from app.model import Categoria, Movimentacao, Docs, Usuario, Empresa, Formapagamento
import datetime
from dateutil.relativedelta import relativedelta



movs =  Movimentacao.query.filter(Movimentacao.parcelas == 0, Movimentacao.finalizada == False ).order_by('data_v').all()

for mov in movs:
	print(mov.id)
	print(mov.titulo)
	print(mov.parcelas)
	print(mov.parcelas_id)
	print(mov.finalizada)

	

	
