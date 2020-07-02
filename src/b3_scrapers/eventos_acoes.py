from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoEventosCorporativos.aspx?tab=3&codigoCvm='
url2 = 'http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoProventosDinheiro.aspx?tab=3.1&codigoCvm='


def busca_eventos_acoes(codigo_cvm):
    return _eventos_em_ativos(codigo_cvm) + _dividendos(codigo_cvm)


def _eventos_em_ativos(codigo_cvm):
    with urlopen(url + codigo_cvm) as html:
        content = html.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('table', {'id': 'ctl00_contentPlaceHolderConteudo_grdBonificacao_ctl01'})
        try:
            df = pd.read_html(str(table), decimal='.', thousands=',')[0]
        except ValueError:
            return []
        df.drop(columns=['Deliberado em',
                         'Observações'], inplace=True)
        df = df.rename(columns={'Proventos': 'tipo',
                                'Código ISIN': 'isin',
                                'Negócios com até': 'data_com',
                                'Ativo Emitido': 'isin_destino',
                                '% / Fator de Grupamento': 'valor'})
        df['data_com'] = pd.to_datetime(df['data_com'], dayfirst=True, errors='coerce')
        return df.to_dict('records')


def _dividendos(codigo_cvm):
    with urlopen(url2 + codigo_cvm) as html:
        content = html.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('table', {'id': 'ctl00_contentPlaceHolderConteudo_grdProventos_ctl01'})
        try:
            df = pd.read_html(str(table), decimal=',', thousands='.')[0]
        except ValueError:
            return []
        df.drop(columns=['Data da Aprovação (I)',
                         'Proventos por unidade ou mil',
                         "Últ. Preço 'Com'",
                         'Preço por unidade ou mil',
                         'Provento/Preço(%)',
                         "Data do Últ. Preço 'Com' (III)"], inplace=True)
        df = df.rename(columns={'Tipo do Provento (II)': 'tipo',
                                'Tipo de Ativo': 'tipo_ativo',
                                "Últ. Dia 'Com'": 'data_com',
                                'Valor do Provento (R$)': 'valor'})
        df['data_com'] = pd.to_datetime(df['data_com'], dayfirst=True, errors='coerce')
        return df.to_dict('records')


