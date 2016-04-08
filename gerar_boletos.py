import pyboleto
from pyboleto.bank.bradesco import BoletoBradesco

from pyboleto.pdf import BoletoPDF
import datetime


def print_bradesco():
    listaDadosBradesco = []
    for i in range(2):
        d = BoletoBradesco()
        d.carteira = '06'  # Contrato firmado com o Banco Bradesco
        d.cedente = 'DECORO ESCRITORIO DE CONTABILIDADE, AUDITORIA'
        d.cedente_documento = "015.682.241/0001-35"
        d.cedente_endereco = "Estrada São Francisco, 2008 - CJ 204, Taboão da Serra"
        d.agencia_cedente = '0348-1'
        d.conta_cedente = '24217-9'

        d.data_vencimento = datetime.date(2016, 3, 15)
        d.data_documento = datetime.date(2016, 3, 15)
        d.data_processamento = datetime.date(2016, 3, 15)

        d.instrucoes = [            
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Sr Caixa, cobrar juros de 1% ao dia",
            ]
        d.demonstrativo = [
            "- Serviços Contais R$ 1,00",
            "- Reembolso de Imposto R$ 1.00",
            ]
        d.valor_documento = 3.00

        d.nosso_numero = "1112011668"
        d.numero_documento = "1112011668"
        d.sacado = [
            "Clodonil Honorio Trigo",
            "Rua Desconhecida, 00/0000 - NÃ£o Sei - Cidade - Cep. 00000-000",
            ""
            ]
        listaDadosBradesco.append(d)

    # Bradesco Formato carne - duas paginas por folha A4
    boleto = BoletoPDF('boleto-novo.pdf', True)
    for i in range(0, len(listaDadosBradesco), 2):
        boleto.drawBoletoCarneDuplo(
            listaDadosBradesco[i],
            listaDadosBradesco[i + 1]
        )
        boleto.nextPage()
    boleto.save()

    # Bradesco Formato normal - uma pagina por folha A4
    #boleto = BoletoPDF('boleto_novo.pdf')
    #for i in range(len(listaDadosBradesco)):
    #    boleto.drawBoleto(listaDadosBradesco[i])
    #    boleto.nextPage()
    #boleto.save()




print_bradesco()