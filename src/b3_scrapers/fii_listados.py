from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://bvmf.bmfbovespa.com.br/Fundos-Listados/FundosListados.aspx?tipoFundo=imobiliario'


def busca_codigos_fii():
    with urlopen(url) as html:
        content = html.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')

    table = soup.find('table')
    try:
        df = pd.read_html(str(table))[0]
        df.drop(columns=['Fundo',
                         'Segmento'], inplace=True)
        df = df.rename(columns={'Razão Social': 'nome',
                                'Código': 'sigla'})
    except ValueError:
        return []
    return df.to_dict('records')
