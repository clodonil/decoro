from fpdf import FPDF, HTMLMixin
import fpdf
from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from wtforms.validators import DataRequired
from sqlalchemy.sql import func
from werkzeug import secure_filename
from app import db
from app.controllers.faturamento.forms import  ReembolsoForm, ImpostoForm
from app.model import Cliente, Categoria, Faturamento, Faturas, Reembolso, Usuario, Imposto, Faturas
from flask.ext.login import login_required, current_user
from datetime import date
import os



faturamento = Blueprint('faturamento',__name__)

@faturamento.route('/index')
@faturamento.route('/')
@login_required
def index():
    todos = Faturamento.query.all()
    session['tela'] = "faturamento"
    return render_template('faturamento/index.html',title='Lista de Faturamento',todos=todos)


'''
 Lista de Clientes para faturamento
'''
@faturamento.route('/new', methods=['GET','POST'])
@login_required
def new():
    hoje = date.today()
    old_ano = 0
    if hoje.month == 1:
       old_ano = 1 
       mes_ref = 12
    else:
       mes_ref = hoje.month - 1   
    ano_ref = hoje.year - old_ano  
    vencimento =  date(hoje.year, hoje.month, 20)
    
    if not Faturamento.query.filter(Faturamento.mes_comp == mes_ref, Faturamento.ano_comp == ano_ref).all():
        f = Faturamento(mes_ref, ano_ref)
        f.add(f)


        for cliente in Cliente.query.filter(Cliente.status == 0).order_by('nome').all():            
            fatura = Faturas(f.id, cliente.id, cliente.valor,1,vencimento)
        
        todos = Faturas.query.filter(Faturas.faturamento_id == f.id).all()         
    else:       
        # Pesquisa pela faturamento  atual
        f     = Faturamento.query.filter(Faturamento.mes_comp == mes_ref, Faturamento.ano_comp == ano_ref).first() 
        # Pesquisa por todos as faturas feitas
        todos = Faturas.query.filter(Faturas.faturamento_id == f.id).all()

    return render_template('faturamento/new.html',title='Lançamento de Faturamento', todos=todos)

'''
  Calculo de Reembolso
'''

@faturamento.route("/reembolso/<int:faturas_id>", methods = ["GET","POST"])
@login_required
def reembolso(faturas_id):
    form = ReembolsoForm()

    if form.validate_on_submit():
         emp = Reembolso(
                form.descricao.data,
                form.valor.data,
                faturas_id
            )
         emp.add(emp)
    todos = Reembolso.query.filter(Reembolso.faturas_id== faturas_id).all()
    return render_template('faturamento/reembolso.html',title='Lançamento de Faturamento', 
                            todos=todos, form=form, faturas_id = faturas_id)


@faturamento.route("/reembolso_delete/<int:emp_id>/<int:faturas_id>")
@login_required
def reembolso_delete(emp_id,faturas_id):
    emp = Reembolso.query.get(emp_id)
    emp.delete(emp)
    return redirect(url_for('faturamento.reembolso',faturas_id = faturas_id))


'''
   Calculo de Imposto para o faturamento do mes 
'''

@faturamento.route("/imposto/<int:faturas_id>", methods = ["GET","POST"])
@login_required
def imposto(faturas_id):
    mes_ext = {1: 'JANEIRO', 2 : 'FEVEREIRO', 3: 'MARÇO', 4: 'ABRIL', 5: 'MAIO',6:'JUNHO', 
               7:'JULHO', 8:'AGOSTO', 9:'SETEMBRO',10:'OUTUBRO',11:'NOVEMBRO',12:'DEZEMBRO'    }


    faturas = Faturas.query.get(faturas_id)

    

    #verificando se o imposto já foi alterado
    imposto = Imposto.query.filter(Imposto.faturas_id == faturas_id).first()
   
    if imposto:
       form = ImpostoForm(obj=imposto)
    else:
       form = ImpostoForm()
       imposto = Imposto(0,0,0,0,0,0,0,0,0,0,0,0)

    
    if form.validate_on_submit():
          
          if imposto.faturas_id == 0:
               
               imp = Imposto(
                     form.valor_faturamento.data,
                     form.pis_aliquota.data,
                     form.pis_deducao.data,
                     form.cofins_aliquota.data,
                     form.cofins_deducao.data,
                     form.csll_aliquota.data,
                     form.csll_deducao.data,
                     form.irpj_aliquota.data,
                     form.irpj_deducao.data,
                     form.iss_aliquota.data,
                     form.iss_deducao.data,
                     faturas.id
                     )
               imp.add(imp)
    
          else:

               imposto.valor_faturamento = form.valor_faturamento.data
               imposto.pis_aliquota      = form.pis_aliquota.data
               imposto.pis_deducao       = form.pis_deducao.data
               imposto.cofins_aliquota   = form.cofins_aliquota.data
               imposto.cofins_deducao    = form.cofins_deducao.data
               imposto.csll_aliquota     = form.csll_aliquota.data
               imposto.csll_deducao      = form.csll_deducao.data
               imposto.irpj_aliquota     = form.irpj_aliquota.data
               imposto.irpj_deducao      = form.irpj_deducao.data
               imposto.iss_aliquota      = form.iss_aliquota.data
               imposto.iss_deducao       = form.iss_deducao.data
               imposto.update()
    
    
    ano_comp = faturas.faturamento.ano_comp    
    mes_comp = faturas.faturamento.mes_comp
    mes = mes_ext[mes_comp]

    #verificando se o imposto já foi alterado
    imposto = Imposto.query.filter(Imposto.faturas_id == faturas_id).first()


    return render_template('faturamento/imposto.html',ano=ano_comp, mes=mes,title='Calculo de Imposto',faturas=faturas, form = form, imposto = imposto)




