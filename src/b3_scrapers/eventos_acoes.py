from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoEventosCorporativos.aspx?tab=3&codigoCvm='


def busca_eventos_acoes(codigo_cvm):
    with urlopen(url + codigo_cvm) as html:
        content = html.read().decode('utf-8')
        return _eventos_em_ativos(content) + _dividendos(content)


def _eventos_em_ativos(html):
    soup = BeautifulSoup(html, 'html.parser')
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


def _dividendos(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'ctl00_contentPlaceHolderConteudo_grdDividendo_ctl01'})
    try:
        df = pd.read_html(str(table), decimal=',', thousands='.')[0]
    except ValueError:
        return []
    df.drop(columns=['Deliberado em',
                     'Relativo a',
                     'Observações'], inplace=True)
    df = df.rename(columns={'Proventos': 'tipo',
                            'Código ISIN': 'isin',
                            'Negócios com até': 'data_com',
                            'Valor (R$)': 'valor',
                            'Início de Pagamento': 'data_pgto'})
    df['data_com'] = pd.to_datetime(df['data_com'], dayfirst=True, errors='coerce')
    df['data_pgto'] = pd.to_datetime(df['data_pgto'], dayfirst=True, errors='coerce')
    return df.to_dict('records')


