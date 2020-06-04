from urllib.request import urlopen
import re

url = 'http://bvmf.bmfbovespa.com.br/pt-br/mercados/acoes/empresas/ExecutaAcaoConsultaInfoEmp.asp?CodCVM='


def busca_codigos_negociacao(codigo_cvm):
    data = {'codigo_cvm': codigo_cvm}
    with urlopen(url + codigo_cvm) as html:
        source = html.read().decode('utf-8')
        symbols = re.compile("var symbols = '(.*)';").search(source)
        if symbols:
            data['symbols'] = symbols.group(1).split('|')

        isin = re.compile("ISIN:.*\r\n(.*)<br", re.MULTILINE).search(source)
        if isin:
            data['isin'] = [i.strip() for i in isin.group(1).split(',')]
        else:
            print('não encontrou isin para ' + codigo_cvm)

    return data