@faturamento.route("/edit/<int:emp_id>", methods = ["GET","POST"])
@login_required
def edit(emp_id):
    emp = Cliente.query.get(emp_id)    
    form = EmpForm(obj=emp)
    form.categoria_id.choices = [(h.id,h.titulo) for h in Categoria.query.all()]
    if form.validate_on_submit():
        emp.nome         = form.nome.data,
        emp.cnpj         = form.cnpj.data,
        emp.tel          = form.tel.data,
        emp.nome_resp    = form.nome_resp.data,
        emp.tel_resp     = form.tel_resp.data,                           
        emp.email        = form.email.data,
        emp.categoria_id = form.categoria_id.data,
        emp.status       = form.status.data,
        emp.outros       = form.outros.data,
        emp.end          = form.end.data,
        emp.cep          = form.cep.data,
        emp.cep          = form.uf.data,
        emp.cidade       = form.cidade.data,
        emp.bairro       = form.bairro.data,
        emp.aniversario  = form.aniversario.data


        emp.update()
        return redirect(url_for('cliente.index'))
    return render_template("cliente/edit.html",title='Alterar de cliente', form=form)

@faturamento.route("/delete/<int:emp_id>")
@login_required
def delete(emp_id):
    emp = cliente.query.get(emp_id)
    if len(emp.Usuario.all()) == 0:
       emp.delete(emp)
    return redirect(url_for('cliente.index'))

'''
  Gerar o anexo para enviar para o cliente
'''  

@faturamento.route("/anexo/<int:faturas_id>")
@login_required
def anexo(faturas_id):
    todos = Reembolso.query.filter(Reembolso.faturas_id== faturas_id).all()
    html = """
               <h2><center> Relatório de Reembolso </center></h2>
              <table border="1">
                 <thead><tr bgcolor="#A0A0A0"><th width="80%">Descrição</th><th width="20%">Valor</th></tr></thead>
                 
              <tbody>
           """ 
    x = 0
    sum = 0 
    for item in todos:
        x = x + 1
        sum = sum + item.valor
        if x % 2 == 0:
           
            l1 = '<tr bgcolor="#FFFFFF"><td>%s</td><td>R$ %d</td></tr>' %(item.descricao, item.valor)
        else:    
            l1 = '<tr bgcolor="#F0F0F0"><td>%s</td><td>R$ %d</td></tr>' %(item.descricao, item.valor) 
        html = html + l1
    html = html + '</tbody><tfoot><tr bgcolor="#E0E0E0"><td>Total</td><td>R$ %d</td></tr></tfoot></table>' %(sum)  


#
#""" + """<tr bgcolor="#F0F0F0">
#<td>cell 3</td><td>cell 4</td>
#</tr>""" * 200 + """
#</tbody>
#</table>

#
 
 #         """

 

    gerar_pdf(html,'teste.pdf')   

    return redirect(url_for('faturamento.index'))

@faturamento.context_processor


def utility_processor():
    def total_reembolso(faturas_id):
       total = Reembolso.query.filter(Reembolso.faturas_id == faturas_id).all()
       sum = 0
       for k in total:
          sum = sum + k.valor
       return sum
       
       

    def total_imposto(fatura_id):
         imposto = Imposto.query.filter(Imposto.faturas_id == fatura_id).first()

         if imposto:
             #pis 
             vimposto  = imposto.valor_faturamento * imposto.pis_aliquota
             tpis      = vimposto - imposto.pis_deducao 

             vimposto  = imposto.valor_faturamento * imposto.cofins_aliquota
             tcofins   = vimposto - imposto.cofins_deducao

             vimposto  = imposto.valor_faturamento * imposto.csll_aliquota
             tcsll     = vimposto - imposto.csll_deducao

             vimposto  = imposto.valor_faturamento * imposto.irpj_aliquota
             tirpj     = vimposto - imposto.irpj_deducao

             vimposto  = imposto.valor_faturamento * imposto.iss_aliquota
             tiss      = vimposto - imposto.iss_deducao

             total     = imposto.valor_faturamento + tpis + tcofins + tcofins + tcsll + tirpj + tiss  
         else:
             total     = 0    
         return total

    def cnpj(cnpj ):
           return "%s.%s.%s/%s-%s" % ( cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14] )
     
    return dict(total_reembolso=total_reembolso, cnpj=cnpj, total_imposto=total_imposto)

def dados():
    usuario = Usuario.query.index.get(current_user.id)
    hoje    = date.today()
    return dict(usuario = usuario.nome,hoje=hoje)


def gerar_pdf(html,filename):
    class MyFPDF(FPDF, HTMLMixin):
        def header(self):            
            self.set_font('Arial','B',16)
            self.cell(80)
            self.cell(30,10,'DECORO CONTABILIDADE',0,0,'C')
            self.ln(20)
            
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial','I',8)
            self.cell(0,0,'Tel(11) 3037-7327',0,0,'C')
            self.set_y(-15)
            self.set_font('Arial','I',8)
            txt = 'Página %s de %s' % (self.page_no(), self.alias_nb_pages())
            self.cell(0,10,txt,0,0,'C')

                    
    pdf=MyFPDF()
    #First page
    pdf.add_page()
    pdf.write_html(html)
    pdf.output(filename,'F')