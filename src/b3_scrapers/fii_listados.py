from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://bvmf.bmfbovespa.com.br/Fundos-Listados/FundosListados.aspx?tipoFundo=imobiliario'


def busca_codigos_fii():
    with urlopen(url) as html:
        soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table')
    try:
        df = pd.read_html(str(table))[0]
        df.drop(columns=['Razão Social',
                         'Fundo',
                         'Segmento'], inplace=True)
    except ValueError:
        return []
    return df.values.flatten().tolist()
