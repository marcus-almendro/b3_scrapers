from urllib.request import urlopen, Request
import pandas as pd
from bs4 import BeautifulSoup
import ssl
from tqdm import tqdm

url = 'https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id='


def busca_proventos_no_range(inicio, fim):
    proventos = []
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    for i in tqdm(range(inicio, fim)):
        with urlopen(Request(url + str(i), headers=headers), context=ssl._create_unverified_context()) as html:
            if html.getheader('Content-Type') == 'text/html; charset=UTF-8':
                content = html.read().decode('utf-8')
                provento = _parse_provento(i, content)
                if provento:
                    proventos.append(provento)
            else:
                continue
    return proventos


def _parse_provento(i, html):
    if html.find('sobre Pagamento de Proventos') < 0:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    try:
        table = soup.findAll('table')[1]
        df = pd.read_html(str(table), decimal=',', thousands='.')[0]
        df.drop(columns=[0], inplace=True)
        df = df.transpose()
        df = df.rename(columns={3: 'data_com', 5: 'valor', 4: 'data_pgto'})
        df['data_com'] = pd.to_datetime(df['data_com'], dayfirst=True, errors='coerce')
        df['data_pgto'] = pd.to_datetime(df['data_pgto'], dayfirst=True, errors='coerce')
        if not pd.isna(df.to_dict('records')[0]['valor']):
            valores = df.to_dict('records')[0]
            valores['amort'] = False
        else:
            valores = df.to_dict('records')[1]
            valores['amort'] = True

        spans = soup.findAll('table')[0].findAll('span', {'class', 'dado-cabecalho'})
        return {
            'id': i,
            'codigo_negociacao': spans[-1].getText(),
            'isin': spans[-2].getText(),
            'data_com': valores['data_com'],
            'data_pgto': valores['data_pgto'],
            'valor': valores['valor'],
            'amortizacao': valores['amort']
        }
    except Exception:
        return None
